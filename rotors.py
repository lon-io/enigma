from abc import ABC, abstractmethod

from constants import CurrentFlowDirections, RotorDirections
from helpers import *
from rotor_mappings import *

"""
    :param label: The label indicating the specs of this rotor
    :type label: string
"""
class Rotor(ABC):
    def __init__(self, **kwargs):
        self.label = ''

        # Characters as they map to the 26 letter English alphabet
        self.characters = []

        # Character on which the notch is hit
        self.notch_character = None

        self.__set_state(**kwargs)

    # Forces an overide of the initial character set for the rotor
    def override_characters(self, new_characters):
        self.characters = new_characters

    # Resets the state|configuration for the rotor
    def reset_state(self, **kwargs):
        self.__set_state(**kwargs)

    # Sets the state|configuration for the rotor
    def __set_state(self, *, initial_position = 1, ring_setting = 1):
        self.set_slot_position()
        self.set_initial_position(initial_position)
        self.set_ring_setting(ring_setting)

    # Setter for the rotor's position in the machine's slots
    def set_slot_position(self, slot_position = 1):
        # 1 is the rightmost, 2, 3 , 4 are the left (increasing); Defaults to 1
        self.position_in_slots = slot_position

    # Setter for the rotor's initial position (and current position)
    def set_initial_position(self, initial_position):
        # Initial character position (can be character A and Z or number between 1 and 26)
        self.initial_position = get_position_for_character(initial_position) if isinstance(initial_position, str) else initial_position

        # Current character position
        self.current_position = self.initial_position

    # Setter for the rotor's ring settings
    def set_ring_setting(self, ring_setting):
        # Ring Setting number
        self.ring_setting = ring_setting

    @staticmethod
    # Gets the index for a character in the traditional English alphabet
    def get_alphabet_index(character):
        return ord(character.upper()) - ord('A')

    # Gets the index for a character in the rotors alphabet mapping
    def get_mapping_index(self, character):
        return self.characters.index(character)

    @staticmethod
    # Positions may grow out of the 1 to 26 boundary; this normalizes them
    def normalize_character_position(position):
        if position <= 0:
            alphabet_diff = 0 - position
            position = 26 - alphabet_diff
        elif position > 26:
            alphabet_diff = position - 26
            position = 0 + alphabet_diff

        return position

    @staticmethod
    # Indices may grow out of the 0 to 25 boundary; this normalizes them
    def normalize_character_index(index):
        if index < 0:
            alphabet_diff = 0 - index
            index = 26 - alphabet_diff
        elif index > 25:
            alphabet_diff = index - 26
            index = 0 + alphabet_diff

        return index

    @property
    # Character representation for the current position
    def current_character(self):
        return get_character_for_position(self.current_position)

    @property
    # Identifies if the rotor is at it's notch point
    def is_at_notch(self):
        return self.notch_character != None and self.current_character == self.notch_character

    @property
    # Converting the ring setting to a zero based index
    def ring_setting_offset(self):
        return self.ring_setting - 1

    @property
    # Distance between the current position and initial position
    def initial_position_offset(self):
        return self.current_position - self.initial_position

    # Rotor rotation - essentially changing the current position
    def rotate(self, direction = RotorDirections.CLOCKWISE):
        new_position = self.normalize_character_position(self.current_position + direction.value)

        self.current_position = new_position

    # Converts a character across a rotor in either direction
    def handle_key_encoding(self, character, direction = CurrentFlowDirections.FORWARD):
        rotor_offset = self.current_position - get_position_for_character('A')

        if (direction == CurrentFlowDirections.FORWARD):
            matching_rotor_pin_position = get_position_for_character(character) + rotor_offset - self.ring_setting_offset
            matching_rotor_pin = self.normalize_character_position(matching_rotor_pin_position)
            matching_rotor_character = get_character_for_position(matching_rotor_pin)

            encoded_character = self.encode_right_to_left(matching_rotor_character)

            matching_rotor_contact_position = get_position_for_character(encoded_character) - rotor_offset + self.ring_setting_offset
            matching_rotor_contact = self.normalize_character_position(matching_rotor_contact_position)
            encoded_character = get_character_for_position(matching_rotor_contact)

            return encoded_character
        else:
            matching_rotor_contact_position = get_position_for_character(character) + rotor_offset - self.ring_setting_offset
            matching_rotor_contact = self.normalize_character_position(matching_rotor_contact_position)
            matching_rotor_character = get_character_for_position(matching_rotor_contact)

            encoded_character = self.encode_left_to_right(matching_rotor_character)

            matching_rotor_pin_position = get_position_for_character(encoded_character) - rotor_offset + self.ring_setting_offset
            matching_rotor_pin = self.normalize_character_position(matching_rotor_pin_position)
            encoded_character = get_character_for_position(matching_rotor_pin)

            return encoded_character

    # Forward direction encoding
    def encode_right_to_left(self, character):
        character_index = self.get_alphabet_index(character)

        return self.characters[character_index]

    # Reverse direction encoding
    def encode_left_to_right(self, character):
        character_index = self.get_mapping_index(character)

        return chr(character_index + ord('A'))

class BetaRotor(Rotor):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.label = 'Beta'
        self.characters = BetaRotorMapping

class GammaRotor(Rotor):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.label = 'Gamma'
        self.characters = GammaRotorMapping

class IRotor(Rotor):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.label = 'I'
        self.characters = IRotorMapping
        self.notch_character = 'Q'

class IIRotor(Rotor):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.label = 'II'
        self.characters = IIRotorMapping
        self.notch_character = 'E'

class IIIRotor(Rotor):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.label = 'III'
        self.characters = IIIRotorMapping
        self.notch_character = 'V'

class IVRotor(Rotor):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.label = 'IV'
        self.characters = IVRotorMapping
        self.notch_character = 'J'

class VRotor(Rotor):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.label = 'V'
        self.characters = VRotorMapping
        self.notch_character = 'Z'

class ARotor(Rotor):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.label = 'A'
        self.characters = ARotorMapping

class BRotor(Rotor):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.label = 'B'
        self.characters = BRotorMapping

class CRotor(Rotor):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.label = 'C'
        self.characters = CRotorMapping

def get_all_rotors():
    return {
        'Beta': BetaRotor,
        'Gamma': GammaRotor,
        'I': IRotor,
        'II': IIRotor,
        'III': IIIRotor,
        'IV': IVRotor,
        'V': VRotor,
        'A': ARotor,
        'B': BRotor,
        'C': CRotor
    }

def rotor_from_name(name):
    rotors_dict = get_all_rotors()

    if name in rotors_dict:
        cls = rotors_dict[name]
    else:
        raise ValueError('There is no Rotor for the specified name')

    return cls()

def rotor_cls_from_name(name):
    rotors_dict = get_all_rotors()

    if name in rotors_dict:
        cls = rotors_dict[name]
    else:
        raise ValueError('There is no Rotor for the specified name')

    return cls

def assert_rotors():
    rotors_dict = get_all_rotors()

    for (_, rotor_cls) in rotors_dict.items():
        rotor = rotor_cls()
        assert(len(set(rotor.characters)) == 26)

    rotor = rotor_from_name("I")
    assert(rotor.encode_right_to_left("A") == "E")
    assert(rotor.encode_left_to_right("A") == "U")

if __name__ == "__main__":
    assert_rotors()
    pass
