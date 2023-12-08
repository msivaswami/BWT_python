import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import simpledialog
import pandas as pd

#Define the custom implementation of Burrows-Wheeler Transform ()
def bwt(string):
    """
    This function takes a string as input and returns the Burrows-Wheeler Transform (BWT) of the string.
    The BWT is obtained by cyclically permuting the string and sorting the permutations lexicographically.
    The function returns a Pandas DataFrame matrix containing the possible rotations and their sorted forms,
    and the BWT encoded string as its output.
    """
    string += '$'
    indices = [string[i:] + string[:i] for i in range(len(string))]
    sorted_indices = sorted(indices)
    bwt_encoded = ''.join(sorted_indices[-1][-1] for sorted_indices in sorted_indices)
    matrix = pd.DataFrame({
        "Possible rotations": indices,
        "Sorted": sorted_indices
    })
    return matrix, bwt_encoded

#Define the inverse BWT function
def bwt_inverse(bwt_encoded):
    """
    This function takes a BWT encoded string as input and returns the original string before BWT was applied.
    It reconstructs the original string by iteratively following the indices of characters in the BWT encoded string.
    The function returns a Pandas DataFrame df containing the first column and the original sequence column,
    and the original string without the EOF character '$'.
    """
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

#Function to calculate the size of a string in bytes
def calculate_size(input_string):
    """
    This function calculates the size of a string in bytes.
    It encodes the string using the UTF-8 encoding and returns the size in bytes.
    """
    size_in_bytes = len(input_string.encode('utf-8'))
    return size_in_bytes

def measure_compression(input_sequence):
    """
    This function measures the compression rate of a given input sequence.
    It applies the BWT to the input sequence, then applies the inverse BWT to obtain the original sequence.
    It calculates the original size, compressed size, and compression rate (as a percentage)
    and returns the measurements in a Pandas DataFrame.
    """
    _, bwt_encoded = bwt(input_sequence)
    _, string_original = bwt_inverse(bwt_encoded)

    original_size = len(input_sequence)
    compressed_size = len(bwt_encoded)
    compression_rate = (original_size - compressed_size) / original_size if original_size != 0 else 0

    return pd.DataFrame({
        'Sequence': [input_sequence],
        'Original Sequence': [string_original],
        'SequenceLength': [original_size],
        'CompressionRate%': [compression_rate * 100]  # Multiply by 100 to represent as percentage
    })

class BWTApp:
    def __init__(self, master):
        self.master = master
        master.title("BWT Application")

        self.create_widgets()

    def create_widgets(self):
        # Labels
        self.label_instruction = ttk.Label(self.master, text="Choose an option:")
        self.label_instruction.grid(row=0, column=0, columnspan=2, pady=10)

        # Buttons
        self.button_bwt = ttk.Button(self.master, text="Perform BWT", command=self.perform_bwt)
        self.button_bwt.grid(row=1, column=0, pady=5)

        self.button_inverse_bwt = ttk.Button(self.master, text="Inverse BWT", command=self.inverse_bwt)
        self.button_inverse_bwt.grid(row=1, column=1, pady=5)

        self.button_calculate_size = ttk.Button(self.master, text="Calculate Size", command=self.calculate_size)
        self.button_calculate_size.grid(row=2, column=0, pady=5)

        self.button_measure_compression = ttk.Button(self.master, text="Measure Compression", command=self.measure_compression)
        self.button_measure_compression.grid(row=2, column=1, pady=5)

        self.button_exit = ttk.Button(self.master, text="Exit", command=self.master.destroy)
        self.button_exit.grid(row=3, column=0, columnspan=2, pady=10)

    def perform_bwt(self):
        user_input = self.get_user_input("Enter the sequence for BWT:")
        bwt_result, bwt_encoded = bwt(user_input)
        self.display_result("BWT result of the entered sequence is:", bwt_encoded)
        self.show_matrix("Possible rotations and sorted forms:", bwt_result)

    def inverse_bwt(self):
        user_input_inverse = self.get_user_input("Enter the BWT Inverse sequence:")
        inverse_result, string_original = bwt_inverse(user_input_inverse)
        self.display_result("Inverse BWT sequence is:", string_original)
        self.show_matrix("Visualization:", inverse_result)

    def calculate_size(self):
        input_string = self.get_user_input("Enter the string to calculate its size:")
        size_in_bytes = calculate_size(input_string)
        self.display_result("Size in bytes:", size_in_bytes)

    def measure_compression(self):
        user_input = self.get_user_input("Enter the sequence for compression measurement:")
        compression_result = measure_compression(user_input)
        self.display_result("Compression Measurement:", compression_result)

    def get_user_input(self, prompt):
        user_input = simpledialog.askstring("Input", prompt)
        return user_input.strip() if user_input else ""

    def display_result(self, label_text, result_text):
        result_label = ttk.Label(self.master, text=label_text)
        result_label.grid(row=4, column=0, columnspan=2)
        result_textbox = scrolledtext.ScrolledText(self.master, wrap=tk.WORD, width=40, height=5)
        result_textbox.grid(row=5, column=0, columnspan=2, pady=5)
        result_textbox.insert(tk.END, result_text)
        result_textbox.configure(state='disabled')

    def show_matrix(self, label_text, matrix_df):
        self.display_result(label_text, matrix_df.to_string(index=False))


# Create the main window
root = tk.Tk()

# Instantiate the BWTApp
app = BWTApp(root)

# Run the application
root.mainloop()
