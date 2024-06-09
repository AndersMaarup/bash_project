from functools import singledispatch
import re
import os
import tarfile
import shutil
import sys
import re
import shlex

line_count = 0


def cat(*argument_list):
    files_read = False
    file_paths = argument_list
    for file_path in file_paths:
        with open(file_path, "r") as file:
            for line in file:
                yield line
            files_read = True
    # Check if any files were read at all
    if files_read:
        yield "***Last line***"


def grep(arguments, incoming_line):
    pattern = arguments[0]
    # print("grep: ", incoming_line)
    compiled_pattern = re.compile(r"\b" + pattern + r"\b")

    for line in incoming_line.split("\n"):
        # print("line: ", line)
        if compiled_pattern.search(line):
            yield line


def wc(line):
    global line_count
    line_count += 1
    if line == "***Last line***":
        return line_count


def make_command_map(*string):
    # Make an empty array
    command_array = []
    # Set index to 0
    i = 0
    # Set c to True (Next item is a command)
    c = True
    # Make an empty list of arguments
    list_of_arguments = []

    # Transforming the string from the terminal
    list_from_terminal = list(string[0])

    # For each item in the string (not including the first argument, just calling the correct file)
    for item in list_from_terminal[1:]:
        # Initialize next item as a command
        if c:
            # Put item in array
            command_array.append([item])
            # Next item is not a command
            c = False
        # If item is separator
        elif item == "sep":
            # Put list of arguments in command array
            command_array[i].append(list_of_arguments)
            # Increase index
            i += 1
            # Clear list of arguments
            list_of_arguments = []
            # Make next item a command
            c = True
        else:
            list_of_arguments.append(item)
    # Put last list of arguments in command array
    command_array[i].append(list_of_arguments)
    # Return command array
    return command_array


command_functions = {"cat": cat, "grep": grep, "wc_inc": wc}


def runPipeline(pipeline, commandIndex, line, acc):
    # Save command, currently set at index "command"
    current_command_name = pipeline[commandIndex][0]
    # Convert string to command
    current_command_func = command_functions.get(current_command_name)
    # Take arguments corresponding to command
    current_arguments = pipeline[commandIndex][1]

    # If command is wordcount:
    if current_command_name == "wc":
        # Get the result of the linecount
        linecount = wc(line)
        # As long as there is no result, pass
        if linecount == None:
            pass
        else:
            # If wc is last, we print:
            if commandIndex == len(pipeline) - 1:
                print(linecount)
            # Otherwise, we convert the integer to a string and forward
            else:
                line = str(linecount)
                runPipeline(pipeline, commandIndex + 1, line, acc)
    # For all other commands:
    # For all lines yielded from running the current argument in the current function,
    # send the yielded line to the next command
    else:
        # Run the command with all arguments
        # For each result yielded, run the next command with this result
        for line in current_command_func(*current_arguments):
            # If no more commands, accumulate lines and return
            if commandIndex == len(pipeline) - 1 and line == "***Last line***":
                return acc
            elif commandIndex == len(pipeline) - 1:
                print(line)
                acc.append(line)
                continue
            # Else, run recursively with next command in pipeline
            else:
                runPipeline(pipeline, commandIndex + 1, line, acc)

def main():
    # We map our input to a tuple of the type: [*command*][*arguments for command*]
    commands = make_command_map(sys.argv)
    # We run the pipeline
    result = runPipeline(commands, 0, 1, [])
    return result


if __name__ == "__main__":
    main()
