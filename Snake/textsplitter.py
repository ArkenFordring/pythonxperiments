import os

def split_file():
    # Ask the user for the path to the input file
    file_path = input("Please enter the path to the input file: ")

    # Get the directory where the input file is located
    directory = os.path.dirname(file_path)

    # Open the input file for reading
    with open(file_path, 'r') as input_file:
        # Read the entire file into a string
        text = input_file.read()

        # Split the string into 990 character chunks
        chunks = [text[i:i + 2040] for i in range(0, len(text), 990)]

        # Create a separate output file for each chunk
        for i, chunk in enumerate(chunks):
            # Construct the name of the output file
            output_file_name = os.path.join(directory, f"output_{i}.txt")

            # Open the output file for writing
            with open(output_file_name, 'w') as output_file:
                # Write the chunk to the output file
                output_file.write(chunk)

    print("Splitting complete.")


# Call the split_file function
split_file()