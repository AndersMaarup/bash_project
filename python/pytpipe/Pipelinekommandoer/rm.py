import os
import sys

def rm(path):
    """Fjern en fil fra den angivne sti."""
    try:
        os.remove(path)
        print(f"Filen '{path}' er blevet fjernet.")
    except FileNotFoundError:
        print(f"Fejl: '{path}' findes ikke!")
    except PermissionError:
        print(f"Fejl: Adgang nægtet til at fjerne '{path}'.")
    except IsADirectoryError:
        print(f"Fejl: '{path}' er en mappe, ikke en fil.")
    except Exception as e:
        print(f"Fejl: {e}")

def main():
    if len(sys.argv) < 2:
        print("Du skal angive mindst ét argument!", file=sys.stderr)
        sys.exit(1)

    for path in sys.argv[1:]:
        rm(path)

if __name__ == "__main__":
    main()

# Kør programmet med python rm.py testCases/<ny mappe>