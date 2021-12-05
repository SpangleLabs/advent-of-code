from utils.input import load_input

my_input = load_input()

increases = 0
lines = my_input.split("\n")
prev_line = int(lines[0])
for line in lines[1:]:
    cur_line = int(line)
    if cur_line > prev_line:
        increases += 1
    prev_line = cur_line
print(increases)
