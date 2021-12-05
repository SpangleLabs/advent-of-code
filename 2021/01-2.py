from utils.input import load_input

my_input = load_input()

increases = 0
lines = my_input.split("\n")
window = [int(x) for x in lines[:3]]
for line in lines[3:]:
    cur_line = int(line)
    new_window = window[1:] + [cur_line]
    if sum(new_window) > sum(window):
        increases += 1
    window = new_window
print(increases)
