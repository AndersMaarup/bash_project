import sys
import re

def cat(files, output_stream):
    for filename in files:
        with open(filename, 'r') as file:
            for line in file:
                # print("cat found line: ", line)
                output_stream.write(line)

def grep(pattern, input_stream, output_stream):
    for line in input_stream:
        if re.search(pattern, line):
            output_stream.write(line)

def wc(input_stream, output_stream):
    # print("wc called with input: ", input_stream, " and output ", output_stream)
    count_lines, count_words, count_bytes = 0, 0, 0
    for line in input_stream:
        # print("wc running line: ", line)
        count_lines += 1
        count_words += len(line.split())
        count_bytes += len(line.encode('utf-8'))
    output_stream.write(f"Lines: {count_lines}, Words: {count_words}, Bytes: {count_bytes}\n")

# Echo
def echo(input_stream, output_stream):
    for line in input_stream:
        print(line)
        output_stream.write(line)

# Tee

# Cut 
def cut(arguments, input_stream, output_stream):
    delimiter = ","
    for line in input_stream:        
        split_line = line.split(delimiter)
        column_indices = [int(extraction) - 1 for extraction in arguments]
        newLine = []
        for index in column_indices:
            if index < len(split_line):
                newLine.append(split_line[index])
        output_stream.write(str(newLine))

def execute_command(command, args, input_stream, output_stream):
    if command == 'cat':
        # print("Executing cat")
        cat(args, output_stream)
    elif command == 'grep':
        # print("Executing grep")
        grep(args[0], input_stream, output_stream)
    elif command == 'wc':
        # print("Executing wc")
        wc(input_stream, output_stream)
    elif command == 'echo':
        echo(input_stream, output_stream)
    elif command == 'cut':
        cut(args, input_stream, output_stream)
    else:
        raise ValueError(f"Unknown command: {command}")

command_functions = {"cat": cat, "grep": grep, "wc": wc, "echo": echo, "cut": cut}

def streaming(pipeline):
    # Using StringIO to simulate file-like objects for intermediate streams
    from io import StringIO
    commands = pipeline.split(' sep ')
    intermediate_stream = None

    print("Commands: ", commands)

    for i, command_string in enumerate(commands):
        parts = command_string.split()
        command = parts[0]
        # print("Command: ", command)
        args = parts[1:]
        # print("Args: ", args)
        
        if i == 0:  # first command
            input_stream = StringIO()
            cat(args, input_stream)  # Assuming the first command is cat for simplicity to start with
            input_stream.seek(0)  # Reset stream to the beginning for reading
            intermediate_stream = StringIO()
        elif i == len(commands) - 1:  # last command
            execute_command(command, args, input_stream, sys.stdout)
        else:  # intermediate commands
            intermediate_stream = StringIO()
            execute_command(command, args, input_stream, intermediate_stream)
            intermediate_stream.seek(0)  # Reset stream to the beginning for reading
            input_stream = intermediate_stream

if __name__ == "__main__":
    print("Starting")
    # if len(sys.argv) != 2:
    #     print("Usage: python script.py 'pipeline'", file=sys.stderr)
    #     sys.exit(1)
    pipeline = "cat test/navnetabel1.txt sep cut 1 sep grep Morten sep echo sep wc"
    # pipeline = sys.argv[1]
    streaming(pipeline)