{ callPackage, fetchFromGitHub, python3Packages, maim, slop, ffmpeg, xclip, xorg }:

with python3Packages;

buildPythonApplication {
  name = "recap";
  src = ./.;
  checkInputs = [ pytest ];
  checkPhase = null;
  propagatedBuildInputs =  [
    # python
    attrdict
    click
    toml

    # system
    ffmpeg
    maim
    slop
    xclip
    xorg.xdpyinfo
  ];
}
