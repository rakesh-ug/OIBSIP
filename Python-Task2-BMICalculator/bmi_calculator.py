"""OIBSIP Python Task 2: command-line Body Mass Index calculator."""

import math


def positive_number(text: str, label: str) -> float:
    """Convert input to a positive, finite number, or explain the mistake."""
    try:
        value = float(text)
    except ValueError as exc:
        raise ValueError(f"{label} must be a number (for example, 70 or 1.75).") from exc
    if not math.isfinite(value) or value <= 0:
        raise ValueError(f"{label} must be greater than zero and finite.")
    return value


def calculate_bmi(weight_kg: float, height_m: float) -> float:
    """Return BMI in kg/m²; validate even when called without the CLI."""
    weight = positive_number(str(weight_kg), "Weight")
    height = positive_number(str(height_m), "Height")
    square = height * height
    if not math.isfinite(square) or square == 0:
        raise ValueError("Height is outside the supported numeric range.")
    bmi = weight / square
    if not math.isfinite(bmi) or bmi == 0:
        raise ValueError("Measurements are outside the supported numeric range.")
    return bmi


def bmi_category(bmi: float) -> str:
    """Classify the unrounded BMI so boundary values stay correct."""
    bmi = positive_number(str(bmi), "BMI")
    if bmi < 18.5:
        return "Underweight"
    if bmi < 25:
        return "Normal"
    if bmi < 30:
        return "Overweight"
    return "Obese"


def main() -> None:
    print("\n=== BMI CALCULATOR ===")
    print("Enter weight in kilograms and height in meters. Ctrl+C to exit.\n")
    while True:
        try:
            weight = positive_number(input("Weight (kg): ").strip(), "Weight")
            height = positive_number(input("Height (m): ").strip(), "Height")
            bmi = calculate_bmi(weight, height)
        except ValueError as exc:
            print(f"Error: {exc}\nPlease try again.\n")
            continue
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            return
        print(f"\nBMI: {bmi:.2f}")
        print(f"Category: {bmi_category(bmi)}")
        print("Note: BMI is a screening measure, not a medical diagnosis.\n")
        try:
            again = input("Calculate another? (y/N): ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            return
        if again not in ("y", "yes"):
            print("Goodbye!")
            return
        print()


if __name__ == "__main__":
    main()
