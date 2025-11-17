from itertools import product
import string
import sys
import math
import zipfile
import os
import random

print("\n=== PASSWORD COMBINATION GENERATOR ===")
print("Choose character types to include:")
include_lower = input("Include lowercase letters (a-z)? [y/n]: ").strip().lower() == 'y'
include_upper = input("Include uppercase letters (A-Z)? [y/n]: ").strip().lower() == 'y'
include_digits = input("Include digits (0-9)? [y/n]: ").strip().lower() == 'y'
include_symbols = input("Include symbols (!@#$%^&* etc.)? [y/n]: ").strip().lower() == 'y'

# Build character set
chars = ""
if include_lower: chars += string.ascii_lowercase
if include_upper: chars += string.ascii_uppercase
if include_digits: chars += string.digits
if include_symbols: chars += string.punctuation

if not chars:
    print("⚠️ You must select at least one character type!")
    sys.exit()

# Password length
length = int(input("\nEnter password length (e.g. 3, 4, 5): "))
split_limit = 1_000_000  # max lines per file

total = len(chars) ** length
count = 0
file_index = 1
split_count = math.ceil(total / split_limit)
output_files = []

shuffle_choice = input("Do you want the passwords shuffled? [y/n]: ").strip().lower() == 'y'

print(f"\nGenerating {total:,} passwords...")
print(f"Character set: {chars}")
print(f"Output will be split into about {split_count:,} files (~{split_limit:,} lines each)\n")

# --- INITIAL FILE SETUP ---
filename = f"passwords_part{file_index}_len{length}.txt"
file = open(filename, "w", encoding="utf-8")
output_files.append(filename)

# --- GENERATE & SAVE ---
all_passwords = [] if shuffle_choice else None  # store passwords only if shuffle is needed

for combo in product(chars, repeat=length):
    password = ''.join(combo)
    
    if shuffle_choice:
        all_passwords.append(password)
    else:
        file.write(password + "\n")
    
    count += 1

    # Show progress every 1% or every 1000 lines
    if count % (total // 100 or 1000) == 0:
        percent = (count / total) * 100
        sys.stdout.write(f"\rProgress: {percent:.0f}% ({count:,}/{total:,})")
        sys.stdout.flush()

# If shuffling, split into files after randomizing
if shuffle_choice:
    print("\nShuffling passwords...")
    random.shuffle(all_passwords)
    
    # Write shuffled passwords into split files
    count = 0
    file_index = 1
    for i, password in enumerate(all_passwords, 1):
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
    if not file.closed:
        file.close()

# --- ZIP COMPRESSION ---
zip_name = f"passwords_len{length}.zip"
with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for f in output_files:
        zipf.write(f)
        os.remove(f)  # delete txt after adding to zip

print(f"\n✅ Done! All passwords saved and compressed into {zip_name}")
print(f"Total passwords generated: {total:,}")
