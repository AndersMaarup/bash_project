import os
import sys
import re

def nextArgument(index):
    if index + 1 < len(sys.argv):
        return sys.argv[index + 1]
    else:
        print("Missing argument", file=sys.stderr)

def rm(path):
    """Fjern en fil fra den angivne sti."""
    try:
        os.remove(path)
        print(f"Filen '{path}' er blevet fjernet.")
    except FileNotFoundError:
        print(f"Fejl: rm kan ikke fjerne '{path}'")
    except PermissionError:
        print(f"Fejl: rm er blevet nægtet adgang til at fjerne '{path}'.")
    except IsADirectoryError:
        print(f"Fejl: '{path}' er en mappe, ikke en fil.")
    except Exception as e:
        print(f"Fejl: {e}")

def mkdir(path):
    """Skab en mappe på den angivne sti"""
    try:
        os.mkdir(path)
        print(f"Mappen '{path}' er blevet dannet.")
    except FileExistsError:
        print(f"Fejl: mkdir prøver at lave mappen '{path}', men den findes allerede!")
    except PermissionError:
        print(f"Fejl: mkdir bliver nægtet adgang til stien '{path}'.")
    except FileNotFoundError:
        print(f"Fejl: mkdir kan ikke bruge stien '{path}'. Den findes ikke eller er ugyldig.")
    except Exception as e:
        print(f"Fejl: {e}")

def grep(pattern, file_paths):
    print("grep")
    print("Pattern: ", pattern)
    print("file_paths: ", file_paths)
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
    #TODO: Problem med forskelligt antal argumenter
    if len(sys.argv) < 2:
        print("Du har ikke angivet nok argumenter", file=sys.stderr)
        sys.exit(1)

    i = 1  # Start med index 1. 0 er navnet på programmet
    while i < len(sys.argv):
        argument = sys.argv[i]
        if argument == "rm":
            rm(nextArgument(i))
            i += 2  # Skip navnet på filen
        elif argument == "mkdir":
            mkdir(nextArgument(i))
            i += 2  # Skip navnet på mappen
        elif argument == "grep":
            if i+2 < len(sys.argv):  # Vær sikker på, at der er 2 argumenter: Mønster og fil
                grep(sys.argv[i+1], sys.argv[i+2:])
                i += 3 # Skip mønster og filer
        elif argument == "sort":
            open_and_sort(sys.argv[i+1:])
            i += 2
        

if __name__ == "__main__":
    main()