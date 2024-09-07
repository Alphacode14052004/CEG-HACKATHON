import re

def remove_symbols_and_numbers(input_file, output_file):
    # Regular expression to match symbols and numbers
    pattern = r'[^a-zA-Z\s]'  # Matches anything except letters and whitespaces

    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            # Remove symbols and numbers from the line
            clean_line = re.sub(pattern, '', line)
            # Write the clean line to the output file
            outfile.write(clean_line)

# Example usage
input_file = "input.txt"
output_file = "output.txt"

remove_symbols_and_numbers(input_file, output_file)
print("Symbols and numbers removed. Check the output file:", output_file)
