{ python3Packages }:
python3Packages.buildPythonApplication {
  pname = "fantech-x15-driver";
  version = "0.1.0";

  propagatedBuildInputs = with python3Packages; [
    pyusb
    toml
  ];

  src = ./.;
}
