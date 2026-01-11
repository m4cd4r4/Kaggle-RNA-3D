"""
Evaluation metrics for RNA 3D structure prediction.
"""
import torch
import numpy as np
from typing import Tuple, Optional


def rmsd(pred_coords: torch.Tensor, true_coords: torch.Tensor) -> float:
    """
    Calculate Root Mean Square Deviation between predicted and true coordinates.

    Args:
        pred_coords: Predicted 3D coordinates (N, 3)
        true_coords: True 3D coordinates (N, 3)

    Returns:
        RMSD value
    """
    diff = pred_coords - true_coords
    squared_diff = torch.sum(diff ** 2, dim=-1)
    mean_squared_diff = torch.mean(squared_diff)
    return torch.sqrt(mean_squared_diff).item()


def tm_score(pred_coords: torch.Tensor, true_coords: torch.Tensor) -> float:
    """
    Calculate TM-score (Template Modeling score) for structure alignment.

    TM-score is a scale-independent metric that measures structural similarity.
    Range: [0, 1], where 1 indicates identical structures.

    Args:
        pred_coords: Predicted 3D coordinates (N, 3)
        true_coords: True 3D coordinates (N, 3)

    Returns:
        TM-score value
    """
    n = len(pred_coords)

    # Normalize d0 based on sequence length
    d0 = 1.24 * (n - 15) ** (1/3) - 1.8 if n > 15 else 0.5

    # Calculate distances
    distances = torch.sqrt(torch.sum((pred_coords - true_coords) ** 2, dim=-1))

    # Calculate TM-score
    tm = torch.sum(1 / (1 + (distances / d0) ** 2)) / n

    return tm.item()


def gdt_ts(pred_coords: torch.Tensor, true_coords: torch.Tensor) -> float:
    """
    Calculate GDT-TS (Global Distance Test - Total Score).

    GDT-TS measures the percentage of residues within distance cutoffs.

    Args:
        pred_coords: Predicted 3D coordinates (N, 3)
        true_coords: True 3D coordinates (N, 3)

    Returns:
        GDT-TS score (0-100)
    """
    distances = torch.sqrt(torch.sum((pred_coords - true_coords) ** 2, dim=-1))
    n = len(distances)

    # Calculate percentage under each cutoff
    cutoffs = [1.0, 2.0, 4.0, 8.0]
    scores = []

    for cutoff in cutoffs:
        within_cutoff = torch.sum(distances < cutoff).item()
        scores.append(within_cutoff / n * 100)

    # GDT-TS is the average of the four scores
    return np.mean(scores)


def lddt(
    pred_coords: torch.Tensor,
    true_coords: torch.Tensor,
    cutoff: float = 15.0
) -> float:
    """
    Calculate lDDT (local Distance Difference Test).

    lDDT measures local distance agreement within a cutoff radius.

    Args:
        pred_coords: Predicted 3D coordinates (N, 3)
        true_coords: True 3D coordinates (N, 3)
        cutoff: Distance cutoff for considering residue pairs

    Returns:
        lDDT score (0-1)
    """
    n = len(pred_coords)

    # Calculate pairwise distances
    true_dist = torch.cdist(true_coords, true_coords)
    pred_dist = torch.cdist(pred_coords, pred_coords)

    # Mask for pairs within cutoff in true structure
    mask = (true_dist < cutoff) & (true_dist > 0)

    if mask.sum() == 0:
        return 0.0

    # Calculate distance differences
    dist_diff = torch.abs(true_dist[mask] - pred_dist[mask])

    # Count preserved distances at different thresholds
    thresholds = [0.5, 1.0, 2.0, 4.0]
    preserved = []

    for threshold in thresholds:
        preserved.append(torch.sum(dist_diff < threshold).item())

    # lDDT is the mean fraction of preserved distances
    total_pairs = mask.sum().item()
    lddt_score = np.mean([p / total_pairs for p in preserved])

    return lddt_score


def pairwise_distance_accuracy(
    pred_coords: torch.Tensor,
    true_coords: torch.Tensor,
    threshold: float = 2.0
) -> float:
    """
    Calculate percentage of pairwise distances within threshold.

    Args:
        pred_coords: Predicted 3D coordinates (N, 3)
        true_coords: True 3D coordinates (N, 3)
        threshold: Distance threshold in Angstroms

    Returns:
        Accuracy percentage (0-100)
    """
    # Calculate all pairwise distances
    true_dist = torch.cdist(true_coords, true_coords)
    pred_dist = torch.cdist(pred_coords, pred_coords)

    # Calculate differences
    dist_diff = torch.abs(true_dist - pred_dist)

    # Mask out diagonal (self-distances)
    n = len(pred_coords)
    mask = ~torch.eye(n, dtype=torch.bool)

    # Calculate accuracy
    within_threshold = torch.sum(dist_diff[mask] < threshold).item()
    total_pairs = mask.sum().item()

    return (within_threshold / total_pairs) * 100


def clash_score(coords: torch.Tensor, threshold: float = 2.0) -> int:
    """
    Calculate number of steric clashes in predicted structure.

    Clashes occur when atoms are too close together.

    Args:
        coords: 3D coordinates (N, 3)
        threshold: Minimum allowed distance in Angstroms

    Returns:
        Number of clashes
    """
    # Calculate pairwise distances
    distances = torch.cdist(coords, coords)

    # Mask out diagonal and upper triangle
    n = len(coords)
    mask = torch.tril(torch.ones(n, n, dtype=torch.bool), diagonal=-1)

    # Count pairs below threshold
    clashes = torch.sum((distances[mask] < threshold) & (distances[mask] > 0)).item()

    return clashes


class StructureMetrics:
    """Container for computing multiple structure quality metrics."""

    def __init__(self):
        self.metrics = {}

    def compute_all(
        self,
        pred_coords: torch.Tensor,
        true_coords: Optional[torch.Tensor] = None
    ) -> dict:
        """
        Compute all available metrics.

        Args:
            pred_coords: Predicted 3D coordinates
            true_coords: True 3D coordinates (optional)

        Returns:
            Dictionary of metric names and values
        """
        results = {}

        # Structure quality metrics (no ground truth needed)
        results['clash_score'] = clash_score(pred_coords)

        # Comparison metrics (require ground truth)
        if true_coords is not None:
            results['rmsd'] = rmsd(pred_coords, true_coords)
            results['tm_score'] = tm_score(pred_coords, true_coords)
            results['gdt_ts'] = gdt_ts(pred_coords, true_coords)
            results['lddt'] = lddt(pred_coords, true_coords)
            results['pairwise_accuracy'] = pairwise_distance_accuracy(
                pred_coords, true_coords
            )

        return results
