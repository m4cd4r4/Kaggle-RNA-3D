"""
Visualization utilities for RNA structures.
"""
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from typing import Optional


def plot_structure_3d(
    coords: np.ndarray,
    sequence: Optional[str] = None,
    title: str = "RNA 3D Structure",
    save_path: Optional[str] = None
):
    """
    Plot RNA 3D structure.

    Args:
        coords: 3D coordinates (N, 3)
        sequence: Optional RNA sequence for coloring
        title: Plot title
        save_path: Optional path to save figure
    """
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')

    # Color by nucleotide type if sequence provided
    if sequence:
        color_map = {'A': 'red', 'U': 'blue', 'G': 'green', 'C': 'yellow'}
        colors = [color_map.get(n, 'gray') for n in sequence]
    else:
        colors = 'blue'

    # Plot backbone
    ax.plot(coords[:, 0], coords[:, 1], coords[:, 2],
            'gray', linewidth=2, alpha=0.5)

    # Plot nucleotides
    ax.scatter(coords[:, 0], coords[:, 1], coords[:, 2],
               c=colors, s=100, alpha=0.8, edgecolors='black')

    ax.set_xlabel('X (Å)')
    ax.set_ylabel('Y (Å)')
    ax.set_zlabel('Z (Å)')
    ax.set_title(title)

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()


def plot_contact_map(
    contact_map: np.ndarray,
    title: str = "Contact Map",
    save_path: Optional[str] = None
):
    """
    Plot contact map heatmap.

    Args:
        contact_map: Binary contact map (N, N)
        title: Plot title
        save_path: Optional path to save figure
    """
    plt.figure(figsize=(10, 10))
    sns.heatmap(contact_map, cmap='Blues', square=True, cbar_kws={'label': 'Contact'})
    plt.title(title)
    plt.xlabel('Residue Index')
    plt.ylabel('Residue Index')

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()


def plot_distance_matrix(
    dist_matrix: np.ndarray,
    title: str = "Distance Matrix",
    save_path: Optional[str] = None
):
    """
    Plot distance matrix heatmap.

    Args:
        dist_matrix: Distance matrix (N, N)
        title: Plot title
        save_path: Optional path to save figure
    """
    plt.figure(figsize=(10, 10))
    sns.heatmap(dist_matrix, cmap='viridis', square=True,
                cbar_kws={'label': 'Distance (Å)'})
    plt.title(title)
    plt.xlabel('Residue Index')
    plt.ylabel('Residue Index')

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()


def plot_rmsd_over_time(
    rmsd_values: list,
    title: str = "RMSD Over Training",
    save_path: Optional[str] = None
):
    """
    Plot RMSD values over training epochs.

    Args:
        rmsd_values: List of RMSD values per epoch
        title: Plot title
        save_path: Optional path to save figure
    """
    plt.figure(figsize=(12, 6))
    plt.plot(rmsd_values, linewidth=2)
    plt.xlabel('Epoch')
    plt.ylabel('RMSD (Å)')
    plt.title(title)
    plt.grid(True, alpha=0.3)

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()


def plot_sequence_length_distribution(
    lengths: list,
    bins: int = 50,
    title: str = "Sequence Length Distribution",
    save_path: Optional[str] = None
):
    """
    Plot distribution of sequence lengths.

    Args:
        lengths: List of sequence lengths
        bins: Number of histogram bins
        title: Plot title
        save_path: Optional path to save figure
    """
    plt.figure(figsize=(12, 6))
    plt.hist(lengths, bins=bins, edgecolor='black', alpha=0.7)
    plt.xlabel('Sequence Length')
    plt.ylabel('Count')
    plt.title(title)
    plt.axvline(np.mean(lengths), color='red', linestyle='--',
                linewidth=2, label=f'Mean: {np.mean(lengths):.1f}')
    plt.axvline(np.median(lengths), color='green', linestyle='--',
                linewidth=2, label=f'Median: {np.median(lengths):.1f}')
    plt.legend()
    plt.grid(True, alpha=0.3)

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()


def plot_nucleotide_composition(
    composition: dict,
    title: str = "Nucleotide Composition",
    save_path: Optional[str] = None
):
    """
    Plot nucleotide composition bar chart.

    Args:
        composition: Dictionary of nucleotide frequencies
        title: Plot title
        save_path: Optional path to save figure
    """
    nucleotides = list(composition.keys())
    frequencies = list(composition.values())

    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A']

    plt.figure(figsize=(10, 6))
    plt.bar(nucleotides, frequencies, color=colors, edgecolor='black', alpha=0.8)
    plt.xlabel('Nucleotide')
    plt.ylabel('Frequency')
    plt.title(title)
    plt.ylim(0, max(frequencies) * 1.2)
    plt.grid(True, alpha=0.3, axis='y')

    for i, (nuc, freq) in enumerate(zip(nucleotides, frequencies)):
        plt.text(i, freq + 0.01, f'{freq:.3f}', ha='center', va='bottom', fontsize=12)

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()


def plot_training_curves(
    train_losses: list,
    val_losses: list,
    title: str = "Training and Validation Loss",
    save_path: Optional[str] = None
):
    """
    Plot training and validation loss curves.

    Args:
        train_losses: List of training losses
        val_losses: List of validation losses
        title: Plot title
        save_path: Optional path to save figure
    """
    plt.figure(figsize=(12, 6))
    plt.plot(train_losses, label='Training Loss', linewidth=2)
    plt.plot(val_losses, label='Validation Loss', linewidth=2)
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.title(title)
    plt.legend()
    plt.grid(True, alpha=0.3)

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()
