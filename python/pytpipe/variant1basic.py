from functools import singledispatch

import time
import re
import os
import tarfile
import shutil
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import pandas as pd
import random
from generate_random import generate_list

def cat(*file_paths: tuple):
#     print("Cat as tuple")
    def func(lines = None):
        # print("Cat as tuple")
        results = []
        for file_path in file_paths:
            try:
                with open(file_path, "r") as file:
                    results.extend(file.readlines())
            except FileNotFoundError:
                results.append(f"Error: '{file_path}' does not exist.\n")
            except Exception as e:
                results.append(f"Error reading '{file_path}': {e}\n")
        return results
    return func

def cat(*file_paths: str):
    # print("Cat as string")
    def func(lines = None):
        results = []
        for path in file_paths:
            path = path.strip()  # Remove any surrounding whitespace
            try:
                with open(path, "r") as file:
                    results.extend(file.readlines())
            except FileNotFoundError:
                results.append(f"Error: '{path}' does not exist.\n")
            except Exception as e:
                results.append(f"Error reading '{path}': {e}\n")
        return results
    return func

# def cat(file_paths: list):
#     print("Cat as list")
#     def func(lines = None):
#         print("Cat as list")
#         print("length: ", len(file_paths))
#         results = []
#         for file_path in file_paths:
#             path = file_path.strip()
#             try:
#                 with open(path, "r") as file:
#                     print("Read: ", file.readlines())
#                     results.extend(file.readlines())
#             except FileNotFoundError:
#                 results.append(f"Error: '{file_path}' does not exist.\n")
#             except Exception as e:
#                 results.append(f"Error reading '{file_path}': {e}\n")
#         return results
#     return func

def catMiddle():
    def cat_function(lines = None):
        # print("Cat middle")
        results = []
        for file_path in lines:
            try:
                with open(file_path, 'r') as file:
                    results.extend(file.readlines())
            except FileNotFoundError:
                return f"Error: '{file_path}' does not exist."
            except Exception as e:
                return f"Error reading '{file_path}': {e}"
        return results
    return cat_function

# CHMOD
def chmod(mode, *file_paths):
    def func(lines=None):
        try:
            for file_path in file_paths:
                os.chmod(file_path, int(mode, 8))  # Convert mode from string to octal
                print(f"Changed mode of '{file_path}' to '{mode}'.")
        except FileNotFoundError:
            print(f"Error: One or more files do not exist.")
        except PermissionError:
            print(f"Error: Permission denied to change mode of one or more files.")
        except Exception as e:
            print(f"Error changing mode: {e}")
        return lines
    return func



# CP
def cp(source, destination):
    def func(lines=None):
        try:
            if os.path.isdir(source):
                shutil.copytree(source, destination)
                print(f"Copied directory '{source}' to '{destination}'.")
            else:
                shutil.copy2(source, destination)
                print(f"Copied file '{source}' to '{destination}'.")
        except FileNotFoundError:
            print(f"Error: '{source}' does not exist.")
        except PermissionError:
            print(f"Error: Permission denied to copy '{source}'.")
        except Exception as e:
            print(f"Error copying '{source}': {e}")
        return lines
    return func


# CUT
def cut(*arguments):
    if len(arguments) != len(set(arguments)):
        raise ValueError("Duplicate indices detected in extractions.")
    def func(lines = None):
        if lines == None:
            file_paths = arguments[0]
            catFunc = cat(file_paths)
            lines = catFunc()
            extractions = arguments[1:]
        else:
            extractions = arguments
        delimiter = ","
        extraction = []
        column_indices = [int(extraction) - 1 for extraction in extractions]
        for line in lines:
            split_line = line.split(delimiter)
            newLine = []
            for index in column_indices:
                numberOfColumns = len(split_line)
                if index >= numberOfColumns:
                    raise ValueError(f"You are calling 'cut' with index '{index}'. The file only has {numberOfColumns}!")
                if index < len(split_line):
                    newLine.append(split_line[index])
            extraction.append(delimiter.join(newLine))
        return extraction
    return func


# ECHO
def echo(*args):
    def func(lines=None):
        if lines == None:
            file_paths = args
            catFunc = cat(file_paths)
            lines = catFunc()
        print("echo: ", lines, "\n")
        return lines
    return func


# FIND
def find(*arguments, **flag):
    def func(lines = None):
        path = arguments[0]
        type = arguments[1]

        matching_files = []
        # FIND -name "filname"
        if type == "-name":
            for root, dirs, files in os.walk(path):
                for file in files:
                    pattern = arguments[2]
                    pattern = pattern.replace("\\", "/")  # Replace backslashes with forward slashes
                    pattern = re.escape(pattern)  # Escape the pattern to handle special characters
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
        return matching_files
    return func

def grep(*args):
    def func(lines=None):
        # No standard output: Read first
        if lines == None:
            *file_paths, pattern = args
            catFunc = cat(file_paths)
            lines = catFunc()
        else:
            pattern = args[0]
        return [line for line in lines if pattern in line]
    return func

# HEAD
def head(*arguments):
    def head_function(lines):
        if len(arguments) == 1:
            n = 10
        else:
            n = int(arguments[1])
        return lines[:n]
    return head_function

# LN
def ln(source, destination, symbolic=False):
    def func(lines=None):
        try:
            if symbolic:
                os.symlink(source, destination)
                # print(f"Created symbolic link '{destination}' -> '{source}'.")
            else:
                os.link(source, destination)
                # print(f"Created hard link '{destination}' -> '{source}'.")
        except FileNotFoundError:
            print(f"Error: '{source}' does not exist.")
        except FileExistsError:
            print(f"Error: '{destination}' already exists.")
        except PermissionError:
            print(f"Error: Permission denied to link '{source}' to '{destination}'.")
        except Exception as e:
            print(f"Error linking '{source}': {e}")
        return lines
    return func


# LS
def ls(path=".", **flag):
    def ls_function(lines = None):
        try:
            # Get a list of files and directories in the specified path
            contents = os.listdir(path)
            # Sort the contents alphabetically
            contents.sort()
            if flag.get("r", True):
                contents.reverse()
            if flag.get("directory", True):
                # Prepend the path to each content item
                contents = [os.path.join(path, item) for item in contents]
        except FileNotFoundError:
            print(f"Error: The directory '{path}' does not exist.")
            return []
        except PermissionError:
            print(f"Error: Permission denied to list contents of '{path}'.")
            return []
        return contents    
    return ls_function


# MKDIR
def mkdir(path):
    def func(lines = None):
        try:
            os.mkdir(path)
            # print(f"The directory '{path}' has been created.")
        except FileExistsError:
            print(f"Error: The directory '{path}' already exists!")
        except PermissionError:
            print(f"Error: Permission denied to path '{path}'.")
        except FileNotFoundError:
            print(f"Error: The path '{path}' doesn't exist or is invalid.")
        except Exception as e:
            print(f"Error: {e}")
        return None
    return func

# MV
def mv(source, destination):
    def func(lines=None):
        try:
            shutil.move(source, destination)
        except FileNotFoundError:
            print(f"Error: '{source}' does not exist.")
        except PermissionError:
            print(f"Error: Permission denied to move '{source}'.")
        except Exception as e:
            print(f"Error moving '{source}': {e}")
        return lines
    return func


# READ
def read(prompt=""):
    def func(lines=None):
        user_input = input(prompt)
        if lines is None:
            return [user_input]
        else:
            return lines + [user_input]
    return func


# RM
def rm(*paths, recursive=False):
    def func(lines=None):
        for path in paths:
            if os.path.isfile(path):
                os.remove(path)
                # print(f"File '{path}' has been removed.")
            elif os.path.isdir(path) and recursive:
                shutil.rmtree(path)
                # print(f"Directory '{path}' and its contents have been removed.")
            elif os.path.isdir(path):
                print(f"Error: Directory '{path}' is not empty. Use recursive=True to remove it and its contents.")
            else:
                print(f"Error: '{path}' does not exist.")
        return lines
    return func

# SORT
def sort(reverse=False):
    def sort_function(lines):
        numeric = True
        for item in lines:
            try:
                float(item)  # Prøv at konvertér til float
            except ValueError:  # Hvis ikke...
                numeric = False  # ... er listen ikke numerisk
                break  # Hvis én ikke er, så behøver vi ikke at gå videre
        if numeric:
            # Sorter numerisk. Strings konverteres til float.
            sorted_lines = sorted(lines, key=lambda x: float(x), reverse=reverse)
        else:
            # Sorter leksikografisk:
            sorted_lines = sorted(lines, key=lambda x: x.lower(), reverse=reverse)
        return sorted_lines
    return sort_function


# Tail
def tail(*arguments):
    def tail_function(lines = None):
        # If no standard output, read first
        if lines == None:
            file_paths = arguments[0]
            catFunc = cat(file_paths)
            lines = catFunc()
            if type(arguments[-1]) == int:
                n = arguments[-1]
            else:
                n = 10
        else:
            if len(arguments) == 1:
                n = 10
            elif arguments[0] == "-n":
                n = int(arguments[1])
        return lines[-n:]
    return tail_function

# TEE
def tee(filename, directory):
    def tee_function(lines):
        # Check if directory exists
        os.makedirs(directory, exist_ok=True)
        # Make file path
        file_path = os.path.join(directory, filename)
        # Convert list to string
        linesAsOneString = '\n'.join(lines)
        # Open file and write
        with open(file_path, "w") as file:
            file.write(linesAsOneString)
        return lines
    return tee_function


# TR
def tr(*arguments):
    # print("Translate")
    def tr_function(lines):
        delete = False
        translated_lines = []

        if arguments[0] == "-d":
            delete = True
            convert = arguments[1]
        else:
            convert_from = arguments[0]
            convert_to = arguments[1]

        # -d option
        if delete:
            for line in lines:
                translated = ''.join(char for char in line if char not in convert)
                translated_lines.append(translated)
            return translated_lines

        # Convert
        # Convert from lower to upper case
        if (
            convert_from == "lower" and convert_to == "upper" or
            convert_from == "a-z" and convert_to == "A-Z"
        ):
            for line in lines:
                translated = line.upper()
                translated_lines.append(translated)
            return translated_lines
        
        # Convert from upper to lower case
        elif (
            (convert_from == "upper" and convert_to == "lower") or
            (convert_from == "A-Z" and convert_to == "a-z")
            ):
            # print("Convert from ", convert_from, " to ", convert_to)
            for line in lines:
                translated = line.lower()
                translated_lines.append(translated)
            return translated_lines

        # If no valid arguments, return the original lines
        return lines

    return tr_function

# UNIQ
def uniq():
    def func(lines):
        unique_lines = []
        for line in lines:
            if line not in unique_lines:
                unique_lines.append(line)
        return unique_lines
    return func

# TOUCH
def touch(*file_paths):
    def func(lines=None):
        for file_path in file_paths:
            # Open the file in append mode, which will create it if it does not exist
            print("file_path: ", file_path)
            with open(file_path, 'a'):
                os.utime(file_path, None)
        return lines
    return func


# WC
def wc(*args):
    def func(lines = None):
        if lines == None:
            file_paths = args
            catFunc = cat(file_paths)
            lines = catFunc()
        total_words = 0
        total_characters = 0
        total_bytes = 0
        for line in lines:
            words = line.split(',')
            total_words += len(words)
            total_characters += sum(len(word) for word in words)
            total_bytes += sum(len(word.encode('utf-8')) for word in words)
        return f"Total words: ", total_words, "Total characters: ", total_characters, "Total bytes: ", total_bytes
    return func


class Pipeline:
    def __init__(self):
        self.steps = []

    def run(self, *steps):
        self.add_steps(*steps)
        return self.execute()

    def add_steps(self, *steps):
        self.steps = steps  # Directly set steps for each run

    def execute(self):
        standardOutput = None
        for step in self.steps:
            if standardOutput is None:  # For the first step, call without previous data
                standardOutput = step()  # Execute the callable
            else:  # For subsequent steps, pass the previous output as an argument
                standardOutput = step(standardOutput)
        return standardOutput
    
# Test functions
def pipeline1(file_path, output=False):
    # Define pipeline
    pipeline = Pipeline()
    # Run pipeline
    result = pipeline.run(
        cat(file_path),
        cut(1)
    )
    if output:
        print(result)

def pipeline2(file_path, output=False):
    pipeline = Pipeline()
    result = pipeline.run(
        cat(file_path),
        sort(),
        sort(reverse=True),
        sort(),
        sort(reverse=True),
        tail(len(file_path)),
        wc()
        )
    if output:
        print(result)

def pipeline3(file_path, output=False):
    # Define pipeline
    pipeline = Pipeline()
    # Define steps
    result = pipeline.run(
        find("./test", "-name", file_path),
        catMiddle(),
        grep("John"),
        cut(4),
        uniq(),
        sort(),
        tee("pipeline3.txt", "./results"),
        wc()
    )
    if output:
        print(result)

def pipeline4(file_path, output=False):
    # Define pipeline
    pipeline = Pipeline()
    # Define steps
    result = pipeline.run(
        mkdir("temp"),
        ls("./test/lsTest1", directory=True),
        grep(file_path),
        catMiddle(),
        grep("Gamma"),
        uniq(),
        sort(),
        tee("pipeline4_output1.txt", "temp"),
        ls("./test/lsTest2", directory=True),
        grep(file_path),
        catMiddle(),
        grep("Gamma"),
        uniq(),
        sort(),
        tee("pipeline4_output2.txt", "temp"),
        cat("./temp/pipeline4_output1.txt", "./temp/pipeline4_output2.txt"),
        uniq(),
        tee("finalOutput.txt", "temp"),
        mv("temp/finalOutput.txt", "./resultater/finalOutput.txt"),
        rm("temp", recursive=True)
    )
    if output:
        print(result)

def pipeline3b(file_path, output = False):
    # Define pipeline
    pipeline = Pipeline()
    # Define steps
    result = pipeline.run(
        find("./test", "-name", file_path),
        cat(),
        grep("John"),
        cut(4),
        tr("upper", "lower"),
        tr("lower", "upper"),
        tee("pipeline5.txt", "./results"),
        wc()
    )
    if output:
        print(result)    

def timing(pipelines, num_runs):
    timing_data = {}

    data_lengths = [10, 100, 1000, 10000, 100000, 1000000]

    for pipeline in pipelines:
        timing_data[pipeline.__name__] = {}

        for length in data_lengths:
            timing_data[pipeline.__name__][length] = []
            total_elapsed_time = 0
            for _ in range(num_runs):
                file_path = generate_list(length)
                start_time = time.perf_counter()
                pipeline(file_path)
                end_time = time.perf_counter()
                elapsed_time = end_time - start_time
                total_elapsed_time += elapsed_time
                timing_data[pipeline.__name__][length].append(elapsed_time)
                os.remove(file_path)
            
            elapsed_time_avg = total_elapsed_time / num_runs
            timing_data[pipeline.__name__][length].insert(0, elapsed_time_avg)
        # print(f"Timing data for {pipeline.__name__}:\n{timing_data[pipeline.__name__]}")
    return timing_data

def export(file_paths, timing_data, path):
    # Collect and export timing data
    all_timing_data = []

    for pipeline_name, data in timing_data.items():
        pipeline_df = []
        for file_path in file_paths:
            timings = np.array(data[file_path])
            df = pd.DataFrame(timings, columns=[f'{pipeline_name} ({file_path})'])
            pipeline_df.append(df)
        # Concatenate all dataframes for the current pipeline
        pipeline_result_df = pd.concat(pipeline_df, axis=1)
        all_timing_data.append(pipeline_result_df)

    # Concatenate all pipelines' DataFrames, filling missing values with NaN
    result_df = pd.concat(all_timing_data, axis=1)

    if os.path.exists(path):
        os.remove(path)
    result_df.to_excel(path, index=False)

def main():
    timing_enabled = False
    export_enabled = False

    num_runs = 1  # Adjusted for better averaging

    pipelines = [pipeline2]
    
    data_lenghts = [10]

    # Perform the timing measurements
    timing_data = timing(pipelines, num_runs)

    # Export the timing data for each pipeline
    if timing_enabled and export_enabled:
        for pipeline in pipelines:
            export(data_lenghts, {pipeline.__name__: timing_data[pipeline.__name__]}, f'variant_1_pipeline_timing_data_varying_size_{pipeline.__name__}.xlsx')

if __name__ == "__main__":
    main()