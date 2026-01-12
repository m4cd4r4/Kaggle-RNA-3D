#!/usr/bin/env python3
"""
Investigate why 9CFN has a failing identity test.
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from tm_score import load_coords_from_labels

# Paths
DATA_DIR = Path(__file__).parent.parent / "data" / "raw"

print("=" * 70)
print("Investigating 9CFN Data Quality Issue")
print("=" * 70)

# Load validation data
val_labels = pd.read_csv(DATA_DIR / "validation_labels.csv")

# Focus on 9CFN
target_id = "9CFN"
mask = val_labels['ID'].str.startswith(target_id + '_')
target_data = val_labels[mask].copy()

print(f"\nTarget: {target_id}")
print(f"Total coordinates: {len(target_data)}")

# Check for issues
print("\nData inspection:")
print("-" * 70)
print(target_data.head(20))

# Check for duplicates
print("\nChecking for duplicate residues...")
duplicate_resids = target_data[target_data.duplicated(subset='resid', keep=False)]
if len(duplicate_resids) > 0:
    print(f"  [!] Found {len(duplicate_resids)} duplicate residue IDs!")
    print("\nDuplicate entries:")
    print(duplicate_resids.sort_values('resid'))
else:
    print("  [OK] No duplicate residue IDs")

# Check chains
print(f"\nChains present: {target_data['chain'].unique()}")
print(f"Chain counts:")
print(target_data['chain'].value_counts())

# Check copies
print(f"\nCopies present: {target_data['copy'].unique()}")
print(f"Copy counts:")
print(target_data['copy'].value_counts())

# The issue: Multiple copies!
print("\n" + "=" * 70)
print("ROOT CAUSE IDENTIFIED")
print("=" * 70)
print("\nThe validation data contains MULTIPLE COPIES of chains!")
print("This is biological reality - multimers, dimers, etc.")
print("\nWe need to handle multi-copy structures correctly:")
print("  Option 1: Use only copy=1")
print("  Option 2: Handle all copies (average or best match)")
print("  Option 3: Predict all copies")

# Test both approaches
print("\n\nTesting solutions:")
print("-" * 70)

# Solution 1: Use only copy=1
print("\n1. Using only copy=1:")
target_copy1 = target_data[target_data['copy'] == 1].sort_values('resid')
print(f"   Coordinates: {len(target_copy1)}")
coords_copy1 = target_copy1[['x_1', 'y_1', 'z_1']].values
print(f"   Unique residues: {target_copy1['resid'].nunique()}")

# Check if copy=1 has duplicates
dupes_copy1 = target_copy1[target_copy1.duplicated(subset='resid', keep=False)]
if len(dupes_copy1) > 0:
    print(f"   [!] Copy=1 still has duplicates: {len(dupes_copy1)}")
else:
    print(f"   [OK] Copy=1 has no duplicates")

# Solution 2: Handle all copies
print("\n2. Handling all copies:")
for copy_num in sorted(target_data['copy'].unique()):
    copy_data = target_data[target_data['copy'] == copy_num].sort_values('resid')
    print(f"   Copy {copy_num}: {len(copy_data)} coordinates")

print("\n" + "=" * 70)
print("SOLUTION")
print("=" * 70)
print("\nUpdate load_coords_from_labels() to handle multi-copy structures:")
print("  - Default: Use copy=1 only")
print("  - Optional: Return all copies as dict")
