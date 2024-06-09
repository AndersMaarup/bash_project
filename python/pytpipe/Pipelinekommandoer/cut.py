import sys
import re


def cut(string, *extractions):
    print("Running cut")
    lines = string.split("\n")
    delimiter = ","
    extraction = []
    column_indices = [int(extraction) - 1 for extraction in extractions]
    for line in lines:
        split_line = line.split(delimiter)
        newLine = []
        # For hvert ord, hvis indeks passer med "extractions", så tilføj til "extraction"
        for index in column_indices:
            if index < len(split_line):
                newLine.append(split_line[index])
        extraction.append(delimiter.join(newLine))
    return "\n".join(extraction)

def main():
    if len(sys.argv) < 3:
        print(
            "Du har angivet for få argumenter. Du skal angive mindst én gyldig kommando",
            file=sys.stderr,
        )
        sys.exit(1)

    filepath = sys.argv[1]
    try:
        with open(filepath, "r") as file:
            string = file.read()
    except FileNotFoundError:
            print(f"Fejl: Filen '{filepath}' findes ikke.", file=sys.stderr)
    except PermissionError:
            print(f"Fejl: Du har ikke tilladelse '{filepath}'.", file=sys.stderr)
    except Exception as e:
            print(f"Fejl: {e}", file=sys.stderr)
    
    cutted = cut(string, *sys.argv[2:])
    print(cutted)

if __name__ == "__main__":
    main()
