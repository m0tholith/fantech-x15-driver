{
  config,
  pkgs,
  lib,
  ...
}:
with lib;
let
  cfg = config.services.fantech-x15;
  keys = [
    "leftclick"
    "middleclick"
    "rightclick"
    "forward"
    "backward"
    "dpiloop"
    "showdesktop"
    "doubleclick"
    "fire"
    "off"
    "dpiplus"
    "dpiminus"
  ];
in
{
  options.services.fantech-x15 = {
    enable = mkEnableOption "Fantech Phantom X15 Driver";

    led.type = mkOption {
      type = types.enum [
        "off"
        "static"
        "fixed"
        "cyclic"
      ];
      default = "static";
      description = ''
        Type of LED mode to set.
        Available values: off, static, fixed, cyclic
        Default: static
      '';
    };
    led.blinkTime = mkOption {
      type = types.ints.between 1 6;
      default = 2;
      description = ''
        Duration of LED animation. Used only when LED type is "static" or "cyclic."
        Range is between 1 and 6 (inclusive).
        Default: 2s
      '';
    };

    keymaps.lmb = mkOption {
      type = types.enum keys;
      default = "leftclick";
      description = ''
        Key to assign to left mouse button.
        Available values: leftclick, middleclick, rightclick, forward, backward, dpiloop, showdesktop, doubleclick, fire, off, dpiplus, dpiminus
        Default: leftclick
      '';
    };
    keymaps.scrollButton = mkOption {
      type = types.enum keys;
      default = "middleclick";
      description = ''
        Key to assign to scroll button.
        Available values: leftclick, middleclick, rightclick, forward, backward, dpiloop, showdesktop, doubleclick, fire, off, dpiplus, dpiminus
        Default: middleclick
      '';
    };
    keymaps.rmb = mkOption {
      type = types.enum keys;
      default = "rightclick";
      description = ''
        Key to assign to right mouse button.
        Available values: leftclick, middleclick, rightclick, forward, backward, dpiloop, showdesktop, doubleclick, fire, off, dpiplus, dpiminus
        Default: rightclick
      '';
    };
    keymaps.forward = mkOption {
      type = types.enum keys;
      default = "forward";
      description = ''
        Key to assign to forward button.
        Available values: leftclick, middleclick, rightclick, forward, backward, dpiloop, showdesktop, doubleclick, fire, off, dpiplus, dpiminus
        Default: forward
      '';
    };
    keymaps.backward = mkOption {
      type = types.enum keys;
      default = "backward";
      description = ''
        Key to assign to backward button.
        Available values: leftclick, middleclick, rightclick, forward, backward, dpiloop, showdesktop, doubleclick, fire, off, dpiplus, dpiminus
        Default: backward
      '';
    };
    keymaps.plus = mkOption {
      type = types.enum keys;
      default = "dpiplus";
      description = ''
        Key to assign to plus button.
        Available values: leftclick, middleclick, rightclick, forward, backward, dpiloop, showdesktop, doubleclick, fire, off, dpiplus, dpiminus
        Default: dpiplus
      '';
    };
    keymaps.minus = mkOption {
      type = types.enum keys;
      default = "dpiminus";
      description = ''
        Key to assign to minus button.
        Available values: leftclick, middleclick, rightclick, forward, backward, dpiloop, showdesktop, doubleclick, fire, off, dpiplus, dpiminus
        Default: dpiminus
      '';
    };

    mode1 = mkOption {
      type = types.submodule {
        enabled = mkEnableOption;
        dpi = mkOption {
          type = types.enum [
            200
            400
            600
            800
            1000
            1200
            1600
            2000
            2400
            3200
            4000
            4800
          ];
          default = 1600;
        };
        color = mkOption {
          type = types.str;
          default = "FFF";
        };
      };
    };
    mode2 = mkOption {
      type = types.submodule {
        enabled = mkEnableOption;
        dpi = mkOption {
          type = types.enum [
            200
            400
            600
            800
            1000
            1200
            1600
            2000
            2400
            3200
            4000
            4800
          ];
          default = 1600;
        };
        color = mkOption {
          type = types.str;
          default = "FFF";
        };
      };
    };
    mode3 = mkOption {
      type = types.submodule {
        enabled = mkEnableOption;
        dpi = mkOption {
          type = types.enum [
            200
            400
            600
            800
            1000
            1200
            1600
            2000
            2400
            3200
            4000
            4800
          ];
          default = 1600;
        };
        color = mkOption {
          type = types.str;
          default = "FFF";
        };
      };
    };
    mode4 = mkOption {
      type = types.submodule {
        enabled = mkEnableOption;
        dpi = mkOption {
          type = types.enum [
            200
            400
            600
            800
            1000
            1200
            1600
            2000
            2400
            3200
            4000
            4800
          ];
          default = 1600;
        };
        color = mkOption {
          type = types.str;
          default = "FFF";
        };
      };
    };
    mode5 = mkOption {
      type = types.submodule {
        enabled = mkEnableOption;
        dpi = mkOption {
          type = types.enum [
            200
            400
            600
            800
            1000
            1200
            1600
            2000
            2400
            3200
            4000
            4800
          ];
          default = 1600;
        };
        color = mkOption {
          type = types.str;
          default = "FFF";
        };
      };
    };
    mode6 = mkOption {
      type = types.submodule {
        enabled = mkEnableOption;
        dpi = mkOption {
          type = types.enum [
            200
            400
            600
            800
            1000
            1200
            1600
            2000
            2400
            3200
            4000
            4800
          ];
          default = 1600;
        };
        color = mkOption {
          type = types.str;
          default = "FFF";
        };
      };
    };
  };

  config = mkIf cfg.enable {
    home.packages =
      let
        fantech-x15-driver = pkgs.callPackage ./default.nix { };
      in
      [
        fantech-x15-driver
      ];
  };
}
