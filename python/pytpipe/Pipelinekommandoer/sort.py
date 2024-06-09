import sys
import re

def sort(iterable, reverse=False):
  # Tjek, om listen er numerisk
  numeric = True
  for item in iterable:
      try:
          float(item)  # Prøv at konvertér til float
      except ValueError: #Hvis ikke...
          numeric = False # ... er listen ikke numerisk
          break  # Hvis én ikke er, så behøver vi ikke at gå videre
  if numeric:
    #Sorter numerisk. Strings konverteres til float.
    sorted_list = sorted(iterable, key=lambda x: float(x), reverse=reverse)
  else:
    #Sorter leksikografisk:
    sorted_list = sorted(iterable, key=lambda x: x.lower(), reverse=reverse)
  return sorted_list

def open_and_sort(file_paths):
    # Gennemgå filer
    for file_path in file_paths:
        print("filepath")
        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()
                sorted_lines = sort(lines)
                for line in sorted_lines:
                    print(line, end='')  # Print fundet linje
        except FileNotFoundError:
            print(f"Fejl: Filen '{file_path}' findes ikke.", file=sys.stderr)
        except PermissionError:
            print(f"Fejl: Du har ikke tilladelse '{file_path}'.", file=sys.stderr)
        except Exception as e:
            print(f"Fejl: {e}", file=sys.stderr)

def main():
    if len(sys.argv) < 2:
        print("Du har angivet for få argumenter. Du skal angive mindst ét gyldigt filnavn", file=sys.stderr)
        sys.exit(1)

    file_paths = sys.argv[1:]
    open_and_sort(file_paths)

if __name__ == "__main__":
    main()


# Kør programmet med
# python sort.py testCases/liste.txt
# python sort.py testCases/listeAfInt.txt
# python sort.py testCases/listeAfIntOgOrd.txt