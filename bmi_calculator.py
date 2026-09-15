"""
BMI Calculator (Beginner Tier)
-------------------------------
Prompts the user for weight (kg) and height (m), calculates their
Body Mass Index, and classifies the result into a standard health
category.

Formula: BMI = weight / (height ** 2)

Categories:
    Underweight : BMI < 18.5
    Normal      : 18.5 <= BMI < 25
    Overweight  : 25   <= BMI < 30
    Obese       : BMI >= 30
"""


def get_positive_float(prompt: str) -> float:
    """Repeatedly ask the user for input until a valid positive number is given."""
    while True:
        raw_value = input(prompt).strip()
        try:
            value = float(raw_value)
        except ValueError:
            print("  ⚠  Please enter a valid number (e.g., 68.5).")
            continue

        if value <= 0:
            print("  ⚠  Value must be a positive number. Please try again.")
            continue

        return value


def calculate_bmi(weight_kg: float, height_m: float) -> float:
    """Return BMI rounded to 2 decimal places."""
    bmi = weight_kg / (height_m ** 2)
    return round(bmi, 2)


def classify_bmi(bmi: float) -> str:
    """Return the standard BMI category for a given BMI value."""
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"


def main():
    print("=" * 40)
    print("        BMI CALCULATOR")
    print("=" * 40)

    while True:
        weight = get_positive_float("Enter your weight in kg: ")
        height = get_positive_float("Enter your height in m (e.g., 1.75): ")

        bmi = calculate_bmi(weight, height)
        category = classify_bmi(bmi)

        print("\n--- Result ---")
        print(f"Your BMI is: {bmi}")
        print(f"Category   : {category}")
        print("--------------\n")

        again = input("Calculate another BMI? (y/n): ").strip().lower()
        if again != "y":
            print("Goodbye! Stay healthy.")
            break


if __name__ == "__main__":
    main()
