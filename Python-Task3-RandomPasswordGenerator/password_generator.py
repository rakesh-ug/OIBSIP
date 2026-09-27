"""OIBSIP Python Task 3: secure, customizable command-line passwords."""

import secrets
import string

CHARACTER_GROUPS = {
    "uppercase": string.ascii_uppercase,
    "lowercase": string.ascii_lowercase,
    "numbers": string.digits,
    "symbols": "!@#$%^&*()-_=+[]{}:,.?",
}
MIN_LENGTH = 8
MAX_LENGTH = 128
AMBIGUOUS = "0O1lI"


def generate_password(length: int, selected: list[str], exclude_ambiguous: bool = False) -> str:
    """Choose at least one from each group; securely shuffle the result."""
    if isinstance(length, bool) or not isinstance(length, int) or not MIN_LENGTH <= length <= MAX_LENGTH:
        raise ValueError(f"Length must be a whole number from {MIN_LENGTH} to {MAX_LENGTH}.")
    if len(set(selected)) < 2 or len(selected) != len(set(selected)):
        raise ValueError("Select at least two different character types.")
    if any(group not in CHARACTER_GROUPS for group in selected):
        raise ValueError("Unknown character type selected.")
    groups = [CHARACTER_GROUPS[group] for group in selected]
    if exclude_ambiguous:
        groups = ["".join(c for c in group if c not in AMBIGUOUS) for group in groups]
    if any(not group for group in groups):
        raise ValueError("A selected character group has no available characters.")
    if length < len(groups):
        raise ValueError("Length is too short to include every selected type.")
    characters = [secrets.choice(group) for group in groups]
    pool = "".join(groups)
    characters.extend(secrets.choice(pool) for _ in range(length - len(characters)))
    # Fisher-Yates with secrets.randbelow, never random.shuffle for passwords.
    for index in range(len(characters) - 1, 0, -1):
        other = secrets.randbelow(index + 1)
        characters[index], characters[other] = characters[other], characters[index]
    return "".join(characters)


def prompt_yes_no(label: str, default: bool = True) -> bool:
    hint = "Y/n" if default else "y/N"
    while True:
        answer = input(f"{label} ({hint}): ").strip().lower()
        if not answer:
            return default
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print("Please type y or n.")


def main() -> None:
    print("\n=== SECURE PASSWORD GENERATOR ===")
    print("Choose at least two character types; use 16+ characters for important accounts.")
    print("Your passwords are displayed only here and are never saved to disk.\n")
    while True:
        try:
            raw = input("Password length (8-128, Enter = 16): ").strip() or "16"
            try:
                length = int(raw)
            except ValueError as exc:
                raise ValueError("Length must be a whole number, such as 16.") from exc
            selected = [name for name in CHARACTER_GROUPS
                        if prompt_yes_no(f"Include {name}?", name != "symbols")]
            exclude = prompt_yes_no("Exclude ambiguous characters (0, O, 1, l, I)?", False)
            password = generate_password(length, selected, exclude)
        except ValueError as exc:
            print(f"Error: {exc}\nPlease try again.\n")
            continue
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            return
        print(f"\nGenerated password: {password}")
        print("Security tip: use a unique password per account and store it in a password manager.")
        try:
            if not prompt_yes_no("Generate another password?", False):
                print("Goodbye!")
                return
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            return
        print()


if __name__ == "__main__":
    main()
