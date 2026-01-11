"""
RNA Dataset utilities for loading and processing competition data.
"""
import torch
from torch.utils.data import Dataset
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Optional, Tuple, List


class RNADataset(Dataset):
    """PyTorch Dataset for RNA sequences and 3D structures."""

    def __init__(
        self,
        sequences: List[str],
        targets: Optional[np.ndarray] = None,
        max_length: Optional[int] = None
    ):
        """
        Args:
            sequences: List of RNA sequences (strings)
            targets: Optional array of 3D coordinates
            max_length: Maximum sequence length (for padding/truncation)
        """
        self.sequences = sequences
        self.targets = targets
        self.max_length = max_length

        # Nucleotide to index mapping
        self.vocab = {'A': 0, 'U': 1, 'G': 2, 'C': 3, 'N': 4, '<PAD>': 5}
        self.vocab_size = len(self.vocab)

    def __len__(self) -> int:
        return len(self.sequences)

    def encode_sequence(self, seq: str) -> torch.Tensor:
        """Convert RNA sequence to numerical encoding."""
        encoded = [self.vocab.get(n, 4) for n in seq]

        # Pad or truncate if max_length is specified
        if self.max_length:
            if len(encoded) < self.max_length:
                encoded += [self.vocab['<PAD>']] * (self.max_length - len(encoded))
            else:
                encoded = encoded[:self.max_length]

        return torch.tensor(encoded, dtype=torch.long)

    def __getitem__(self, idx: int) -> Tuple[torch.Tensor, ...]:
        seq = self.sequences[idx]
        x = self.encode_sequence(seq)

        if self.targets is not None:
            y = torch.tensor(self.targets[idx], dtype=torch.float)
            return x, y
        return x,


def load_competition_data(data_dir: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Load training and test data from competition files.

    Args:
        data_dir: Path to directory containing competition data

    Returns:
        Tuple of (train_df, test_df)
    """
    data_path = Path(data_dir)

    train_df = pd.read_csv(data_path / 'train.csv')
    test_df = pd.read_csv(data_path / 'test.csv')

    return train_df, test_df


def parse_fasta(fasta_path: str) -> List[Tuple[str, str]]:
    """
    Parse FASTA file containing RNA sequences.

    Args:
        fasta_path: Path to FASTA file

    Returns:
        List of (header, sequence) tuples
    """
    sequences = []
    current_header = None
    current_seq = []

    with open(fasta_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('>'):
                if current_header:
                    sequences.append((current_header, ''.join(current_seq)))
                current_header = line[1:]
                current_seq = []
            else:
                current_seq.append(line)

        # Add last sequence
        if current_header:
            sequences.append((current_header, ''.join(current_seq)))

    return sequences


def compute_sequence_features(sequence: str) -> dict:
    """
    Compute basic features for an RNA sequence.

    Args:
        sequence: RNA sequence string

    Returns:
        Dictionary of features
    """
    length = len(sequence)

    # Nucleotide composition
    composition = {
        'A': sequence.count('A') / length if length > 0 else 0,
        'U': sequence.count('U') / length if length > 0 else 0,
        'G': sequence.count('G') / length if length > 0 else 0,
        'C': sequence.count('C') / length if length > 0 else 0,
    }

    # GC content
    gc_content = (composition['G'] + composition['C'])

    return {
        'length': length,
        'gc_content': gc_content,
        **{f'composition_{k}': v for k, v in composition.items()}
    }


def collate_fn(batch):
    """
    Custom collate function for DataLoader to handle variable-length sequences.

    Args:
        batch: List of samples from Dataset

    Returns:
        Batched tensors with padding
    """
    if len(batch[0]) == 2:  # Training data with targets
        sequences, targets = zip(*batch)

        # Pad sequences
        max_len = max(len(s) for s in sequences)
        padded_seqs = torch.stack([
            torch.nn.functional.pad(s, (0, max_len - len(s)), value=5)
            for s in sequences
        ])

        # Stack targets
        stacked_targets = torch.stack(targets)

        return padded_seqs, stacked_targets
    else:  # Test data without targets
        sequences = [s[0] for s in batch]
        max_len = max(len(s) for s in sequences)
        padded_seqs = torch.stack([
            torch.nn.functional.pad(s, (0, max_len - len(s)), value=5)
            for s in sequences
        ])

        return padded_seqs,
