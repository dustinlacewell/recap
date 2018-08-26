{ callPackage, fetchFromGitHub, python3Packages, maim, slop, ffmpeg, xorg }:

with python3Packages;

buildPythonApplication {
  name = "recap";
  src = ./.;
  checkInputs = [ pytest ];
  checkPhase = null;
  propagatedBuildInputs =  [
    toml click maim slop ffmpeg xorg.xdpyinfo ];
}
