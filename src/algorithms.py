"""Implementasi pembanding assignment: Hungarian, GA, Hill-Climbing random restart."""
import time
import numpy as np
from scipy.optimize import linear_sum_assignment

def score_assignment(scores, assignment):
    return int(scores[np.arange(len(assignment)), assignment].sum())

def expand_slots(scores):
    n, d = scores.shape
    if n % d:
        raise ValueError("Jumlah panitia harus habis dibagi jumlah divisi.")
    return np.repeat(scores, n // d, axis=1)

def hungarian(scores):
    costs = 100 - expand_slots(scores)
    rows, cols = linear_sum_assignment(costs)
    assignment = cols // (scores.shape[0] // scores.shape[1])
    return assignment, score_assignment(scores, assignment)

def repair_capacity(assignment, n, d, rng):
    cap = n // d
    counts = np.zeros(d, dtype=int)
    repaired = np.full(n, -1, dtype=int)
    for i, div in enumerate(assignment):
        if counts[div] < cap:
            repaired[i] = div
            counts[div] += 1
    remaining = [i for i in range(n) if repaired[i] < 0]
    slots = [div for div in range(d) for _ in range(cap - counts[div])]
    rng.shuffle(slots)
    for i, div in zip(remaining, slots):
        repaired[i] = div
    return repaired

def genetic_algorithm(scores, seed=42, population_size=40, generations=80, mutation_rate=0.08):
    rng = np.random.default_rng(seed)
    n, d = scores.shape
    if n % d:
        raise ValueError("Jumlah panitia harus habis dibagi jumlah divisi.")
    cap = n // d
    slots = np.repeat(np.arange(d), cap)
    def individual():
        x = slots.copy()
        rng.shuffle(x)
        return x
    def fitness(x):
        return score_assignment(scores, x)
    population = [individual() for _ in range(population_size)]
    for _ in range(generations):
        population.sort(key=fitness, reverse=True)
        new_population = population[:2]  # elitism
        while len(new_population) < population_size:
            p1 = population[int(rng.integers(0, max(2, population_size // 2)))]
            p2 = population[int(rng.integers(0, max(2, population_size // 2)))]
            mask = rng.random(n) < 0.5
            child = np.where(mask, p1, p2).astype(int)
            child = repair_capacity(child, n, d, rng)
            if rng.random() < mutation_rate:
                i, j = rng.choice(n, size=2, replace=False)
                child[i], child[j] = child[j], child[i]
            new_population.append(child)
        population = new_population
    best = max(population, key=fitness)
    return best, fitness(best)

def hill_climbing_random_restart(scores, seed=42, restarts=10, max_steps=300):
    rng = np.random.default_rng(seed)
    n, d = scores.shape
    if n % d:
        raise ValueError("Jumlah panitia harus habis dibagi jumlah divisi.")
    slots = np.repeat(np.arange(d), n // d)
    best, best_score = None, -1
    for _ in range(restarts):
        current = slots.copy()
        rng.shuffle(current)
        current_score = score_assignment(scores, current)
        for _ in range(max_steps):
            i, j = rng.choice(n, size=2, replace=False)
            candidate = current.copy()
            candidate[i], candidate[j] = candidate[j], candidate[i]
            candidate_score = score_assignment(scores, candidate)
            if candidate_score > current_score:
                current, current_score = candidate, candidate_score
        if current_score > best_score:
            best, best_score = current.copy(), current_score
    return best, best_score

def benchmark(scores, repeats=5):
    rows = []
    a, score = hungarian(scores)
    rows.append(("Hungarian", score))
    for method in (genetic_algorithm, hill_climbing_random_restart):
        values = [method(scores, seed=seed)[1] for seed in range(repeats)]
        rows.append((method.__name__, float(np.mean(values))))
    return rows
