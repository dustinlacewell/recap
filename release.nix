{ callPackage, fetchFromGitHub, python3Packages, maim, slop, ffmpeg, xclip, xorg }:

with python3Packages;

let
  reqs = import ./requirements.nix { inherit python3Packages fetchFromGitHub; };

in buildPythonApplication {
  name = "recap";
  src = ./.;
  checkInputs = [ pytest ];
  checkPhase = null;
  propagatedBuildInputs =  [
    # python
    reqs.addict
    attrdict
    click
    toml
    reqs.python-rofi

    # system
    ffmpeg
    maim
    slop
    xclip
    xorg.xdpyinfo
  ];
}
