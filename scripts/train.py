"""
Training script for RNA 3D structure prediction.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

import argparse
import yaml
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, random_split
import wandb
from tqdm import tqdm

from data.rna_dataset import RNADataset
from data.synthetic_data import SyntheticRNADataset
from models.metrics import StructureMetrics


class RNA3DPredictor(nn.Module):
    """Simple baseline model for RNA 3D structure prediction."""

    def __init__(self, vocab_size=5, embed_dim=128, hidden_dim=256, num_layers=4, dropout=0.2):
        super(RNA3DPredictor, self).__init__()

        self.embedding = nn.Embedding(vocab_size, embed_dim)

        self.lstm = nn.LSTM(
            embed_dim,
            hidden_dim,
            num_layers=num_layers,
            bidirectional=True,
            dropout=dropout if num_layers > 1 else 0,
            batch_first=True
        )

        # Output: 3D coordinates (x, y, z) per nucleotide
        self.fc = nn.Linear(hidden_dim * 2, 3)

    def forward(self, x):
        # x: (batch, seq_len)
        embedded = self.embedding(x)  # (batch, seq_len, embed_dim)
        lstm_out, _ = self.lstm(embedded)  # (batch, seq_len, hidden_dim*2)
        coords = self.fc(lstm_out)  # (batch, seq_len, 3)
        return coords


def train_epoch(model, dataloader, optimizer, criterion, device, metrics):
    """Train for one epoch."""
    model.train()
    total_loss = 0
    total_rmsd = 0
    total_tm = 0

    progress = tqdm(dataloader, desc='Training')

    for batch_x, batch_y in progress:
        batch_x = batch_x.to(device)
        batch_y = batch_y.to(device)

        optimizer.zero_grad()
        outputs = model(batch_x)

        # Compute loss
        loss = criterion(outputs, batch_y)
        loss.backward()
        optimizer.step()

        total_loss += loss.item()

        # Compute metrics
        with torch.no_grad():
            batch_metrics = metrics.compute_all(outputs[0], batch_y[0])
            total_rmsd += batch_metrics['rmsd']
            total_tm += batch_metrics['tm_score']

        progress.set_postfix({
            'loss': f"{loss.item():.4f}",
            'rmsd': f"{batch_metrics['rmsd']:.3f}",
            'tm': f"{batch_metrics['tm_score']:.3f}"
        })

    n = len(dataloader)
    return {
        'loss': total_loss / n,
        'rmsd': total_rmsd / n,
        'tm_score': total_tm / n
    }


def validate(model, dataloader, criterion, device, metrics):
    """Validate the model."""
    model.eval()
    total_loss = 0
    total_rmsd = 0
    total_tm = 0

    progress = tqdm(dataloader, desc='Validation')

    with torch.no_grad():
        for batch_x, batch_y in progress:
            batch_x = batch_x.to(device)
            batch_y = batch_y.to(device)

            outputs = model(batch_x)
            loss = criterion(outputs, batch_y)

            total_loss += loss.item()

            # Compute metrics
            batch_metrics = metrics.compute_all(outputs[0], batch_y[0])
            total_rmsd += batch_metrics['rmsd']
            total_tm += batch_metrics['tm_score']

            progress.set_postfix({
                'loss': f"{loss.item():.4f}",
                'rmsd': f"{batch_metrics['rmsd']:.3f}",
                'tm': f"{batch_metrics['tm_score']:.3f}"
            })

    n = len(dataloader)
    return {
        'loss': total_loss / n,
        'rmsd': total_rmsd / n,
        'tm_score': total_tm / n
    }


def main(args):
    """Main training function."""
    # Load config
    with open(args.config, 'r') as f:
        config = yaml.safe_load(f)

    # Initialize wandb
    if args.wandb:
        wandb.init(
            project=config['experiment']['wandb_project'],
            config=config,
            name=args.run_name
        )

    # Set device
    device = torch.device(config['experiment']['device']
                          if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")

    # Load or generate data
    if args.use_synthetic:
        print("Generating synthetic data...")
        synth_data = SyntheticRNADataset(
            num_samples=args.num_samples,
            min_length=50,
            max_length=200,
            seed=config['experiment']['seed']
        )
        dataset = RNADataset(synth_data.sequences, synth_data.coordinates)
    else:
        print("Loading competition data...")
        # TODO: Load real data when available
        raise NotImplementedError("Real data loading not yet implemented")

    # Split dataset
    train_size = int(0.8 * len(dataset))
    val_size = len(dataset) - train_size
    train_dataset, val_dataset = random_split(dataset, [train_size, val_size])

    # Create dataloaders
    train_loader = DataLoader(
        train_dataset,
        batch_size=config['training']['batch_size'],
        shuffle=True,
        num_workers=config['experiment']['num_workers']
    )
    val_loader = DataLoader(
        val_dataset,
        batch_size=config['training']['batch_size'],
        num_workers=config['experiment']['num_workers']
    )

    print(f"Train size: {len(train_dataset)}, Val size: {len(val_dataset)}")

    # Initialize model
    model = RNA3DPredictor(
        vocab_size=5,
        embed_dim=config['model']['hidden_dim'] // 2,
        hidden_dim=config['model']['hidden_dim'],
        num_layers=config['model']['num_layers'],
        dropout=config['model']['dropout']
    ).to(device)

    print(f"Model parameters: {sum(p.numel() for p in model.parameters()):,}")

    # Loss and optimizer
    criterion = nn.MSELoss()
    optimizer = optim.Adam(
        model.parameters(),
        lr=config['training']['learning_rate']
    )

    # Metrics
    metrics_calculator = StructureMetrics()

    # Training loop
    best_tm_score = 0
    patience_counter = 0

    for epoch in range(config['training']['epochs']):
        print(f"\nEpoch {epoch + 1}/{config['training']['epochs']}")

        # Train
        train_metrics = train_epoch(
            model, train_loader, optimizer, criterion, device, metrics_calculator
        )

        # Validate
        val_metrics = validate(
            model, val_loader, criterion, device, metrics_calculator
        )

        # Print results
        print(f"\nTrain - Loss: {train_metrics['loss']:.4f}, "
              f"RMSD: {train_metrics['rmsd']:.3f}, "
              f"TM-score: {train_metrics['tm_score']:.3f}")
        print(f"Val   - Loss: {val_metrics['loss']:.4f}, "
              f"RMSD: {val_metrics['rmsd']:.3f}, "
              f"TM-score: {val_metrics['tm_score']:.3f}")

        # Log to wandb
        if args.wandb:
            wandb.log({
                'epoch': epoch,
                'train/loss': train_metrics['loss'],
                'train/rmsd': train_metrics['rmsd'],
                'train/tm_score': train_metrics['tm_score'],
                'val/loss': val_metrics['loss'],
                'val/rmsd': val_metrics['rmsd'],
                'val/tm_score': val_metrics['tm_score']
            })

        # Save best model
        if val_metrics['tm_score'] > best_tm_score:
            best_tm_score = val_metrics['tm_score']
            patience_counter = 0

            model_path = Path(args.output_dir) / f'{args.run_name}_best.pth'
            model_path.parent.mkdir(exist_ok=True, parents=True)
            torch.save({
                'epoch': epoch,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'val_tm_score': best_tm_score,
                'config': config
            }, model_path)
            print(f"✅ Saved best model (TM-score: {best_tm_score:.3f})")
        else:
            patience_counter += 1

        # Early stopping
        if patience_counter >= config['training']['early_stopping_patience']:
            print(f"\nEarly stopping triggered after {epoch + 1} epochs")
            break

    print(f"\n✅ Training complete! Best TM-score: {best_tm_score:.3f}")

    if args.wandb:
        wandb.finish()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Train RNA 3D structure prediction model')

    parser.add_argument('--config', type=str, default='configs/default.yaml',
                        help='Path to config file')
    parser.add_argument('--run-name', type=str, default='baseline',
                        help='Name for this training run')
    parser.add_argument('--output-dir', type=str, default='models',
                        help='Directory to save models')
    parser.add_argument('--use-synthetic', action='store_true',
                        help='Use synthetic data instead of real competition data')
    parser.add_argument('--num-samples', type=int, default=1000,
                        help='Number of synthetic samples to generate')
    parser.add_argument('--wandb', action='store_true',
                        help='Enable Weights & Biases logging')

    args = parser.parse_args()

    main(args)
