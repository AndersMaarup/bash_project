import sys
import re

def cat(*file_paths):

    contents = []
    for file_path in file_paths:
        try:
            with open(file_path, 'r') as file:
                contents.append(file.read())
        except FileNotFoundError:
            contents.append(f"Error: '{file_path}' does not exist.")
        except Exception as e:
            contents.append(f"Error reading '{file_path}': {e}")
    
    return "\n".join(contents)

def main():
    if len(sys.argv) < 2:
        print("Du har angivet for få argumenter. Du skal angive mindst ét gyldigt filnavn", file=sys.stderr)
        sys.exit(1)

    file_paths = sys.argv[1:]
    concatenated=cat(*file_paths)
    print("The cat function passed on: '",concatenated, "' as a String")

if __name__ == "__main__":
    main()