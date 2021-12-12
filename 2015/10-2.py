from utils.input import load_input


def construct_look_and_say(inp: str) -> str:
    out = ""
    count = 1
    last_char = inp[0]
    for char in inp[1:]:
        if char == last_char:
            count += 1
        else:
            out += f"{count}{last_char}"
            count = 1
            last_char = char
    out += f"{count}{last_char}"
    return out


if __name__ == "__main__":
    my_input = load_input()
    for step in range(50):
        my_input = construct_look_and_say(my_input)
    print(len(my_input))
