"""Run benchmark on synthetic dataset and save CSV results."""
import argparse, time
import pandas as pd
from algorithms import hungarian, genetic_algorithm, hill_climbing_random_restart

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="data/synthetic_scores.csv")
    parser.add_argument("--repeats", type=int, default=5)
    parser.add_argument("--output", default="results/benchmark_results.csv")
    args = parser.parse_args()
    df = pd.read_csv(args.input)
    scores = df.drop(columns=["Panitia"]).to_numpy(dtype=int)
    n, d = scores.shape
    rows = []
    for name, fn in [
        ("Hungarian", lambda seed: hungarian(scores)),
        ("Genetic Algorithm", lambda seed: genetic_algorithm(scores, seed=seed)),
        ("Hill-Climbing Random Restart", lambda seed: hill_climbing_random_restart(scores, seed=seed))
    ]:
        times, values = [], []
        for seed in range(args.repeats):
            start = time.perf_counter()
            _, value = fn(seed)
            times.append(time.perf_counter() - start)
            values.append(value)
        rows.append({"Panitia": n, "Divisi": d, "Algoritma": name,
                     "Rata_rata_skor": sum(values)/len(values),
                     "Rata_rata_waktu_detik": sum(times)/len(times),
                     "Pengulangan": args.repeats})
    out = pd.DataFrame(rows)
    out.to_csv(args.output, index=False)
    print(out.to_string(index=False))
if __name__ == "__main__":
    main()
