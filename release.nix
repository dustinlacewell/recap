{ callPackage, fetchFromGitHub, python3Packages, maim, slop, ffmpeg, xorg }:

with python3Packages;

let
  extra = callPackage ./requirements.nix { };

in buildPythonApplication {
  name = "recap";
  src = ./.;
  checkInputs = [ pytest ];
  checkPhase = null;
  propagatedBuildInputs =  [
    toml click maim slop ffmpeg xorg.xdpyinfo extra.xdg ];
}
