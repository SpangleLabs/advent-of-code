import string

from utils.input import load_input


def increment_password(old_pass: str) -> str:
    letter_dict = {
        char: num
        for num, char in enumerate(string.ascii_lowercase)
    }
    pass_number = [letter_dict[char] for char in old_pass]
    pass_number[-1] += 1
    for num, char in enumerate(pass_number, start=1):
        if pass_number[-num] == 26:
            pass_number[-num - 1] += 1
            pass_number[-num] = 0
    return "".join(string.ascii_lowercase[char_num] for char_num in pass_number)


def is_valid_password(password: str) -> bool:
    straights = [string.ascii_lowercase[x:x+3] for x in range(26 - 2)]
    forbidden = "iol"
    doubles = [char * 2 for char in string.ascii_lowercase]
    if not any(straight in password for straight in straights):
        print("No straight")
        return False
    if any(letter in password for letter in forbidden):
        print("Forbidden letter")
        return False
    check = password
    for double in doubles:
        check = check.replace(double, "-")
    if len(password) - len(check) >= 2:
        return True
    print("Not enough doubles")
    return False


if __name__ == "__main__":
    start_password = load_input()
    next_password = increment_password(start_password)
    while not is_valid_password(next_password):
        next_password = increment_password(next_password)
        print(next_password)
    print(next_password)
