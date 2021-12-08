from utils.input import load_lines

if __name__ == "__main__":
    count = 0
    for line in load_lines():
        inp, results = line.split(" | ")
        for result in results.split():
            if len(result) in [2, 4, 3, 7]:
                count += 1
    print(count)
