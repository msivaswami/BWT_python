# This is an implementation of the BWT in Python, written by M Sivaswami, B Gaber, H Pandhi and H Ghoalzideh
# for the BWT Programming project, as part of the coursework for the NGS module


# Importing libraries required
import time
import pandas as pd
import matplotlib.pyplot as plt


# Define the Burrows-Wheeler Transform function
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


# Define the inverse BWT function
def bwt_inverse(bwt_encoded):
    if '$' not in bwt_encoded:
        bwt_encoded += '$'
    ln = len(bwt_encoded)
    # Creating a list of tuples with each character and index followed by sorting
    tuples = [(char, i) for i, char in enumerate(bwt_encoded)]
    tuples.sort()
    # Reconstructing the first column of Matrix
    column_1 = [char for char, n in tuples]
    # Initializing current BWT row to the row containing '$'
    current_BWT_row = tuples[bwt_encoded.index('$')][1]
    # Reconstructing the original string input by the user
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


def measure_compression(input_sequence):
    start_time_compress = time.time()
    _, bwt_encoded = bwt(input_sequence)
    compression_time = time.time() - start_time_compress

    start_time_decompress = time.time()
    _, _ = bwt_inverse(bwt_encoded)
    decompression_time = time.time() - start_time_decompress

    original_size = len(input_sequence)
    compressed_size = len(bwt_encoded)
    compression_rate = compressed_size / original_size if original_size != 0 else 0

    return pd.DataFrame({
        'Sequence': [input_sequence],
        'SequenceLength': [original_size],
        'CompressionTime': [compression_time],
        'DecompressionTime': [decompression_time],
        'CompressionRate': [compression_rate * 100]  # Multiply by 100 to represent as percentage
    })


while True:
    user_input_direction = input(
        "Do you want to perform Forward or Inverse BWT? (Type 'Forward' or 'Inverse', or 'Exit' to end): ").strip().lower()

    if user_input_direction == 'exit':
        print("Exiting the program.")
        break

    if user_input_direction == 'forward':
        user_input = input("Please enter the sequence: ").strip()
        bwt_result, bwt_encoded = bwt(user_input)

        user_input_2 = input("Do you want to see all the possible permutations sorted? ").strip().lower()

        if user_input_2 in ["yes", "y"]:
            print("\nHere are all the possible permutations and sorted form: ")
            print(bwt_result)
            print("\nBWT result of your entered sequence is: ", bwt_encoded)
            print()

            show_compression = input(
                "Do you want to see compression measurement? (Type 'Yes' or 'No'): ").strip().lower()
            if show_compression in ["yes", "y"]:
                result_df = measure_compression(user_input)
                print(result_df)
        else:
            print("BWT result of your entered sequence is: ", bwt_encoded)
            print()
            show_compression = input(
                "Do you want to see compression measurement? (Type 'Yes' or 'No'): ").strip().lower()
            if show_compression in ["yes", "y"]:
                result_df = measure_compression(user_input)
                print(result_df)

    elif user_input_direction == 'inverse':
        user_input_inverse = input("Please enter the BWT Inverse sequence: ").strip()
        inverse_result, string_original = bwt_inverse(user_input_inverse)
        print("\nInverse BWT sequence is:", string_original)
        print("\nVisualization:")
        print(inverse_result)
        print()
        show_compression = input("Do you want to see compression measurement? (Type 'Yes' or 'No'): ").strip().lower()
        if show_compression in ["yes", "y"]:
            result_df = measure_compression(user_input)
            print(result_df)


    else:
        print("Invalid input. Please type 'Forward', 'Inverse', or 'Exit'")