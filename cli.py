import os
import sys

from enigma import *
from rotors import *

AVAILABLE_OPTIONS = ['rt', 'rf', 'rtp,' 'rtr,' 'pl', '-h']


class EnigmaCliMachine():
    def __init__(self):
        self.rotors = []
        self.rotor_classes = []
        self.ring_settings = [1, 1, 1]
        self.rotor_positions = ['A', 'A', 'A']
        self.plug_lead_mappings = []
        self.reflector_cls = ARotor
        self.machine = ARotor

    def create_machine(self):
        self.machine = EnigmaMachine(self.rotors, self.reflector, self.plug_lead_mappings)

    def reset_machine(self):
        self.set_rotors()
        self.set_reflector()
        self.machine.reset_state(self.rotors, self.reflector, self.plug_lead_mappings)

    def accept_texts(self):
        while True:
            try:
                text = input("Please enter the text to encode or 'exit' to cancel:\n")

                if text == 'exit':
                    print('Exited')
                    sys.exit(os.EX_OK)

                encoding = self.machine.encode_text(text.upper())

                print(f'The encoding is: {encoding}')

                self.reset_machine()
            except KeyboardInterrupt:
                print('You Interrupted')
                sys.exit(os.EX_OK)
            except Exception:
                print('An error occured; please check that you passed the right settings')
                sys.exit(os.EX_USAGE)

    def print_help(self):
        print("""
Welcome to the Enigma CLI client!

## Options
rt   : Rotors (I, II, III, IV, V, Beta, Gamma)
rf   : Reflector (A, B, C)
rtp  : Rotor Starting Positions (A-Z; E.g. "A B E")
rtr  : Ring Settings (1-26; E.g. "1 14 26")
pl   : Plug Leads (E.g. "AB CD ES")
-h    : Show help

For example:
> python3 cli.py rt="I II III" rf="C" rtr="1 14 26" rtp="A B E" pl="AC DE LH"
            """)

    def parse_args(self, args):
        probably_valid_args = False
        for arg_text in args:
            if not '=' in arg_text:
                print("Please input valid arguments")
                return False
            (key, value) = arg_text.split("=")
            if key in AVAILABLE_OPTIONS:
                probably_valid_args = self.parse_arg(key, value)

        if probably_valid_args:
            self.set_rotors()
            self.set_reflector()

        return probably_valid_args

    def is_rotor_arg_value_valid(self, value):
        print(value)
        val_len = len(value)
        if val_len != 3 and val_len != 4:
            print('Please enter 3 or 4 values')
            return False

        valid_values = ['I', 'II', 'III', 'IV', 'V', 'Beta', 'Gamma']
        for i in value:
            if not i in valid_values:
                print(f'Please enter one of the following {valid_values}')
                return False

        return True

    def is_reflector_valid(self, value):
        valid_values = ['A', 'B', 'C']
        is_valid = value in valid_values

        if not is_valid:
            print(f'Please enter one of the following {valid_values}')
        return is_valid

    def is_plug_lead_mappings_valid(self, value):
        return len(value) <= 10

    def parse_arg(self, arg, value):

        if arg == 'rt':
            labels = value.split(" ")
            if not self.is_rotor_arg_value_valid(labels):
                return False
            self.set_rotors_classes(labels)
        elif arg == 'rf':
            if not self.is_reflector_valid(value):
                return False
            self.set_reflector_cls(value)
        elif arg == 'rtp':
            positions = value.split(" ")
            if not self.is_rotor_arg_value_valid(positions):
                return False
            self.set_rotor_positions(positions)
        elif arg == 'rtr':
            settings = value.split(" ")
            if not self.is_rotor_arg_value_valid(settings):
                return False
            self.set_ring_settings(settings)
        elif arg == 'pl':
            mappings = value.split(" ")
            if not self.is_plug_lead_mappings_valid(mappings):
                return False
            self.set_plug_lead_mappings(mappings)
        elif arg == '-h':
            self.print_help()
            return False
        else:
            self.print_help()
            return False

        return True

    def set_rotors_classes(self, rotor_labels):
        rotor_classes = [rotor_cls_from_name(label) for label in rotor_labels]

        self.rotor_classes = rotor_classes

    def set_rotors(self):
        self.rotors = [
            r_cls(initial_position=self.rotor_positions[i],
                  ring_setting=self.ring_settings[i])
            for i, r_cls in enumerate(self.rotor_classes)
        ]

    def set_reflector_cls(self, label):
        self.reflector = rotor_cls_from_name(label)

    def set_reflector(self):
        self.reflector = self.reflector_cls()

    def set_rotor_positions(self, positions):
        self.rotor_positions = positions

    def set_ring_settings(self, settings):
        self.ring_settings = settings

    def set_plug_lead_mappings(self, mappings):
        self.plug_lead_mappings = mappings

    def run(self):
        (_, *args) = sys.argv

        if len(args) == 0 or len(args) == 1 and args[0] == '-h':
            self.print_help()
            return

        can_proceed = self.parse_args(args)
        if can_proceed:
            self.create_machine()
            self.accept_texts()

if __name__ == "__main__":
    cli_client = EnigmaCliMachine()
    cli_client.run()
