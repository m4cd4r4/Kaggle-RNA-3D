"""
Generate synthetic RNA data for testing the pipeline.
"""
import numpy as np
import torch
from typing import Tuple, List


def generate_random_sequence(length: int, nucleotides: str = "AUGC") -> str:
    """
    Generate a random RNA sequence.

    Args:
        length: Sequence length
        nucleotides: Available nucleotides (default: AUGC)

    Returns:
        Random RNA sequence string
    """
    return ''.join(np.random.choice(list(nucleotides), size=length))


def generate_3d_coordinates(length: int, noise_level: float = 0.5) -> np.ndarray:
    """
    Generate synthetic 3D coordinates for RNA structure.

    Creates a helical backbone with added noise to simulate realistic structures.

    Args:
        length: Number of nucleotides
        noise_level: Amount of random noise to add

    Returns:
        3D coordinates array of shape (length, 3)
    """
    # Create helical backbone
    t = np.linspace(0, 4 * np.pi, length)
    radius = 10.0
    pitch = 3.4  # Rise per nucleotide in Angstroms

    # Helical coordinates
    x = radius * np.cos(t)
    y = radius * np.sin(t)
    z = pitch * t

    # Stack coordinates
    coords = np.stack([x, y, z], axis=1)

    # Add random noise
    noise = np.random.randn(*coords.shape) * noise_level
    coords += noise

    return coords.astype(np.float32)


def generate_secondary_structure(length: int) -> str:
    """
    Generate a random dot-bracket secondary structure notation.

    Args:
        length: Sequence length

    Returns:
        Dot-bracket string (e.g., "(((...)))")
    """
    structure = ['.'] * length

    # Generate random base pairs
    num_pairs = length // 4  # ~25% paired
    available = list(range(length))

    for _ in range(num_pairs):
        if len(available) < 2:
            break

        # Pick two positions with some distance
        i = np.random.choice(available)
        available.remove(i)

        # Find valid pairing partner (at least 4 bases away)
        valid_partners = [j for j in available if abs(j - i) >= 4]

        if valid_partners:
            j = np.random.choice(valid_partners)
            available.remove(j)

            # Assign brackets
            if i < j:
                structure[i] = '('
                structure[j] = ')'
            else:
                structure[i] = ')'
                structure[j] = '('

    return ''.join(structure)


class SyntheticRNADataset:
    """Generate synthetic RNA dataset for testing."""

    def __init__(
        self,
        num_samples: int = 100,
        min_length: int = 50,
        max_length: int = 200,
        seed: int = 42
    ):
        """
        Initialize synthetic dataset generator.

        Args:
            num_samples: Number of sequences to generate
            min_length: Minimum sequence length
            max_length: Maximum sequence length
            seed: Random seed for reproducibility
        """
        np.random.seed(seed)
        torch.manual_seed(seed)

        self.num_samples = num_samples
        self.min_length = min_length
        self.max_length = max_length

        # Generate data
        self.sequences = []
        self.coordinates = []
        self.secondary_structures = []

        for _ in range(num_samples):
            length = np.random.randint(min_length, max_length + 1)

            self.sequences.append(generate_random_sequence(length))
            self.coordinates.append(generate_3d_coordinates(length))
            self.secondary_structures.append(generate_secondary_structure(length))

    def __len__(self) -> int:
        return self.num_samples

    def __getitem__(self, idx: int) -> Tuple[str, np.ndarray, str]:
        """
        Get a single sample.

        Returns:
            (sequence, coordinates, secondary_structure)
        """
        return (
            self.sequences[idx],
            self.coordinates[idx],
            self.secondary_structures[idx]
        )

    def get_batch(self, batch_size: int = 32) -> Tuple[List[str], List[np.ndarray], List[str]]:
        """
        Get a random batch of samples.

        Args:
            batch_size: Number of samples in batch

        Returns:
            (sequences, coordinates, secondary_structures)
        """
        indices = np.random.choice(self.num_samples, size=batch_size, replace=False)

        sequences = [self.sequences[i] for i in indices]
        coords = [self.coordinates[i] for i in indices]
        structures = [self.secondary_structures[i] for i in indices]

        return sequences, coords, structures

    def save_fasta(self, filepath: str):
        """
        Save sequences in FASTA format.

        Args:
            filepath: Path to save FASTA file
        """
        with open(filepath, 'w') as f:
            for i, seq in enumerate(self.sequences):
                f.write(f">synthetic_rna_{i}\n")
                f.write(f"{seq}\n")

    def save_coordinates(self, filepath: str):
        """
        Save coordinates in PDB format.

        Args:
            filepath: Base path for PDB files (will append index)
        """
        import os
        base_dir = os.path.dirname(filepath)
        base_name = os.path.basename(filepath).replace('.pdb', '')

        for i, (seq, coords) in enumerate(zip(self.sequences, self.coordinates)):
            pdb_path = os.path.join(base_dir, f"{base_name}_{i}.pdb")
            self._write_pdb(pdb_path, seq, coords, i)

    def _write_pdb(self, filepath: str, sequence: str, coords: np.ndarray, model_id: int):
        """Write a single PDB file."""
        with open(filepath, 'w') as f:
            f.write(f"HEADER    SYNTHETIC RNA {model_id}\n")
            f.write(f"TITLE     GENERATED FOR TESTING\n")

            for i, (res, coord) in enumerate(zip(sequence, coords), start=1):
                # PDB format: ATOM serial atom_name res_name chain res_seq x y z occupancy temp element
                atom_line = (
                    f"ATOM  {i:5d}  P   {res:3} A{i:4d}    "
                    f"{coord[0]:8.3f}{coord[1]:8.3f}{coord[2]:8.3f}"
                    f"  1.00 20.00           P\n"
                )
                f.write(atom_line)

            f.write("END\n")


def test_synthetic_data():
    """Test synthetic data generation."""
    print("Testing Synthetic RNA Data Generator")
    print("=" * 50)

    # Generate dataset
    dataset = SyntheticRNADataset(num_samples=10, min_length=30, max_length=100)

    print(f"\nGenerated {len(dataset)} samples")

    # Get a sample
    seq, coords, struct = dataset[0]
    print(f"\nSample 0:")
    print(f"  Sequence: {seq[:50]}... (length: {len(seq)})")
    print(f"  Coordinates shape: {coords.shape}")
    print(f"  Secondary structure: {struct[:50]}...")

    # Get a batch
    seqs, coords_batch, structs = dataset.get_batch(batch_size=5)
    print(f"\nBatch of 5 samples:")
    print(f"  Sequence lengths: {[len(s) for s in seqs]}")
    print(f"  Coordinate shapes: {[c.shape for c in coords_batch]}")

    # Test FASTA export
    import tempfile
    import os

    with tempfile.TemporaryDirectory() as tmpdir:
        fasta_path = os.path.join(tmpdir, "test.fasta")
        dataset.save_fasta(fasta_path)

        with open(fasta_path, 'r') as f:
            lines = f.readlines()

        print(f"\nFASTA file created: {len(lines)} lines")
        print(f"  First entry:\n    {lines[0].strip()}\n    {lines[1][:50]}...")

    print("\n✅ All tests passed!")


if __name__ == "__main__":
    test_synthetic_data()
