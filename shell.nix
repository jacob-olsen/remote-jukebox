# shell.nix
let
  pkgs = import (fetchTarball "https://github.com/NixOS/nixpkgs/archive/59e618d90c065f55ae48446f307e8c09565d5ab0.tar.gz") {};
in pkgs.mkShell {
  packages = [
    (pkgs.python3.withPackages (python-pkgs: with python-pkgs; [
      # select Python packages here
      flask
      python-vlc
    ]))
    pkgs.vlc
    pkgs.uv
  ];
}
