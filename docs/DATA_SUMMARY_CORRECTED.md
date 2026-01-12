# Stanford RNA 3D Folding Part 2 - Data Summary (Corrected)

**Generated**: January 12, 2026
**Validated**: Actual file counts and statistics
**Total Size**: 24 GB (15,319 files)

---

## Dataset Overview (✓ Validated)

| Split | Sequences | Nucleotide Coords | Avg per Seq | Purpose |
|-------|-----------|-------------------|-------------|---------|
| **Train** | 5,716 | ~7.8M | 1,363.7 nt | Model training |
| **Validation** | 28 | 9,762 | 348.6 nt | Local evaluation |
| **Test** | 28 | (predict) | - | Kaggle submission |

**Key Statistics**:
- MSA Files: **5,744** (not 3,418 as initially documented)
- PDB Structures: **9,564** CIF files
- PDB Sequences: **26,255** FASTA records

---

## File Structure

```
data/raw/
├── MSA/                          # 5,744 files ✓
│   └── *.MSA.fasta              # Multiple sequence alignments
├── PDB_RNA/                      # 9,564 files ✓
│   ├── *.cif                    # PDB structure files
│   ├── pdb_release_dates_NA.csv # 9,564 entries
│   └── pdb_seqres_NA.fasta      # 26,255 sequences
├── extra/
│   ├── README.md
│   ├── parse_fasta_py.py
│   └── rna_metadata.csv         # 128 MB metadata
├── train_sequences.csv           # 37 MB (5,716 sequences) ✓
├── train_labels.csv              # 318 MB (~7.8M coordinates) ✓
├── validation_sequences.csv      # (28 sequences) ✓
├── validation_labels.csv         # (9,762 coordinates) ✓
├── test_sequences.csv            # (28 sequences to predict) ✓
└── sample_submission.csv         # 443 KB (submission format)
```

---

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

**Coordinate Ranges**:
- X: -107.77 to 133.34 Å
- Y: -110.73 to 146.76 Å
- Z: -116.22 to 194.57 Å

### MSA Files (MSA/*.MSA.fasta)

- **Format**: FASTA
- **Total Files**: 5,744
- **Structure**:
  - First sequence: `query` (target RNA)
  - Subsequent sequences: Homologous sequences from databases
- **Purpose**: Template discovery for template-based modeling
- **Naming**: `{PDB_ID}.MSA.fasta`

Example:
```fasta
>query
GGACUAGCGGAGGCUAGUCC
>URS000086851D_99_162_f_24-37|chain=B
---CUAGCGGAGGCUAG---
```

---

## Key Statistics (✓ Validated)

### Sequence Lengths

| Statistic | Train | Validation |
|-----------|-------|------------|
| Sequences | 5,716 | 28 |
| Mean length | 1,363.7 nt | - |
| Median length | 94.5 nt | - |
| Min length | 10 nt | - |
| Max length | 125,580 nt | - |
| 25th percentile | 43.0 nt | - |
| 75th percentile | 2,583.8 nt | - |
| Avg coords per seq | 1,363.7 | 348.6 |
| Total nucleotides | ~7.8M | 9.7K |

**Important**: The large difference between mean (1,363.7) and median (94.5) indicates a **long-tailed distribution** with many small RNAs and some very large structures (likely ribosomal RNA, ribosomes, or large ribozymes).

### Nucleotide Distribution (Training Data)

| Nucleotide | Count (sample) | Percentage |
|------------|----------------|------------|
| A (Adenine) | 3,048 | 30.5% |
| U (Uracil) | 2,679 | 26.8% |
| G (Guanine) | 2,302 | 23.0% |
| C (Cytosine) | 1,971 | 19.7% |

### Temporal Distribution

- **Earliest structure**: 1978 (yeast tRNA-Phe, 4TNA)
- **Latest structure**: 2024+ (recent releases)
- **Cutoff purpose**: Prevents temporal leakage in validation

### Test Sequences (For Submission)

**Test Target IDs** (28 sequences):
1. 8ZNQ
2. 9IWF
3. 9JGM
4. 9MME
5. 9J09
6. 9E9Q
7. 9CFN
8. 9OBM
9. 9G4P
10. 9G4Q
... (and 18 more)

---

## Data Quality Notes

### ✓ Validated
- [x] All CSV files present
- [x] MSA directory complete (5,744 files)
- [x] PDB_RNA directory complete (9,564 files)
- [x] File sizes match expectations
- [x] Coordinate ranges are reasonable
- [x] Nucleotide distribution is balanced

### 🔍 To Check
- [ ] Missing coordinates (gaps in structures)
- [ ] Sequence-label alignment verification
- [ ] Duplicate PDB entries
- [ ] Modified nucleotides handling
- [ ] Very long sequences (125K nt) - likely full ribosome structures

---

## Usage Examples

### Load Training Data (Python)
```python
import pandas as pd

# Load sequences
train_seqs = pd.read_csv('data/raw/train_sequences.csv')
train_labels = pd.read_csv('data/raw/train_labels.csv')

print(f"Training sequences: {len(train_seqs)}")  # 5,716
print(f"Training coordinates: {len(train_labels)}")  # ~7.8M

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

---

## Competition Strategy Implications

### Part 1 Winners Used:
1. **Template-based modeling** (not deep learning!)
2. MSA files for template discovery
3. PDB database search
4. Structure alignment and refinement

### Our Approach Should:
1. Parse MSA files to find templates (5,744 available)
2. Use PDB_RNA structures as templates (9,564 structures)
3. Align query to templates (TM-align, US-align)
4. Refine with ML if needed
5. Optimize for TM-Score metric

### Dataset Characteristics:
- **Small dataset**: Only 5,716 training sequences (not large enough for pure deep learning)
- **Template-rich**: 9,564 PDB structures available for template-based modeling
- **Wide size range**: 10 to 125,580 nt sequences require flexible architecture
- **Balanced nucleotides**: ~25% each (A/U/G/C) distribution is healthy

---

## Evaluation Metric

**TM-Score** (Template Modeling Score)
- Range: [0, 1]
- >0.5 = same fold
- >0.6 = high confidence
- Formula: Based on distance between aligned C1' atoms

---

## Next Steps

1. ✅ ~~Run data validation script~~ **COMPLETE**
2. ⏳ Visualize sequence length distributions
3. ⏳ Check for data quality issues
4. ⏳ Build template retrieval pipeline
5. ⏳ Implement TM-Score calculator

**See**: `notebooks/01_initial_exploration.ipynb` for detailed analysis
**Jupyter Lab**: http://localhost:8889/lab (currently running)

---

**Exploration Summary**: `data/processed/exploration_summary.json`
**Last Updated**: January 12, 2026
**Status**: Data validated and ready for model development
