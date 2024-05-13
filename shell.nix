let
    pkgs = import (fetchTarball "https://github.com/NixOS/nixpkgs/tarball/nixos-23.11") {};
in
pkgs.mkShellNoCC {
    packages = with pkgs; [
        python3
    ];
    
    shellHook = "sudo pip install -r requirements.txt";
}