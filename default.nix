{ lib, python3Packages }:
python3Packages.buildPythonApplication {
  pname = "fantech-x15-driver";
  version = "0.1.0";

  propagatedBuildInputs = with python3Packages; [
    pyusb
    toml
  ];

  src = ./.;

  meta = {
    description = "Driver for Fantech X15";
    homepage = "https://github.com/m0tholith/fantech-x15-driver";
    license = lib.licenses.gpl3Only;
    mainProgram = "fantech-x15-driver";
  };
  
  build-system = with python3Packages; [
    setuptools
  ];
  pyproject = true;
}
