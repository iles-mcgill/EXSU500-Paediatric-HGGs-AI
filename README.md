# EXSU500-Paediatric-HGGs-AI
Automated 3D Segmentation of Paediatric High-Grade Gliomas from Multiparametric Magnetic Resonance Imaging (MRI), with Potential Applications in Treatment Planning.


**Team Members:** Itzel Priscilla Aguilar-Valdez, Steven Gill, Iles Ousmer, Ansar Tlemussov


**Problem:**
Paediatric central nervous system tumours, particularly high-grade gliomas, have a dismal prognosis, with a five-year survival rate below 20% (TCIA, 2025). These tumours are diffuse and highly infiltrative. Many cases in BraTS-PEDs are diffuse midline gliomas, including diffuse intrinsic pontine gliomas, for which surgical resection is generally not feasible; for selected non-pontine high-grade gliomas, resection remains an option, but precise tumour margins are difficult to identify and injury to healthy functional brain tissue can cause severe neurological deficits.

Accurate delineation of tumor extent and its heterogeneous subregions on magnetic resonance imaging (MRI) is thus crucial for tumor characterization and treatment planning. However, manual three-dimensional tumor segmentation requires expert input, is time-consuming, and is susceptible to inter-observer variability (Odland et al., 2015).

Our project therefore focuses on the automated 3D segmentation of paediatric high-grade gliomas on MRI. Patient-specific tumour delineations could potentially support treatment planning, radiotherapy planning, response assessment and, where appropriate, biopsy or surgical planning. The project evaluates segmentation accuracy only; it does not test any clinical use.


**Task Type:**
3D Image Segmentation. Primary target: whole tumour (the union of ET, NET, CC and ED). Secondary targets: the individual subregions.

Input: Multiparametric brain MRI (T1, contrast-enhanced T1, T2, and T2-FLAIR).  

Output: Voxel-wise whole-tumour segmentation (primary) and, as a secondary analysis, segmentation of the subregions: enhancing tumour (ET), non-enhancing tumour (NET), cystic component (CC) and peritumoral edema (ED).


**Data Set:**

Name: BraTS-PEDs - The Brain Tumor Segmentation in Pediatric Magnetic Resonance Imaging 

Source: The Cancer Imaging Archive (TCIA)

Subjects: 457 in the full cohort (257 training, 91 validation, 109 hidden test); the TCIA image download covers 348 training/validation subjects.

Dataset Size: 32.7 GB (TCIA training/validation image download)


**Link to Data Set:** [TCIA BraTS-PEDs Collection](https://www.cancerimagingarchive.net/collection/brats-peds/)

**Dataset licence and attribution:** BraTS-PEDs (Version 1, 2025), hosted by TCIA, is licensed under [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/). Data DOI: [10.7937/DX5C-TJ86](https://doi.org/10.7937/DX5C-TJ86). See [DATA_LICENSE.md](DATA_LICENSE.md) for the required dataset citation and usage links. This dataset licence does not license this repository's code.


**Repository structure:**

| Folder / file | Contents |
| --- | --- |
| `scripts/` | Cohort description, split and label-volume scripts (preprocessing and evaluation scripts to be added) |
| `notebooks/` | Exploration and modelling notebooks (planned) |
| `splits/` | Patient-level train/validation/test ID lists (fixed seed) |
| `results/` | Cohort and label summaries; later metrics and run settings (no images, no model weights) |
| `figures/` | Figures used in the reports |
| `docs/model_card.md` | Model card: intended use, data, evaluation, limitations |
| `requirements.txt` | Python dependencies (to be pinned) |

MRI data are never committed; download them directly from TCIA (see the link above).

**Reproducing the cohort description and split:** download `BraTS-PEDs_metadata.tsv` and `BraTS-PEDs_Imaging_Info.tsv` from the TCIA page into `data/`, then run

```
python scripts/describe_cohort.py   # results/cohort_summary.md, figures/cohort_overview.png
python scripts/make_splits.py       # splits/train.txt, val.txt, test.txt (seed 42)
```

The split, agreed by the team before any model was trained, is patient-level (one baseline scan per subject) and stratified by data source. It uses the 257 TCIA training subjects, the only ones released with expert masks (the 91 validation subjects have no `seg` files).

`python scripts/label_volumes.py --root <path to BraTS-PEDs-v1/Training>` summarises subregion volumes from the masks (`results/label_volume_summary.md`).
