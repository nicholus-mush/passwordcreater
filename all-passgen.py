from itertools import product
import string
import sys
import math
import zipfile
import os

print("\n=== PASSWORD COMBINATION GENERATOR ===")
print("Choose character types to include:")
include_lower = input("Include lowercase letters (a-z)? [y/n]: ").strip().lower() == 'y'
include_upper = input("Include uppercase letters (A-Z)? [y/n]: ").strip().lower() == 'y'
include_digits = input("Include digits (0-9)? [y/n]: ").strip().lower() == 'y'
include_symbols = input("Include symbols (!@#$%^&* etc.)? [y/n]: ").strip().lower() == 'y'

# --- Build character set based on user choices ---
chars = ""
if include_lower: chars += string.ascii_lowercase
if include_upper: chars += string.ascii_uppercase
if include_digits: chars += string.digits
if include_symbols: chars += string.punctuation

if not chars:
    print("⚠️ You must select at least one character type!")
    sys.exit()

# --- Get password length and split limit ---
length = int(input("\nEnter password length (e.g. 3, 4, 5): "))
split_limit = 1_000_000  # lines per file

total = len(chars) ** length
count = 0
file_index = 1
split_count = math.ceil(total / split_limit)
output_files = []

print(f"\nGenerating {total:,} passwords...")
print(f"Character set: {chars}")
print(f"Output will be split into about {split_count:,} files (~{split_limit:,} lines each)\n")

# --- INITIAL FILE SETUP ---
filename = f"passwords_part{file_index}_len{length}.txt"
file = open(filename, "w", encoding="utf-8")
output_files.append(filename)

# --- GENERATE & SAVE ---
for combo in product(chars, repeat=length):
    file.write(''.join(combo) + "\n")
    count += 1

    # Auto-split when file limit reached
    if count % split_limit == 0 and count < total:
        file.close()
        file_index += 1
        filename = f"passwords_part{file_index}_len{length}.txt"
        file = open(filename, "w", encoding="utf-8")
        output_files.append(filename)

    # Show progress
    if count % (total // 100 or 1000) == 0:
        percent = (count / total) * 100
        sys.stdout.write(f"\rProgress: {percent:.0f}% ({count:,}/{total:,})")
        sys.stdout.flush()

file.close()
print(f"\n✅ Done! Generated {total:,} passwords across {split_count:,} file(s).")

# --- ZIP COMPRESSION ---
zip_name = f"passwords_len{length}.zip"
with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for f in output_files:
        zipf.write(f)
        os.remove(f)  # remove the txt file after adding to zip

print(f"✅ All files compressed into {zip_name}")

