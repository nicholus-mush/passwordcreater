from itertools import product
import sys

# --- USER INPUT ---
length = int(input("Enter password length (e.g. 3, 4, 5, 6, etc.): "))
chunk_size = int(input("Enter how many passwords per file (e.g. 100000 for 100k per file): "))

digits = '0123456789'
total = 10 ** length  # total possible passwords

print(f"\nGenerating {total:,} possible passwords... (this may take time)\n")

count = 0
file_index = 1

# Open first output file
file = open(f"passwords_part{file_index}.txt", "w")

for combo in product(digits, repeat=length):
    file.write(''.join(combo) + "\n")
    count += 1

    # Split file when chunk limit is reached
    if count % chunk_size == 0:
        file.close()
        file_index += 1
        file = open(f"passwords_part{file_index}.txt", "w")

    # Display progress every 1%
    if count % (total // 100 or 1) == 0:
        percent = (count / total) * 100
        sys.stdout.write(f"\rProgress: {percent:.0f}%")
        sys.stdout.flush()

file.close()
print(f"\n✅ Done! Generated {total:,} total passwords across {file_index} file(s).")
