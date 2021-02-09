
from constants import CurrentFlowDirections
from rotors import *

PLUG_LEADS_LIMIT = 10

class PlugLead:
    def __init__(self, mapping):
        self.setMapping(mapping)

    def setMapping(self, mapping):
        if len(mapping) != 2 or mapping[0] == mapping[1]:
            raise ValueError('You can only connect 2 leads and they must be of different values')

        self.mapping = {}
        self.mapping[mapping[0]] = mapping[1]
        self.mapping[mapping[1]] = mapping[0]

    def encode(self, character):
        if character in self.mapping:
            return self.mapping[character]
        else:
            return character

class Plugboard:
    def __init__(self, plug_leads = []):
        self.plug_leads = plug_leads

    def encode(self, character):
        result = character
        for plug_lead in self.plug_leads:
            result = plug_lead.encode(character)

            # Break as early as possible
            if result != character:
                break

        return result

    def add(self, plug_lead):
        if len(self.plug_leads) == PLUG_LEADS_LIMIT:
            raise Exception(f'You cannot have more than {PLUG_LEADS_LIMIT} plug leads')

        self.plug_leads.append(plug_lead)

    @staticmethod
    def generate_plug_leads(mapping = []):
        return [PlugLead(pair) for pair in mapping]


class EnigmaMachine:
    def __init__(self, rotors, reflector, leads_mapping = []):
        self.__set_state(rotors, reflector, leads_mapping)

    # Resets the state of the machine to the given config
    def reset_state(self, rotors, reflector, leads_mapping = []):
        self.__set_state(rotors, reflector, leads_mapping)

    # Internal state setter
    def __set_state(self, rotors, reflector, leads_mapping = []):
        # Reverse to slots order
        self.rotors = rotors[::-1]
        self.reflector = reflector
        self.set_plugboard(leads_mapping)
        self.set_rotor_positions()

    # Setter for the Machine's plugboard
    def set_plugboard(self, leads_mapping):
        plug_leads = Plugboard.generate_plug_leads(leads_mapping)
        self.plug_board = Plugboard(plug_leads)

    # Sets the positions of the rotors
    def set_rotor_positions(self):
        for i, rotor in enumerate(self.rotors):
            rotor.set_slot_position(i + 1)

    # Sets a single Machine rotor
    def set_single_rotor(self, rotor, slot_position):
        rotor_index = slot_position - 1

        if rotor_index < 0 or rotor_index >= len(self.rotors):
            raise IndexError(f'The machine only supports {len(self.rotors)} rotors')

        self.rotors[rotor_index] = rotor

    # Setter for the Machine's reflector
    def set_reflector(self, reflector):
        self.reflector = reflector

    # Sets a single Machine rotor initial position
    def set_single_initial_position(self, slot_position, rotor_initial_position):
        if slot_position < 0 or slot_position >= len(self.rotors):
            raise IndexError(f'The machine only supports {len(self.rotors)} rotors')

        self.rotors[slot_position -1].set_initial_position(rotor_initial_position)

    # Sets a single Machine rotor ring setting
    def set_single_ring_setting(self, slot_position, ring_setting):
        if slot_position < 0 or slot_position >= len(self.rotors):
            raise IndexError(f'The machine only supports {len(self.rotors)} rotors')

        self.rotors[slot_position -1].set_ring_setting(ring_setting)

    # Rotates a Single rotor
    def rotate_single_rotor(self, slot_position, direction):
        if slot_position < 0 or slot_position >= len(self.rotors):
            raise IndexError(f'The machine only supports {len(self.rotors)} rotors')

        self.rotors[slot_position -1].rotate(direction)

    # Metadata for the rotor
    def get_rotors_meta_data(self):
        positions = ''
        ring_settings = ''
        for rotor in self.rotors[::-1]:
            positions += rotor.current_character
            ring_settings += f'{rotor.ring_setting} '

        return (positions, ring_settings)

    # Simulates the rotations that happen on a key press
    def perform_rotations(self):
        turnover_signaled = False
        for rotor in self.rotors:
            # Store before rotation
            is_at_notch = rotor.is_at_notch

            # Rotor in first slot should always rotate
            if rotor.position_in_slots == 1:
                rotor.rotate()
            # Rotors in other slot should rotate on turnover
            elif turnover_signaled:
                rotor.rotate()
            # Notch point causes rotation for only the second rotor
            elif is_at_notch and rotor.position_in_slots == 2:
                rotor.rotate()

            # Notch point causes "Turnover" in next rotor | only in 3 rotor system
            if is_at_notch and rotor.position_in_slots < 3:
                turnover_signaled = True
            else:
                turnover_signaled = False

    # Simulates the machine's operation on a key press
    def handle_key_press(self, character_key):
        self.perform_rotations()

        encoded_char = character_key

        # Current flow in the forward direction
        if self.plug_board is not None:
            encoded_char = self.plug_board.encode(character_key)

        for rotor in self.rotors:
            encoded_char = rotor.handle_key_encoding(encoded_char, CurrentFlowDirections.FORWARD)

        if self.reflector is not None:
            encoded_char = self.reflector.handle_key_encoding(encoded_char)

        # Current flow in the reverse direction
        for rotor in self.rotors[::-1]:
            encoded_char = rotor.handle_key_encoding(encoded_char, CurrentFlowDirections.REVERSE)

        if self.plug_board is not None:
            encoded_char = self.plug_board.encode(encoded_char)

        return encoded_char

    # Simulates pressing multiple keys in succession
    def encode_text(self, text):
        result = ''
        for character in text:
            result += self.handle_key_press(character)

        return result

if __name__ == "__main__":
    pass
