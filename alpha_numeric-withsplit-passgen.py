from itertools import product
import string
import sys
import math

# --- USER INPUT ---
length = int(input("Enter password length (e.g. 3, 4, 5): "))
split_limit = 1_000_000  # lines per file before creating a new one

# Character set: lowercase, uppercase, digits, punctuation
chars = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation
total = len(chars) ** length
count = 0
file_index = 1
split_count = math.ceil(total / split_limit)

print(f"\nGenerating {total:,} passwords...")
print(f"Output will be split into about {split_count:,} files (≈{split_limit:,} lines each)\n")

# --- INITIAL FILE SETUP ---
filename = f"passwords_part{file_index}_len{length}.txt"
file = open(filename, "w", encoding="utf-8")

# --- GENERATE AND SAVE ---
for combo in product(chars, repeat=length):
    file.write(''.join(combo) + "\n")
    count += 1

    # When current file reaches limit → open a new one
    if count % split_limit == 0 and count < total:
        file.close()
        file_index += 1
        filename = f"passwords_part{file_index}_len{length}.txt"
        file = open(filename, "w", encoding="utf-8")

    # Show progress (1% steps)
    if count % (total // 100 or 1000) == 0:
        percent = (count / total) * 100
        sys.stdout.write(f"\rProgress: {percent:.0f}% ({count:,}/{total:,})")
        sys.stdout.flush()

file.close()
print(f"\n✅ Done! Generated {total:,} passwords across {split_count:,} file(s).")
