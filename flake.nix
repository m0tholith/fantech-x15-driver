{
  description = "Flake utils demo";

  inputs.nixpkgs.url = "github:nixos/nixpkgs?ref=nixpkgs-unstable";
  inputs.flake-utils.url = "github:numtide/flake-utils";

  outputs =
    {
      self,
      nixpkgs,
      flake-utils,
    }:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
      in
      {
        packages = rec {
          fantech-x15-driver = pkgs.python3Packages.buildPythonApplication {
            pname = "fantech-x15-driver";
            version = "0.1.0";

            propagatedBuildInputs = with pkgs.python3Packages; [
              pyusb
              toml
            ];

            src = ./.;
          };
          default = fantech-x15-driver;
        };
        devShells.default = pkgs.mkShell {
          propagatedBuildInputs = with pkgs; [
            usbutils

            python3
            python3Packages.pyusb
            python3Packages.toml
          ];
        };
      }
    );
}
