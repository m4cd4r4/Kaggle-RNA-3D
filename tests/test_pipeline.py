"""
Test the entire pipeline with synthetic data.
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

import torch
import numpy as np
from data.synthetic_data import SyntheticRNADataset
from data.rna_dataset import RNADataset
from models.metrics import StructureMetrics, rmsd, tm_score
from features.rna_features import (
    one_hot_encode,
    compute_gc_content,
    compute_nucleotide_frequencies
)


def test_synthetic_data_generation():
    """Test synthetic data generation."""
    print("\n" + "=" * 60)
    print("TEST 1: Synthetic Data Generation")
    print("=" * 60)

    dataset = SyntheticRNADataset(num_samples=20, min_length=50, max_length=150)

    assert len(dataset) == 20, "Dataset size mismatch"

    seq, coords, struct = dataset[0]
    assert isinstance(seq, str), "Sequence should be string"
    assert coords.shape[1] == 3, "Coordinates should be (N, 3)"
    assert len(seq) == len(coords), "Sequence and coords length mismatch"

    print(f"✅ Generated {len(dataset)} samples")
    print(f"   Sample sequence length: {len(seq)}")
    print(f"   Coordinates shape: {coords.shape}")


def test_feature_extraction():
    """Test feature extraction functions."""
    print("\n" + "=" * 60)
    print("TEST 2: Feature Extraction")
    print("=" * 60)

    # Test sequence
    seq = "AUGCAUGC"

    # One-hot encoding
    encoded = one_hot_encode(seq)
    assert encoded.shape == (len(seq), 4), "One-hot encoding shape mismatch"
    assert encoded.sum() == len(seq), "One-hot encoding should have one 1 per position"

    print(f"✅ One-hot encoding: {seq} -> shape {encoded.shape}")

    # GC content
    gc = compute_gc_content(seq)
    assert 0 <= gc <= 1, "GC content should be between 0 and 1"

    print(f"✅ GC content: {gc:.2%}")

    # Nucleotide frequencies
    freqs = compute_nucleotide_frequencies(seq)
    assert abs(sum(freqs.values()) - 1.0) < 1e-6, "Frequencies should sum to 1"

    print(f"✅ Nucleotide frequencies: {freqs}")


def test_metrics():
    """Test evaluation metrics."""
    print("\n" + "=" * 60)
    print("TEST 3: Evaluation Metrics")
    print("=" * 60)

    # Generate test coordinates
    np.random.seed(42)
    length = 100

    true_coords = torch.randn(length, 3) * 10
    pred_coords = true_coords + torch.randn(length, 3) * 2  # Add noise

    # Test RMSD
    rmsd_val = rmsd(pred_coords, true_coords)
    assert rmsd_val > 0, "RMSD should be positive"

    print(f"✅ RMSD: {rmsd_val:.3f} Å")

    # Test TM-score
    tm_val = tm_score(pred_coords, true_coords)
    assert 0 <= tm_val <= 1, "TM-score should be between 0 and 1"

    print(f"✅ TM-score: {tm_val:.3f}")

    # Test all metrics
    metrics = StructureMetrics()
    results = metrics.compute_all(pred_coords, true_coords)

    print(f"✅ All metrics computed:")
    for metric_name, value in results.items():
        print(f"   {metric_name}: {value:.3f}")


def test_dataset_loader():
    """Test PyTorch dataset loader."""
    print("\n" + "=" * 60)
    print("TEST 4: PyTorch Dataset Loader")
    print("=" * 60)

    # Generate synthetic data
    synth_dataset = SyntheticRNADataset(num_samples=10)

    # Create PyTorch dataset
    sequences = synth_dataset.sequences
    targets = synth_dataset.coordinates

    dataset = RNADataset(sequences, targets)

    assert len(dataset) == 10, "Dataset length mismatch"

    # Test single item
    x, y = dataset[0]
    assert isinstance(x, torch.Tensor), "Input should be tensor"
    assert isinstance(y, torch.Tensor), "Target should be tensor"

    print(f"✅ PyTorch Dataset created with {len(dataset)} samples")
    print(f"   Input shape: {x.shape}")
    print(f"   Target shape: {y.shape}")

    # Test batch loading
    from torch.utils.data import DataLoader

    loader = DataLoader(dataset, batch_size=4, shuffle=True)
    batch_x, batch_y = next(iter(loader))

    print(f"✅ DataLoader batch:")
    print(f"   Batch input shape: {batch_x.shape}")
    print(f"   Batch target shape: {batch_y.shape}")


def test_end_to_end():
    """Test end-to-end pipeline."""
    print("\n" + "=" * 60)
    print("TEST 5: End-to-End Pipeline")
    print("=" * 60)

    # 1. Generate synthetic data
    synth_data = SyntheticRNADataset(num_samples=5, min_length=50, max_length=100)
    print(f"✅ Step 1: Generated {len(synth_data)} synthetic samples")

    # 2. Create dataset
    dataset = RNADataset(synth_data.sequences, synth_data.coordinates)
    print(f"✅ Step 2: Created PyTorch dataset")

    # 3. Extract features
    seq = synth_data.sequences[0]
    features = {
        'one_hot': one_hot_encode(seq),
        'gc_content': compute_gc_content(seq),
        'nucleotide_freqs': compute_nucleotide_frequencies(seq)
    }
    print(f"✅ Step 3: Extracted features for sample sequence")

    # 4. Simulate predictions (just use target + noise as "prediction")
    true_coords = torch.tensor(synth_data.coordinates[0], dtype=torch.float32)
    pred_coords = true_coords + torch.randn_like(true_coords) * 1.0

    # 5. Evaluate
    metrics = StructureMetrics()
    results = metrics.compute_all(pred_coords, true_coords)

    print(f"✅ Step 4: Evaluated predictions")
    print(f"   TM-score: {results['tm_score']:.3f}")
    print(f"   RMSD: {results['rmsd']:.3f} Å")

    print("\n✅ END-TO-END PIPELINE TEST PASSED!")


def run_all_tests():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("RNA 3D FOLDING - PIPELINE TESTS")
    print("=" * 60)

    try:
        test_synthetic_data_generation()
        test_feature_extraction()
        test_metrics()
        test_dataset_loader()
        test_end_to_end()

        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("=" * 60)
        print("\nThe pipeline is ready for real competition data.")

    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

    return True


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
