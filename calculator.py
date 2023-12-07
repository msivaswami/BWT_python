# This is an implementation of the string size calculator in Python, written by M Sivaswami,
# for the BWT Programming project, as part of the coursework for the NGS module

import sys

# Function to calculate the size of a string in bytes
def calculate_size(input_string):
    size_in_bytes = sys.getsizeof(input_string)
    return size_in_bytes


# Predefined options for strings
strings_to_process = [
    "GATTACA",
    "ATTACATTAC",
    "ATATATATATA",
    "ATATATATAT",
    "AATAATAATAAT",
    "AAAATAAATAAA",
    "ATATACACACA",
    "ATATGTATACAT"
]

# Loop to restart the application
while True:
    print("Welcome to a python implementation of M Sivaswami's String Size Calculator!")
    print("======================================")

    # Get user input
    use_predefined = input("Do you want to use predefined strings? (yes/no): ")

    if use_predefined.lower() == "yes":
        print("Choose a predefined string:")
        for i, string in enumerate(strings_to_process):
            print(f"{i + 1}. {string}")
        choice = int(input("Enter the number corresponding to your choice: "))
        input_string = strings_to_process[choice - 1]
    else:
        input_string = input("Enter your custom string: ")

    # Calculate and print the size of the input string
    size_in_bytes = calculate_size(input_string)
    print(f"Size in bytes: {size_in_bytes}")

    # Ask if the user wants to restart the application
    restart = input("Do you want to calculate the size of another string? (yes/no): ")
    if restart.lower() != "yes":
        break

print("Thank you for using M Sivaswami's String Size Calculator. Goodbye!")