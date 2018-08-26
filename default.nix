with (import ((import <nixpkgs> { }).fetchFromGitHub {
  owner = "NixOS";
  repo = "nixpkgs";
  rev = "0fd58ed0997009431306e9b0ad36016f8bdab73e";
  sha256 = "00d8g17dfwkwxh45359ji7cl4lwx7c1g5w5y7pli7c57n48qqcay";
})) { config = { }; };
  callPackage ./release.nix {}
