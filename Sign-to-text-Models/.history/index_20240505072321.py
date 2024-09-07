def remove_lines_with_words(input_file, output_file, words):
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            # Check if the line contains any of the specified words
            if any(word in line for word in words):
                continue  # Skip the line
            # Write the line to the output file if it doesn't contain the words
            outfile.write(line)

# Example usage
input_file = "input.txt"
output_file = "output.txt"
words_to_remove = ["media omitted", "null"]

remove_lines_with_words(input_file, output_file, words_to_remove)
print("Lines containing specified words removed. Check the output file:", output_file)
