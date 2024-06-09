import sys


def tr(string, convert_from, convert_to):
  translated = ""

  # Convert from lower to upper case  
  if convert_from == "[:lower]" and convert_to == "[:upper]" or convert_from == "[:a-z]" and convert_to == "[:A-Z]":    
    for char in string:
      if char.islower():
        translated += char.upper()
      else:
        translated += char
  # Convert from upper to lower case
  elif convert_from == "[:upper]" and convert_to == "[:lower]" or convert_from == "[:A-Z]" and convert_to == "[:a-z]":
    for char in string:
      if char.isupper():
        translated += char.lower()
      else:
        translated += char
  return translated

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
    
    convert_from = sys.argv[2]
    convert_to = sys.argv[3]
    translated = tr(string, convert_from, convert_to)
    print(translated)

if __name__ == "__main__":
    main()

# Kør programmet med python tr.py ../test/text.txt [:a-z] [:A-Z]