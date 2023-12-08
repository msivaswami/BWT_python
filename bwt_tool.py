import tkinter as tk
from tkinter import simpledialog, messagebox
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
    
    # Calculate the compression rate
    compression_rate = (original_size - compressed_size) / original_size if original_size != 0 else 0
    
    # Calculate the modulus of the compression rate percentage
    compression_rate_modulus = abs(compression_rate * 100)

    return pd.DataFrame({
        'Sequence': [input_sequence],
        'Original Sequence': [string_original],
        'SequenceLength': [original_size],
        'CompressionRate%': [compression_rate_modulus]  # Use the modulus value
    })


#Predefined options for strings
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

class BWTToolGUI:
    def __init__(self, master):
        self.master = master
        master.title("BWT Tool")

        self.menu_label = tk.Label(master, text="Choose an option:")
        self.menu_label.pack()

        self.options = [
            "Perform Burrows-Wheeler Transform",
            "Inverse Burrows-Wheeler Transform",
            "Calculate size of a string",
            "Measure Compression",
            "Exit"
        ]

        for i, option in enumerate(self.options, start=1):
            button = tk.Button(master, text=f"{i}. {option}", command=lambda opt=option: self.handle_option(opt))
            button.pack()

    def handle_option(self, option):
        if option == "Exit":
            self.master.destroy()
        elif option == "Perform Burrows-Wheeler Transform":
            user_input = simpledialog.askstring("Input", "Please enter the sequence:")
            show_rotations = messagebox.askyesno("Show Rotations", "Do you want to see all the possible permutations sorted?")
            bwt_result, bwt_encoded = bwt(user_input)
            self.show_bwt_results(user_input, bwt_encoded, show_rotations)
        elif option == "Inverse Burrows-Wheeler Transform":
            user_input_inverse = simpledialog.askstring("Input", "Please enter the BWT Inverse sequence:")
            self.show_inverse_bwt_results(user_input_inverse)
        elif option == "Calculate size of a string":
            self.calculate_size_option()
        elif option == "Measure Compression":
            user_input = simpledialog.askstring("Input", "Please enter the sequence for compression measurement:")
            self.show_compression_results(user_input)

    def show_bwt_results(self, user_input, bwt_encoded, show_rotations):
        result, _ = bwt(user_input)
        if show_rotations:
            rotations_window = tk.Toplevel(self.master)
            rotations_text = tk.Text(rotations_window)
            rotations_text.insert(tk.END, str(result))
            rotations_text.pack()

        bwt_window = tk.Toplevel(self.master)
        bwt_label = tk.Label(bwt_window, text=f"BWT result of your entered sequence is: {bwt_encoded}")
        bwt_label.pack()

    def show_inverse_bwt_results(self, user_input_inverse):
        inverse_result, string_original = bwt_inverse(user_input_inverse)
        inverse_window = tk.Toplevel(self.master)
        inverse_label = tk.Label(inverse_window, text=f"Inverse BWT sequence is: {string_original}")
        inverse_label.pack()

        visualization_window = tk.Toplevel(self.master)
        visualization_text = tk.Text(visualization_window)
        visualization_text.insert(tk.END, str(inverse_result))
        visualization_text.pack()

    def calculate_size_option(self):
        size_option = simpledialog.askstring("Calculate Size", "Choose an option for string size calculation:\n1. Enter a custom string\n2. Use a predefined sequence")

        if size_option == '1':
            input_string = simpledialog.askstring("Input", "Enter the string to calculate its size: ")
        elif size_option == '2':
            strings_menu = [f"{i + 1}. {string}" for i, string in enumerate(strings_to_process)]
            choice = simpledialog.askinteger("Choose a predefined string", "\n".join(strings_menu), minvalue=1, maxvalue=len(strings_menu))
            input_string = strings_to_process[choice - 1]
        else:
            messagebox.showwarning("Invalid Input", "Invalid input. Please enter a valid option.")
            return

        size_in_bytes = calculate_size(input_string)
        messagebox.showinfo("Size in Bytes", f"Size in bytes: {size_in_bytes}")

    def show_compression_results(self, user_input):
        compression_result = measure_compression(user_input)
        compression_window = tk.Toplevel(self.master)
        compression_label = tk.Label(compression_window, text=f"Compression Measurement:\n{compression_result}")
        compression_label.pack()

# Tkinter GUI setup
root = tk.Tk()
app = BWTToolGUI(root)
root.mainloop()
