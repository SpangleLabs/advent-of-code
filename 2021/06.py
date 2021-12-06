from utils.input import load_input

if __name__ == "__main__":
    population = load_input()
    population = population.strip().replace(",", "")
    for day in range(80):
        population = population + "9" * population.count("0")
        population = population.replace("0", "7")
        population = "".join([str(int(x) - 1) for x in population])
        print(population)
    print(len(population))