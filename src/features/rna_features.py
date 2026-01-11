"""
Feature extraction utilities for RNA sequences.
"""
import numpy as np
import torch
from typing import Dict


def one_hot_encode(sequence: str, nucleotides: str = "AUGC") -> np.ndarray:
    """
    One-hot encode an RNA sequence.

    Args:
        sequence: RNA sequence string
        nucleotides: Nucleotide alphabet (default: AUGC)

    Returns:
        One-hot encoded array of shape (len(sequence), len(nucleotides))
    """
    nuc_to_idx = {nuc: i for i, nuc in enumerate(nucleotides)}

    encoded = np.zeros((len(sequence), len(nucleotides)), dtype=np.float32)

    for i, nuc in enumerate(sequence):
        if nuc in nuc_to_idx:
            encoded[i, nuc_to_idx[nuc]] = 1.0

    return encoded


def compute_gc_content(sequence: str) -> float:
    """
    Calculate GC content of RNA sequence.

    Args:
        sequence: RNA sequence string

    Returns:
        GC content as fraction (0-1)
    """
    if len(sequence) == 0:
        return 0.0

    gc_count = sequence.count('G') + sequence.count('C')
    return gc_count / len(sequence)


def compute_nucleotide_frequencies(sequence: str) -> Dict[str, float]:
    """
    Calculate nucleotide frequencies in sequence.

    Args:
        sequence: RNA sequence string

    Returns:
        Dictionary of nucleotide frequencies
    """
    if len(sequence) == 0:
        return {'A': 0.0, 'U': 0.0, 'G': 0.0, 'C': 0.0}

    total = len(sequence)
    return {
        'A': sequence.count('A') / total,
        'U': sequence.count('U') / total,
        'G': sequence.count('G') / total,
        'C': sequence.count('C') / total
    }


def positional_encoding(length: int, d_model: int = 128) -> torch.Tensor:
    """
    Generate sinusoidal positional encoding.

    Args:
        length: Sequence length
        d_model: Embedding dimension

    Returns:
        Positional encoding tensor of shape (length, d_model)
    """
    position = torch.arange(length).unsqueeze(1)
    div_term = torch.exp(torch.arange(0, d_model, 2) * (-np.log(10000.0) / d_model))

    pe = torch.zeros(length, d_model)
    pe[:, 0::2] = torch.sin(position * div_term)
    pe[:, 1::2] = torch.cos(position * div_term)

    return pe
