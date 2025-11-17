from itertools import product
import sys

# Ask the user for password length
length = int(input("Enter password length (e.g. 3, 4, 5): "))

digits = '0123456789'
filename = f"passwords_{length}_digits.txt"

total = 10 ** length  # total combinations
count = 0

with open(filename, "w") as file:
    for combo in product(digits, repeat=length):
        file.write(''.join(combo) + "\n")
        count += 1

        # Display progress every 1% (or more often for smaller files)
        if count % (total // 100 or 1) == 0:
            percent = (count / total) * 100
            sys.stdout.write(f"\rProgress: {percent:.0f}%")
            sys.stdout.flush()

print(f"\n✅ Done! All {length}-digit passwords saved to {filename}")
print(f"Total passwords generated: {total:,}")
