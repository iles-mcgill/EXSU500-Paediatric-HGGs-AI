# Tumour subregion volumes (expert segmentations)

Subjects: 257. Image shape(s): 240x240x155; voxel spacing: 1x1x1. Header spatial units: mm 256, unknown 1 (volumes assume the published 1 mm grid where units are not set).
Mask checks (readable, 3-D, integer labels 0-4 only, geometry vs images where present): 0 problem(s).

Volumes are reported only among subjects in whom the region is present; for rare regions the median over all subjects is 0 cm3.

| Region | Present, n (%) | Median volume, cm3 (IQR) among present | Present but < 0.1 cm3, n |
|---|---|---|---|
| ET | 171 (66.5%) | 4.1 (1.1-10.7) | 9 |
| NET | 256 (99.6%) | 30.7 (16.7-48.1) | 1 |
| CC | 83 (32.3%) | 1.9 (0.4-6.2) | 9 |
| ED | 52 (20.2%) | 15.8 (3.9-36.9) | 2 |
| WT | 257 (100.0%) | 37.0 (22.7-64.4) | 0 |

Whole-tumour volume by data source, median cm3 (IQR):

- CBTN (n = 116): 38.7 (22.9-70.1)
- DFCI-BCH-BWH-PEDs-HGG (n = 61): 58.0 (29.2-119.0)
- DIPGr (n = 80): 32.0 (21.5-42.9)

Subregion present (volume > 0) by data source, n (%):

| Source | ET | NET | CC | ED |
|---|---|---|---|---|
| CBTN | 87 (75.0%) | 116 (100.0%) | 57 (49.1%) | 31 (26.7%) |
| DFCI-BCH-BWH-PEDs-HGG | 35 (57.4%) | 60 (98.4%) | 14 (23.0%) | 14 (23.0%) |
| DIPGr | 49 (61.3%) | 80 (100.0%) | 12 (15.0%) | 7 (8.8%) |

Notes: very small annotated regions make overlap metrics (Dice) unstable and warrant targeted review; they are not removed. Data source (e.g. DIPGr) describes where a case came from, not an individual diagnosis or tumour location.
