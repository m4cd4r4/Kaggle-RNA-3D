#!/usr/bin/env python3
"""Generate visualizations for Stanford RNA 3D Folding Part 2 data."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from datetime import datetime

# Configure plotting
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)

# Paths
DATA_DIR = Path(__file__).parent.parent / "data" / "raw"
OUTPUT_DIR = Path(__file__).parent.parent / "visualizations"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 70)
print("Generating Data Visualizations")
print("=" * 70)

# Load training data
print("\n1. Loading training data...")
train_seqs = pd.read_csv(DATA_DIR / "train_sequences.csv")
print(f"   Loaded {len(train_seqs):,} training sequences")

# Sample labels (full file is large)
print("2. Loading training labels (sample)...")
train_labels = pd.read_csv(DATA_DIR / "train_labels.csv", nrows=100000)
print(f"   Loaded {len(train_labels):,} coordinate labels (sample)")

# --- Figure 1: Sequence Length Distribution ---
print("\n3. Creating sequence length distribution plot...")
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('Stanford RNA 3D Folding Part 2 - Data Distribution Analysis',
             fontsize=16, fontweight='bold')

# 3a. Histogram (all data)
seq_lengths = train_seqs['sequence'].str.len()
axes[0, 0].hist(seq_lengths, bins=50, color='#3498db', alpha=0.7, edgecolor='black')
axes[0, 0].set_xlabel('Sequence Length (nucleotides)', fontsize=11)
axes[0, 0].set_ylabel('Frequency', fontsize=11)
axes[0, 0].set_title('Sequence Length Distribution (All Data)', fontsize=12, fontweight='bold')
axes[0, 0].grid(axis='y', alpha=0.3)
axes[0, 0].axvline(seq_lengths.mean(), color='red', linestyle='--',
                   label=f'Mean: {seq_lengths.mean():.0f} nt')
axes[0, 0].axvline(seq_lengths.median(), color='green', linestyle='--',
                   label=f'Median: {seq_lengths.median():.0f} nt')
axes[0, 0].legend()

# 3b. Log scale histogram (to see long tail better)
axes[0, 1].hist(seq_lengths, bins=50, color='#e74c3c', alpha=0.7, edgecolor='black')
axes[0, 1].set_xlabel('Sequence Length (nucleotides)', fontsize=11)
axes[0, 1].set_ylabel('Frequency (log scale)', fontsize=11)
axes[0, 1].set_title('Sequence Length Distribution (Log Scale)', fontsize=12, fontweight='bold')
axes[0, 1].set_yscale('log')
axes[0, 1].grid(axis='y', alpha=0.3)

# 3c. Box plot
axes[1, 0].boxplot([seq_lengths], vert=True, widths=0.5, patch_artist=True,
                    boxprops=dict(facecolor='#2ecc71', alpha=0.7),
                    medianprops=dict(color='red', linewidth=2))
axes[1, 0].set_ylabel('Sequence Length (nucleotides)', fontsize=11)
axes[1, 0].set_title('Sequence Length Box Plot', fontsize=12, fontweight='bold')
axes[1, 0].set_xticklabels(['All Sequences'])
axes[1, 0].grid(axis='y', alpha=0.3)

# Add statistics text
stats_text = f"""
Statistics:
• Total: {len(seq_lengths):,}
• Mean: {seq_lengths.mean():.1f} nt
• Median: {seq_lengths.median():.1f} nt
• Std Dev: {seq_lengths.std():.1f}
• Min: {seq_lengths.min()} nt
• Max: {seq_lengths.max():,} nt
• Q1: {seq_lengths.quantile(0.25):.1f} nt
• Q3: {seq_lengths.quantile(0.75):.1f} nt
"""
axes[1, 0].text(1.5, seq_lengths.max() * 0.5, stats_text,
                fontsize=9, verticalalignment='center',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

# 3d. Nucleotide Distribution
nuc_counts = train_labels['resname'].value_counts()
total = len(train_labels)
colors = ['#e74c3c', '#3498db', '#2ecc71', '#f39c12']
bars = axes[1, 1].bar(nuc_counts.index, nuc_counts.values,
                       color=colors, alpha=0.7, edgecolor='black')
axes[1, 1].set_xlabel('Nucleotide', fontsize=11)
axes[1, 1].set_ylabel('Count', fontsize=11)
axes[1, 1].set_title('Nucleotide Distribution (Sample)', fontsize=12, fontweight='bold')
axes[1, 1].grid(axis='y', alpha=0.3)

# Add percentage labels on bars
for bar, (nuc, count) in zip(bars, nuc_counts.items()):
    height = bar.get_height()
    pct = count / total * 100
    axes[1, 1].text(bar.get_x() + bar.get_width()/2., height,
                    f'{pct:.1f}%\n({count:,})',
                    ha='center', va='bottom', fontsize=10)

plt.tight_layout()
output_path = OUTPUT_DIR / "01_sequence_distribution.png"
plt.savefig(output_path, dpi=150, bbox_inches='tight')
print(f"   Saved: {output_path}")
plt.close()

# --- Figure 2: 3D Coordinate Ranges ---
print("4. Creating 3D coordinate distribution plot...")
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('3D Coordinate Distributions (C1\' Atoms)',
             fontsize=16, fontweight='bold')

# X, Y, Z distributions
for idx, (coord, color, title) in enumerate([
    ('x_1', '#3498db', 'X Coordinate'),
    ('y_1', '#2ecc71', 'Y Coordinate'),
    ('z_1', '#e74c3c', 'Z Coordinate')
]):
    row = idx // 2
    col = idx % 2

    axes[row, col].hist(train_labels[coord], bins=50, color=color,
                        alpha=0.7, edgecolor='black')
    axes[row, col].set_xlabel(f'{title} (Ångströms)', fontsize=11)
    axes[row, col].set_ylabel('Frequency', fontsize=11)
    axes[row, col].set_title(f'{title} Distribution', fontsize=12, fontweight='bold')
    axes[row, col].grid(axis='y', alpha=0.3)

    # Add statistics
    mean_val = train_labels[coord].mean()
    std_val = train_labels[coord].std()
    min_val = train_labels[coord].min()
    max_val = train_labels[coord].max()

    axes[row, col].axvline(mean_val, color='red', linestyle='--',
                           label=f'Mean: {mean_val:.1f} Å')
    axes[row, col].legend()

    # Add text box
    stats_text = f'Range: {min_val:.1f} to {max_val:.1f} Å\nStd: {std_val:.1f} Å'
    axes[row, col].text(0.02, 0.98, stats_text, transform=axes[row, col].transAxes,
                        fontsize=9, verticalalignment='top',
                        bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

# 3D scatter plot (sample)
ax = fig.add_subplot(224, projection='3d')
sample_size = min(1000, len(train_labels))
sample = train_labels.sample(sample_size)
ax.scatter(sample['x_1'], sample['y_1'], sample['z_1'],
           c=sample.index, cmap='viridis', alpha=0.5, s=10)
ax.set_xlabel('X (Å)', fontsize=10)
ax.set_ylabel('Y (Å)', fontsize=10)
ax.set_zlabel('Z (Å)', fontsize=10)
ax.set_title(f'3D Coordinate Space (n={sample_size:,})', fontsize=12, fontweight='bold')

plt.tight_layout()
output_path = OUTPUT_DIR / "02_coordinate_distribution.png"
plt.savefig(output_path, dpi=150, bbox_inches='tight')
print(f"   Saved: {output_path}")
plt.close()

# --- Figure 3: Temporal Distribution ---
print("5. Creating temporal distribution plot...")
train_seqs['temporal_cutoff'] = pd.to_datetime(train_seqs['temporal_cutoff'])
train_seqs['year'] = train_seqs['temporal_cutoff'].dt.year

fig, axes = plt.subplots(1, 2, figsize=(16, 6))
fig.suptitle('Temporal Distribution of RNA Structures',
             fontsize=16, fontweight='bold')

# Year histogram
year_counts = train_seqs['year'].value_counts().sort_index()
axes[0].bar(year_counts.index, year_counts.values, color='#9b59b6', alpha=0.7)
axes[0].set_xlabel('Year', fontsize=11)
axes[0].set_ylabel('Number of Structures', fontsize=11)
axes[0].set_title('RNA Structure Releases by Year', fontsize=12, fontweight='bold')
axes[0].grid(axis='y', alpha=0.3)
axes[0].tick_params(axis='x', rotation=45)

# Cumulative distribution
cumulative = year_counts.cumsum()
axes[1].plot(cumulative.index, cumulative.values, linewidth=2,
             color='#e67e22', marker='o', markersize=3)
axes[1].set_xlabel('Year', fontsize=11)
axes[1].set_ylabel('Cumulative Structures', fontsize=11)
axes[1].set_title('Cumulative RNA Structures Over Time', fontsize=12, fontweight='bold')
axes[1].grid(alpha=0.3)
axes[1].tick_params(axis='x', rotation=45)

# Add milestone annotations
milestones = [
    (1978, '1st tRNA structure'),
    (2000, '1st ribosome structure'),
    (2020, 'COVID-19 pandemic')
]
for year, label in milestones:
    if year in cumulative.index:
        axes[1].annotate(label, xy=(year, cumulative[year]),
                        xytext=(10, 20), textcoords='offset points',
                        bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.5),
                        arrowprops=dict(arrowstyle='->', color='black'),
                        fontsize=8)

plt.tight_layout()
output_path = OUTPUT_DIR / "03_temporal_distribution.png"
plt.savefig(output_path, dpi=150, bbox_inches='tight')
print(f"   Saved: {output_path}")
plt.close()

# --- Summary Report ---
print("\n" + "=" * 70)
print("Visualization Summary")
print("=" * 70)
print(f"\nGenerated 3 visualization files in: {OUTPUT_DIR}")
print("\n1. 01_sequence_distribution.png")
print("   - Sequence length histogram (linear & log scale)")
print("   - Box plot with statistics")
print("   - Nucleotide distribution")
print("\n2. 02_coordinate_distribution.png")
print("   - X, Y, Z coordinate histograms")
print("   - 3D scatter plot of coordinate space")
print("\n3. 03_temporal_distribution.png")
print("   - Structure releases by year")
print("   - Cumulative structure count over time")
print("\n" + "=" * 70)
print("Next: Open Jupyter Lab to explore interactively")
print("URL: http://localhost:8889/lab")
print("=" * 70)
