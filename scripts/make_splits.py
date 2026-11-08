"""Create a fixed patient-level train/validation/test split for BraTS-PEDs.

Each subject in BraTS-PEDs has one baseline scan, so splitting by subject ID
keeps every patient's images in exactly one split (no leakage). The split is
stratified by data source (CBTN / DFCI-BCH-BWH / DIPG Registry) so each split
has the same mix of institutions and DIPG-registry cases.

Only the official BraTS 2025 "Training" cohort (257 subjects) is used: it is the
only part of the TCIA download released with expert masks. The 91 "Validation"
subjects contain no *-seg.nii.gz files (checked 2026-10-31), so they are never
included in this supervised split.

Usage:
    python scripts/make_splits.py                 # 257 subjects, seed 42
Outputs: splits/train.txt, splits/val.txt, splits/test.txt, splits/split_summary.csv
"""
import argparse
from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split

SEED = 42


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--metadata", default="data/BraTS-PEDs_metadata.tsv")
    ap.add_argument("--outdir", default="splits")
    ap.add_argument("--val-frac", type=float, default=0.15)
    ap.add_argument("--test-frac", type=float, default=0.15)
    ap.add_argument("--seed", type=int, default=SEED)
    args = ap.parse_args()

    df = pd.read_csv(args.metadata, sep="\t", dtype=str).fillna("")
    df.columns = [c.strip() for c in df.columns]
    cohorts = ["Training"]
    df = df[df["BraTS2025_cohort"].isin(cohorts)].copy()
    assert df["BraTS-SubjectID"].is_unique, "duplicate subject IDs"

    ids, strata = df["BraTS-SubjectID"], df["Source"]
    trainval, test = train_test_split(ids, test_size=args.test_frac, stratify=strata,
                                      random_state=args.seed)
    val_share = args.val_frac / (1 - args.test_frac)
    train, val = train_test_split(trainval, test_size=val_share,
                                  stratify=strata.loc[trainval.index], random_state=args.seed)

    out = Path(args.outdir)
    out.mkdir(parents=True, exist_ok=True)
    splits = {"train": train, "val": val, "test": test}
    for name, s in splits.items():
        (out / f"{name}.txt").write_text("\n".join(sorted(s)) + "\n", encoding="utf-8")

    assert not (set(train) & set(val) or set(train) & set(test) or set(val) & set(test))
    df["split"] = ""
    for name, s in splits.items():
        df.loc[s.index, "split"] = name
    summary = pd.crosstab(df["Source"], df["split"]).reindex(columns=list(splits), fill_value=0)
    summary.loc["Total"] = summary.sum()
    summary.to_csv(out / "split_summary.csv")
    print(f"Cohorts used: {', '.join(cohorts)}; seed {args.seed}")
    print(summary.to_string())


if __name__ == "__main__":
    main()
