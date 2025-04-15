User Manual

Author - Muthukumaraswami Sivaswami (1833616)

2023-12-07

User Manual for BWT app built in Python

This user guide was written in R by M Sivaswami (1833616) for the python code written as part of the BWT Programming Coursework by B Gaber (2538271), H Pandhi (2694547), H Gholazideh (2710124) and M Sivaswami (1833616).

Introduction

The BWT app allows users to apply the Burrows-Wheeler Transform to a given string and obtain the BWT encoded string. Users can also perform the inverse BWT to retrieve the original string. Additionally, the app provides features to calculate the size of a string in bytes and measure its compression rate.

Dependencies

Before running the app, ensure that the following dependencies are installed:

sys: provides access to system-specific parameters and functions. 
pandas: a powerful data analysis and manipulation library. 

# Functions

bwt(string):

This function takes a string as input and returns the Burrows-Wheeler Transform (BWT) of the string. The BWT is obtained by cyclically permuting the string and sorting the permutations lexicographically. The function returns a Pandas DataFrame matrix containing the possible rotations and their sorted forms, and the BWT encoded string as its output.

bwt_inverse(bwt_encoded):

This function takes a BWT encoded string as input and returns the original string before BWT was applied. It reconstructs the original string by iteratively following the indices of characters in the BWT encoded string. The function returns a Pandas DataFrame df containing the first column and the original sequence column, and the original string.

calculate_size(input_string):

This function calculates the size of a string in bytes. It encodes the string using the UTF-8 encoding and returns the size in bytes.

measure_compression(input_sequence):

This function measures the compression rate of a given input sequence. It applies the BWT to the input sequence, then applies the inverse BWT to obtain the original sequence. It calculates the original size, compressed size, and compression rate (as a percentage) and returns the measurements in a Pandas DataFrame.

Main Program
The main program provides a user-friendly interface to interact with the implemented functions. It presents a menu with the following options:

Perform Burrows-Wheeler Transform: Allows the user to enter a sequence and displays the BWT encoded string.

Inverse Burrows-Wheeler Transform: Allows the user to enter a BWT encoded string and displays the original string.

Calculate size of a string: Allows the user to calculate the size of a string in bytes.

Measure Compression: Allows the user to enter a sequence and measure its compression rate.

Exit: Exits the program.

The program uses the input() function to receive user input and executes the corresponding option based on the input value.

Note that the program includes a predefined list of strings called strings_to_process. These strings can be used to test the functionality of the app. The user can choose to either enter a custom string or select one of the predefined strings for size calculation.

Usage

To use the BWT app, follow these steps:

Run the program.

Follow the instructions provided in the menu.
Choose the desired option by entering the corresponding number.
Provide valid inputs when prompted to ensure correct execution of the program.
That’s the end of this user manual. I hope you found it useful. Now, go test the app out and feel free to experiment.
