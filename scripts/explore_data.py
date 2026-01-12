#!/usr/bin/env python3
"""Initial data exploration script for Stanford RNA 3D Folding Part 2."""

import numpy as np
import pandas as pd
from pathlib import Path
from Bio import SeqIO
import json

# Paths
DATA_DIR = Path(__file__).parent.parent / "data" / "raw"
PROCESSED_DIR = Path(__file__).parent.parent / "data" / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 70)
print("Stanford RNA 3D Folding Part 2 - Data Exploration")
print("=" * 70)

# 1. Check MSA files
print("\n1. Multiple Sequence Alignment (MSA) Files")
print("-" * 70)
msa_dir = DATA_DIR / "MSA"
if msa_dir.exists():
    msa_files = list(msa_dir.glob("*.fasta"))
    print(f"Total MSA files: {len(msa_files)}")

    # Sample first 5 files
    print("\nSample MSA file analysis:")
    for i, msa_file in enumerate(msa_files[:5], 1):
        sequences = list(SeqIO.parse(msa_file, "fasta"))
        if sequences:
            seq_lengths = [len(seq.seq) for seq in sequences]
            print(f"\n  {i}. {msa_file.name}")
            print(f"     Sequences: {len(sequences)}")
            print(f"     Avg length: {np.mean(seq_lengths):.0f} nucleotides")
            print(f"     Range: {min(seq_lengths)}-{max(seq_lengths)} nt")
            print(f"     Query: {str(sequences[0].seq)[:50]}...")
else:
    print("MSA directory not found")

# 2. Load and analyze training sequences
print("\n\n2. Training Sequences")
print("-" * 70)
train_seq_path = DATA_DIR / "train_sequences.csv"
if train_seq_path.exists():
    train_seqs = pd.read_csv(train_seq_path)
    print(f"Total training sequences: {len(train_seqs):,}")
    print(f"\nColumns: {', '.join(train_seqs.columns.tolist())}")

    # Sequence length distribution
    seq_lengths = train_seqs['sequence'].str.len()
    print(f"\nSequence length statistics:")
    print(f"  Mean: {seq_lengths.mean():.1f} nucleotides")
    print(f"  Median: {seq_lengths.median():.1f} nucleotides")
    print(f"  Min: {seq_lengths.min()} nucleotides")
    print(f"  Max: {seq_lengths.max()} nucleotides")
    print(f"  25th percentile: {seq_lengths.quantile(0.25):.1f} nt")
    print(f"  75th percentile: {seq_lengths.quantile(0.75):.1f} nt")

    # Sample a few sequences
    print(f"\nFirst 3 training examples:")
    for idx, row in train_seqs.head(3).iterrows():
        print(f"\n  Target ID: {row['target_id']}")
        print(f"  Sequence: {row['sequence'][:60]}...")
        print(f"  Length: {len(row['sequence'])} nt")
        if pd.notna(row.get('temporal_cutoff')):
            print(f"  Release date: {row['temporal_cutoff']}")
else:
    print("train_sequences.csv not found")

# 3. Load and analyze training labels
print("\n\n3. Training Labels (3D Coordinates)")
print("-" * 70)
train_labels_path = DATA_DIR / "train_labels.csv"
if train_labels_path.exists():
    # Read first 10000 rows to check structure
    train_labels = pd.read_csv(train_labels_path, nrows=10000)
    print(f"Total labels (sampled 10k): {len(train_labels):,}")
    print(f"\nColumns: {', '.join(train_labels.columns.tolist())}")

    # Check coordinate statistics
    print(f"\nCoordinate statistics (first 10k):")
    print(f"  X range: {train_labels['x_1'].min():.2f} to {train_labels['x_1'].max():.2f} Å")
    print(f"  Y range: {train_labels['y_1'].min():.2f} to {train_labels['y_1'].max():.2f} Å")
    print(f"  Z range: {train_labels['z_1'].min():.2f} to {train_labels['z_1'].max():.2f} Å")

    # Nucleotide distribution
    print(f"\nNucleotide distribution:")
    nuc_counts = train_labels['resname'].value_counts()
    total = len(train_labels)
    for nuc, count in nuc_counts.items():
        print(f"  {nuc}: {count:,} ({count/total*100:.1f}%)")

    # Sample coordinates for one target
    sample_id = train_labels['ID'].iloc[0].rsplit('_', 1)[0]
    sample_coords = train_labels[train_labels['ID'].str.startswith(sample_id)]
    print(f"\nSample target: {sample_id}")
    print(f"  Nucleotides: {len(sample_coords)}")
    print(sample_coords[['ID', 'resname', 'resid', 'x_1', 'y_1', 'z_1']].head())
else:
    print("train_labels.csv not found")

# 4. Load validation data
print("\n\n4. Validation Data")
print("-" * 70)
val_seq_path = DATA_DIR / "validation_sequences.csv"
val_labels_path = DATA_DIR / "validation_labels.csv"
if val_seq_path.exists() and val_labels_path.exists():
    val_seqs = pd.read_csv(val_seq_path)
    val_labels = pd.read_csv(val_labels_path)
    print(f"Validation sequences: {len(val_seqs)}")
    print(f"Validation coordinates: {len(val_labels):,}")
    print(f"Avg coords per sequence: {len(val_labels) / len(val_seqs):.1f}")
else:
    print("Validation files not found")

# 5. Load test data
print("\n\n5. Test Data (For Submission)")
print("-" * 70)
test_seq_path = DATA_DIR / "test_sequences.csv"
if test_seq_path.exists():
    test_seqs = pd.read_csv(test_seq_path)
    print(f"Test sequences to predict: {len(test_seqs)}")
    print(f"\nTest sequence IDs:")
    for idx, target_id in enumerate(test_seqs['target_id'].head(10), 1):
        print(f"  {idx}. {target_id}")
    if len(test_seqs) > 10:
        print(f"  ... and {len(test_seqs) - 10} more")
else:
    print("test_sequences.csv not found")

# 6. PDB RNA files
print("\n\n6. PDB RNA Structure Files")
print("-" * 70)
pdb_dir = DATA_DIR / "PDB_RNA"
if pdb_dir.exists():
    cif_files = list(pdb_dir.glob("*.cif"))
    print(f"Total PDB CIF files: {len(cif_files):,}")

    # Check metadata files
    metadata_file = pdb_dir / "pdb_release_dates_NA.csv"
    seqres_file = pdb_dir / "pdb_seqres_NA.fasta"

    if metadata_file.exists():
        metadata = pd.read_csv(metadata_file)
        print(f"PDB metadata entries: {len(metadata):,}")
        print(f"Metadata columns: {', '.join(metadata.columns.tolist())}")

    if seqres_file.exists():
        seqres = list(SeqIO.parse(seqres_file, "fasta"))
        print(f"PDB sequence records: {len(seqres):,}")
else:
    print("PDB_RNA directory not found")

# 7. Save exploration summary
print("\n\n7. Saving Exploration Summary")
print("-" * 70)

summary = {
    "exploration_date": "2026-01-12",
    "msa_files": len(msa_files) if 'msa_files' in locals() else 0,
    "training_sequences": len(train_seqs) if 'train_seqs' in locals() else 0,
    "validation_sequences": len(val_seqs) if 'val_seqs' in locals() else 0,
    "test_sequences": len(test_seqs) if 'test_seqs' in locals() else 0,
    "pdb_structures": len(cif_files) if 'cif_files' in locals() else 0,
}

if 'train_seqs' in locals():
    summary["sequence_length_stats"] = {
        "mean": float(seq_lengths.mean()),
        "median": float(seq_lengths.median()),
        "min": int(seq_lengths.min()),
        "max": int(seq_lengths.max()),
        "q25": float(seq_lengths.quantile(0.25)),
        "q75": float(seq_lengths.quantile(0.75)),
    }

summary_path = PROCESSED_DIR / "exploration_summary.json"
with open(summary_path, 'w') as f:
    json.dump(summary, f, indent=2)

print(f"Summary saved to: {summary_path}")

print("\n" + "=" * 70)
print("Exploration Complete!")
print("=" * 70)
print("\nNext steps:")
print("  1. Open Jupyter Lab to visualize data: http://localhost:8889/lab")
print("  2. Run notebooks/01_initial_exploration.ipynb for detailed analysis")
print("  3. Start building template retrieval pipeline")
print("  4. Implement TM-Score calculation")
