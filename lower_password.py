from itertools import product

# Ask for password length
length = int(input("Enter password length (e.g. 2, 3, 4): "))

# Define the character set
chars = 'abcdefghijklmnopqrstuvwxyz'

# File to save passwords
filename = f"char_passwords_{length}_letters.txt"

# Generate and save
with open(filename, "w") as file:
    for combo in product(chars, repeat=length):
        file.write(''.join(combo) + "\n")

print(f"✅ All {length}-letter passwords saved to {filename}")
print(f"Total passwords generated: {len(chars) ** length:,}")

