# Kaggle Dashboard Design System

A comprehensive, reusable design system for building modern Kaggle competition dashboards.

## 🎨 Overview

This design system provides a consistent, beautiful foundation for Kaggle project dashboards with:
- **Glassmorphism UI** - Modern frosted glass aesthetic
- **Kaggle-inspired colors** - Blues, purples, and accent colors
- **Reusable components** - Drop-in UI components
- **Type-safe** - Full TypeScript support
- **Responsive** - Mobile-first design
- **Accessible** - WCAG 2.1 compliant

## 📦 Installation

The design system is already included in this project. For new projects:

1. Copy these directories:
   ```
   /lib/theme.ts
   /components/ui/
   ```

2. Import in your components:
   ```tsx
   import { theme } from '@/lib/theme';
   import { Card, Button, Badge } from '@/components/ui';
   ```

## 🎯 Quick Start

### Using Theme Tokens

```tsx
import { colors, gradients, components } from '@/lib/theme';

// Use color tokens
<div className="text-primary-500">Kaggle Blue</div>

// Use gradient presets
<div className={gradients.primary}>Beautiful gradient</div>

// Use component presets
<div className={components.card}>Glassmorphic card</div>
```

### Using UI Components

```tsx
import { Card, Button, Badge, StatCard } from '@/components/ui';

function Dashboard() {
  return (
    <div>
      <StatCard
        title="TM-Score"
        value="0.825"
        trend={{ value: 12.5, label: "from last run" }}
        icon={<ChartIcon />}
        color="blue"
      />

      <Card variant="hover">
        <h3>My Content</h3>
        <Button variant="primary" onClick={handleClick}>
          Run Experiment
        </Button>
      </Card>
    </div>
  );
}
```

## 🎨 Color Palette

### Primary Colors (Kaggle Blue)

```tsx
colors.primary[500]  // Main Kaggle blue: #0090ff
colors.primary[600]  // Darker blue
colors.primary[400]  // Lighter blue
```

### Secondary Colors (Purple Accent)

```tsx
colors.secondary[500] // Purple: #8b5cf6
colors.secondary[600] // Darker purple
```

### Status Colors

```tsx
colors.status.success  // Green: #22c55e
colors.status.warning  // Yellow: #eab308
colors.status.error    // Red: #ef4444
colors.status.running  // Purple: #8b5cf6
```

### Accent Colors

```tsx
colors.accent.cyan     // #06b6d4
colors.accent.emerald  // #10b981
colors.accent.amber    // #f59e0b
```

## 🎭 Gradients

### Background Gradients

```tsx
<div className={gradients.bgLight}>
  {/* Light blue-purple background */}
</div>

<div className={gradients.bgSubtle}>
  {/* Subtle gray-blue background */}
</div>
```

### Button Gradients

```tsx
<button className={gradients.btnPrimary}>
  Primary Button
</button>

<button className={gradients.btnSuccess}>
  Success Button
</button>
```

### Metric Gradients

```tsx
<div className={gradients.metricPositive}>
  {/* Emerald-cyan gradient for positive metrics */}
</div>

<div className={gradients.metricNegative}>
  {/* Rose-orange gradient for negative metrics */}
</div>
```

## 🧩 Components

### Cards

```tsx
import { Card, StatCard, MetricCard } from '@/components/ui';

// Basic card
<Card>Content here</Card>

// Card with hover effect
<Card variant="hover">Hover me!</Card>

// Stat card with icon and trend
<StatCard
  title="Total Questions"
  value="10,395"
  subtitle="Across 24 certifications"
  icon={<DatabaseIcon />}
  trend={{ value: 5.2, label: "vs last month" }}
  color="purple"
/>

// Metric card with comparison
<MetricCard
  name="TM-Score"
  value={0.825}
  previousValue={0.798}
  format="decimal"
  precision={3}
/>
```

### Buttons

```tsx
import { Button, IconButton } from '@/components/ui';

// Primary button
<Button variant="primary" onClick={handleClick}>
  Run Model
</Button>

// Secondary button
<Button variant="secondary" size="sm">
  Cancel
</Button>

// Success button
<Button variant="success" fullWidth>
  Submit Prediction
</Button>

// Icon button
<IconButton
  icon={<TrashIcon />}
  variant="danger"
  onClick={handleDelete}
  tooltip="Delete experiment"
/>
```

### Badges

```tsx
import { Badge, StatusBadge, MedalBadge, TierBadge } from '@/components/ui';

// Basic badge
<Badge variant="success">Completed</Badge>

// Status badge
<StatusBadge status="running" />

// Medal badge (for rankings)
<MedalBadge rank={1} size="md" />

// Tier badge (Kaggle tiers)
<TierBadge tier="expert" />
```

### Progress Indicators

```tsx
import { ProgressBar, CircularProgress, StepProgress } from '@/components/ui';

// Linear progress bar
<ProgressBar
  value={75}
  max={100}
  label="Training Progress"
  color="blue"
/>

// Circular progress
<CircularProgress
  value={60}
  size="lg"
  color="green"
/>

// Step progress
<StepProgress
  steps={["Data", "Train", "Evaluate", "Submit"]}
  currentStep={2}
/>
```

### Tables

```tsx
import { DataTable } from '@/components/ui';

// Sortable data table
<DataTable
  data={experiments}
  columns={[
    { key: 'name', header: 'Name', sortable: true },
    { key: 'score', header: 'Score', sortable: true, align: 'right' },
    {
      key: 'status',
      header: 'Status',
      render: (exp) => <StatusBadge status={exp.status} />
    },
  ]}
  onRowClick={(experiment) => viewDetails(experiment)}
/>
```

### Form Inputs

```tsx
import { Input, TextArea, Select, Checkbox } from '@/components/ui';

// Text input
<Input
  label="Model Name"
  value={modelName}
  onChange={setModelName}
  placeholder="Enter model name"
  required
/>

// Select dropdown
<Select
  label="Architecture"
  options={architectures}
  value={selected}
  onChange={setSelected}
/>

// Checkbox
<Checkbox
  label="Use data augmentation"
  checked={useAugmentation}
  onChange={setUseAugmentation}
/>
```

## 🎭 Effects & Animations

### Glassmorphism

```tsx
<div className={effects.glass}>
  Frosted glass effect
</div>

<div className={effects.glassDark}>
  Dark mode glass
</div>
```

### Hover Effects

```tsx
<div className={effects.hoverScale}>
  Scales up on hover
</div>

<div className={effects.hoverLift}>
  Lifts up with shadow
</div>

<div className={effects.hoverGlow}>
  Glows blue on hover
</div>
```

### Transitions

```tsx
<div className={animations.fast}>Fast transition</div>
<div className={animations.normal}>Normal transition</div>
<div className={animations.slow}>Slow transition</div>
```

## 📐 Layout System

### Containers

```tsx
<div className={layout.container}>
  {/* Max-width 7xl container */}
</div>

<div className={layout.containerWide}>
  {/* Max-width 2xl container */}
</div>
```

### Grid Layouts

```tsx
<div className={layout.grid.cols3}>
  {/* 3-column grid */}
  <Card>Column 1</Card>
  <Card>Column 2</Card>
  <Card>Column 3</Card>
</div>

<div className={layout.grid.dashboard}>
  {/* Dashboard layout (1 col mobile, 3 cols desktop) */}
</div>
```

### Flex Layouts

```tsx
<div className={layout.flex.between}>
  {/* Space between items */}
</div>

<div className={layout.flex.center}>
  {/* Center items */}
</div>
```

## 🏆 Competition-Specific Features

### Medal Colors

```tsx
<div className={kaggle.medals.gold.bg}>
  Gold medal background
</div>

<Badge className={kaggle.medals.silver.text}>
  Silver text
</Badge>
```

### Ranking Tiers

```tsx
<TierBadge tier="grandmaster" />
<TierBadge tier="master" />
<TierBadge tier="expert" />
```

### Competition Status

```tsx
<Badge className={kaggle.status.active.bg + ' ' + kaggle.status.active.text}>
  <span className={kaggle.status.active.dot + ' w-2 h-2 rounded-full'}></span>
  Active
</Badge>
```

## 📊 Metric Helpers

### Format Scores

```tsx
import { metrics } from '@/lib/theme';

// Format score with precision
metrics.formatScore(0.82456, 3) // "0.825"

// Get color based on score
<span className={metrics.getScoreColor(0.85)}>
  Excellent score
</span>

// Get improvement indicator
const indicator = metrics.getImprovementIndicator(0.85, 0.80);
// { icon: '+', color: 'text-green-600', text: '+6.3%' }
```

## 🚀 Example: Complete Dashboard

```tsx
import { Card, StatCard, Button, Badge, ProgressBar } from '@/components/ui';
import { layout, gradients } from '@/lib/theme';

export default function Dashboard() {
  return (
    <div className={gradients.bgLight + ' min-h-screen p-8'}>
      <div className={layout.container}>
        <h1 className="text-4xl font-bold mb-8">RNA 3D Folding</h1>

        {/* Stats Grid */}
        <div className={layout.grid.cols4 + ' mb-8'}>
          <StatCard
            title="Best TM-Score"
            value="0.825"
            trend={{ value: 12.5, label: "improvement" }}
            color="blue"
          />
          <StatCard
            title="Experiments"
            value="47"
            subtitle="23 completed"
            color="purple"
          />
          <StatCard
            title="Training Time"
            value="18.5h"
            color="green"
          />
          <StatCard
            title="Leaderboard"
            value="#23"
            trend={{ value: 5, label: "rank up" }}
            color="yellow"
          />
        </div>

        {/* Main Content */}
        <div className={layout.grid.dashboard}>
          <div className="lg:col-span-2">
            <Card>
              <h2 className="text-xl font-bold mb-4">Training Progress</h2>
              <ProgressBar
                value={75}
                label="Epoch 45/60"
                color="blue"
              />
              <div className="mt-4 flex gap-2">
                <Button variant="primary">Resume Training</Button>
                <Button variant="secondary">View Logs</Button>
              </div>
            </Card>
          </div>

          <div>
            <Card>
              <h2 className="text-xl font-bold mb-4">Status</h2>
              <div className="space-y-2">
                <Badge variant="success" dot>Training Active</Badge>
                <p className="text-sm text-gray-600">GPU: NVIDIA A100</p>
                <p className="text-sm text-gray-600">Time: 3h 24m</p>
              </div>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
}
```

## 🎨 Customization

### Tailwind Configuration

The theme integrates with Tailwind CSS. To customize, edit `tailwind.config.ts`:

```ts
import { colors } from './lib/theme';

export default {
  theme: {
    extend: {
      colors: {
        primary: colors.primary,
        secondary: colors.secondary,
      },
    },
  },
};
```

### Global Styles

Add custom animations and utilities in `globals.css`:

```css
@layer utilities {
  .glassmorphism {
    @apply bg-white/70 backdrop-blur-lg border border-white/20 shadow-xl;
  }

  .stat-card {
    @apply glassmorphism rounded-xl p-6 hover:shadow-2xl transition-all duration-300 hover:scale-105;
  }
}
```

## 📱 Responsive Design

All components are mobile-first and responsive:

```tsx
{/* Stack on mobile, grid on desktop */}
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
  <Card>Card 1</Card>
  <Card>Card 2</Card>
  <Card>Card 3</Card>
</div>
```

## ♿ Accessibility

All components follow accessibility best practices:
- Semantic HTML
- ARIA labels where needed
- Keyboard navigation support
- Focus indicators
- Sufficient color contrast

## 📝 Best Practices

1. **Use theme tokens** - Always use `theme.colors.primary[500]` instead of hardcoded hex values
2. **Leverage components** - Use pre-built components for consistency
3. **Follow naming conventions** - Use descriptive names (e.g., `handleSubmit`, not `f1`)
4. **Keep it simple** - Don't over-engineer; use what you need
5. **Test responsive** - Always test on mobile, tablet, and desktop

## 🔄 Reusing Across Projects

To use this design system in other Kaggle projects:

1. **Copy the files**:
   ```
   cp -r lib/theme.ts ../new-project/lib/
   cp -r components/ui ../new-project/components/
   ```

2. **Update branding** (optional):
   - Change primary colors in `theme.ts`
   - Update competition-specific content
   - Customize gradient presets

3. **Import and use**:
   ```tsx
   import { theme } from '@/lib/theme';
   import { Card, Button } from '@/components/ui';
   ```

## 📚 Resources

- **Tailwind CSS**: https://tailwindcss.com/docs
- **React**: https://react.dev
- **Next.js**: https://nextjs.org/docs
- **Glassmorphism**: https://glassmorphism.com

## 🤝 Contributing

To add new components:

1. Create component in `/components/ui/YourComponent.tsx`
2. Export from `/components/ui/index.ts`
3. Document usage in this file
4. Add examples

---

**Version**: 1.0.0
**Last Updated**: January 2026
**License**: MIT (reusable across all Kaggle projects)
