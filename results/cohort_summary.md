# BraTS-PEDs cohort summary

Source file: `BraTS-PEDs_metadata.tsv` (TCIA, BraTS-PEDs Version 1). Subjects: 457 (all IDs unique).

## Subjects by BraTS 2025 cohort and data source

| Source | Training | Validation | Test | Total |
|---|---|---|---|---|
| CBTN | 116 | 0 | 0 | 116 |
| DFCI-BCH-BWH-PEDs-HGG | 61 | 0 | 0 | 61 |
| DIPGr | 80 | 91 | 56 | 227 |
| Duke | 0 | 0 | 26 | 26 |
| Yale | 0 | 0 | 27 | 27 |
| Total | 257 | 91 | 109 | 457 |

## Demographics (training + validation, downloadable subjects)

- Subjects downloadable from TCIA: 348
- Age and sex reported for 116 (33%); all from source(s): CBTN
- Age at imaging: median 8.3 y (IQR 6.0-12.5; range 0.4-25.9), n = 116
- Subjects older than 18 y at imaging: 5
- Sex: Female 64, Male 52

Imaging institution (where reported):

| Organization | n |
|---|---|
| The Children's Hospital of Philadelphia | 75 |
| Children's National Hospital (CNH) | 36 |
| Lurie Children's Hospital | 3 |
| Children's National Medical Center (CNMC) | 1 |
| Dayton Children's Hospital | 1 |

## Scanner information (acquisition metadata records)

Acquisition metadata available for 112 subjects (BraTS-PED-00001-000 to BraTS-PED-00122-000), one row per MRI sequence. A subject's four sequences can come from different scanners, so values are combined across all sequences of each subject. These are metadata records, not a count of physical scanners.

| Scanner Vendor (per subject) | n |
|---|---|
| SIEMENS only | 70 |
| GE Medical Systems only | 34 |
| GE Medical Systems + SIEMENS | 3 |
| missing | 1 |
| Hitachi Medical Corporation only | 1 |
| Philips Medical System only | 1 |
| Toshiba only | 1 |
| Philips Medical System + SIEMENS | 1 |

| Scanner Field strength (T) (per subject) | n |
|---|---|
| 1.5 only | 53 |
| 3 only | 46 |
| 1.5 + 3 | 6 |
| 1.494 only | 5 |
| missing | 1 |
| 1.16 only | 1 |

T2-FLAIR acquisition slice thickness reported for 76 of 112 subjects (1 mm: 1, 3 mm: 33, 4 mm: 26, 5 mm: 16). This is the original acquisition thickness; the released NIfTI images are resampled to 1 mm isotropic voxels.
