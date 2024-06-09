from functools import singledispatch

import timeit
import time
import re
import os
import tarfile
import shutil
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import pandas as pd

from generate_random import generate_list

line_count = 0

# String
def cat():
    def func(line=None):
        paths = [line]
        for file_path in paths:
            path = file_path.strip()
            try:
                with open(path, 'r') as file:
                    for line in file:
                        yield line.strip()
            except FileNotFoundError:
                yield f"Error: '{file_path}' does not exist."
            except Exception as e:
                yield f"Error reading '{file_path}': {e}"
    return func

def cat(*file_paths: str):
    def func(line=None):
        if line is None:
            paths = file_paths
        else:
            paths = [line]
        for file_path in paths:
            path = file_path.strip()
            try:
                with open(path, 'r') as file:
                    for line in file:
                        yield line.strip()
            except FileNotFoundError:
                yield f"Error: '{file_path}' does not exist."
            except Exception as e:
                yield f"Error reading '{file_path}': {e}"
    return func

def cat(*file_paths: tuple):
    def func(line=None):
        paths = file_paths if line is None else [line]
        for file_path in paths:
            file_path = file_path.strip()
            try:
                with open(file_path, 'r') as file:
                    for file_line in file:
                        yield file_line.strip()
            except FileNotFoundError:
                yield f"Error: '{file_path}' does not exist."
            except Exception as e:
                yield f"Error reading '{file_path}': {e}"
        yield "***Last line***"
    return func

def catMiddle():
    def cat_function(line = None):
        path = line.strip()
        try:
            with open(path, 'r') as file:
                for line in file:
                    yield line.strip()   
        except FileNotFoundError:
            yield f"Error: '{line}' does not exist."
        except Exception as e:
            yield f"Error reading '{line}': {e}"
        yield "***Last line***"
    return cat_function

def catList(*file_paths: list):
    def func(line):
        paths = file_paths
        for file_path in paths:
            path = file_path.strip()
            try:
                with open(path, 'r') as file:
                    for line in file:
                        yield line.strip()
            except FileNotFoundError:
                yield f"Error: '{file_path}' does not exist."
            except Exception as e:
                yield f"Error reading '{file_path}': {e}"
    return func

# CHMOD
def chmod(mode):
    def func(line):
        try:
            os.chmod(line, int(mode, 8))  # Convert mode from string to octal
            print(f"Changed mode of '{line}' to '{mode}'.")
        except FileNotFoundError:
            print(f"Error: One or more files do not exist.")
        except PermissionError:
            print(f"Error: Permission denied to change mode of one or more files.")
        except Exception as e:
            print(f"Error changing mode: {e}")
        yield line
    return func

# CP
def cp(source, destination):
    def func(line=None):
        try:
            if os.path.isdir(source):
                shutil.copytree(source, destination)
            else:
                shutil.copy2(source, destination)
        except FileNotFoundError:
            print(f"Error: '{source}' does not exist.")
        except PermissionError:
            print(f"Error: Permission denied to copy '{source}'.")
        except Exception as e:
            print(f"Error copying '{source}': {e}")
        yield line
    return func

# CUT
def cut(*args):
    def cut_func(line=None):
        if line is None:
            # Reading from a file
            file_path = args[0]

            column_indices = [int(arg) - 1 for arg in args[1:]]
            cat_func = cat(file_path)

            for line in cat_func():
                if line == "***Last line***":
                    yield line
                else:
                    yield cutting(line, *column_indices)
        elif line == "***Last line***":
            yield line
        else:
            # Processing incoming lines
            column_indices = [int(arg) - 1 for arg in args]
            yield cutting(line, *column_indices)
    return cut_func

def cutting(line, *column_indices):
    split_line = line.split(",")
    new_line = [split_line[index] for index in column_indices if index < len(split_line)]
    return ",".join(new_line)

# ECHO
def echo(*args):
    def func(line=None):
        if line == None:
            if len(args) <= 0:
                raise ValueError("echo: missing arguments. You need to provide at least one file path.")
            file_paths = args
            catFunc = cat(file_paths)
            line = catFunc()
        print("echo: ", line, "\n")
        yield line
    return func


# FIND
def find(*arguments, **flag):
    def func(line=None):
        path = arguments[0]
        type = arguments[1]

        # FIND -name "filename"
        if type == "-name":
            pattern = arguments[2]
            pattern = pattern.replace("\\", "/")  # Replace backslashes with forward slashes
            pattern = re.escape(pattern)  # Escape the pattern to handle special characters
            for root, dirs, files in os.walk(path):
                for file in files:
                    if re.search(pattern, file):
                        # If -d flag is set, only return the filename
                        if flag.get('directory', True):
                            yield file
                        else:
                            yield os.path.join(root, file)

        elif type == "-type":
            filetype = arguments[2]
            if filetype == "f":
                for root, dirs, files in os.walk(path):
                    for file in files:
                        if flag.get('directory', True):
                            yield file
                        else:
                            yield os.path.join(root, file)
            elif filetype == "d":
                for root, dirs, files in os.walk(path):
                    for dir in dirs:
                        if flag.get('directory', True):
                            yield dir
                        else:
                            yield os.path.join(root, dir)
    return func

def grep(pattern):
    def grep_func(line):
        if line == "***Last line***":
            yield line
        else:
            compiled_pattern = re.compile(pattern)
            if compiled_pattern.search(line):
                yield line
    return grep_func

# HEAD
def head(*arguments):
    def head_func(line):
        if line == "***Last line***":
            yield line
        else:
            n = int(arguments[0])
            yield line[:n]
    return head_func

# LN
def ln(source, destination, symbolic=False):
    def func(line=None):
        try:
            if symbolic:
                os.symlink(source, destination)
                print(f"Created symbolic link '{destination}' -> '{source}'.")
            else:
                os.link(source, destination)
                print(f"Created hard link '{destination}' -> '{source}'.")
        except FileNotFoundError:
            print(f"Error: '{source}' does not exist.")
        except FileExistsError:
            print(f"Error: '{destination}' already exists.")
        except PermissionError:
            print(f"Error: Permission denied to link '{source}' to '{destination}'.")
        except Exception as e:
            print(f"Error linking '{source}': {e}")
        yield line
    return func

# LS
def ls(path=".", **flags):
    def ls_func(line=None):
        if line == "***Last line***":
            yield line
        elif():
            try:
                for entry in os.scandir(path):
                    if flags.get('directory', True):
                        yield os.path.join(path, entry.name)
                    else:
                        yield entry.name
            except FileNotFoundError:
                yield f"Error: '{path}' does not exist."
            except Exception as e:
                yield f"Error reading '{path}': {e}"
    return ls_func

# MKDIR
def mkdir(path):
    def func(line = None):
        try:
            os.mkdir(path)
        except FileExistsError:
            print(f"Error at mkdir: mkdir tries to make the directory '{path}' which already exists!")
        except PermissionError:
            print(f"Error at mkdir: Mkdir was denied permission to make a directory at '{path}'.")
        except FileNotFoundError:
            print(f"Error at mkdir: The directory '{path}' doesn't exist or are invalid.")
        except Exception as e:
            print(f"Error at mkdir: {e}")
        yield None
    return func

# MV
def mv(source, destination):
    def func(line=None):
        try:
            shutil.move(source, destination)
        except FileNotFoundError:
            print(f"Error: '{source}' does not exist.")
        except PermissionError:
            print(f"Error: Permission denied to move '{source}'.")
        except Exception as e:
            print(f"Error moving '{source}': {e}")
        yield line
    return func

# READ
def read(prompt=""):
    def func(line=None):
        user_input = input(prompt)
        if line is None:
            yield [user_input]
        else:
            yield line + [user_input]
    return func

# RM
def rm(*paths, recursive=False):
    def func(line=None):
        for path in paths:
            if os.path.isfile(path):
                os.remove(path)
            elif os.path.isdir(path) and recursive:
                shutil.rmtree(path)
                # print(f"Directory '{path}' and its contents have been removed.")
            elif os.path.isdir(path):
                print(f"Error: Directory '{path}' is not empty. Use recursive=True to remove it and its contents.")
            else:
                print(f"Error: '{path}' does not exist.")
        yield line
    return func

# SORT
def sort(reverse=False):
    def sort_func(lines):
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
    return sort_func

# TAIL  
def tail(*arguments):
    def tail_function(lines):
        if len(arguments) == 0:
            n = 10
        else:
            n = int(arguments[0])
        return lines[-n:]
    return tail_function

# TEE
def tee(filename, directory):
    def func(line=None):
        # Check if directory exists
        os.makedirs(directory, exist_ok=True)
        # Make file path
        file_path = os.path.join(directory, filename)
        # Open file in append mode and write
        with open(file_path, "a") as file:
            if line is not None:
                file.write(line + "\n")
                yield line
    return func

# TR
def tr(*arguments):
    def func(line):
        if line == "***Last line***":
            yield line
        else:
            translated = ""
            conversion = arguments[0]
            # Delete - option
            if (conversion == "delete"):
                for char in line:
                    if char not in arguments[1]:
                        translated += char
                yield translated

            # Convert from lower to upper case 
            elif (conversion == "lower" and arguments[1] == "upper" or 
                  conversion == "a-z" and arguments[1] == "A-Z"):
                for char in line:
                    if char.islower():
                        translated += char.upper()
                    else:
                        translated += char
            # Convert from upper to lower case
            elif (conversion == "upper" and arguments[1] == "lower" or
                    conversion == "A-Z" and arguments[1] == "a-z"):
                for char in line:
                    if char.isupper():
                        translated += char.lower()
                    else:
                        translated += char
            yield translated
    return func

# UNIQ
def uniq():
    def uniq_function(lines):
        unique_lines = []
        for line in lines:
            if line not in unique_lines:
                unique_lines.append(line)
        return unique_lines
    return uniq_function

# TOUCH
def touch(*file_paths):
    def func(line=None):
        for file_path in file_paths:
            # Open the file in append mode, which will create it if it does not exist
            with open(file_path, 'a'):
                os.utime(file_path, None)
        yield line
    return func

# WC
def wc(*args):
    def wc_function(lines = None):
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
    return wc_function


class Pipeline:
    def __init__(self):
        self.steps = []

    def run(self, *steps):
        self.add_steps(*steps)
        return self.execute()

    def add_steps(self, *steps):
        for step in steps:
            self.steps.append(step)  # Store the callable directly

    def execute(self, index=0, startLines=None):
        acc = []
        first_step = self.steps[index]

        # If execute is called recursively, we need to remove "***Last line***" from the list
        if type(startLines) is list:
            if "***Last line***" in startLines:
                startLines.remove("***Last line***")

        # If startLines is given, we start with these lines
        if startLines is not None:
            lines = startLines
        # Else, we get lines from first command
        else:
            lines = list(first_step()) 

        # Accumulator for bottle-neck functions
        bottleNeckAcc = []
        # Flag to not append lines to acc, in case of bottle-neck function
        doNotAppend = False

        # List of bottle-neck functions, ie. functions that need to be run on all lines before continuing
        bottleNeckFunctions = ["sort_func", "tail_function", "wc_function", "uniq_function"]

        # If only one step, accumulate and return
        if len(self.steps) == 1:
            acc.extend(lines)
            return acc
        # Else, we extend with "***Last Line***" to make sure we know when to stop
        else:
            lines.extend(["***Last Line***"])
            
        # If more commands, iterate through the lines:
        for line in lines:
            # Run the line through all commands
            for step_index, step in enumerate(self.steps[index+1:], index):
                # If command is bottle-function, ...                    
                if step.__name__ in bottleNeckFunctions:
                    if line == "***Last Line***" and step == self.steps[-1]:
                        returnValue = step(bottleNeckAcc)
                        for value in returnValue:
                            acc.append(value)
                            bottleNeckAcc = []
                        return acc
                    elif line == "***Last Line***":
                        doNotAppend = False
                        returnValue = step(bottleNeckAcc)
                        # Continue to next step with new lines
                        bottleNeckAcc = []
                        restOfList = self.execute(step_index + 1, returnValue)
                        return restOfList
                    else:
                        doNotAppend = True
                        bottleNeckAcc.append(line)
                        break
                # If the last line is reached in the last command, we break
                elif step == self.steps[-1] and line == "***Last Line***":
                    break
                
                # For all other functions, we run the line through the function
                else:
                    new_lines = list(step(line))
                    # If the function generates new lines, we overwrite the current line
                    if new_lines:
                        line = new_lines[0]  # Assuming only one line is returned
                    else:
                        # With no result, we will set to None and break, continuing to next line
                        line = None
                        # TODO: The next function should still be called
                        break
                        

            # We accumulate the line if it is not "Last Line"
            if line is not None and line != "***Last Line***" and not doNotAppend:
                    acc.append(line)

        return acc
    
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
    # Define pipeline
    pipeline = Pipeline()
    # Define steps
    result = pipeline.run(
        find("./test", "-name", file_path),
        catMiddle(),
        grep("Zeta"),
        cut(4),
        uniq(),
        sort(),
        tee("pipeline2.txt", "./resultater"),
        wc()
    )
    if output:
        print(result)

def pipeline3(file_path, output=False):
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
        cat("./temp/pipeline5_output1.txt", "./temp/pipeline4_output2.txt"),
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
        catMiddle(),
        grep("John"),
        cut(4),
        tr("upper", "lower"),
        tr("lower", "upper"),
        tee("pipeline5.txt", "./results"),
        wc()
    )
    if output:
        print(result)   

def timing(data_lengths, pipelines, num_runs):
    timing_data = {}

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
    timing_enabled = True
    export_enabled = True

    num_runs = 100  # Adjusted for better averaging

    pipelines = [pipeline1, pipeline2, pipeline3, pipeline4, pipeline3b]    
    data_lenghts = [10, 100, 1000, 10000, 100000, 1000000]

    # Perform the timing measurements
    timing_data = timing(data_lenghts,pipelines, num_runs)

    # Export the timing data for each pipeline
    if timing_enabled and export_enabled:
        for pipeline in pipelines:
            export(data_lenghts, {pipeline.__name__: timing_data[pipeline.__name__]}, f'variant_2_pipeline_timing_data_varying_size_{pipeline.__name__}.xlsx')

if __name__ == "__main__":
    main()