# BitBlaster
uploads firmware to an arduino leonardo using avrdude

## Functions

- `list`: lists all available COM ports
- `upload`: starts the upload process at the given COM port for Arduino Leonardo using avrdude. The `firmware.hex` file should be at the same path as the `BitBlaster.py`
- `help`: provides help for the usage

## ⚠️Disclaimers
- Requires Python to be installed
- Only tested on Windows
- the hex file must be called `firmware.hex`
