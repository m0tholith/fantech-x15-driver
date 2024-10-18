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
    "show_desktop"
    "double_leftclick"
    "fire"
    "off"
    "dpiplus"
    "dpiminus"
  ];
  modeType =
    { ... }:
    {
      options = {
        enabled = mkOption {
          type = types.bool;
          default = true;
        };
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
in
{
  options.services.fantech-x15 = {
    enable = mkEnableOption "Fantech Phantom X15 Driver";
    settings = rec {
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
      led.time = mkOption {
        type = types.ints.between 0 6;
        default = 2;
        description = ''
          Duration of LED animation. Used only when LED type is "static" or "cyclic."
          Range is between 0 and 6 (inclusive).
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

      modes = mkOption {
        type = types.listOf (types.submodule modeType);
        default = [
          {
            enabled = true;
            dpi = 200;
            color = "111";
          }
          {
            enabled = true;
            dpi = 600;
            color = "445";
          }
          {
            enabled = true;
            dpi = 1000;
            color = "CDF";
          }
          {
            enabled = true;
            dpi = 1600;
            color = "47F";
          }
          {
            enabled = true;
            dpi = 2400;
            color = "6E6";
          }
          {
            enabled = true;
            dpi = 4800;
            color = "F46";
          }
        ];
        description = ''
          List of mouse modes. Definition:
          {
            enabled: bool;
            dpi: int; # 200, 400, 600, 800, 1000, 1200, 1600, 2000, 2400, 3200, 4000, 4800
            color: str; # 24-bit RGB: "1B4", "FC9"
          }
        '';
      };

      defaultMode = mkOption {
        type = types.ints.between 1 6;
        default = 5;
        description = ''
          Default/initial mouse mode.
          Default: 5
        '';
      };
      fireSpeed = mkOption {
        type = types.ints.between 0 300;
        default = 50;
        description = ''
          Speed of the fire key, in milliseconds.
          Default: 50ms
        '';
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
    xdg.configFile."fantech/x15.toml" = {
      enable = true;
      source = (pkgs.formats.toml { }).generate "x15.toml" cfg.settings;
    };
  };
}
