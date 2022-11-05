import sys
import time

name = sys.argv[1]
input = open(name + ".txt", "r")
output = open(name + "_raw.txt", "w")

input_lines = input.readlines()
output_line = ""
for line in input_lines:
    if ":" in line:
        colon_index = line.find(':')
        output_line = output_line + line[colon_index + 2:-1] + ","
    else:
        output.write(output_line + "\n")
        output_line = ""

input.close()
output.close()
