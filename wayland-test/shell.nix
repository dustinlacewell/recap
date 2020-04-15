let
  pkgs = import <nixpkgs> {};
  recap = (import ../default.nix).override {
    maim = pkgs.writeScriptBin "maim" ''grim $@'';
    slop = pkgs.writeScriptBin "slop" ''slurp $@'';
    xdpyinfo = pkgs.writeScriptBin "xdpyinfo" ''
      echo "dimensions $(swaymsg -p -t get_outputs | grep mode | awk '{print $3}')"
    '';
  };

in pkgs.stdenv.mkDerivation {
  name = "recap-wayland-test";
  buildInputs = with pkgs; [
    # System requirements.
    readline
    which
    gcc
    binutils
    openssl
    python36Packages.poetry
    sway
    grim
    slurp
    alacritty
    recap
  ];
  src = null;
  PIPENV_VENV_IN_PROJECT=1;

  shellHook = ''
    # Allow the use of wheels.
    SOURCE_DATE_EPOCH=$(date +%s)
    # Augment the dynamic linker path
    export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:${pkgs.readline}/lib
  '';
}
