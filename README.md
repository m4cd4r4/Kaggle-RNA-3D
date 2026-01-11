# Stanford RNA 3D Folding Part 2

[![Kaggle Competition](https://img.shields.io/badge/Kaggle-Competition-20BEFF?logo=kaggle)](https://www.kaggle.com/competitions/stanford-rna-3d-folding-2)
[![Next.js](https://img.shields.io/badge/Next.js-15-black?logo=next.js)](https://nextjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5-blue?logo=typescript)](https://www.typescriptlang.org/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-EE4C2C?logo=pytorch)](https://pytorch.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Kaggle Competition**: [stanford-rna-3d-folding-2](https://www.kaggle.com/competitions/stanford-rna-3d-folding-2)

> 🧬 A complete RNA 3D structure prediction dashboard with **reusable design system**, interactive visualizations, and production-ready Python pipeline. Built for the \$75,000 Stanford Kaggle competition.

## 🌟 Features

### 🎨 Reusable Design System
- **26 UI components** (Cards, Buttons, Badges, Progress, Tables, Inputs)
- **400+ design tokens** (colors, gradients, layouts, effects)
- **Glassmorphism UI** with Kaggle-inspired aesthetics
- **100% reusable** for any Kaggle competition
- Fully documented ([DESIGN_SYSTEM.md](web/DESIGN_SYSTEM.md))

### 📊 Interactive Dashboard
- **Homepage**: Competition stats, Part 1 winners analysis, approach comparison
- **3D Visualizer**: RNA structure viewer (2D linear + 3D helix)
- **Metrics Dashboard**: Training progress, comparison charts (Recharts)
- **Experiment Tracker**: Sortable data tables, hyperparameters, status tracking

### 🐍 Python Pipeline
- **Metrics**: TM-score, RMSD, GDT-TS, lDDT implementations
- **Dataset**: PyTorch Dataset with FASTA parsing
- **Features**: One-hot encoding, GC content, positional encoding
- **Visualization**: 3D structure plots, contact maps
- **Training**: Experiment tracking, checkpointing


## Competition Overview

- **Goal**: Predict the 3D structure of RNA molecules from their sequences
- **Prize Pool**: $75,000
- **Dataset Size**: 23.4 GB (competition data)
- **Entry Deadline**: March 18, 2026
- **Hosts**: Stanford Medicine + HHMI Janelia
- **Challenge**: "Solve RNA structure prediction - one of biology's remaining grand challenges"

## Background & Motivation

Understanding RNA three-dimensional structure is essential for advancing research in:
- Medicine and drug discovery
- Molecular biology
- Synthetic biology design
- RNA-targeting therapeutics

The structural flexibility of RNA leads to scarcity of experimentally determined data, making computational prediction critical but challenging.

## Part 1 Competition Insights (Key Learnings)

### Competition Results
- **1,700+ teams** participated
- **43 previously unreleased structures** as test set
- **Top 3 winners**: "john", "odat", and team "Eigen"
- **Performance**: Mean TM-align scores of **0.671**, **0.653**, and **0.615** on Public leaderboard

### Winning Approaches

#### 🏆 Template-Based Modeling (Surprise Winner!)
The most unexpected finding: **the top strategy used template-based modeling WITHOUT deep learning**.

Key insights:
- Template discovery pipeline outperformed deep learning approaches
- Winners achieved scores within statistical error of CASP16 competition winners
- **All three top teams significantly outperformed AlphaFold 3**
- Post-competition, the organizers developed **RNAPro** by integrating Kaggle strategies

#### Deep Learning Approaches (Also Competitive)
Teams used diverse strategies including:
- **RNA foundation models**: Aido.RNA, RNet
- **Language model-based methods**: RhoFold+
- **Multi-modal approaches**: Combining sequence, structure, and MSA features

### Key Takeaway
> "Template-based modeling shows growing importance in RNA structure prediction"

## State-of-the-Art Methods (2024)

### 1. RhoFold+ (Leading Deep Learning Method)
- **Type**: RNA language model-based deep learning
- **Training**: Pretrained on ~23.7 million RNA sequences
- **Performance**: Superior on RNA-Puzzles and CASP15
- **Advantage**: Fully automated end-to-end pipeline

### 2. AlphaFold 3
- **Publisher**: DeepMind (Nature, 2024)
- **Capability**: Biomolecular interactions including RNA
- **Limitation**: Comparable to ML methods, challenges with ligand binding

### 3. RoseTTAFoldNA
- **Extension of**: RoseTTAFold (protein structure prediction)
- **Specialty**: Protein-DNA and protein-RNA complexes
- **Output**: 3D structures with confidence estimates

### 4. Other Notable Methods
- DRfold, DeepFoldRNA, trRosettaRNA
- Template-based methods (validated by Part 1 winners)

## Evaluation Metrics

### TM-score (Template Modeling score)
- Range: [0, 1] (1 = identical structures)
- Scale-independent structural similarity measure
- **Primary metric** for Part 1 competition

### Other Important Metrics
- **RMSD**: Root Mean Square Deviation
- **GDT-TS**: Global Distance Test - Total Score
- **lDDT**: Local Distance Difference Test
- **Pairwise Distance Accuracy**: Correctly predicted distances

## Project Structure

```
stanford-rna-3d-folding-2/
├── data/
│   ├── raw/              # Original competition data (23.4 GB)
│   ├── processed/        # Cleaned/transformed data
│   └── external/         # External datasets (PDB, RNA-Puzzles)
├── notebooks/
│   ├── 01-data-exploration.ipynb
│   └── 02-baseline-model.ipynb
├── src/
│   ├── data/
│   │   └── rna_dataset.py            # PyTorch Dataset classes
│   ├── models/
│   │   └── metrics.py                # TM-score, RMSD, GDT-TS, lDDT
│   ├── features/
│   │   └── rna_features.py           # Feature extraction
│   └── utils/
│       └── visualization.py          # 3D plots, contact maps
├── submissions/          # Competition submissions
├── configs/
│   └── default.yaml      # Experiment settings
├── models/               # Saved checkpoints
└── requirements.txt
```

## Setup

### 1. Install Dependencies

```bash
conda create -n rna3d python=3.11
conda activate rna3d
pip install -r requirements.txt
```

### 2. Download Competition Data

Data is automatically downloading in background (currently at 36% - 8.5GB/23.4GB).

Once complete, extract:
```bash
cd data/raw
unzip stanford-rna-3d-folding-2.zip
```

## Quick Start

### Explore Data
```bash
jupyter notebook notebooks/01-data-exploration.ipynb
```

### Train Baseline Model
```bash
jupyter notebook notebooks/02-baseline-model.ipynb
```

### Custom Training
```python
from src.data.rna_dataset import RNADataset
from src.models.metrics import StructureMetrics

# Create dataset
dataset = RNADataset(sequences=sequences)

# Evaluate predictions
metrics = StructureMetrics()
results = metrics.compute_all(pred_coords, true_coords)
print(f"TM-score: {results['tm_score']:.3f}")
```

## Utility Files Created

✅ **Data Processing** - `src/data/rna_dataset.py`
- PyTorch Dataset, FASTA parsing, feature computation

✅ **Evaluation** - `src/models/metrics.py`
- TM-score, RMSD, GDT-TS, lDDT, clash detection

✅ **Features** - `src/features/rna_features.py`
- One-hot encoding, GC content, secondary structure

✅ **Visualization** - `src/utils/visualization.py`
- 3D structure plots, contact maps, distance matrices

## Strategy & Approach

### Phase 1: Baseline (Weeks 1-2)
- [ ] Complete data exploration
- [ ] Implement LSTM/Transformer baseline
- [ ] Establish evaluation pipeline with TM-score

### Phase 2: Advanced Models (Weeks 3-6)
- [ ] Implement template-based search (Part 1 winner approach)
- [ ] Experiment with RNA language models
- [ ] Ensemble multiple approaches

### Phase 3: Optimization (Weeks 7-10)
- [ ] Hyperparameter tuning
- [ ] Model ensembling
- [ ] Final submission

## Key Resources

### Competition
- [Competition Page](https://www.kaggle.com/competitions/stanford-rna-3d-folding-2)
- [Part 1 Discussion](https://www.kaggle.com/competitions/stanford-rna-3d-folding/discussion)

### Research Papers
- [Template-based RNA prediction (bioRxiv 2025)](https://www.biorxiv.org/content/10.64898/2025.12.30.696949v1.full)
- [RhoFold+ (Nature Methods 2024)](https://www.nature.com/articles/s41592-024-02487-0)
- [AlphaFold 3 (Nature 2024)](https://www.nature.com/articles/s41586-024-07487-w)
- [RoseTTAFoldNA (Nature Methods 2023)](https://www.nature.com/articles/s41592-023-02086-5)

### External Resources
- [DAS Lab - Stanford](https://daslab.stanford.edu/)
- [RNA-Puzzles](http://rnapuzzles.org/)
- [CASP RNA](https://predictioncenter.org/)

---

**Sources:**
- [Stanford RNA 3D Folding Part 2 - Kaggle](https://www.kaggle.com/competitions/stanford-rna-3d-folding-2)
- [Template-based RNA prediction](https://www.biorxiv.org/content/10.64898/2025.12.30.696949v1.full)
- [RhoFold+ (Nature Methods)](https://www.nature.com/articles/s41592-024-02487-0)
- [DAS Lab Stanford](https://daslab.stanford.edu/news)

## 🤝 Contributing

Contributions welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

## 🌟 Star History

If you find this useful, please ⭐ star this repository!

## 🙏 Acknowledgments

- Stanford Medicine & HHMI Janelia for hosting the competition
- Part 1 winners ("john", "odat", "Eigen") for inspiring the template-based approach
- The Kaggle community for discussions and insights

---

**Built with** 🧬 for RNA 3D structure prediction | **Designed for** 🏆 Kaggle competitions
