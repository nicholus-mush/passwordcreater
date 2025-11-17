from itertools import product

digits = '0123456789'

with open("4_digit_passwords.txt", "w") as file:
    for combo in product(digits, repeat=4):  # 4 digits, repetition allowed
        file.write(''.join(combo) + "\n")

print("✅ All 4-digit passwords (0000–9999) saved to 4_digit_passwords.txt")
