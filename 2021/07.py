from utils.input import load_input

if __name__ == "__main__":
    crabs = [int(x) for x in load_input().split(",")]
    leftmost = min(crabs)
    rightmost = max(crabs)
    min_cost = None
    best_target = None
    for target in range(leftmost, rightmost):
        fuel_cost = sum([abs(crab - target) for crab in crabs])
        if min_cost is None or fuel_cost < min_cost:
            min_cost = fuel_cost
            best_target = target
    print(best_target)
    print(min_cost)
