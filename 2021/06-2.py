from collections import Counter

from utils.input import load_input

if __name__ == "__main__":
    population = load_input()
    population = population.strip().replace(",", "")
    population_ctr = Counter(int(x) for x in population)
    for day in range(256):
        population_ctr[9] = population_ctr.get(0, 0)
        population_ctr[7] = population_ctr.get(7, 0) + population_ctr.get(0, 0)
        if 0 in population_ctr:
            del population_ctr[0]
        new_counter = {}
        for age, count in population_ctr.items():
            new_counter[age - 1] = count
        population_ctr = new_counter
        print(f"After {day + 1} days: {sum(population_ctr.values())}")
    print(sum(population_ctr.values()))
