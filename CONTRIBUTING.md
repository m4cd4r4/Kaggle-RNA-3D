# Contributing to Kaggle-RNA-3D

Thank you for your interest in contributing to the RNA 3D Folding Dashboard project! 🧬

## 🎯 Ways to Contribute

### 1. **Report Bugs**
Found a bug? Please [open an issue](https://github.com/m4cd4r4/Kaggle-RNA-3D/issues/new) with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python/Node version)

### 2. **Suggest Features**
Have an idea? [Create a feature request](https://github.com/m4cd4r4/Kaggle-RNA-3D/issues/new) with:
- Clear description of the feature
- Use case / motivation
- Proposed implementation (optional)

### 3. **Improve Documentation**
- Fix typos or unclear explanations
- Add examples or tutorials
- Improve code comments
- Translate documentation

### 4. **Submit Code**
- Fix bugs
- Add new UI components to the design system
- Improve Python utilities
- Optimize performance
- Add tests

## 🚀 Getting Started

### Fork & Clone

```bash
# Fork the repository on GitHub
# Then clone your fork
git clone https://github.com/YOUR_USERNAME/Kaggle-RNA-3D.git
cd Kaggle-RNA-3D

# Add upstream remote
git remote add upstream https://github.com/m4cd4r4/Kaggle-RNA-3D.git
```

### Setup Development Environment

**Python:**
```bash
conda create -n rna3d python=3.11
conda activate rna3d
pip install -r requirements.txt
pip install -r requirements-dev.txt  # If available
```

**Web Dashboard:**
```bash
cd web
npm install
npm run dev  # Start development server
```

## 📝 Development Workflow

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-description
```

### 2. Make Changes

- Write clear, readable code
- Follow existing code style
- Add comments for complex logic
- Update documentation if needed

### 3. Test Your Changes

**Python:**
```bash
pytest tests/
```

**Web:**
```bash
cd web
npm run build  # Ensure it builds
```

### 4. Commit

Write clear commit messages:

```bash
git add .
git commit -m "feat: Add circular progress component to design system"
# or
git commit -m "fix: Correct TM-score calculation for edge case"
```

**Commit Message Format:**
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes (formatting)
- `refactor:` Code refactoring
- `test:` Adding or updating tests
- `chore:` Maintenance tasks

### 5. Push & Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then [create a Pull Request](https://github.com/m4cd4r4/Kaggle-RNA-3D/compare) with:
- Clear title describing the change
- Description of what changed and why
- Screenshots (for UI changes)
- Link to related issue (if applicable)

## 🎨 Design System Contributions

When adding new UI components:

1. **Create component** in `web/components/ui/YourComponent.tsx`
2. **Export** from `web/components/ui/index.ts`
3. **Document** with JSDoc comments and usage examples
4. **Add section** to `web/DESIGN_SYSTEM.md`
5. **Test** in multiple pages to ensure consistency

### Component Template

```tsx
/**
 * YourComponent - Brief description
 *
 * Usage:
 *   <YourComponent variant="default">Content</YourComponent>
 */

import React from 'react';

interface YourComponentProps {
  children: React.ReactNode;
  variant?: 'default' | 'primary';
  className?: string;
}

export function YourComponent({
  children,
  variant = 'default',
  className = '',
}: YourComponentProps) {
  // Implementation
  return <div className={className}>{children}</div>;
}
```

## 🐍 Python Code Guidelines

- **Follow PEP 8** style guide
- **Type hints** for function arguments and return values
- **Docstrings** for all public functions/classes
- **Unit tests** for new functionality
- **NumPy/PyTorch** conventions for scientific code

### Python Function Template

```python
def calculate_tm_score(
    pred_coords: np.ndarray,
    true_coords: np.ndarray,
    normalize: bool = True
) -> float:
    """
    Calculate TM-score between predicted and true structures.

    Args:
        pred_coords: Predicted 3D coordinates, shape (N, 3)
        true_coords: Ground truth coordinates, shape (N, 3)
        normalize: Whether to normalize by sequence length

    Returns:
        TM-score value between 0 and 1

    Raises:
        ValueError: If coordinate shapes don't match
    """
    # Implementation
    pass
```

## 🧪 Testing

### Python Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_metrics.py

# Run with coverage
pytest --cov=src tests/
```

### Web Tests

```bash
cd web

# Type checking
npm run type-check

# Build test
npm run build
```

## 📖 Documentation Style

- Use **clear, concise** language
- Include **code examples**
- Add **screenshots** for UI components
- Keep **up-to-date** with code changes

## ❓ Questions?

- [Open a discussion](https://github.com/m4cd4r4/Kaggle-RNA-3D/discussions) (if enabled)
- [Create an issue](https://github.com/m4cd4r4/Kaggle-RNA-3D/issues/new)
- Comment on existing issues

## 🎯 Priority Areas

We especially welcome contributions in:

1. **Design System Components**
   - Additional chart types for metrics
   - Data table enhancements
   - Form validation components

2. **Python Utilities**
   - Additional evaluation metrics
   - Data augmentation techniques
   - Visualization improvements

3. **Documentation**
   - Tutorial notebooks
   - Video demos
   - Blog posts about the design system

4. **Performance**
   - Optimize TM-score calculation
   - Parallelize data loading
   - Reduce dashboard bundle size

## 📜 Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on the code, not the person
- Help others learn and grow

## 🙏 Thank You!

Every contribution helps make this project better for the entire Kaggle community. Thank you for taking the time to contribute! 🎉

---

**Questions?** Open an issue or discussion. We're here to help!
