from itertools import product
import string
import sys

# --- USER INPUT ---
length = int(input("Enter password length (e.g. 3, 4, 5, 6): "))

# Character set: lowercase, uppercase, digits, symbols
chars = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation
# Example characters: a-z A-Z 0-9 !@#$%^&*()_+ etc.

filename = f"passwords_fullset_{length}_chars.txt"
total = len(chars) ** length
count = 0

print(f"\nGenerating {total:,} possible passwords... (this may take time)\n")

# --- GENERATE AND SAVE ---
with open(filename, "w", encoding="utf-8") as file:
    for combo in product(chars, repeat=length):
        file.write(''.join(combo) + "\n")
        count += 1

        # Show progress every 1% or at least every 1,000 lines
        if count % (total // 100 or 1000) == 0:
            percent = (count / total) * 100
            sys.stdout.write(f"\rProgress: {percent:.0f}% ({count:,}/{total:,})")
            sys.stdout.flush()

print(f"\n✅ Done! All {length}-character passwords saved to {filename}")
print(f"Total passwords generated: {total:,}")
