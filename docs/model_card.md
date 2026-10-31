# Model card — paediatric high-grade glioma segmentation (draft)

Status: template. Sections are filled in as the models are trained and evaluated (after the midterm).

## Intended use

- **Purpose:** research and teaching (McGill EXSU 500 course project). Automated voxel-wise segmentation of paediatric high-grade glioma subregions on pre-treatment multiparametric brain MRI.
- **Intended users:** researchers and students.
- **Not intended for:** clinical diagnosis, treatment decisions, radiotherapy or surgical planning, or any use on real patients. This is a course prototype, not a medical device.

## Model details

| Model | Type | Inputs | Output |
| --- | --- | --- | --- |
| Baseline | FLAIR intensity threshold | T2-FLAIR | Whole-tumour mask |
| Classical ML | Voxel-wise Random Forest | T1n, T1c, T2w, T2-FLAIR intensities | Subregion labels |
| Deep learning | 3D U-Net (MONAI) | T1n, T1c, T2w, T2-FLAIR | Subregion labels |

Labels: enhancing tumour (ET), non-enhancing tumour (NET), cystic component (CC), peritumoral edema (ED).

## Training data

BraTS-PEDs (TCIA, Version 1, 2025; CC BY 4.0). See [DATA_LICENSE.md](../DATA_LICENSE.md).
Patient-level split: see `splits/`. *To be completed: final cohort size, split sizes, preprocessing steps.*

## Evaluation

*To be completed:* Dice and HD95 per subregion and for whole tumour on the held-out test set, with uncertainty (seeds or bootstrap CIs).

## Limitations and populations not covered

- Retrospective data, mostly from U.S. institutions; enriched for DIPG/DMG.
- Treatment-naive baseline scans only; not validated on post-operative or follow-up imaging.
- Not validated on adult gliomas, low-grade tumours, other paediatric tumour types, or scanners and protocols outside the source institutions.
- Expert reference segmentations still carry inter-observer variability.

## Ethical considerations

Data are de-identified and defaced by TCIA. No images or labels are redistributed in this repository.
