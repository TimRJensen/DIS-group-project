package main

import (
	"crypto/sha1"
	_ "embed"
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"regexp"
	"strings"
	"text/template"
)

const (
	backupDir = "/backups"
)

func backup(args map[string]interface{}) error {
	c, u, d, out :=
		args["-c"].(string),
		args["-u"].(string),
		args["-d"].(string),
		backupDir+"/out"

	cmd := exec.Command("docker", "exec", c, "pg_dump", "-U", u, "-d", d, "-Fd", "-f", out)
	if err := cmd.Run(); err != nil {
		return err
	}

	cmd = exec.Command("docker", "exec", c, "ls", out)
	output, err := cmd.Output()
	if err != nil {
		return err
	}

	sha := sha1.New()
	rexp, _ := regexp.Compile(`.*\.gz$`)
	for _, line := range strings.Split(string(output), "\n") {
		if flag := rexp.MatchString(line); !flag {
			continue
		}

		cmd = exec.Command("docker", "exec", c, "gunzip", "-c", fmt.Sprintf("%s/%s", out, line))
		if output, err := cmd.Output(); err != nil {
			return err
		} else {
			sha.Write(output)
		}
	}

	name := string(sha.Sum(nil))
	path := fmt.Sprintf("%s/%x", backupDir, name)
	cmd = exec.Command("docker", "exec", c, "rm", "-rf", path)
	if err := cmd.Run(); err != nil {
		return err
	}

	cmd = exec.Command("docker", "exec", c, "mv", "-uf", out, path)
	if err := cmd.Run(); err != nil {
		return err
	}

	fmt.Printf("succesfully backed up \"%s\" as \"%x\"\n", d, name)
	return nil
}

func dump(args map[string]interface{}) error {
	c, u, d, o, t :=
		args["-c"].(string),
		args["-u"].(string),
		args["-d"].(string),
		args["-o"].(string),
		args["-t"].(string)

	cmd := exec.Command("docker", "exec", c, "pg_dump", "-U", u, "-d", d, "-t", t, "-c", "--if-exists")
	output, err := cmd.Output()
	if err != nil {
		if t == "public.*" {
			fmt.Printf("exiting: failed to dump \"%s\"\n", d)
		} else {
			fmt.Printf("exiting: failed to dump \"%s\"\n", t)
		}
		return err
	}

	path, err := filepath.Abs(o)
	if err != nil {
		return err
	}

	dir := filepath.Dir(path)
	if _, err := os.Stat(dir); err != nil {
		os.MkdirAll(dir, 0700)
	}

	out, err := os.Create(path)
	if err != nil {
		return err
	}

	defer out.Close()
	out.Write(output)

	if t == "public.*" {
		fmt.Printf("succesfully dumped \"%s\" to \"%s\"\n", d, path)
	} else {
		fmt.Printf("succesfully dumped \"%s\" to \"%s\"\n", t, path)
	}
	return nil
}

func populate(args map[string]interface{}) error {
	c, u, d, f :=
		args["-c"].(string),
		args["-u"].(string),
		args["-d"].(string),
		args["-f"].(string)

	if err := backup(args); err != nil {
		return err
	}

	var result []byte
	if f != "" {
		result, _ = os.ReadFile(f)
	} else {
		data := flatObject{
			"localizations":  []interface{}{},
			"locales:id":     []interface{}{},
			"locales:locale": []interface{}{},
		}
		sql := sqlFromAPI(fmt.Sprintf("standings?league=%d&season=%d", leagueID, season), "groups", data) + "\n"
		sql += sqlFromAPI(fmt.Sprintf("teams?league=%d&season=%d", leagueID, season), "teams", data) + "\n"
		sql += sqlFromAPI(fmt.Sprintf("fixtures?league=%d&season=%d", leagueID, season), "fixtures", data)
		sql += sqlFromLocales("translator/text", "locales", data)
		result = []byte(sql)
	}

	cmd := exec.Command("docker", "exec", c, "psql", "-U", u, "-d", d, "-c", fmt.Sprintf(closeContent, d))
	cmd.Run()

	cmd = exec.Command("docker", "exec", "-it", c, "psql", "-U", u, "-d", d)
	stdin, _ := cmd.StdinPipe()
	defer stdin.Close()

	if err := cmd.Start(); err != nil {
		fmt.Printf("exiting: failed to populate \"%s\"\n", d)
		return err
	}

	if _, err := stdin.Write(result); err != nil {
		fmt.Printf("exiting: failed to populate \"%s\"\n", d)
		return err
	}

	fmt.Printf("sucessfully populated \"%s\"\n", d)
	return nil
}

func restore(args map[string]interface{}) error {
	c, u, d, f, ls :=
		args["-c"].(string),
		args["-u"].(string),
		args["-d"].(string),
		args["-f"].(string),
		args["-ls"].(bool)

	if ls {
		if f != "" {
			cmd := exec.Command("docker", "exec", c, "ls", backupDir+"/"+f)
			output, _ := cmd.Output()

			for _, line := range strings.Split(string(output), "\n") {
				cmd = exec.Command("docker", "exec", c, "gunzip", "-c", backupDir+"/"+f+"/"+line)
				output, _ = cmd.Output()
				fmt.Println(string(output))
			}
		} else {
			cmd := exec.Command("docker", "exec", c, "ls", "-g", "--time", "creation", backupDir)
			output, _ := cmd.Output()
			fmt.Println(string(output))
		}
	} else if f != "" {
		if err := backup(args); err != nil {
			return err
		}

		cmd := exec.Command("docker", "exec", c, "psql", "-U", u, "-d", d, "-c", fmt.Sprintf(closeContent, d))
		cmd.Run()

		cmd = exec.Command("docker", "exec", c, "pg_restore", "-U", u, "-d", "postgres", "-cC", backupDir+"/"+f)
		if err := cmd.Run(); err != nil {
			return err
		}

		fmt.Printf("succesfully restored \"%s\" from \"%s\"\n", d, f)
	}

	return nil
}

//go:embed templates/README.templ
var readmeContent string

//go:embed sql/close.sql
var closeContent string

func main() {
	command := ""
	args := map[string]interface{}{
		"-c":  "postgres",
		"-u":  "group77",
		"-d":  "uefa2024",
		"-f":  "",
		"-o":  "schema/schema.sql",
		"-t":  "public.*",
		"-ls": false,
	}

	if len(os.Args) > 1 {
		command = os.Args[1]
	}
	if len(os.Args) > 2 {
		rexp, _ := regexp.Compile(`-[cdfout]|-ls`)
		for i, flag := range rexp.FindAllString(strings.Join(os.Args[2:], " "), -1) {
			if flag == "-ls" {
				args[flag] = true
			} else {
				args[flag] = os.Args[i+3]
			}
		}
	}

	if command == "backup" {
		if err := backup(args); err != nil {
			os.Exit(1)
		} else {
			os.Exit(0)
		}
	} else if command == "dump" {
		if err := dump(args); err != nil {
			os.Exit(1)
		} else {
			os.Exit(0)
		}
	} else if command == "populate" {
		if err := populate(args); err != nil {
			fmt.Println(err)
			os.Exit(1)
		} else {
			os.Exit(0)
		}
	} else if command == "restore" {
		if err := restore(args); err != nil {
			os.Exit(1)
		} else {
			os.Exit(0)
		}
	}
	tmpl, _ := template.New("readme").Parse(readmeContent)
	tmpl.Execute(os.Stdout, map[string]string{
		"c": os.Getenv("DB"),
		"u": os.Getenv("POSTGRES_USER"),
		"d": os.Getenv("POSTGRES_DB"),
	})
}
