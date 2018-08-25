{ python3Packages, maim, slop, ffmpeg }:

with python3Packages;

python3Packages.buildPythonApplication {
  name = "recap";
  src = ./.;
  checkInputs = [ pytest ];
  propagatedBuildInputs =  [ click maim slop ffmpeg ];
}
