{
  pkgs ? import <nixpkgs> { },
}:
pkgs.mkShell {
  buildInputs = with pkgs; [
    python3
    usbutils
    python3Packages.pyusb
    libusb1
  ];
}
