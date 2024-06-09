import os
import sys

def mkdir(path):
    """Skab en mappe på den angivne sti"""
    try:
        os.mkdir(path)
        print(f"Mappen '{path}' er blevet dannet.")
    except FileExistsError:
        print(f"Fejl: Mappen '{path}' findes allerede!")
    except PermissionError:
        print(f"Fejl: Adgang nægtet til stien '{path}'.")
    except FileNotFoundError:
        print(f"Fejl: Stien '{path}' findes ikke eller er ugyldig.")
    except Exception as e:
        print(f"Fejl: {e}")

def main():
    if len(sys.argv) < 2:
        print("Du mangler at angive en sti til den mappe, der skal oprettes.", file=sys.stderr)
        sys.exit(1)

    for path in sys.argv[1:]:
        mkdir(path)

if __name__ == "__main__":
    main()

# Kør programmet med python mkdir.py testCases/mkdirVirker