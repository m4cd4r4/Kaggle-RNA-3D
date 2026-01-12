#!/usr/bin/env python3
"""
Comprehensive Validation Test with Ensemble Format

Tests TM-Score evaluation on all 28 validation targets with correct ensemble handling.
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from ensemble_eval import extract_coords_from_ensemble, evaluate_ensemble_vs_ensemble, evaluate_single_vs_ensemble

# Paths
DATA_DIR = Path(__file__).parent.parent / "data" / "raw"

print("=" * 70)
print("Comprehensive Ensemble Validation Test")
print("=" * 70)

# Load validation data
print("\n1. Loading validation data...")
val_labels = pd.read_csv(DATA_DIR / "validation_labels.csv")
targets = val_labels['ID'].str.split('_').str[0].unique()
print(f"   Found {len(targets)} validation targets")

# Test all targets
results = []
np.random.seed(42)

print("\n2. Testing all validation targets...")
print("=" * 70)

for i, target_id in enumerate(targets, 1):
    print(f"\n[{i}/{len(targets)}] {target_id}")
    print("-" * 70)

    # Extract reference ensemble
    ref_coords_list = extract_coords_from_ensemble(val_labels, target_id, n_models=40)
    n_refs = len(ref_coords_list)
    n_atoms = len(ref_coords_list[0])

    print(f"  Sequence length: {n_atoms} nucleotides")
    print(f"  Reference ensemble: {n_refs} structures")

    # Analyze reference ensemble variability
    # Compute TM-Scores between all reference pairs
    ref_scores = []
    for j in range(min(5, n_refs)):  # Sample first 5 for speed
        for k in range(j+1, min(5, n_refs)):
            from tm_score import compute_tm_score
            score = compute_tm_score(ref_coords_list[j], ref_coords_list[k])
            ref_scores.append(score)

    ref_variability = 1.0 - np.mean(ref_scores) if ref_scores else 0.0
    print(f"  Reference variability: {ref_variability:.4f} (1-mean TM-Score)")

    # Create test predictions with varying noise levels
    true_coords = ref_coords_list[0]  # Use first as "ground truth"

    noise_levels = [0.5, 1.0, 2.0, 5.0]
    for noise in noise_levels:
        # Create 5-member ensemble
        pred_coords_list = [
            true_coords + np.random.randn(*true_coords.shape) * noise
            for _ in range(5)
        ]

        # Evaluate with best_of_best method (most lenient)
        eval_results = evaluate_ensemble_vs_ensemble(
            pred_coords_list,
            ref_coords_list,
            method='best_of_best'
        )

        results.append({
            'target': target_id,
            'length': n_atoms,
            'n_refs': n_refs,
            'ref_variability': ref_variability,
            'noise_A': noise,
            'tm_score': eval_results['tm_score'],
            'best_pred_idx': eval_results['best_pred_idx'],
            'best_ref_idx': eval_results['best_ref_idx']
        })

    # Show summary for this target
    target_results = [r for r in results if r['target'] == target_id]
    print(f"\n  TM-Scores at different noise levels:")
    for r in target_results:
        print(f"    {r['noise_A']:.1f}A noise -> TM-Score: {r['tm_score']:.4f}")

# Convert to DataFrame
results_df = pd.DataFrame(results)

print("\n\n" + "=" * 70)
print("Summary Statistics")
print("=" * 70)

# Overall statistics by noise level
print("\nTM-Score vs Noise Level (all targets):")
print("-" * 70)
summary = results_df.groupby('noise_A').agg({
    'tm_score': ['mean', 'std', 'min', 'max']
}).round(4)
print(summary)

# Length vs performance
print("\n\nTM-Score vs Sequence Length (2.0A noise):")
print("-" * 70)
subset_2A = results_df[results_df['noise_A'] == 2.0].copy()
subset_2A['length_bin'] = pd.cut(subset_2A['length'],
                                   bins=[0, 50, 100, 200, 500, 10000],
                                   labels=['<50', '50-100', '100-200', '200-500', '>500'])
length_summary = subset_2A.groupby('length_bin').agg({
    'tm_score': ['count', 'mean', 'std']
}).round(4)
print(length_summary)

# Reference variability analysis
print("\n\nReference Ensemble Variability:")
print("-" * 70)
variability_summary = results_df.groupby('target')[['ref_variability']].first().describe()
print(variability_summary.round(4))

print("\nTargets with HIGH variability (flexible structures):")
high_var = results_df.groupby('target')[['ref_variability', 'length']].first().sort_values('ref_variability', ascending=False).head(5)
print(high_var.round(4))

print("\nTargets with LOW variability (rigid structures):")
low_var = results_df.groupby('target')[['ref_variability', 'length']].first().sort_values('ref_variability').head(5)
print(low_var.round(4))

# Performance requirements
print("\n\n" + "=" * 70)
print("Performance Requirements Analysis")
print("=" * 70)

print("\nTo achieve competitive TM-Scores:")
print("-" * 70)
for target_score in [0.5, 0.6, 0.67]:
    # Find noise level that achieves this score on average
    close_results = results_df[results_df['tm_score'] >= target_score].groupby('noise_A')['tm_score'].count()
    if len(close_results) > 0:
        best_noise = close_results.idxmax()
        pct_achieved = (results_df[(results_df['noise_A'] == best_noise) &
                                    (results_df['tm_score'] >= target_score)].shape[0] /
                        results_df[results_df['noise_A'] == best_noise].shape[0] * 100)
        print(f"  TM-Score > {target_score:.2f}: Need ~{best_noise:.1f}A RMSD ({pct_achieved:.0f}% of targets)")

print("\n\n" + "=" * 70)
print("Key Findings")
print("=" * 70)

mean_0_5A = results_df[results_df['noise_A'] == 0.5]['tm_score'].mean()
mean_5A = results_df[results_df['noise_A'] == 5.0]['tm_score'].mean()

print(f"\n1. TM-Score sensitivity verified on all 28 targets:")
print(f"   - 0.5A RMSD → Mean TM-Score: {mean_0_5A:.4f}")
print(f"   - 5.0A RMSD → Mean TM-Score: {mean_5A:.4f}")

print(f"\n2. Reference ensemble variability:")
print(f"   - Mean: {results_df.groupby('target')['ref_variability'].first().mean():.4f}")
print(f"   - Range: {results_df.groupby('target')['ref_variability'].first().min():.4f} - {results_df.groupby('target')['ref_variability'].first().max():.4f}")

print(f"\n3. Part 1 winner score (0.671) achieved with:")
best_noise_for_winner = results_df[results_df['tm_score'] >= 0.671].groupby('noise_A')['tm_score'].count().idxmax()
print(f"   - Approximately {best_noise_for_winner:.1f}A RMSD accuracy")

print("\n" + "=" * 70)
print("Validation Complete: Ready for Baseline Model [OK]")
print("=" * 70)
print("\nNext: Build nearest-neighbor baseline with 5-member ensemble")
