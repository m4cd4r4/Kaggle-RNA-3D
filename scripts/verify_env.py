#!/usr/bin/env python3
"""Verify the Python environment is set up correctly."""

import sys

def check_import(module_name, package_name=None):
    """Try to import a module and report status."""
    package_name = package_name or module_name
    try:
        module = __import__(module_name)
        version = getattr(module, '__version__', 'unknown')
        print(f"  [OK] {package_name}: {version}")
        return True
    except ImportError as e:
        print(f"  [X] {package_name}: NOT INSTALLED ({e})")
        return False

def main():
    print("=" * 50)
    print("RNA 3D Folding - Environment Verification")
    print("=" * 50)
    print(f"\nPython: {sys.version}")
    print(f"Path: {sys.executable}\n")

    all_ok = True

    # Core ML
    print("Core ML Libraries:")
    all_ok &= check_import('torch', 'PyTorch')
    all_ok &= check_import('numpy', 'NumPy')
    all_ok &= check_import('pandas', 'Pandas')

    # Check CUDA
    try:
        import torch
        cuda_available = torch.cuda.is_available()
        if cuda_available:
            print(f"  [OK] CUDA: {torch.version.cuda} ({torch.cuda.get_device_name(0)})")
        else:
            print("  [!] CUDA: Not available (CPU only)")
    except:
        pass

    # Deep Learning
    print("\nDeep Learning:")
    all_ok &= check_import('pytorch_lightning', 'PyTorch Lightning')
    all_ok &= check_import('transformers', 'Transformers')

    # Bioinformatics
    print("\nBioinformatics:")
    all_ok &= check_import('Bio', 'BioPython')
    all_ok &= check_import('biotite', 'Biotite')

    # Visualization
    print("\nVisualization:")
    all_ok &= check_import('matplotlib', 'Matplotlib')
    all_ok &= check_import('seaborn', 'Seaborn')
    all_ok &= check_import('plotly', 'Plotly')

    # Utilities
    print("\nUtilities:")
    all_ok &= check_import('tqdm', 'tqdm')
    all_ok &= check_import('wandb', 'Weights & Biases')
    all_ok &= check_import('kaggle', 'Kaggle API')

    print("\n" + "=" * 50)
    if all_ok:
        print("[OK] All packages installed successfully!")
    else:
        print("[!] Some packages missing - run: pip install -r requirements.txt")
    print("=" * 50)

    return 0 if all_ok else 1

if __name__ == "__main__":
    sys.exit(main())
