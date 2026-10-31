# EXSU500-Paediatric-HGGs-AI
Automated 3D Multi-Class Image Segmentation of Paediatric High-Grade Gliomas from Multiparametric Magnetic Resonance Imaging (MRI) for Neurosurgical Navigation.


**Team Members:** Itzel Priscilla Aguilar-Valdez, Steven Gill, Iles Ousmer, Ansar Tlemussov


**Problem:**
Paediatric central nervous system tumours, particularly high-grade gliomas, have a dismal prognosis, with a five-year survival rate historically sitting below 20% (TCIA, 2025). The surgical treatment of these tumours is exceptionally challenging because high-grade gliomas are diffuse and highly infiltrative. This makes it incredibly difficult to identify precise tumour margins during surgery, where the accidental resection of healthy neural networks can lead to severe neurological deficits or death.

Accurate delineation of tumor extent and its heterogeneous subregions on magnetic resonance imaging (MRI) is thus crucial for tumor characterization and treatment planning. However, manual three-dimensional tumor segmentation requires expert input, is time-consuming, and is susceptible to inter-observer variability (Odland et al., 2015).

Our project therefore focuses on the automated 3D image segmentation of paediatric high-grade gliomas to generate precise, patient-specific anatomical maps that could potentially support preoperative neurosurgical planning and intraoperative image-guided navigation.


**Task Type:**
Multi-class 3D Image Segmentation

Input: Multiparametric brain MRI (T1, contrast-enhanced T1, T2, and T2-FLAIR).  

Output: Voxel-wise segmentation of pediatric high-grade glioma subregions, which include enhancing tumor (ET), non-enhancing tumor (NET), cystic component (CC), and peritumoral edema (ED)


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
| `scripts/` | Data download, preprocessing and evaluation scripts |
| `notebooks/` | Exploration and modelling notebooks (EDA, splits, models) |
| `splits/` | Patient-level train/validation/test ID lists (fixed seed) |
| `results/` | Metrics and run settings (no images, no model weights) |
| `figures/` | Figures used in the reports |
| `docs/model_card.md` | Model card: intended use, data, evaluation, limitations |
| `requirements.txt` | Python dependencies (to be pinned) |

MRI data are never committed; download them directly from TCIA (see the link above).
