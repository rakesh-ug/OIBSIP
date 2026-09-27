# BMI Calculator

A simple Python command-line program to calculate Body Mass Index using weight in kilograms and height in meters.

## What it does

- Calculates BMI using `weight / height²`.
- Shows BMI to two decimal places and classifies it as Underweight, Normal, Overweight, or Obese.
- Rejects empty, non-numeric, zero, negative, and non-finite values with a clear error message.
- Lets you calculate another BMI without reopening the program.

Categories use the unrounded result: below 18.5 = Underweight; 18.5 to below 25 = Normal; 25 to below 30 = Overweight; 30 or above = Obese.

## Run

Requires Python 3.9 or newer. No external packages are needed.

```bash
python3 bmi_calculator.py
```

Enter `70` for weight and `1.75` for height to see `BMI: 22.86` and `Category: Normal`. Use `python3` to run this project.

## Test

```bash
python3 -m unittest discover -v
```

BMI is a screening measure, not a diagnosis.
