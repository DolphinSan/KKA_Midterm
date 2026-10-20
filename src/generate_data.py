"""Generate reproducible synthetic committee-to-division compatibility scores."""
import argparse
import numpy as np
import pandas as pd

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--members", type=int, default=30)
    parser.add_argument("--divisions", type=int, default=5)
    parser.add_argument("--seed", type=int, default=20261048)
    parser.add_argument("--output", default="data/synthetic_scores.csv")
    args = parser.parse_args()
    if args.members % args.divisions:
        raise SystemExit("Jumlah panitia harus habis dibagi jumlah divisi pada versi eksperimen ini.")
    rng = np.random.default_rng(args.seed)
    scores = rng.integers(20, 101, size=(args.members, args.divisions))
    df = pd.DataFrame(scores, columns=[f"Divisi_{j+1}" for j in range(args.divisions)])
    df.insert(0, "Panitia", [f"Panitia_{i+1:03d}" for i in range(args.members)])
    df.to_csv(args.output, index=False)
    print(f"Dataset tersimpan: {args.output}; bentuk={scores.shape}; seed={args.seed}")

if __name__ == "__main__":
    main()
