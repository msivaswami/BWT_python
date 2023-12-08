# bwt_package/bwt_script.py

import pandas as pd

def bwt(string):
    string += '$'
    indices = [string[i:] + string[:i] for i in range(len(string))]
    sorted_indices = sorted(indices)
    bwt_encoded = ''.join(sorted_indices[-1][-1] for sorted_indices in sorted_indices)
    matrix = pd.DataFrame({
        "Possible rotations": indices,
        "Sorted": sorted_indices
    })
    return matrix, bwt_encoded

def bwt_inverse(bwt_encoded):
    if '$' not in bwt_encoded:
        bwt_encoded += '$'
    ln = len(bwt_encoded)
    tuples = [(char, i) for i, char in enumerate(bwt_encoded)]
    tuples.sort()
    column_1 = [char for char, n in tuples]
    current_BWT_row = tuples[bwt_encoded.index('$')][1]
    string_original = ''
    for n in range(ln):
        string_original = column_1[current_BWT_row] + string_original
        current_BWT_row = tuples[current_BWT_row][1]
    sorted_indices = sorted(range(ln), key=lambda x: bwt_encoded[x])
    current_index = sorted_indices[bwt_encoded.index('$')]
    string_original = ''
    for _ in range(ln - 1):
        string_original += bwt_encoded[current_index]
        current_index = sorted_indices[current_index]
    df = pd.DataFrame({
        "First Column": column_1,
        "Original Sequence Column": list(bwt_encoded)
    })
    return df, string_original

def calculate_size(input_string):
    size_in_bytes = len(input_string.encode('utf-8'))
    return size_in_bytes

def measure_compression(input_sequence):
    _, bwt_encoded = bwt(input_sequence)
    _, string_original = bwt_inverse(bwt_encoded)

    original_size = len(input_sequence)
    compressed_size = len(bwt_encoded)
    compression_rate = compressed_size / original_size if original_size != 0 else 0

    return pd.DataFrame({
        'Sequence': [input_sequence],
        'Original Sequence': [string_original],
        'SequenceLength': [original_size],
        'CompressionRate': [compression_rate * 100]  # Multiply by 100 to represent as percentage
    })

def main():
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

    while True:
        print("Choose an option:")
        print("1. Perform Burrows-Wheeler Transform")
        print("2. Inverse Burrows-Wheeler Transform")
        print("3. Calculate size of a string")
        print("4. Measure Compression")
        print("5. Exit")

        option = input("Enter the number corresponding to your choice: ")

        if option == '5':
            print("Exiting the program.")
            break

        if option == '1':
            user_input = input("Please enter the sequence: ").strip()
            bwt_result, bwt_encoded = bwt(user_input)
            user_input_2 = input("Do you want to see all the possible permutations sorted? ").strip().lower()
            if user_input_2 in ["yes", "y"]:
                print("\nHere are all the possible permutations and sorted form: ")
                print(bwt_result)
            print("\nBWT result of your entered sequence is: ", bwt_encoded)
            print()

        elif option == '2':
            user_input_inverse = input("Please enter the BWT Inverse sequence: ").strip()
            inverse_result, string_original = bwt_inverse(user_input_inverse)
            print("\nInverse BWT sequence is:", string_original)
            print("\nVisualization:")
            print(inverse_result)
            print()

        elif option == '3':
            print("Choose an option for string size calculation:")
            print("1. Enter a custom string")
            print("2. Use a predefined sequence")

            size_option = input("Enter the number corresponding to your choice: ")

            if size_option == '1':
                input_string = input("Enter the string to calculate its size: ").strip()
            elif size_option == '2':
                print("Choose a predefined string:")
                for i, string in enumerate(strings_to_process):
                    print(f"{i + 1}. {string}")
                choice = int(input("Enter the number corresponding to your choice: "))
                input_string = strings_to_process[choice - 1]
            else:
                print("Invalid input. Please enter a valid option.")
                continue

            size_in_bytes = calculate_size(input_string)
            print(f"Size in bytes: {size_in_bytes}")

        elif option == '4':
            user_input = input("Please enter the sequence for compression measurement: ").strip()
            compression_result = measure_compression(user_input)
            print("\nCompression Measurement:")
            print(compression_result)
            print()

        else:
            print("Invalid input. Please enter a valid option.")

if __name__ == "__main__":
    main()
