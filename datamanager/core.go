package main

import (
	"bytes"
	_ "embed"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os"
	"regexp"
	"slices"
	"strings"
	"text/template"

	"github.com/joho/godotenv"
)

// API stuff
//
//go:embed secrets/api-key
var secret string

const (
	leagueID = 4
	season   = 2024
)

var (
	endpoints = [2]string{
		"api-football-v1.p.rapidapi.com",
		"google-translate113.p.rapidapi.com",
	}
	headers = [2]map[string]string{
		{
			"x-rapidapi-key":  "",
			"x-rapidapi-host": endpoints[0],
		},
		{
			"x-rapidapi-key":  "",
			"x-rapidapi-host": endpoints[1],
			"Content-Type":    "application/json",
		},
	}
)

func fetch(method, url string, headers map[string]string, body map[string]string) jsonObject {
	payload, _ := json.Marshal(body)
	req, _ := http.NewRequest(method, url, strings.NewReader(string(payload)))

	for key, val := range headers {
		req.Header.Add(key, val)
	}

	res, err := http.DefaultClient.Do(req)
	if err != nil {
		print(err.Error())
	}
	data := make(jsonObject)
	payload, _ = io.ReadAll(res.Body)
	json.Unmarshal(payload, &data)

	return data
}

// SQL stuff
//
//go:embed templates/sql.templ
var sqlTemplate string

type column struct {
	Name     string `json:"name"`
	Type     string `json:"type"`
	ApiKey   string `json:"api-key"`
	PKey     bool   `json:"primary-key"`
	LKey     string `json:"local-key"`
	FKey     string `json:"foreign-key"`
	FTable   string `json:"foreign-table"`
	Localize bool   `json:"localize"`
	Deupe    bool   `json:"dedupe"`
}

type table struct {
	Name   string    `json:"name"`
	ApiKey string    `json:"api-key"`
	Limit  int       `json:"limit"`
	Cols   []*column `json:"cols"`
}

func (t *table) col(name string) *column {
	for _, c := range t.Cols {
		if c.Name == name {
			return c
		}
	}
	return nil
}

type localizeData struct {
	table *table
	col   *column
	id    float64
	val   string
}

type templateData struct {
	Table *table
	Cols  []*column
	PKeys []*column
	FKeys []*column
	Data  flatObject
}

type schemaObject map[string]table
type jsonObject = map[string]interface{}
type flatObject = map[string][]interface{}

var schema schemaObject
var locales []jsonObject

func jsonFlatten(data interface{}, key string, result flatObject) flatObject {
	switch d := data.(type) {
	case []interface{}:
		for _, item := range d {
			jsonFlatten(item, key, result)
		}
	case jsonObject:
		for k, v := range d {
			jsonFlatten(v, key+":"+k, result)
		}
	default:
		if val, ok := result[key]; ok {
			result[key] = append(val, data)
		} else {
			result[key] = []interface{}{data}
		}
	}

	return result
}

func jsonWalk(data interface{}, tokens []string) []interface{} {
	for len(tokens) > 0 {
		switch d := data.(type) {
		case []interface{}:
			data = d[0]
		case jsonObject:
			data = d[tokens[0]]
			tokens = tokens[1:]
		}
	}

	return data.([]interface{})
}

func sqlStringify(val interface{}) string {
	if val == nil {
		return "NULL"
	}

	switch v := val.(type) {
	case string:
		return "'" + v + "'"
	case float64:
		return fmt.Sprintf("%v", int(v))
	default:
		return fmt.Sprintf("%v", v)
	}
}

func sqlFromAPI(query, table string, data flatObject) string {
	res := fetch("GET", "https://"+endpoints[0]+"/v3/"+query, headers[0], nil)

	if _, ok := res["response"]; !ok {
		fmt.Println(res)
		return ""
	}

	t := schema[table]

	// sanitize the response & flatten it
	rs := jsonWalk(res, strings.Split(t.ApiKey, ":"))
	if t.Limit > 0 {
		rs = rs[:t.Limit]
	}
	rf := jsonFlatten(rs, table, make(flatObject))

	// extend existing data with new data
	for key, val := range rf {
		data[key] = val
	}

	// process the tables columns
	cols, pKeys, fKeys := t.Cols, []*column{}, []*column{}
	for _, col := range cols {
		if _, ok := data[col.ApiKey]; ok {
			if col.Deupe {
				data[col.ApiKey] = slices.Compact(data[col.ApiKey])
			}
		} else if col.Name == "id" {
			data[table+":id"] = []interface{}{}
			for i := 0; i < t.Limit; i++ {
				data[table+":id"] = append(data[table+":id"], float64(i))
			}
		}
		if col.PKey {
			pKeys = append(pKeys, col)
		}
		if col.FKey != "" && col.FTable != "" {
			fKeys = append(fKeys, col)
		}
		if col.Localize {
			for i, val := range data[col.ApiKey] {
				data["localizations"] = append(data["localizations"], &localizeData{
					&t, col, data[t.col("id").ApiKey][i].(float64), val.(string),
				})
			}
		}
	}
	tmpl, _ := template.New("sql").
		Funcs(template.FuncMap{
			"sub": func(a, b int) int { return a - b },
			"row": func(col *column) interface{} { return data[col.ApiKey] },
			"item": func(col *column, i int) interface{} {
				if col.FKey != "" {
					var fcol *column = nil
					if ftable, ok := schema[col.FTable]; ok {
						fcol = ftable.col(col.FKey)
					}

					j := slices.Index(data[col.ApiKey], data[col.LKey][i])
					if fcol == nil {
						return sqlStringify(data[col.FKey][j])
					}

					if fcol.Deupe {
						j /= len(data[col.LKey]) / len(data[fcol.ApiKey])
					}

					return sqlStringify(data[fcol.ApiKey][j])
				}

				return sqlStringify(data[col.ApiKey][i])
			},
			"match": func(s string) bool {
				flag, _ := regexp.MatchString(`^VARCHAR(\d+)$`, s)
				return flag
			},
		}).
		Parse(sqlTemplate)
	td := &templateData{
		&t, cols, pKeys, fKeys, data,
	}

	var buff bytes.Buffer
	tmpl.Execute(&buff, td)

	return buff.String()
}

func sqlFromLocales(query, table string, data flatObject) string {
	t := schema[table]

	txt := ""
	for i, ld := range data["localizations"] {
		if i < len(data["localizations"])-1 {
			txt += ld.(*localizeData).val + ";"
		} else {
			txt += ld.(*localizeData).val
		}
	}

	queires := []string{}
	for n := 1000; 1000 < len(txt); {
		n = strings.LastIndex(txt[:n], ";")
		queires = append(queires, txt[:n])
		txt = txt[n+1:]
	}
	queires = append(queires, txt)

	for _, locale := range locales {
		rexp, _ := regexp.Compile(`^([a-z]{2})_[A-Z]{2,3}$`)
		iso := rexp.FindStringSubmatch(locale["id"].(string))[1]

		items := []string{}
		for _, q := range queires {
			if iso == "en" {
				items = append(items, strings.Split(q, ";")...)
			} else {
				res := fetch(
					"POST",
					"https://"+endpoints[1]+"/api/v1/"+query,
					headers[1],
					map[string]string{"from": "en", "to": iso, "text": q},
				)

				if r, ok := res["trans"]; !ok {
					fmt.Println(res)
					return ""
				} else {
					items = append(items, strings.Split(r.(string), ";")...)
				}
			}
		}

		for i, ld := range data["localizations"] {
			ld := ld.(*localizeData)
			t := ld.table
			tokens := []string{
				t.Name,
				ld.col.Name,
				fmt.Sprintf("%d", int(ld.id)),
			}

			l := locale
			token := ""
			for len(tokens) > 1 {
				token = tokens[0]
				if _, ok := l[token]; !ok {
					l[token] = map[string]interface{}{}
				}
				tokens = tokens[1:]
				l = l[token].(map[string]interface{})
			}

			l[tokens[0]] = strings.TrimSpace(items[i])
		}

		val, _ := json.Marshal(locale)
		data["locales:id"] = append(data["locales:id"], locale["id"])
		data["locales:locale"] = append(data["locales:locale"], string(val))
	}

	tmpl, _ := template.New("sql").
		Funcs(template.FuncMap{
			"sub": func(a, b int) int { return a - b },
			"row": func(col *column) interface{} { return data[col.ApiKey] },
			"item": func(col *column, i int) interface{} {
				return sqlStringify(data[col.ApiKey][i])
			},
			"match": func(s string) bool {
				flag, _ := regexp.MatchString(`^VARCHAR(\d+)$`, s)
				return flag
			},
		}).
		Parse(sqlTemplate)
	td := &templateData{
		&t, t.Cols, []*column{t.Cols[0]}, nil, data,
	}

	var buff bytes.Buffer
	tmpl.Execute(&buff, td)

	return buff.String()
}

func init() {
	godotenv.Load(".env")

	if f, err := os.ReadFile(os.Getenv("SCHEMA_PATH")); err != nil {
		panic(err)
	} else {
		schema = map[string]table{}
		json.Unmarshal(f, &schema)
	}

	if dir, err := os.ReadDir(os.Getenv("LOCALE_PATH")); err != nil {
		panic(err)
	} else {
		locales = []jsonObject{}
		for _, fd := range dir {
			if f, err := os.ReadFile(os.Getenv("LOCALE_PATH") + "/" + fd.Name()); err != nil {
				panic(err)
			} else {
				l := map[string]interface{}{}
				json.Unmarshal(f, &l)
				locales = append(locales, l)
			}
		}
	}

	secret = strings.TrimSpace(secret)
	headers[0]["x-rapidapi-key"] = secret
	headers[1]["x-rapidapi-key"] = secret
}
