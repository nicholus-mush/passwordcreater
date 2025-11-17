from itertools import product
import string
import sys
import math
import zipfile
import os
import random

print("\n=== ULTIMATE PASSWORD GENERATOR ===")

# --- CHARACTER SELECTION ---
print("\nChoose character types to include:")
include_lower = input("Include lowercase letters (a-z)? [y/n]: ").strip().lower() == 'y'
include_upper = input("Include uppercase letters (A-Z)? [y/n]: ").strip().lower() == 'y'
include_digits = input("Include digits (0-9)? [y/n]: ").strip().lower() == 'y'
include_symbols = input("Include symbols (!@#$%^&* etc.)? [y/n]: ").strip().lower() == 'y'

chars = ""
if include_lower: chars += string.ascii_lowercase
if include_upper: chars += string.ascii_uppercase
if include_digits: chars += string.digits
if include_symbols: chars += string.punctuation

if not chars:
    print("⚠️ You must select at least one character type!")
    sys.exit()

# --- PASSWORD LENGTH ---
length = int(input("\nEnter password length (e.g. 3, 4, 5, 6): "))
total = len(chars) ** length

# --- OPTIONS ---
shuffle_choice = input("Shuffle passwords? [y/n]: ").strip().lower() == 'y'
zip_choice = input("Compress output to ZIP? [y/n]: ").strip().lower() == 'y'
split_input = input("Split output into multiple files? [y/n]: ").strip().lower() == 'y'

split_limit = 1_000_000
if split_input:
    split_limit = int(input("Enter maximum passwords per file (e.g. 1000000): "))

print(f"\nGenerating {total:,} passwords...")
print(f"Character set: {chars}")
if split_input:
    print(f"Output will split into ~{math.ceil(total / split_limit):,} file(s) (~{split_limit:,} lines each)")
print("")

# --- FILE GENERATION ---
output_files = []
all_passwords = [] if shuffle_choice else None
count = 0
file_index = 1

if not shuffle_choice:
    filename = f"passwords_part{file_index}_len{length}.txt"
    file = open(filename, "w", encoding="utf-8")
    output_files.append(filename)

for combo in product(chars, repeat=length):
    password = ''.join(combo)
    count += 1

    if shuffle_choice:
        all_passwords.append(password)
    else:
        file.write(password + "\n")
        # Split file if needed
        if split_input and count % split_limit == 0 and count < total:
            file.close()
            file_index += 1
            filename = f"passwords_part{file_index}_len{length}.txt"
            file = open(filename, "w", encoding="utf-8")
            output_files.append(filename)

    # Progress display
    if count % (total // 100 or 1000) == 0:
        percent = (count / total) * 100
        sys.stdout.write(f"\rProgress: {percent:.0f}% ({count:,}/{total:,})")
        sys.stdout.flush()

if not shuffle_choice:
    file.close()

# --- HANDLE SHUFFLE ---
if shuffle_choice:
    print("\nShuffling passwords...")
    random.shuffle(all_passwords)
    count = 0
    file_index = 1
    temp_list = all_passwords
    all_passwords = None  # free memory

    for i, password in enumerate(temp_list, 1):
        if split_input:
            if count == 0:
                filename = f"passwords_part{file_index}_len{length}_shuffled.txt"
                file = open(filename, "w", encoding="utf-8")
                output_files.append(filename)
            file.write(password + "\n")
            count += 1
            if count >= split_limit:
                file.close()
                file_index += 1
                count = 0
        else:
            if i == 1:
                filename = f"passwords_len{length}_shuffled.txt"
                file = open(filename, "w", encoding="utf-8")
                output_files.append(filename)
            file.write(password + "\n")
    if not file.closed:
        file.close()

# --- ZIP COMPRESSION ---
if zip_choice:
    zip_name = f"passwords_len{length}.zip"
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for f in output_files:
            zipf.write(f)
            os.remove(f)  # remove txt file after adding to zip
    print(f"\n✅ All passwords compressed into {zip_name}")
else:
    print(f"\n✅ Password files saved: {', '.join(output_files)}")

print(f"Total passwords generated: {total:,}")

