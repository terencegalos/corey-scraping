from itertools import product
from string import ascii_uppercase




# Generate invite codes using all upper case permutations of the first two characters
def generate_codes_with_prefix(start_prefix='',start=1000, end=5000):
    codes = []
    alphabet_permutations = [''.join(pair) for pair in product(ascii_uppercase, repeat=2)]
    index = alphabet_permutations.index(start_prefix)

    for num in range(start, end + 1):
        numeric_component = f"{num:07d}"

        for prefix in alphabet_permutations[index:]:
            invite_code = f"{prefix}{numeric_component}"
            codes.append(invite_code)

    return codes


def generate_code(start,end,prefix,width=7):
        codes = []
        
        for num in range(start, end+1):
            # Generate zero-padded numeric component
            numeric_component = f"{num:0{width}d}"
            
            # Create the invite code by combining the prefix "HA" and the numeric component
            invite_code = f"{prefix}{numeric_component}" # mobilendloan
            # invite_code = f"NA{numeric_component}" # myonlineloanpro
            
            codes.append(invite_code)
            
        return codes

def generate_code_gen(start,end,prefix,width=7,batch_size=100):
        
        print(f'Generating codes.')
        codes = []
        
        for num in range(start, end+1):
            # Generate zero-padded numeric component
            numeric_component = f"{num:0{width}d}"
            
            # Create the invite code by combining the prefix "HA" and the numeric component
            invite_code = f"{prefix}{numeric_component}" # mobilendloan
            # invite_code = f"NA{numeric_component}" # myonlineloanpro
            print(f'invite code: {invite_code}')
            
            codes.append(invite_code)

            if len(codes) % batch_size == 0:
                 yield codes
                 codes = []
            
        
        # yield remaining codes
        if codes:
            yield codes

def num_generator(last_interrupt = 1):

     num = last_interrupt

     while True:
          yield num
          num += 1





# Example: Generate 10 invite codes with permutations of 2 characters from the alphabet
invite_codes_with_prefix = generate_codes_with_prefix('HA',101100,150000) # mobilendloan
# invite_codes_with_prefix = generate_codes_with_prefix('AA',100,500) # myonlineloanpro

# print(f"Total number of codes: {len(invite_codes_with_prefix)}")

