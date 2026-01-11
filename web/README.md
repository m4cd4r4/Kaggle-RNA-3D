# RNA 3D Folding Dashboard

A modern, interactive dashboard for the Stanford RNA 3D Folding Part 2 Kaggle competition.

## 🚀 Quick Start

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Open http://localhost:3008
```

## 📁 Project Structure

```
web/
├── app/                        # Next.js App Router pages
│   ├── layout.tsx             # Root layout with navigation
│   ├── page.tsx               # Homepage with stats & winners
│   ├── visualizer/            # 3D RNA structure visualizer
│   ├── metrics/               # Metrics dashboard with charts
│   └── experiments/           # Experiment tracker
├── components/
│   └── ui/                    # Reusable UI component library
│       ├── Card.tsx           # Card components (Card, StatCard, MetricCard)
│       ├── Button.tsx         # Button components
│       ├── Badge.tsx          # Status badges & medals
│       ├── Progress.tsx       # Progress indicators
│       ├── Table.tsx          # Data tables
│       ├── Input.tsx          # Form inputs
│       └── index.ts           # Centralized exports
├── lib/
│   └── theme.ts               # Complete design system (400+ tokens)
├── DESIGN_SYSTEM.md           # Full documentation (500+ lines)
└── DESIGN_SYSTEM_SUMMARY.md   # Quick reference guide
```

## 🎨 Design System

This project includes a complete, reusable design system built for Kaggle competition dashboards.

### Quick Import

```tsx
import { Card, StatCard, Button, Badge } from '@/components/ui';
import { layout, gradients } from '@/lib/theme';
```

### Example Usage

```tsx
// Stats card with trend
<StatCard
  title="Best TM-Score"
  value="0.825"
  trend={{ value: 12.5, label: "improvement" }}
  icon={<ChartIcon />}
  color="blue"
/>

// Winner card with medal
<Card variant="solid" className={gradients.cardGold}>
  <MedalBadge rank={1} />
  <h3>john</h3>
  <p>0.671 TM-Score</p>
</Card>
```

### 26 Components Available

- **Cards**: Card, StatCard, MetricCard
- **Buttons**: Button, IconButton
- **Badges**: Badge, StatusBadge, MedalBadge, TierBadge
- **Progress**: ProgressBar, CircularProgress, StepProgress, LoadingSpinner
- **Tables**: Table, TableHeader, TableBody, TableRow, TableHead, TableCell, SortableTableHead, DataTable
- **Inputs**: Input, TextArea, Select, Checkbox, RadioGroup

See [DESIGN_SYSTEM.md](DESIGN_SYSTEM.md) for full documentation.

## 📊 Features

### Homepage
- Hero section with competition info
- 4 stat cards (dataset size, models, best score, deadline)
- Part 1 winners showcase with medal badges
- Approach comparison (template-based vs deep learning)
- Quick action buttons

### 3D Visualizer (`/visualizer`)
- 2D linear RNA structure view
- 3D helix backbone visualization
- Custom sequence input
- Sample structure selector

### Metrics Dashboard (`/metrics`)
- Training progress line chart
- Part 1 winners comparison bar chart
- Current vs target radar chart
- Epoch progress area chart
- All powered by Recharts

### Experiment Tracker (`/experiments`)
- Experiment list with status indicators
- Sortable data table
- Experiment details panel
- New experiment modal
- Hyperparameter display

## 🎯 Competition Details

- **Name**: Stanford RNA 3D Folding Part 2
- **Prize**: $75,000
- **Deadline**: March 18, 2026
- **Dataset**: 23.4 GB
- **Metrics**: TM-score, RMSD, GDT-TS, lDDT

### Key Insight from Part 1

All top 3 teams used **template-based modeling** (no deep learning) and outperformed AlphaFold 3:
- 🥇 john: 0.671 TM-Score
- 🥈 odat: 0.653 TM-Score
- 🥉 Eigen: 0.615 TM-Score

## 🛠️ Tech Stack

- **Framework**: Next.js 15 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Charts**: Recharts
- **Design**: Glassmorphism UI
- **Port**: 3008

## 🔄 Reusability

This design system is **100% reusable** for other Kaggle competitions:

1. Copy `lib/theme.ts` and `components/ui/` to new project
2. Update primary colors (optional)
3. Import and use components
4. Build dashboards 3x faster

## 📚 Documentation

- **[DESIGN_SYSTEM.md](DESIGN_SYSTEM.md)** - Complete component documentation
- **[DESIGN_SYSTEM_SUMMARY.md](DESIGN_SYSTEM_SUMMARY.md)** - Quick reference guide
- **Inline JSDoc** - All components have usage examples

## 🎨 Customization

### Change Primary Color

Edit `lib/theme.ts`:

```ts
export const colors = {
  primary: {
    500: '#0090ff', // Change this to your color
  },
};
```

### Add Custom Component

1. Create in `components/ui/YourComponent.tsx`
2. Export from `components/ui/index.ts`
3. Use: `import { YourComponent } from '@/components/ui';`

## 🚀 Next Steps

1. **Run the dashboard**: `npm run dev`
2. **Explore pages**: Navigate through all sections
3. **Check design system**: Read [DESIGN_SYSTEM.md](DESIGN_SYSTEM.md)
4. **Customize**: Update colors, add features
5. **Reuse**: Copy to other Kaggle projects

## 📝 License

Reusable across all Kaggle projects - no restrictions.

---

**Built with** 🧬 RNA 3D Folding in mind, **designed for** 🏆 Kaggle competitions.
