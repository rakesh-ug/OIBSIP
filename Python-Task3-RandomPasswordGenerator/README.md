# Random Password Generator

A Python command-line tool that creates passwords with the length and character types you choose.

## What it does

- Accepts a password length between 8 and 128 characters.
- Lets you choose uppercase letters, lowercase letters, numbers, and symbols; at least two types are required.
- Guarantees at least one character from every selected type.
- Can exclude ambiguous characters (`0`, `O`, `1`, `l`, `I`).
- Lets you generate another password without restarting.

The program uses Python's `secrets` module for generation and shuffling. Passwords are shown in the terminal and are not saved to a file.

## Run

Requires Python 3.9 or newer. No external packages are needed.

```bash
python3 password_generator.py
```

Press Enter at the length prompt for the default of 16. Answer `y` or `n` for each character type. Use `python3` to run this project.

## Test

```bash
python3 -m unittest discover -v
```

Keep the terminal private while a generated password is visible. Use a different password for each account.
