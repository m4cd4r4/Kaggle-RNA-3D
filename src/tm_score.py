#!/usr/bin/env python3
"""
TM-Score Implementation for RNA 3D Structure Comparison

TM-Score (Template Modeling Score) is the evaluation metric for this competition.
Range: [0, 1], where:
- 0.0-0.3: Random structural similarity
- 0.3-0.5: Topology may be similar
- >0.5: Same fold (significant)
- >0.6: High confidence in fold similarity

Reference: Zhang & Skolnick (2004) "Scoring function for automated
assessment of protein structure template quality"
"""

import numpy as np
from typing import Tuple, Optional
from scipy.spatial.transform import Rotation
from scipy.optimize import linear_sum_assignment


def kabsch_algorithm(coords_pred: np.ndarray, coords_true: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Find optimal rotation and translation to align coords_pred to coords_true.

    Uses the Kabsch algorithm for optimal superposition.

    Args:
        coords_pred: Predicted coordinates (N, 3)
        coords_true: True coordinates (N, 3)

    Returns:
        rotation: Optimal rotation matrix (3, 3)
        translation: Optimal translation vector (3,)
        coords_aligned: Aligned predicted coordinates (N, 3)
    """
    assert coords_pred.shape == coords_true.shape, "Coordinate arrays must have same shape"
    assert coords_pred.shape[1] == 3, "Coordinates must be 3D"

    # Center both structures at origin
    centroid_pred = coords_pred.mean(axis=0)
    centroid_true = coords_true.mean(axis=0)

    coords_pred_centered = coords_pred - centroid_pred
    coords_true_centered = coords_true - centroid_true

    # Compute covariance matrix
    H = coords_pred_centered.T @ coords_true_centered

    # Singular Value Decomposition
    U, S, Vt = np.linalg.svd(H)

    # Compute optimal rotation
    rotation = Vt.T @ U.T

    # Ensure right-handed coordinate system (det(R) = 1)
    if np.linalg.det(rotation) < 0:
        Vt[-1, :] *= -1
        rotation = Vt.T @ U.T

    # Apply rotation and translation
    coords_aligned = coords_pred_centered @ rotation.T + centroid_true

    # Translation is from centroid to centroid after rotation
    translation = centroid_true - centroid_pred @ rotation.T

    return rotation, translation, coords_aligned


def compute_tm_score(
    coords_pred: np.ndarray,
    coords_true: np.ndarray,
    normalize_by: str = 'target',
    return_details: bool = False
) -> float:
    """
    Compute TM-Score between predicted and true coordinates.

    TM-Score formula:
    TM-score = (1/L_norm) * Σ(1 / (1 + (d_i/d0)^2))

    Where:
    - L_norm = normalization length (target length or average)
    - d_i = distance between aligned atoms i
    - d0 = 1.24 * (L_norm - 15)^(1/3) - 1.8 (for L > 15)

    Args:
        coords_pred: Predicted 3D coordinates (N, 3) in Ångströms
        coords_true: True 3D coordinates (N, 3) in Ångströms
        normalize_by: How to compute L_norm ('target', 'pred', or 'average')
        return_details: If True, return dict with detailed metrics

    Returns:
        tm_score: TM-Score value [0, 1]
        or dict with tm_score, rmsd, aligned_coords if return_details=True
    """
    assert coords_pred.shape == coords_true.shape, \
        f"Shape mismatch: pred {coords_pred.shape} vs true {coords_true.shape}"

    N = len(coords_pred)
    assert N > 0, "Cannot compute TM-Score for empty structures"

    # Determine normalization length
    if normalize_by == 'target':
        L_norm = len(coords_true)
    elif normalize_by == 'pred':
        L_norm = len(coords_pred)
    elif normalize_by == 'average':
        L_norm = (len(coords_pred) + len(coords_true)) / 2
    else:
        raise ValueError(f"Invalid normalize_by: {normalize_by}")

    # Compute d0 (scale factor)
    if L_norm > 15:
        d0 = 1.24 * np.power(L_norm - 15, 1.0/3.0) - 1.8
    else:
        d0 = 0.5  # For very short sequences

    # Optimal superposition using Kabsch algorithm
    rotation, translation, coords_aligned = kabsch_algorithm(coords_pred, coords_true)

    # Compute distances after alignment
    distances = np.linalg.norm(coords_aligned - coords_true, axis=1)

    # Compute TM-Score
    tm_score_sum = np.sum(1.0 / (1.0 + (distances / d0) ** 2))
    tm_score = tm_score_sum / L_norm

    if return_details:
        rmsd = np.sqrt(np.mean(distances ** 2))
        return {
            'tm_score': float(tm_score),
            'rmsd': float(rmsd),
            'd0': float(d0),
            'L_norm': int(L_norm),
            'mean_distance': float(np.mean(distances)),
            'max_distance': float(np.max(distances)),
            'min_distance': float(np.min(distances)),
            'rotation': rotation,
            'translation': translation,
            'coords_aligned': coords_aligned,
            'distances': distances
        }

    return float(tm_score)


def compute_tm_score_multiple_chains(
    coords_pred_dict: dict,
    coords_true_dict: dict,
    normalize_by: str = 'target'
) -> float:
    """
    Compute TM-Score for structures with multiple chains.

    Handles multi-chain RNA structures by:
    1. Finding optimal chain assignment (Hungarian algorithm)
    2. Computing TM-Score for aligned chains

    Args:
        coords_pred_dict: Dict of {chain_id: coords (N, 3)}
        coords_true_dict: Dict of {chain_id: coords (N, 3)}
        normalize_by: How to compute L_norm

    Returns:
        tm_score: Overall TM-Score across all chains
    """
    # For single-chain structures, use simple TM-Score
    if len(coords_pred_dict) == 1 and len(coords_true_dict) == 1:
        pred_coords = list(coords_pred_dict.values())[0]
        true_coords = list(coords_true_dict.values())[0]
        return compute_tm_score(pred_coords, true_coords, normalize_by)

    # For multi-chain, find optimal assignment
    pred_chains = list(coords_pred_dict.keys())
    true_chains = list(coords_true_dict.keys())

    # Build cost matrix (negative TM-Score, since we minimize)
    n_pred = len(pred_chains)
    n_true = len(true_chains)
    cost_matrix = np.zeros((n_pred, n_true))

    for i, pred_chain in enumerate(pred_chains):
        for j, true_chain in enumerate(true_chains):
            try:
                score = compute_tm_score(
                    coords_pred_dict[pred_chain],
                    coords_true_dict[true_chain],
                    normalize_by
                )
                cost_matrix[i, j] = -score  # Negative for minimization
            except:
                cost_matrix[i, j] = 0  # No match

    # Find optimal assignment
    row_ind, col_ind = linear_sum_assignment(cost_matrix)

    # Compute overall TM-Score
    total_score = 0
    total_length = 0

    for i, j in zip(row_ind, col_ind):
        pred_chain = pred_chains[i]
        true_chain = true_chains[j]

        coords_p = coords_pred_dict[pred_chain]
        coords_t = coords_true_dict[true_chain]

        score = compute_tm_score(coords_p, coords_t, normalize_by)
        length = len(coords_t) if normalize_by == 'target' else len(coords_p)

        total_score += score * length
        total_length += length

    return total_score / total_length if total_length > 0 else 0.0


def evaluate_prediction(
    pred_coords: np.ndarray,
    true_coords: np.ndarray,
    verbose: bool = True
) -> dict:
    """
    Comprehensive evaluation of a single prediction.

    Args:
        pred_coords: Predicted coordinates (N, 3)
        true_coords: True coordinates (N, 3)
        verbose: Print evaluation summary

    Returns:
        metrics: Dictionary with TM-Score, RMSD, and other metrics
    """
    metrics = compute_tm_score(pred_coords, true_coords, return_details=True)

    if verbose:
        print("=" * 60)
        print("RNA Structure Prediction Evaluation")
        print("=" * 60)
        print(f"Sequence length: {metrics['L_norm']} nucleotides")
        print(f"TM-Score: {metrics['tm_score']:.4f}")
        print(f"RMSD: {metrics['rmsd']:.3f} A")
        print(f"d0 (scale): {metrics['d0']:.3f} A")
        print(f"\nDistance statistics:")
        print(f"  Mean: {metrics['mean_distance']:.3f} A")
        print(f"  Min:  {metrics['min_distance']:.3f} A")
        print(f"  Max:  {metrics['max_distance']:.3f} A")
        print("\nInterpretation:")
        if metrics['tm_score'] > 0.6:
            print("  [OK] Excellent! High confidence in fold similarity")
        elif metrics['tm_score'] > 0.5:
            print("  [OK] Good! Same fold predicted")
        elif metrics['tm_score'] > 0.3:
            print("  [!] Moderate. Topology may be similar")
        else:
            print("  [X] Poor. Likely different fold")
        print("=" * 60)

    return metrics


# ============================================================================
# Helper Functions for Loading Competition Data
# ============================================================================

def load_coords_from_labels(labels_df, target_id: str) -> np.ndarray:
    """
    Extract 3D coordinates for a specific target from labels DataFrame.

    Args:
        labels_df: DataFrame with columns [ID, resname, resid, x_1, y_1, z_1, chain, copy]
        target_id: Target identifier (e.g., '4TNA')

    Returns:
        coords: Array of shape (N, 3) with C1' atom coordinates
    """
    # Filter for this target
    mask = labels_df['ID'].str.startswith(target_id + '_')
    target_labels = labels_df[mask].copy()

    # Sort by residue ID to ensure correct order
    target_labels = target_labels.sort_values('resid')

    # Extract coordinates
    coords = target_labels[['x_1', 'y_1', 'z_1']].values

    return coords


def load_coords_by_chain(labels_df, target_id: str) -> dict:
    """
    Extract coordinates organized by chain.

    Args:
        labels_df: DataFrame with labels
        target_id: Target identifier

    Returns:
        coords_dict: {chain_id: coords (N, 3)}
    """
    mask = labels_df['ID'].str.startswith(target_id + '_')
    target_labels = labels_df[mask].copy()

    coords_dict = {}
    for chain in target_labels['chain'].unique():
        chain_data = target_labels[target_labels['chain'] == chain].sort_values('resid')
        coords_dict[chain] = chain_data[['x_1', 'y_1', 'z_1']].values

    return coords_dict


# ============================================================================
# Benchmarking and Testing
# ============================================================================

def test_tm_score_properties():
    """Test mathematical properties of TM-Score implementation."""
    print("Testing TM-Score Implementation...")
    print("=" * 60)

    # Test 1: Identical structures should give TM-Score = 1.0
    print("\n1. Testing identical structures...")
    coords = np.random.randn(50, 3) * 10
    score = compute_tm_score(coords, coords)
    assert abs(score - 1.0) < 1e-6, f"Identical structures should give 1.0, got {score}"
    print(f"   [OK] Identical structures: TM-Score = {score:.6f}")

    # Test 2: Translated structure should give TM-Score = 1.0
    print("\n2. Testing translation invariance...")
    translation = np.array([100, -50, 75])
    coords_translated = coords + translation
    score = compute_tm_score(coords_translated, coords)
    assert abs(score - 1.0) < 1e-6, f"Translated structures should give 1.0, got {score}"
    print(f"   [OK] Translation invariance: TM-Score = {score:.6f}")

    # Test 3: Rotated structure should give TM-Score = 1.0
    print("\n3. Testing rotation invariance...")
    rotation = Rotation.from_euler('xyz', [45, 30, 60], degrees=True).as_matrix()
    coords_rotated = coords @ rotation.T
    score = compute_tm_score(coords_rotated, coords)
    assert abs(score - 1.0) < 1e-6, f"Rotated structures should give 1.0, got {score}"
    print(f"   [OK] Rotation invariance: TM-Score = {score:.6f}")

    # Test 4: Rotated + Translated should give TM-Score = 1.0
    print("\n4. Testing combined transformation...")
    coords_transformed = (coords @ rotation.T) + translation
    score = compute_tm_score(coords_transformed, coords)
    assert abs(score - 1.0) < 1e-6, f"Transformed structures should give 1.0, got {score}"
    print(f"   [OK] Combined transformation: TM-Score = {score:.6f}")

    # Test 5: Random structure should give low TM-Score
    print("\n5. Testing random structures...")
    coords_random = np.random.randn(50, 3) * 100
    score = compute_tm_score(coords_random, coords)
    assert score < 0.3, f"Random structures should give low score, got {score}"
    print(f"   [OK] Random structures: TM-Score = {score:.6f}")

    # Test 6: Small perturbation should give high TM-Score
    print("\n6. Testing small perturbation...")
    coords_perturbed = coords + np.random.randn(50, 3) * 0.5  # 0.5 A noise
    score = compute_tm_score(coords_perturbed, coords)
    assert score > 0.8, f"Small perturbation should give good score, got {score}"
    print(f"   [OK] Small perturbation (0.5A): TM-Score = {score:.6f}")

    # Test 7: Different lengths (should handle gracefully)
    print("\n7. Testing different lengths...")
    coords_short = coords[:30]
    try:
        # This should raise an assertion error
        score = compute_tm_score(coords_short, coords)
        print(f"   [X] ERROR: Should have raised assertion for length mismatch")
    except AssertionError as e:
        print(f"   [OK] Correctly raises error for length mismatch")

    print("\n" + "=" * 60)
    print("All tests passed! [OK]")
    print("=" * 60)


if __name__ == "__main__":
    # Run tests
    test_tm_score_properties()

    # Example usage
    print("\n\nExample Usage:")
    print("=" * 60)

    # Create example structures
    np.random.seed(42)
    true_coords = np.random.randn(100, 3) * 20

    # Prediction 1: Good prediction (small noise)
    pred_coords_good = true_coords + np.random.randn(100, 3) * 1.0

    # Prediction 2: Poor prediction (large noise)
    pred_coords_poor = true_coords + np.random.randn(100, 3) * 10.0

    print("\nGood Prediction (1A noise):")
    metrics_good = evaluate_prediction(pred_coords_good, true_coords, verbose=True)

    print("\n\nPoor Prediction (10A noise):")
    metrics_poor = evaluate_prediction(pred_coords_poor, true_coords, verbose=True)
