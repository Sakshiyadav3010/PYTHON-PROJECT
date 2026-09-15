"""
Random Password Generator (Beginner Tier)
------------------------------------------
Generates strong, random passwords based on user-defined criteria:
length and which character types to include.

Rules enforced:
    - Minimum length of 8 characters
    - At least 2 character types must be selected
"""

import random
import string

MIN_LENGTH = 8

CHARACTER_SETS = {
    "u": ("uppercase letters", string.ascii_uppercase),
    "l": ("lowercase letters", string.ascii_lowercase),
    "n": ("numbers", string.digits),
    "s": ("symbols", string.punctuation),
}


def get_length() -> int:
    """Ask for a password length, enforcing the minimum."""
    while True:
        raw_value = input(f"Enter desired password length (min {MIN_LENGTH}): ").strip()
        if not raw_value.isdigit():
            print("  ⚠  Please enter a whole number.")
            continue

        length = int(raw_value)
        if length < MIN_LENGTH:
            print(f"  ⚠  Length must be at least {MIN_LENGTH} characters.")
            continue

        return length


def get_character_types() -> str:
    """Ask which character types to include; require at least 2."""
    print("\nChoose character types to include (at least 2):")
    print("  u = uppercase letters (A-Z)")
    print("  l = lowercase letters (a-z)")
    print("  n = numbers (0-9)")
    print("  s = symbols (!@#$...)")

    while True:
        raw_value = input("Enter your choices (e.g., uln): ").strip().lower()
        chosen = set(ch for ch in raw_value if ch in CHARACTER_SETS)

        if len(chosen) < 2:
            print("  ⚠  Please select at least 2 valid character types.")
            continue

        return "".join(sorted(chosen))


def generate_password(length: int, types: str) -> str:
    """Build a password guaranteeing at least one char from each selected type."""
    pools = [CHARACTER_SETS[t][1] for t in types]

    # Guarantee at least one character from every selected type.
    password_chars = [random.choice(pool) for pool in pools]

    # Fill the rest of the length from the combined pool.
    combined_pool = "".join(pools)
    remaining = length - len(password_chars)
    password_chars += [random.choice(combined_pool) for _ in range(remaining)]

    random.shuffle(password_chars)
    return "".join(password_chars)


def main():
    print("=" * 42)
    print("       RANDOM PASSWORD GENERATOR")
    print("=" * 42)

    while True:
        length = get_length()
        types = get_character_types()

        password = generate_password(length, types)

        included = ", ".join(CHARACTER_SETS[t][0] for t in types)
        print("\n--- Generated Password ---")
        print(password)
        print(f"(length: {length}, includes: {included})")
        print("---------------------------\n")

        again = input("Generate another password? (y/n): ").strip().lower()
        if again != "y":
            print("Goodbye! Stay secure.")
            break


if __name__ == "__main__":
    main()
