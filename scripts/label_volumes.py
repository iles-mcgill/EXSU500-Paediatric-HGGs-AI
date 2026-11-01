"""Summarise tumour subregion volumes in the BraTS-PEDs expert segmentations.

Labels (BraTS-PEDs 2024+): 1 = enhancing tumour (ET), 2 = non-enhancing tumour
(NET), 3 = cystic component (CC), 4 = peritumoral edema (ED). Whole tumour (WT)
is the union of labels 1-4.

Usage:
    python scripts/label_volumes.py --root D:/EXSU500-data/BraTS-PEDs-v1/Training
Outputs:
    results/label_volumes.csv         one row per subject, volumes in cm^3
    results/label_volume_summary.md   cohort-level table for the reports
    figures/label_volumes.png         per-subregion volume distribution
"""
import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import nibabel as nib
import numpy as np
import pandas as pd

LABELS = {1: "ET", 2: "NET", 3: "CC", 4: "ED"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True, help="folder with BraTS-PED-xxxxx-000 subfolders")
    ap.add_argument("--metadata", default="data/BraTS-PEDs_metadata.tsv")
    ap.add_argument("--out", default="results/label_volumes.csv")
    ap.add_argument("--summary", default="results/label_volume_summary.md")
    ap.add_argument("--fig", default="figures/label_volumes.png")
    ap.add_argument("--allow-problems", action="store_true",
                    help="write outputs even if some masks fail the checks")
    args = ap.parse_args()

    rows, problems = [], []
    subject_dirs = sorted(d for d in Path(args.root).iterdir() if d.is_dir())
    for d in subject_dirs:
        seg_path = d / f"{d.name}-seg.nii.gz"
        if not seg_path.exists():
            problems.append(f"{d.name}: no segmentation file")
            continue
        try:
            img = nib.load(str(seg_path))
            raw = np.asarray(img.dataobj)  # read fully: a corrupt gzip fails here
        except Exception as exc:  # noqa: BLE001 - report any unreadable file
            problems.append(f"{d.name}: cannot read mask ({exc})")
            continue
        if raw.ndim != 3:
            problems.append(f"{d.name}: mask is {raw.ndim}-D, expected 3-D")
            continue
        if not np.all(np.isfinite(raw)) or not np.all(np.equal(np.mod(raw, 1), 0)):
            problems.append(f"{d.name}: mask has non-finite or non-integer values")
            continue
        seg = raw.astype(np.int16)
        bad = [int(v) for v in np.unique(seg) if v not in (0, *LABELS)]
        if bad:
            problems.append(f"{d.name}: unexpected label values {bad}")
        # Geometry check against the images when they are present (header only, cheap).
        for seq in ("t1n", "t1c", "t2w", "t2f"):
            ip = d / f"{d.name}-{seq}.nii.gz"
            if ip.exists():
                ih = nib.load(str(ip))
                if ih.shape[:3] != seg.shape or not np.allclose(ih.affine, img.affine, atol=1e-3):
                    problems.append(f"{d.name}: mask geometry differs from {seq}")
        voxel_cm3 = float(np.prod(img.header.get_zooms()[:3])) / 1000.0
        row = {"subject": d.name,
               "shape": "x".join(map(str, seg.shape)),
               "spacing": "x".join(f"{z:g}" for z in img.header.get_zooms()[:3]),
               "spatial_unit": img.header.get_xyzt_units()[0] or "not set"}
        for lab, name in LABELS.items():
            row[name] = (seg == lab).sum() * voxel_cm3
        row["WT"] = (seg > 0).sum() * voxel_cm3
        rows.append(row)

    if problems:
        print("Mask problems found:\n  " + "\n  ".join(problems))
        if not args.allow_problems:
            raise SystemExit("Stopping: fix or review the problems above (or rerun with --allow-problems).")

    df = pd.DataFrame(rows)
    meta = pd.read_csv(args.metadata, sep="\t", dtype=str).fillna("")
    df = df.merge(meta[["BraTS-SubjectID", "Source"]], left_on="subject",
                  right_on="BraTS-SubjectID", how="left").drop(columns="BraTS-SubjectID")
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    df.round(3).to_csv(args.out, index=False)

    names = list(LABELS.values()) + ["WT"]
    lines = ["# Tumour subregion volumes (expert segmentations)", "",
             f"Subjects: {len(df)}. Image shape(s): {', '.join(df['shape'].unique())}; "
             f"voxel spacing: {', '.join(df['spacing'].unique())}. Header spatial units: "
             + ", ".join(f"{k} {v}" for k, v in df['spatial_unit'].value_counts().items())
             + " (volumes assume the published 1 mm grid where units are not set).",
             f"Mask checks (readable, 3-D, integer labels 0-4 only, geometry vs images where present): "
             f"{len(problems)} problem(s){': ' + '; '.join(problems) if problems else ''}.", "",
             "Volumes are reported only among subjects in whom the region is present; "
             "for rare regions the median over all subjects is 0 cm3.", "",
             "| Region | Present, n (%) | Median volume, cm3 (IQR) among present | Present but < 0.1 cm3, n |",
             "|---|---|---|---|"]
    for n in names:
        pres = df[n] > 0
        v = df.loc[pres, n]
        lines.append(f"| {n} | {pres.sum()} ({pres.mean():.1%}) | "
                     f"{v.median():.1f} ({v.quantile(.25):.1f}-{v.quantile(.75):.1f}) | {(v < 0.1).sum()} |")
    lines += ["", "Whole-tumour volume by data source, median cm3 (IQR):", ""]
    for src, g in df.groupby("Source"):
        lines.append(f"- {src} (n = {len(g)}): {g['WT'].median():.1f} "
                     f"({g['WT'].quantile(.25):.1f}-{g['WT'].quantile(.75):.1f})")
    lines += ["", "Subregion present (volume > 0) by data source, n (%):", "",
              "| Source | " + " | ".join(LABELS.values()) + " |",
              "|---|" + "---|" * len(LABELS)]
    for src, g in df.groupby("Source"):
        lines.append(f"| {src} | " + " | ".join(
            f"{(g[n] > 0).sum()} ({(g[n] > 0).mean():.1%})" for n in LABELS.values()) + " |")
    lines += ["", "Notes: very small annotated regions make overlap metrics (Dice) unstable and "
              "warrant targeted review; they are not removed. Data source (e.g. DIPGr) describes "
              "where a case came from, not an individual diagnosis or tumour location."]
    Path(args.summary).write_text("\n".join(lines) + "\n", encoding="utf-8")

    fig, ax = plt.subplots(figsize=(6.5, 3.4))
    data = [df.loc[df[n] > 0, n] for n in names]
    ax.boxplot(data, showfliers=True, flierprops={"markersize": 3})
    ax.set_xticks(range(1, len(names) + 1))
    ax.set_xticklabels([f"{n}\n(n={len(d)})" for n, d in zip(names, data)])
    ax.set_yscale("log")
    ax.set_ylabel("Volume (cm$^3$, log scale)")
    ax.set_title("Subregion volumes where present")
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    Path(args.fig).parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.fig, dpi=300)
    print(Path(args.summary).read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
