# Stanford RNA 3D Folding Part 2 - Competition Information

## Overview
- **Competition**: Stanford RNA 3D Folding Part 2
- **Platform**: Kaggle Featured Competition
- **Prize**: $75,000 USD
- **Deadline**: March 25, 2026 (23:59 UTC)
- **Teams**: 186 participating teams
- **Status**: Registered and approved ✓

## Objective
Predict the 3D structure of RNA molecules from their sequences. This is one of biology's remaining grand challenges.

## Evaluation Metric
**TM-Score** (Template Modeling Score)
- Range: 0 to 1
- >0.5 indicates same fold
- Scale-independent measure of structural similarity
- Higher is better

## Data Structure

### Multiple Sequence Alignments (MSA)
The competition provides MSA files for template discovery:
- Format: FASTA files
- Location: `MSA/*.MSA.fasta`
- Size: Variable (20 bytes to 271 KB per file)
- Purpose: Evolutionary information for template-based modeling

### Expected File Structure
```
data/raw/
├── train/                  # Training sequences and structures
├── test/                   # Test sequences (predict these)
├── MSA/                    # Multiple sequence alignments
├── sample_submission.csv   # Submission format template
└── README.txt             # Competition data description
```

## Key Insights from Part 1

### What Won Part 1
1. **Template-based modeling WITHOUT deep learning**
2. Winners achieved TM-scores: 0.671, 0.653, 0.615
3. All top 3 teams beat AlphaFold 3
4. Template discovery pipelines were the winning strategy

### Implications for Part 2
- Template retrieval + refinement is proven
- Pure deep learning (like AlphaFold) was insufficient
- RNA-specific methods needed (generic protein methods failed)
- Organizers developed RNAPro by integrating Kaggle strategies

## Submission Format
- Predictions must be 3D coordinates
- TM-Score used for evaluation
- Submissions via Kaggle API or website

## Strategy Recommendations
Based on Part 1 results and literature:
1. **Primary Approach**: Template-based modeling
2. **Enhancement**: SE(3)-equivariant neural networks for refinement
3. **Data Augmentation**: Inverse folding to generate training pairs
4. **Architecture**: Hybrid template retrieval + deep learning
5. **Evaluation**: Focus on TM-Score optimization

## Resources
- Competition URL: https://www.kaggle.com/competitions/stanford-rna-3d-folding-2
- Part 1 Solutions: https://www.kaggle.com/competitions/stanford-rna-3d-folding/discussion
- Dashboard: http://127.0.0.1:3008/ (local Next.js app)

## Current Status
- [x] Environment setup complete (PyTorch 2.6.0 + CUDA 12.4)
- [x] Kaggle API configured
- [ ] Data download in progress (7.8 GB / ~24 GB)
- [ ] Initial exploration notebook
- [ ] Baseline model implementation

## Next Steps
1. Complete data download and extraction
2. Explore training data structure
3. Analyze MSA files for template discovery
4. Implement baseline TM-Score calculation
5. Build template retrieval pipeline

---

**Last Updated**: January 11, 2026
**Session**: Data preparation and environment setup
