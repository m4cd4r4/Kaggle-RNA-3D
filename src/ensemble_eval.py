#!/usr/bin/env python3
"""
Ensemble Evaluation for RNA 3D Structure Prediction

Handles ensemble prediction format where multiple coordinate predictions
are provided for each atom/residue.

Format:
- Training: 1 prediction per atom (x_1, y_1, z_1)
- Validation: 40 reference structures (x_1...x_40, y_1...y_40, z_1...z_40)
- Submission: 5 predictions per atom (x_1...x_5, y_1...y_5, z_1...z_5)
"""

import numpy as np
import pandas as pd
from typing import List, Tuple, Dict
import sys
from pathlib import Path

# Import our TM-Score implementation
sys.path.insert(0, str(Path(__file__).parent))
from tm_score import compute_tm_score


def extract_coords_from_ensemble(
    df: pd.DataFrame,
    target_id: str,
    n_models: int = 40
) -> List[np.ndarray]:
    """
    Extract coordinate ensembles from validation/submission format.

    Args:
        df: DataFrame with ensemble format (x_1...x_N, y_1...y_N, z_1...z_N)
        target_id: Target structure ID
        n_models: Number of models in ensemble (40 for validation, 5 for submission)

    Returns:
        coords_list: List of coordinate arrays, each (N_atoms, 3)
    """
    # Filter for target
    mask = df['ID'].str.startswith(target_id + '_')
    target_data = df[mask].copy().sort_values('resid')

    coords_list = []
    for model_idx in range(1, n_models + 1):
        # Extract x, y, z for this model
        x_col = f'x_{model_idx}'
        y_col = f'y_{model_idx}'
        z_col = f'z_{model_idx}'

        # Check if columns exist
        if x_col not in target_data.columns:
            break

        coords = target_data[[x_col, y_col, z_col]].values
        coords_list.append(coords)

    return coords_list


def evaluate_ensemble_vs_ensemble(
    pred_coords_list: List[np.ndarray],
    ref_coords_list: List[np.ndarray],
    method: str = 'best_of_best'
) -> Dict:
    """
    Evaluate ensemble of predictions against ensemble of references.

    Args:
        pred_coords_list: List of predicted coordinate arrays (e.g., 5 predictions)
        ref_coords_list: List of reference coordinate arrays (e.g., 40 references)
        method: Evaluation method:
            'best_of_best': Best prediction vs best reference (max TM-Score)
            'avg_of_best': Average of (best pred vs each ref)
            'best_of_avg': Best prediction vs average reference

    Returns:
        results: Dict with tm_score, best_pred_idx, best_ref_idx, all_scores
    """
    n_preds = len(pred_coords_list)
    n_refs = len(ref_coords_list)

    # Compute all pairwise TM-Scores
    score_matrix = np.zeros((n_preds, n_refs))

    for i, pred_coords in enumerate(pred_coords_list):
        for j, ref_coords in enumerate(ref_coords_list):
            try:
                score = compute_tm_score(pred_coords, ref_coords)
                score_matrix[i, j] = score
            except Exception as e:
                print(f"Warning: Failed to compute TM-Score for pred {i} vs ref {j}: {e}")
                score_matrix[i, j] = 0.0

    # Apply evaluation method
    if method == 'best_of_best':
        # Find best prediction-reference pair
        best_score = np.max(score_matrix)
        best_idx = np.unravel_index(np.argmax(score_matrix), score_matrix.shape)
        best_pred_idx, best_ref_idx = best_idx

        return {
            'tm_score': float(best_score),
            'method': method,
            'best_pred_idx': int(best_pred_idx),
            'best_ref_idx': int(best_ref_idx),
            'score_matrix': score_matrix,
            'pred_scores': score_matrix[best_pred_idx, :],  # Best pred vs all refs
            'ref_scores': score_matrix[:, best_ref_idx]     # All preds vs best ref
        }

    elif method == 'avg_of_best':
        # For each reference, find best prediction, then average
        best_pred_per_ref = np.max(score_matrix, axis=0)
        avg_score = np.mean(best_pred_per_ref)

        return {
            'tm_score': float(avg_score),
            'method': method,
            'best_pred_per_ref': best_pred_per_ref,
            'score_matrix': score_matrix
        }

    elif method == 'best_of_avg':
        # Find best prediction against average of references
        # Average reference
        ref_coords_avg = np.mean(np.stack(ref_coords_list), axis=0)

        # Evaluate each prediction vs average
        pred_scores = []
        for pred_coords in pred_coords_list:
            score = compute_tm_score(pred_coords, ref_coords_avg)
            pred_scores.append(score)

        best_score = max(pred_scores)
        best_pred_idx = np.argmax(pred_scores)

        return {
            'tm_score': float(best_score),
            'method': method,
            'best_pred_idx': int(best_pred_idx),
            'pred_scores': np.array(pred_scores),
            'ref_coords_avg': ref_coords_avg
        }

    else:
        raise ValueError(f"Unknown method: {method}")


def evaluate_single_vs_ensemble(
    pred_coords: np.ndarray,
    ref_coords_list: List[np.ndarray]
) -> Dict:
    """
    Evaluate single prediction against ensemble of references.

    Args:
        pred_coords: Single predicted coordinate array (N_atoms, 3)
        ref_coords_list: List of reference coordinate arrays

    Returns:
        results: Dict with best_score, avg_score, all_scores
    """
    scores = []
    for ref_coords in ref_coords_list:
        try:
            score = compute_tm_score(pred_coords, ref_coords)
            scores.append(score)
        except Exception as e:
            print(f"Warning: Failed to compute TM-Score: {e}")
            scores.append(0.0)

    scores = np.array(scores)

    return {
        'best_score': float(np.max(scores)),
        'avg_score': float(np.mean(scores)),
        'worst_score': float(np.min(scores)),
        'std_score': float(np.std(scores)),
        'all_scores': scores,
        'best_ref_idx': int(np.argmax(scores))
    }


def create_ensemble_submission(
    predictions_list: List[pd.DataFrame],
    test_sequences: pd.DataFrame
) -> pd.DataFrame:
    """
    Create submission file from ensemble of predictions.

    Args:
        predictions_list: List of DataFrames, each with columns [ID, resname, resid, x_1, y_1, z_1]
        test_sequences: Test sequences DataFrame

    Returns:
        submission: DataFrame in competition format with x_1...x_5, y_1...y_5, z_1...z_5
    """
    # Start with first prediction
    submission = predictions_list[0][['ID', 'resname', 'resid']].copy()

    # Add coordinate columns for each ensemble member
    for i, pred_df in enumerate(predictions_list[:5], 1):  # Max 5 for submission
        submission[f'x_{i}'] = pred_df['x_1'].values
        submission[f'y_{i}'] = pred_df['y_1'].values
        submission[f'z_{i}'] = pred_df['z_1'].values

    # If fewer than 5 predictions, duplicate the best one
    while i < 5:
        i += 1
        submission[f'x_{i}'] = submission['x_1'].values
        submission[f'y_{i}'] = submission['y_1'].values
        submission[f'z_{i}'] = submission['z_1'].values

    return submission


if __name__ == "__main__":
    # Test ensemble evaluation
    print("=" * 70)
    print("Testing Ensemble Evaluation")
    print("=" * 70)

    # Load validation data
    DATA_DIR = Path(__file__).parent.parent / "data" / "raw"
    val_labels = pd.read_csv(DATA_DIR / "validation_labels.csv")

    # Get first target
    targets = val_labels['ID'].str.split('_').str[0].unique()
    target_id = targets[0]

    print(f"\nTarget: {target_id}")

    # Extract reference ensemble (40 structures)
    ref_coords_list = extract_coords_from_ensemble(val_labels, target_id, n_models=40)
    print(f"Reference ensemble: {len(ref_coords_list)} structures")
    print(f"Each structure: {ref_coords_list[0].shape}")

    # Create synthetic ensemble predictions (5 predictions with varying noise)
    true_coords = ref_coords_list[0]  # Use first reference as "true" structure
    pred_coords_list = []
    for noise_level in [0.5, 1.0, 1.5, 2.0, 2.5]:
        pred = true_coords + np.random.randn(*true_coords.shape) * noise_level
        pred_coords_list.append(pred)

    print(f"\nTest predictions: {len(pred_coords_list)} ensemble members")

    # Test evaluation methods
    print("\n" + "-" * 70)
    print("Evaluation Method Comparison:")
    print("-" * 70)

    for method in ['best_of_best', 'avg_of_best', 'best_of_avg']:
        results = evaluate_ensemble_vs_ensemble(pred_coords_list, ref_coords_list, method=method)
        print(f"\n{method}:")
        print(f"  TM-Score: {results['tm_score']:.4f}")
        if 'best_pred_idx' in results:
            print(f"  Best prediction: #{results['best_pred_idx']}")
        if 'best_ref_idx' in results:
            print(f"  Best reference: #{results['best_ref_idx']}")

    # Test single prediction vs ensemble
    print("\n" + "-" * 70)
    print("Single Prediction vs Ensemble:")
    print("-" * 70)

    single_pred = pred_coords_list[0]
    results = evaluate_single_vs_ensemble(single_pred, ref_coords_list)
    print(f"\nBest score: {results['best_score']:.4f}")
    print(f"Average score: {results['avg_score']:.4f}")
    print(f"Worst score: {results['worst_score']:.4f}")
    print(f"Std dev: {results['std_score']:.4f}")
    print(f"Best reference: #{results['best_ref_idx']}")

    print("\n" + "=" * 70)
    print("Ensemble Evaluation: Ready [OK]")
    print("=" * 70)
