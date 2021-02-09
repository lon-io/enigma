# Enigma Machine

This code base contains the source code for simulating an Enigma Machine

## Prerequisites

The only requirements is having Python (preferably Python3) installed

## Files

- `enigma.py`: Contains the following representational Models:
  - Enigma Machine
  - Plug Lead
  - Plug Board

- `rotors.py`: Contains the following representational Models:
  - Rotor (Base Class)
  - A, B, C, I, II, III, IV, V, Beta, Gamma Rotor Classes
  - Functions for generating rotors from labels

- `cli.py`: A CLI for interacting with the simulation

- `rotor_mappings.py`: Static definition of Rotor character mappings according to the specification

- `helpers.py`: Helper methods for various Enigma based operations

- `constants.py`: Enums (and potentially other constant values) for various Enigma based operations

## Usage

CLI:

```bash
python3 cli.py rt="I II III" rf="C" rtr="1 14 26" rtp="A B E" pl="AC DE LH"
```

## Contributing

TBD

## License

[MIT](https://choosealicense.com/licenses/mit/)
