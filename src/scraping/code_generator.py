from itertools import product
from string import ascii_uppercase




# Generate invite codes using all upper case permutations of the first two characters
def generate_codes_with_prefix(start_prefix='EW',start=1, end=10):
    codes = []
    alphabet_permutations = [''.join(pair) for pair in product(ascii_uppercase, repeat=2)]
    index = alphabet_permutations.index(start_prefix)

    for num in range(start, end + 1):
        numeric_component = f"{num:07d}"

        for prefix in alphabet_permutations[index:]:
            invite_code = f"{prefix}{numeric_component}"
            codes.append(invite_code)

    return codes


def generate_code(start,end):
        codes = []
        
        for num in range(start, end+1):
            # Generate zero-padded numeric component
            numeric_component = f"{num:07d}"
            
            # Create the invite code by combining the prefix "HA" and the numeric component
            invite_code = f"HA{numeric_component}"
            
            codes.append(invite_code)
            
        return codes





# Example: Generate 10 invite codes with permutations of 2 characters from the alphabet
invite_codes_with_prefix = generate_codes_with_prefix('AA',20,25)

print(f"Total number of codes: {len(invite_codes_with_prefix)}")

