# Research Summary: RNA 3D Structure Prediction

*Compiled: January 11, 2026*

## Key Findings from Part 1 Competition

### Unexpected Winner: Template-Based Methods Beat Deep Learning

The Stanford RNA 3D Folding Part 1 competition produced a surprising result that challenges conventional wisdom in the field:

**The winning approach used template-based modeling WITHOUT deep learning**, outperforming sophisticated neural network methods including AlphaFold 3.

### Competition Statistics

| Metric | Value |
|--------|-------|
| Teams | 1,700+ |
| Test Structures | 43 (previously unreleased) |
| 1st Place (john) | TM-score: 0.671 |
| 2nd Place (odat) | TM-score: 0.653 |
| 3rd Place (Eigen) | TM-score: 0.615 |

**All three top teams outperformed AlphaFold 3** and achieved scores within statistical error of CASP16 winners.

### Post-Competition Development

The Das Lab integrated winning strategies to create **RNAPro**, which retrospectively outperformed individual Kaggle models.

## Template-Based vs. Deep Learning Approaches

### Template-Based Modeling (Winner)

**Approach:**
1. Search for similar known RNA structures in databases (PDB)
2. Use structural templates as starting points
3. Apply refinement and modeling to adapt templates to target sequence

**Advantages:**
- Leverages existing experimental data
- Domain knowledge-driven
- Interpretable results
- Computationally efficient

**Disadvantages:**
- Requires good template matches
- May fail on novel folds
- Limited by database coverage

### Deep Learning Approaches (Competitive)

**Popular Methods:**
- **RNA Foundation Models**: Aido.RNA, RNet
- **Language Models**: RhoFold+ (23.7M sequences)
- **Protein-inspired**: RoseTTAFoldNA, AlphaFold 3
- **Hybrid**: Combining sequences, MSAs, structure features

**Advantages:**
- Can predict novel folds
- Learn from massive sequence data
- End-to-end automated

**Disadvantages:**
- Data-hungry (RNA data scarcity problem)
- Computationally expensive
- Black box nature

## State-of-the-Art Deep Learning Methods (2024)

### 1. RhoFold+ (Current Leader)

**Publication**: Nature Methods, 2024

**Key Features:**
- RNA language model pretrained on 23.7 million sequences
- Addresses data scarcity through self-supervised learning
- Fully automated end-to-end pipeline
- Superior performance on RNA-Puzzles and CASP15 benchmarks

**Performance**: Outperforms human expert groups on blind predictions

**Architecture**: Transformer-based with specialized RNA sequence encoding

### 2. AlphaFold 3

**Publication**: Nature, 2024 (DeepMind)

**Key Features:**
- Extends protein structure prediction to RNA and complexes
- Predicts biomolecular interactions
- Uses MSA (Multiple Sequence Alignment) construction

**Performance**: Comparable to other ML methods, but not best-in-class for RNA

**Limitations**: Challenges with ligand binding site accuracy

### 3. RoseTTAFoldNA

**Publication**: Nature Methods, 2023

**Key Features:**
- Extends protein prediction method to nucleic acids
- Predicts protein-DNA and protein-RNA complexes
- Provides confidence estimates

**Use Case**: Particularly good for protein-RNA interactions

### 4. Comparative Benchmarks (2024)

Recent systematic evaluation on three datasets:
- RNA-Puzzles
- CASP15 RNA targets
- Sequentially distinct RNAs

**Evaluated Methods:**
- DRfold
- DeepFoldRNA
- RhoFold
- RoseTTAFoldNA
- trRosettaRNA
- AlphaFold 3

**Finding**: AlphaFold 3 performance comparable to other ML methods, with ongoing challenges in novel structure prediction.

## Implications for Part 2 Competition

### Strategy Recommendations

1. **Hybrid Approach** (Recommended)
   - Start with template-based search (proven winner)
   - Use deep learning for novel/difficult cases
   - Ensemble multiple methods

2. **Template-Based Pipeline**
   - Implement structure database search (PDB, RNA-specific DBs)
   - Sequence alignment and template selection
   - Structural refinement

3. **Deep Learning Models**
   - Fine-tune RhoFold+ or similar pretrained models
   - Experiment with RNA foundation models
   - Consider protein-RNA complex prediction tools

4. **Ensemble Strategy**
   - Combine template-based and ML predictions
   - Use confidence scores for model selection
   - Weighted averaging based on sequence similarity

### Critical Success Factors

Based on Part 1 learnings:

1. **Template Quality**
   - Access to comprehensive structure databases
   - Effective sequence/structure similarity search
   - Multiple template sources

2. **Evaluation Pipeline**
   - Robust TM-score implementation
   - Fast iteration on validation set
   - Proper cross-validation

3. **Computational Resources**
   - Template search can be parallelized
   - Deep learning requires GPU
   - Consider compute budget for different approaches

## Technical Metrics Deep Dive

### TM-score (Primary Metric)

**Formula**: `TM-score = (1/N) * Σ [1 / (1 + (di/d0)²)]`

Where:
- N = sequence length
- di = distance between aligned residue pairs
- d0 = 1.24(N-15)^(1/3) - 1.8 (length normalization)

**Interpretation:**
- TM-score < 0.3: Random similarity
- TM-score = 0.5: Borderline fold similarity
- TM-score > 0.6: Same fold
- TM-score > 0.8: High structural similarity

**Why it matters**: Scale-independent, suitable for different RNA lengths

### Supporting Metrics

**RMSD (Root Mean Square Deviation)**
- Direct distance measurement
- Sensitive to outliers
- Good for local quality assessment

**GDT-TS (Global Distance Test)**
- Percentage of residues within distance cutoffs (1Å, 2Å, 4Å, 8Å)
- Range: 0-100
- Robust to local errors

**lDDT (Local Distance Difference Test)**
- Measures local distance agreement
- Less sensitive to domain movements
- Range: 0-1

## Open Questions & Research Opportunities

1. **Why did template-based methods win?**
   - RNA structure space more conserved than expected?
   - Deep learning models undertrained on RNA?
   - Test set bias toward template-friendly structures?

2. **Can we combine best of both worlds?**
   - Template-guided deep learning
   - Hybrid scoring functions
   - Learned template selection

3. **Data scarcity problem**
   - How to leverage protein structure knowledge?
   - Transfer learning opportunities
   - Synthetic data generation

## References

### Competition Results
- [Stanford RNA 3D Folding Part 1](https://www.kaggle.com/competitions/stanford-rna-3d-folding)
- [Template-based RNA structure prediction (bioRxiv 2025)](https://www.biorxiv.org/content/10.64898/2025.12.30.696949v1.full)

### Deep Learning Methods
- [RhoFold+ (Nature Methods 2024)](https://www.nature.com/articles/s41592-024-02487-0)
- [AlphaFold 3 (Nature 2024)](https://www.nature.com/articles/s41586-024-07487-w)
- [RoseTTAFoldNA (Nature Methods 2023)](https://www.nature.com/articles/s41592-023-02086-5)

### Benchmarks & Challenges
- [RNA-Puzzles](http://rnapuzzles.org/)
- [CASP RNA Targets](https://predictioncenter.org/)
- [DAS Lab Publications](https://daslab.stanford.edu/news)

---

*This document will be updated as we progress through the competition and gather more insights.*
