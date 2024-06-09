import sys
import re

def grep(pattern, file_paths):
    # Find mønster, der ledes efter
    compiled_pattern = re.compile(pattern)
    # Gennemgå filer
    for file_path in file_paths:
        try:
            with open(file_path, 'r') as file:
                for line in file:
                    if compiled_pattern.search(line):
                        print(line, end='')  # Print fundet linje
        except FileNotFoundError:
            print(f"Fejl: Filen '{file_path}' findes ikke.", file=sys.stderr)
        except PermissionError:
            print(f"Fejl: Du har ikke tilladelse '{file_path}'.", file=sys.stderr)
        except Exception as e:
            print(f"Fejl: {e}", file=sys.stderr)

def main():
    if len(sys.argv) < 3:
        print("Du har angivet for få argumenter. Du skal angive mindst ét gyldigt filnavn", file=sys.stderr)
        sys.exit(1)

    pattern = sys.argv[1]
    file_paths = sys.argv[2:]
    grep(pattern, file_paths)

if __name__ == "__main__":
    main()

# Kør programmet med python grep.py "hej" eks1.txt eks2.txt