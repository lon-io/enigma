import time


# Maps from a position to it's character
def get_position_for_character(character):
    # TODO: Validate between A and Z
    return ord(character.upper()) - ord('A') + 1

# Maps from a character to it's position
def get_character_for_position(position):
    # TODO: Validate between 1 and 26
    return chr(ord('A') + position - 1)

def number_has_odd_digit(value):
    digits_str = str(value)

    for i in digits_str:
        if int(i) % 2 == 1:
            return True

    return False

# Helps to mark the time spent on an algorithm
def timer():
    def marker():
        return time.time()

    start = marker()
    def end_marker():
        end = marker()

        print(f'Time elapsed (seconds): {end - start}')
        print()

    return end_marker

# Helps to mark the number off steps in an algorithm's completion
def mark_steps(label, steps):
    print(f'[Code {label}] - Broken after {steps} number of steps')

# Helps to build a list of tuple of pairs for a reflector character set
def get_reflector_mapping_pairs(characters):
    result = []
    copy_of_characters = characters.copy()
    for i in range(26):
        if len(copy_of_characters) == 0:
            break

        pair_index = get_position_for_character(characters[i]) - 1
        if characters[i] in copy_of_characters:
            result.append((characters[i], characters[pair_index]))
            copy_of_characters.remove(characters[i])
            copy_of_characters.remove(characters[pair_index])

    return result

# Helps to flatten a list of tuple of pairs for a reflector back to a character set
def flatten_reflector_mapping_pairs(mapping_pairs):
    result = ['' for i in range(26)]
    for letter_one, letter_two in mapping_pairs:
        ord_one = ord(letter_one)
        ord_two = ord(letter_two)
        ord_a = ord('A')

        result[ord_one - ord_a] = chr(ord_two)
        result[ord_two - ord_a] = chr(ord_one)

    return result
