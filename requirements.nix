{ python3Packages, fetchFromGitHub }:

with python3Packages;

rec {
  setuptools_scm = buildPythonPackage {
    name = "setuptools_scm";
    src = fetchFromGitHub {
      owner = "pypa";
      repo = "setuptools_scm";
      rev = "19e3c8d636dd54d901c684d169655b87887dc990";
      sha256 = "0kd5id1inmj6d8g8a9k1r2wii177m0s78bc7jgg5ch19i68jc01h";
    };
  };
  pytest-runner = buildPythonPackage {
    name = "pytest-runner";
    src = fetchFromGitHub {
      owner = "pytest-dev";
      repo = "pytest-runner";
      rev = "8355b65ff6d3a15b3910f3a8c2c982f6a299b0e5";
      sha256 = "1sbs5k341p578lyniisrqp2326l74mgc3iypl27k6cp1knhz62g3";
    };
    buildInputs = [ setuptools_scm ];
    propagatedBuiltInputs = [ pytest ];
  };
  xdg = buildPythonPackage {
    name = "xdg";
    src = fetchFromGitHub {
      owner = "srstevenson";
      repo = "xdg";
      rev = "91ee21928a159f486da09ac7bf9bd246dd54f518";
      sha256 = "12r6rav6gmyygihaaxwz0fmilz45x4hl39vg1027kpmfs83q4b5n";
    };
    checkInputs = [ pytest ];
  };
}
