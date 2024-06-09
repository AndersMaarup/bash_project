import sys
import re
from io import StringIO
import os
import shutil
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import pandas as pd

from generate_random import generate_list

# Define commands using streams
def cat(*arguments):
    input_stream = arguments[-2]
    output_stream = arguments[-1]
    files = arguments[:-2]
    for filename in files:
        with open(filename, 'r') as file:
            for line in file:
                output_stream.write(line)

def catMiddle(input_stream, output_stream):
    for filename in input_stream:
        filename = filename.strip()
        with open(filename, 'r') as file:
            for line in file:
                output_stream.write(line)

def echo(input_stream, output_stream):
    for line in input_stream:
        output_stream.write(line)

def cut(arguments, input_stream, output_stream):
    delimiter = ","
    if isinstance(arguments, int):
        arguments = [arguments]
    for line in input_stream:
        split_line = line.split(delimiter)
        column_indices = [int(extraction) - 1 for extraction in arguments]
        new_line = [split_line[index] for index in column_indices if index < len(split_line)]
        output_stream.write(",".join(new_line) + "\n")

def chmod(mode, input_stream, output_stream):
    for line in input_stream:
        path = line.strip()
        try:
            os.chmod(path, int(mode, 8))
            output_stream.write(f"Changed mode of '{path}' to '{mode}'.\n")
        except Exception as e:
            output_stream.write(f"Error changing mode of '{path}': {e}\n")

def cp(source, destination, input_stream, output_stream):
    for line in input_stream:
        try:
            if os.path.isdir(source):
                shutil.copytree(source, destination)
            else:
                shutil.copy2(source, destination)
            output_stream.write(f"Copied '{source}' to '{destination}'.\n")
        except Exception as e:
            output_stream.write(f"Error copying '{source}': {e}\n")

def find(path, type, pattern, input_stream, output_stream):
    for root, dirs, files in os.walk(path):
        if type == '-name':
            for file in files:
                pattern = pattern.replace("\\", "/")  # Replace backslashes with forward slashes
                pattern = re.escape(pattern)  # Escape the pattern to handle special characters
                if re.search(pattern, file):
                    output_stream.write(os.path.join(root, file) + "\n")
        elif type == '-type':
            if pattern == 'f':
                for file in files:
                    output_stream.write(os.path.join(root, file) + "\n")
            elif pattern == 'd':
                for dir in dirs:
                    output_stream.write(os.path.join(root, dir) + "\n")

def grep(pattern, input_stream, output_stream):
    for line in input_stream:
        pattern = pattern.replace("\\", "/")  # Replace backslashes with forward slashes
        pattern = re.escape(pattern)  # Escape the pattern to handle special characters
        if re.search(pattern, line):
            output_stream.write(line)

def head(n, input_stream, output_stream):
    for i, line in enumerate(input_stream):
        if i < n:
            output_stream.write(line)
        else:
            break

def ln(source, destination, symbolic=False, input_stream=None, output_stream=None):
    try:
        if symbolic:
            os.symlink(source, destination)
        else:
            os.link(source, destination)
        output_stream.write(f"Linked '{source}' to '{destination}'.\n")
    except Exception as e:
        output_stream.write(f"Error linking '{source}': {e}\n")

def ls(path, input_stream, output_stream, **flags):
    try:
        for entry in os.scandir(path):
            if flags.get('directory'):
                output_stream.write(os.path.join(path, entry.name) + "\n")
            else:
                output_stream.write(entry.name + "\n")
    except Exception as e:
        output_stream.write(f"Error reading '{path}': {e}\n")


def mkdir(path, input_stream, output_stream):
    try:
        os.mkdir(path)
        output_stream.write(f"Directory '{path}' created.\n")
    except Exception as e:
        output_stream.write(f"Error creating directory '{path}': {e}\n")

def mv(source, destination, input_stream, output_stream):
    for line in input_stream:
        try:
            shutil.move(source, destination)
            output_stream.write(f"Moved '{source}' to '{destination}'.\n")
        except Exception as e:
            output_stream.write(f"Error moving '{source}': {e}\n")

def read(prompt, input_stream, output_stream):
    for line in input_stream:
        user_input = input(prompt)
        output_stream.write(user_input + "\n")

def rm(path, input_stream, output_stream):
    for line in input_stream:
        try:
            if os.path.isfile(path):
                os.remove(path)
            output_stream.write(f"Removed '{path}'.\n")
        except Exception as e:
            output_stream.write(f"Error removing '{path}': {e}\n")

def sort(input_stream, output_stream, **flags):
    lines = input_stream.readlines()
    if flags.get('reverse'):
        lines.sort(reverse=True)
    else:
        lines.sort() 
    for line in lines:
        output_stream.write(line)

def tail(n, input_stream, output_stream):
    lines = input_stream.readlines()[-n:]
    for line in lines:
        output_stream.write(line)

def tee(filename, directory, input_stream, output_stream):
    os.makedirs(directory, exist_ok=True)
    file_path = os.path.join(directory, filename)
    with open(file_path, 'a') as file:
        for line in input_stream:
            file.write(line)
            output_stream.write(line)

def tr(*args):
    input_stream = args[-2]
    output_stream = args[-1]
    arguments = args[:-2]
    if len(arguments) == 1:
        conversion = args[0]
    else:
        conversion, target = args[0], args[1]
    for line in input_stream:
        if conversion == 'delete':
            output_stream.write("".join(char for char in line if char not in target))
        elif conversion == 'lower' and target == 'upper':
            output_stream.write(line.lower())
        elif conversion == 'upper' and target == 'lower':
            output_stream.write(line.upper())
        else:
            output_stream.write(line)

def touch(files, input_stream, output_stream):
    for file_path in files:
        with open(file_path, 'a'):
            os.utime(file_path, None)
        output_stream.write(f"Touched '{file_path}'.\n")

def uniq(input_stream, output_stream):
    seen = set()
    for line in input_stream:
        if line not in seen:
            seen.add(line)
            output_stream.write(line)

def wc(input_stream, output_stream):
    count_lines, count_words, count_bytes = 0, 0, 0
    for line in input_stream:
        count_lines += 1
        count_words += len(line.split())
        count_bytes += len(line.encode('utf-8'))
    output_stream.write(f"Lines: {count_lines}, Words: {count_words}, Bytes: {count_bytes}\n")


class Pipeline:
    def __init__(self):
        self.commands = []

    def run(self, *steps):
        self.add_steps(*steps)
        return self.execute()

    def add_steps(self, *steps):
        for step in steps:
            self.commands.append(step)

    def execute(self):
        input_stream = StringIO()
        output_stream = StringIO()

        for step in self.commands:
            input_stream.seek(0)
            output_stream = StringIO()
            step(input_stream, output_stream)
            input_stream = output_stream
            input_stream.seek(0)

        output_stream.seek(0)
        return output_stream.read()

# Wrapping command functions to match original usage
def pc(func, *args, **flags):
    return lambda input_stream, output_stream: func(*args, input_stream, output_stream, **flags)

def pipeline1(file_path, output=False):
    pipeline1 = Pipeline()
    result = pipeline1.run(
        pc(cat, file_path),
        pc(cut, [1])
    )
    if output:
        print(result)

def pipeline2(file_path, output=False):
    pipeline = Pipeline()
    result = pipeline.run(
        pc(cat, file_path),
        pc(sort),
        pc(sort, reverse=True),
        pc(sort),
        pc(sort, reverse=True),
        pc(tail, len(file_path)),
        pc(wc)
    )
    if output:
        print(result)

def pipeline3(file_path, output=False):
    # Define pipeline
    pipeline = Pipeline()
    # Define steps
    result = pipeline.run(
        pc(find, "./test", "-name", file_path),
        pc(catMiddle),
        pc(grep,"Zeta"),
        pc(cut, 4),
        pc(uniq),
        pc(sort),
        pc(tee,"pipeline3.txt", "./resultater"),
        pc(wc)
    )
    if output:
        print(result)

def pipeline4(file_path, output=False):
    # Define pipeline
    pipeline = Pipeline()
    # Define steps
    result = pipeline.run(
        pc(mkdir,"temp"),
        pc(ls,"./test/lsTest1", directory=True),
        pc(grep,file_path),
        pc(catMiddle),
        pc(grep,"Gamma"),
        pc(uniq),
        pc(sort),
        pc(tee,"pipeline4_output1.txt", "temp"),
        pc(ls,"./test/lsTest2", directory=True),
        pc(grep,file_path),
        pc(catMiddle),
        pc(grep,"Gamma"),
        pc(uniq),
        pc(sort),
        pc(tee,"pipeline4_output2.txt", "temp"),
        pc(cat,"./temp/pipeline4_output1.txt", "./temp/pipeline4_output2.txt"),
        pc(uniq),
        pc(tee,"finalOutput.txt", "temp"),
        pc(mv,"temp/finalOutput.txt", "./resultater/finalOutput.txt"),
        pc(rm,"temp")
    )
    if output:
        print(result)

def pipeline3b(file_path, output = False):
    # Define pipeline
    pipeline = Pipeline()
    # Define steps
    result = pipeline.run(
        pc(find,"./test", "-name", file_path),
        pc(catMiddle,),
        pc(grep,"John"),
        pc(cut,4),
        pc(tr,"upper", "lower"),
        pc(tr,"lower", "upper"),
        pc(tee,"pipeline5.txt", "./results"),
        pc(wc)
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

    pipelines = [pipeline1]
    
    data_lenghts = [10, 100, 1000, 10000, 100000, 1000000]

    # Perform the timing measurements
    timing_data = timing(data_lenghts,pipelines, num_runs)

    # Export the timing data for each pipeline
    if timing_enabled and export_enabled:
        for pipeline in pipelines:
            export(data_lenghts, {pipeline.__name__: timing_data[pipeline.__name__]}, f'variant_3_pipeline_timing_data_varying_size_{pipeline.__name__}.xlsx')

if __name__ == "__main__":
    main()