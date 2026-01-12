# Stanford RNA 3D Folding Part 2 - Data Summary

**Generated**: January 12, 2026
**Total Size**: 24 GB (15,319 files)

---

## Dataset Overview

| Split | Sequences | Nucleotide Coords | Purpose |
|-------|-----------|-------------------|---------|
| **Train** | 204,658 | 7,794,971 | Model training |
| **Validation** | 80 | 9,762 | Local evaluation |
| **Test** | 80 | - | Kaggle submission |

## File Structure

```
data/raw/
├── MSA/                          # 3,418 files
│   └── *.MSA.fasta              # Multiple sequence alignments
├── PDB_RNA/                      # ~11,500+ files
│   ├── *.cif                    # PDB structure files
│   ├── pdb_release_dates_NA.csv
│   └── pdb_seqres_NA.fasta
├── extra/
│   ├── README.md
│   ├── parse_fasta_py.py
│   └── rna_metadata.csv         # 128 MB metadata
├── train_sequences.csv           # 37 MB (204,658 sequences)
├── train_labels.csv              # 318 MB (7.8M coordinates)
├── validation_sequences.csv      # 22 KB (80 sequences)
├── validation_labels.csv         # 8.1 MB (9,762 coordinates)
├── test_sequences.csv            # 22 KB (80 sequences to predict)
└── sample_submission.csv         # 443 KB (submission format)
```

## Data Format Details

### Sequences (train_sequences.csv, validation_sequences.csv, test_sequences.csv)

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `target_id` | str | PDB identifier | `4TNA` |
| `sequence` | str | RNA nucleotide sequence (AUGC) | `GCGGAUUUAGCUC...` |
| `temporal_cutoff` | date | Structure release date | `1978-04-12` |
| `description` | str | Structure description | `REFINEMENT OF...` |
| `stoichiometry` | str | Chain composition | `A:1` |
| `all_sequences` | str | Full FASTA format | `>4TNA_1\|Chain...` |
| `ligand_ids` | str | Bound ligands (if any) | `MG` |
| `ligand_SMILES` | str | Ligand chemical structure | `[Mg+2]` |

### Labels (train_labels.csv, validation_labels.csv)

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `ID` | str | target_id + residue number | `157D_1` |
| `resname` | str | Nucleotide (A/U/G/C) | `G` |
| `resid` | int | Residue position (1-indexed) | `1` |
| `x_1` | float | X coordinate (Ångströms) | `4.843` |
| `y_1` | float | Y coordinate (Ångströms) | `-5.64` |
| `z_1` | float | Z coordinate (Ångströms) | `13.265` |
| `chain` | str | Chain identifier | `A` |
| `copy` | int | Copy number | `1` |

**Note**: Coordinates are C1' atom positions of ribose sugar backbone.

### MSA Files (MSA/*.MSA.fasta)

- Format: FASTA
- Structure:
  - First sequence: `query` (target RNA)
  - Subsequent sequences: Homologous sequences from databases
- Purpose: Template discovery for template-based modeling
- Naming: `{PDB_ID}.MSA.fasta`

Example:
```fasta
>query
GGACUAGCGGAGGCUAGUCC
>URS000086851D_99_162_f_24-37|chain=B
---CUAGCGGAGGCUAG---
```

## Key Statistics

### Sequence Lengths

| Statistic | Train | Validation |
|-----------|-------|------------|
| Sequences | 204,658 | 80 |
| Avg coords per seq | 38.1 | 122.0 |
| Total nucleotides | 7.79M | 9.7K |

### Temporal Distribution

- **Earliest structure**: 1978 (yeast tRNA-Phe)
- **Latest structure**: 2024+ (recent releases)
- **Cutoff purpose**: Prevents temporal leakage in validation

## Data Quality Notes

### ✓ Validated
- [x] All CSV files present
- [x] MSA directory complete (3,418 files)
- [x] PDB_RNA directory complete
- [x] File sizes match expectations

### 🔍 To Check
- [ ] Missing coordinates (gaps in structures)
- [ ] Sequence-label alignment
- [ ] Duplicate PDB entries
- [ ] Modified nucleotides handling

## Usage Examples

### Load Training Data (Python)
```python
import pandas as pd

# Load sequences
train_seqs = pd.read_csv('data/raw/train_sequences.csv')
train_labels = pd.read_csv('data/raw/train_labels.csv')

print(f"Training sequences: {len(train_seqs)}")
print(f"Training coordinates: {len(train_labels)}")

# Get coords for specific target
target = '4TNA'
coords = train_labels[train_labels['ID'].str.startswith(target)]
print(f"\n{target} has {len(coords)} nucleotides")
```

### Load MSA File
```python
from Bio import SeqIO

msa_file = 'data/raw/MSA/1A1T.MSA.fasta'
sequences = list(SeqIO.parse(msa_file, 'fasta'))

query = sequences[0]  # Target sequence
homologs = sequences[1:]  # Template sequences

print(f"Query: {query.seq}")
print(f"Found {len(homologs)} homologous sequences")
```

## Competition Strategy Implications

### Part 1 Winners Used:
1. **Template-based modeling** (not deep learning!)
2. MSA files for template discovery
3. PDB database search
4. Structure alignment and refinement

### Our Approach Should:
1. Parse MSA files to find templates
2. Use PDB_RNA structures as templates
3. Align query to templates (TM-align, US-align)
4. Refine with ML if needed
5. Optimize for TM-Score metric

## Evaluation Metric

**TM-Score** (Template Modeling Score)
- Range: [0, 1]
- >0.5 = same fold
- >0.6 = high confidence
- Formula: Based on distance between aligned C1' atoms

---

**Next Steps**:
1. Run data validation script
2. Visualize sequence length distributions
3. Check for data quality issues
4. Build template retrieval pipeline
5. Implement TM-Score calculator

**See**: `notebooks/01_initial_exploration.ipynb` for detailed analysis
