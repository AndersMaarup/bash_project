import sys
import re
import os
import psutil 
import tarfile
import shutil

# CAT
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



# CUT
def cut(string, *extractions):
    lines = string.split("\n")
    delimiter = ","
    extraction = []
    column_indices = [int(extraction) - 1 for extraction in extractions]
    for line in lines:
        split_line = line.split(delimiter)
        newLine = []
        # For each word, if index matches 'extractions', add to list 'extraction'
        for index in column_indices:
            if index < len(split_line):
                newLine.append(split_line[index])
        extraction.append(delimiter.join(newLine))
    return "\n".join(extraction)

# ECHO
def echo(string):
    print(string)




# FIND
def find(*arguments):
    path = arguments[0]
    type = arguments[1]

    matching_files = []
    # FIND -name "filname"
    if type == "-name":
        for root, dirs, files in os.walk(path):
            for file in files:
                pattern = arguments[2]
                if re.search(pattern, file):
                    matching_files.append(os.path.join(root, file))
    elif type == "-type":
        filetype = arguments[2]
        if filetype == "f":
            for root, dirs, files in os.walk(path):
                for file in files:
                    matching_files.append(os.path.join(root, file))
        elif filetype == "d":
            for root, dirs, files in os.walk(path):
                for dir in dirs:
                    matching_files.append(os.path.join(root, dir))
    return "\n".join(matching_files)

# GREP
def grep(pattern, string):
    compiled_pattern = re.compile(pattern)
    matching_lines = []
    for line in string.split("\n"):
        if compiled_pattern.search(line):
            matching_lines.append(line)
    return "\n".join(matching_lines)

# GUNSIP
def gunzip(*arguments):
    output_file_path = arguments[0].rstrip('.gz')
    with gzip.open(arguments[0], 'rb') as input_file:
        with open(output_file_path, 'wb') as output_file:
            shutil.copyfileobj(input_file, output_file)

# GZIP
def gzip(*arguments):
    output_file_path = arguments[0] + ".gz"
    with open(arguments[0], "rb") as input_file:
        with gzip.open(output_file_path, "wb") as output:
            shutil.copyfileobj(input_file, output)

# HEAD
def head(*arguments):
    content = []
    if len(arguments) == 1:
        n = 10
        file = arguments[0]
    elif arguments[0]== "-n":
        n = int(arguments[1])
        file = arguments[2]
    try:
        with open(file, "r") as file:
            content = file.read()
    except FileNotFoundError:
        print(f"Error: '{file}' does not exist.")
    splittedLines = content.split("\n")
    return "\n".join(splittedLines[:n])

# LS 
def ls(path='.'):
    try:
        # Get a list of files and directories in the specified path
        contents = os.listdir(path)
        # Sort the contents alphabetically
        contents.sort()
        # Print the contents
        for item in contents:
            print(item)
    except FileNotFoundError:
        print(f"Error: The directory '{path}' does not exist.")
    except PermissionError:
        print(f"Error: Permission denied to list contents of '{path}'.")
    return "\n".join(contents)    

# MKDIR
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

# PS
def ps():
    print(f"{'PID':<6} {'USER':<10} {'CPU_TIME':<10} {'CMD'}")
    for proc in psutil.process_iter(['pid', 'username', 'cpu_times', 'cmdline']):
        try:
            pid = proc.info['pid']
            user = proc.info['username']
            cpu_time = sum(proc.info['cpu_times'][:2]) if proc.info['cpu_times'] else 0
            cmdline = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ''

            print(f"{pid:<6} {user:<10} {cpu_time:<10.2f} {cmdline}")

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass  # This process might have ended, or we don't have permission to access its info
            

# SORT
def sort(string, reverse=False):
    lines = string.split("\n")
    numeric = True
    for item in lines:
        try:
            float(item)  # Prøv at konvertér til float
        except ValueError: #Hvis ikke...
            numeric = False # ... er listen ikke numerisk
            break  # Hvis én ikke er, så behøver vi ikke at gå videre
    if numeric:
        #Sorter numerisk. Strings konverteres til float.
        sorted_lines = sorted(lines, key=lambda x: float(x), reverse=reverse)
    else:
        #Sorter leksikografisk:
        sorted_lines = sorted(lines, key=lambda x: x.lower(), reverse=reverse)
    return "\n".join(sorted_lines)

# Tail
def tail(*arguments):
    content = []
    if len(arguments) == 1:
        n = 10
        file = arguments[0]
    elif arguments[0]== "-n":
        n = int(arguments[1])
        file = arguments[2]
    print ("n=", n)
    try:
        with open(file, "r") as file:
            content = file.read()
    except FileNotFoundError:
        print(f"Error: '{file}' does not exist.")
    splittedLines = content.split("\n")
    return "\n".join(splittedLines[-n:])

# TAR
def tar(*arguments):
    # Create a new tar file
    with tarfile.open(arguments[0], "w") as tar:
        # Add all files to the tar file
        for path in arguments[1:]:
            tar.add(path, arcname=path.split("/")[-1])
    
# TEE
def tee(filename, directory, string):
    # Check if directory exists
    os.makedirs(directory, exist_ok=True)
    # Make file path
    file_path = os.path.join(directory, filename)
    # Open file and write
    with open(file_path, "w") as file:
        file.write(string)

# TR
def tr(string, *arguments):
    delete = False
    if arguments[0] == "-d":
        delete = True
        convert = arguments[1]
    else:
        convert_from = arguments[0]
        convert_to = arguments[1]
    translated = ""

    #-d option
    if delete:
        for char in string:
            if char not in convert:
                translated += char
        return translated

  # Convert
  # Convert from lower to upper case  
    if convert_from == "lower" and convert_to == "upper" or convert_from == "a-z" and convert_to == "A-Z":    
        for char in string:
            if char.islower():
                translated += char.upper()
            else:
                translated += char
  # Convert from upper to lower case
    elif convert_from == "upper" and convert_to == "lower" or convert_from == "A-Z" and convert_to == "a-z":
        for char in string:
            if char.isupper():
                translated += char.lower()
            else:
                translated += char
    return translated

# UNIQ
def uniq(string):
    lines = string.split("\n")
    unique_lines = []
    for line in lines:
        if line not in unique_lines:
            unique_lines.append(line)
    return "\n".join(unique_lines)

# WC
def wc(string):
    words = string.split()
    count = len(words)
    return count


def functionCall(command, currentString, *arguments):
        
        # CAT    
        if command == "cat":
            concatenated=cat(*arguments)
            currentString = concatenated
        # GREP
        elif command == "grep":
            pattern = arguments[0]
            matching = grep(pattern, currentString)
            currentString = matching
        # CUT
        elif command == "cut":
            cutted = cut(currentString, *arguments)
            currentString = cutted
        # TEE
        elif command == "tee" or command== ">":
            # Arguments: filename, directory
            file_name = arguments[0]
            directory = arguments[1]
            tee(file_name, directory, currentString)
        # ECHO
        elif command == "echo":
            if len(arguments) > 0:
                currentString = " ".join(arguments)
            echo(currentString)
        # FIND
        elif command == "find":
            matching_files = find(*arguments)
            currentString = matching_files
        # GUNZIP
        elif command == "gunzip":
            gunzip(*arguments)
        # GZIP
        elif command == "gzip":
            gzip(*arguments)
        # HEAD
        elif command == "head":
            currentString = head(*arguments)
        # LS
        elif command == "ls":
            listed = ls(arguments[0])
            currentString = listed
        # PS
        elif command == "ps":
            print("Trying to run ps")
            currentString = ps()
        # SORT
        elif command == "sort":
            sorted = sort(currentString)
            currentString = sorted
        # TAIL
        elif command == "tail":
            currentString = tail(*arguments)
        # TAR
        elif command == "tar":
            # Arguments: navn på mappe (.tar), files og mapper
            tar(*arguments)
        # TEE
        elif command == "tee" or command== ">":
            # Arguments: filename, directory
            file_name = arguments[0]
            directory = arguments[1]
            tee(file_name, directory, currentString)
        # TR
        elif command == "tr":
            translated = tr(currentString, *arguments)
            currentString = translated
        # UNIQ
        elif command == "uniq":
            unique = uniq(currentString)
            currentString = unique
        # WC
        elif command == "wc":
            wordcount = wc(currentString)
            currentString = str(wordcount)

        return currentString
        

def main():
  filepath = "./file.txt"
  pattern = "client"

  pipeline = lambda path, pat: grep(pat, cat(path))

  results = pipeline(filepath, pattern)

  for line in results:
      print(line, end='')
  

if __name__ == "__main__":
    main()