"""Describe the BraTS-PEDs cohort from the TCIA metadata files.

Inputs (download from the TCIA collection page, keep in data/, never commit):
    data/BraTS-PEDs_metadata.tsv
    data/BraTS-PEDs_Imaging_Info.tsv

Outputs:
    results/cohort_summary.md   tables for the dataset section of the reports
    figures/cohort_overview.png source by cohort + age distribution

Usage:
    python scripts/describe_cohort.py
"""
import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

COHORTS = ["Training", "Validation", "Test"]


def load_metadata(path):
    df = pd.read_csv(path, sep="\t", dtype=str).fillna("")
    df.columns = [c.strip() for c in df.columns]
    df = df.apply(lambda col: col.str.strip())
    df["age_years"] = pd.to_numeric(df["Age at imaging (days)"], errors="coerce") / 365.25
    return df


def md_table(df):
    """Render a DataFrame as a Markdown table (no extra dependency)."""
    cols = [str(c) for c in df.columns]
    lines = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    for _, row in df.iterrows():
        lines.append("| " + " | ".join(str(v) for v in row.values) + " |")
    return "\n".join(lines)


def age_text(ages):
    ages = ages.dropna()
    if ages.empty:
        return "not reported"
    q1, med, q3 = ages.quantile([0.25, 0.5, 0.75])
    return (f"median {med:.1f} y (IQR {q1:.1f}-{q3:.1f}; range {ages.min():.1f}-{ages.max():.1f}), "
            f"n = {len(ages)}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--metadata", default="data/BraTS-PEDs_metadata.tsv")
    ap.add_argument("--imaging", default="data/BraTS-PEDs_Imaging_Info.tsv")
    ap.add_argument("--out", default="results/cohort_summary.md")
    ap.add_argument("--fig", default="figures/cohort_overview.png")
    args = ap.parse_args()

    df = load_metadata(args.metadata)
    assert df["BraTS-SubjectID"].is_unique, "duplicate subject IDs"

    out = ["# BraTS-PEDs cohort summary", "",
           f"Source file: `{Path(args.metadata).name}` (TCIA, BraTS-PEDs Version 1). "
           f"Subjects: {len(df)} (all IDs unique).", ""]

    # 1. Cohort x data source
    ct = pd.crosstab(df["Source"], df["BraTS2025_cohort"]).reindex(columns=COHORTS, fill_value=0)
    ct["Total"] = ct.sum(axis=1)
    ct.loc["Total"] = ct.sum()
    out += ["## Subjects by BraTS 2025 cohort and data source", "",
            md_table(ct.reset_index()), ""]

    # 2. Demographics (only reported for some subjects)
    tv = df[df["BraTS2025_cohort"].isin(["Training", "Validation"])]
    has_demo = tv[tv["Sex_at_birth"] != ""]
    sex = has_demo["Sex_at_birth"].value_counts()
    out += ["## Demographics (training + validation, downloadable subjects)", "",
            f"- Subjects downloadable from TCIA: {len(tv)}",
            f"- Age and sex reported for {len(has_demo)} ({len(has_demo) / len(tv):.0%}); "
            f"all from source(s): {', '.join(sorted(has_demo['Source'].unique()))}",
            f"- Age at imaging: {age_text(tv['age_years'])}",
            f"- Subjects older than 18 y at imaging: {int((tv['age_years'] > 18).sum())}",
            "- Sex: " + ", ".join(f"{k} {v}" for k, v in sex.items()),
            ""]
    org = has_demo["Organization"].value_counts().rename_axis("Organization").reset_index(name="n")
    out += ["Imaging institution (where reported):", "", md_table(org), ""]

    # 3. Scanner information
    img = pd.read_csv(args.imaging, sep="\t", dtype=str).fillna("")
    img.columns = [c.strip() for c in img.columns]
    n_subj = img["BraTS-SubjectID"].nunique()
    out += ["## Scanner information (acquisition metadata records)", "",
            f"Acquisition metadata available for {n_subj} subjects "
            f"({img['BraTS-SubjectID'].min()} to {img['BraTS-SubjectID'].max()}), one row per MRI sequence. "
            "A subject's four sequences can come from different scanners, so values are combined "
            "across all sequences of each subject. These are metadata records, not a count of "
            "physical scanners.", ""]
    for col in ["Scanner Vendor", "Scanner Field strength (T)"]:
        def combo(vals):
            known = sorted({v for v in vals if v and v.lower() != "unavailable"})
            return "missing" if not known else (known[0] + " only" if len(known) == 1 else " + ".join(known))
        vc = (img.groupby("BraTS-SubjectID")[col].apply(combo).value_counts()
              .rename_axis(f"{col} (per subject)").reset_index(name="n"))
        out += [md_table(vc), ""]
    t2f = img[img["MR Imaging sequence"].str.contains("t2f", case=False)]
    st = pd.to_numeric(t2f["SliceThickness (mm)"], errors="coerce")
    st_counts = ", ".join(f"{v:g} mm: {n}" for v, n in st.value_counts().sort_index().items())
    out += [f"T2-FLAIR acquisition slice thickness reported for {st.notna().sum()} of {len(t2f)} subjects "
            f"({st_counts}). This is the original acquisition thickness; the released NIfTI images are "
            "resampled to 1 mm isotropic voxels.", ""]

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text("\n".join(out), encoding="utf-8")

    # Figure: (a) source by cohort, (b) age histogram
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.4))
    ct_plot = pd.crosstab(df["BraTS2025_cohort"], df["Source"]).reindex(COHORTS)
    ct_plot.plot(kind="bar", stacked=True, ax=axes[0], width=0.65)
    axes[0].set_xlabel("")
    axes[0].set_ylabel("Subjects")
    axes[0].set_title("(a) Subjects by cohort and source")
    axes[0].tick_params(axis="x", rotation=0)
    axes[0].legend(fontsize=7, frameon=False)
    axes[1].hist(tv["age_years"].dropna(), bins=range(0, 27), color="#4C72B0", edgecolor="white")
    axes[1].set_xlabel("Age at imaging (years)")
    axes[1].set_ylabel("Subjects")
    axes[1].set_title(f"(b) Age (n = {tv['age_years'].notna().sum()} with age reported)")
    axes[1].yaxis.set_major_locator(plt.MaxNLocator(integer=True))
    for ax in axes:
        ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    Path(args.fig).parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.fig, dpi=300)
    print(f"Wrote {args.out} and {args.fig}")


if __name__ == "__main__":
    main()
