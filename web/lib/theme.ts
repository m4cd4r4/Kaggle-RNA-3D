/**
 * Kaggle Dashboard Design System
 *
 * A reusable theme configuration for Kaggle competition dashboards.
 * Import this file to access design tokens, color palettes, and utilities.
 *
 * Usage:
 *   import { theme, colors, gradients } from '@/lib/theme';
 */

// ============================================
// COLOR PALETTE - Kaggle-inspired
// ============================================

export const colors = {
  // Primary - Kaggle Blue
  primary: {
    50: '#e6f4ff',
    100: '#b3dcff',
    200: '#80c4ff',
    300: '#4dacff',
    400: '#20a0ff',
    500: '#0090ff', // Main Kaggle blue
    600: '#007acc',
    700: '#005a99',
    800: '#003a66',
    900: '#001a33',
  },

  // Secondary - Purple accent
  secondary: {
    50: '#f5f0ff',
    100: '#e0d4ff',
    200: '#c9b3ff',
    300: '#b293ff',
    400: '#9b73ff',
    500: '#8b5cf6',
    600: '#7c3aed',
    700: '#6d28d9',
    800: '#5b21b6',
    900: '#4c1d95',
  },

  // Accent - For highlights and CTAs
  accent: {
    cyan: '#06b6d4',
    teal: '#14b8a6',
    emerald: '#10b981',
    amber: '#f59e0b',
    rose: '#f43f5e',
  },

  // Status colors
  status: {
    success: '#22c55e',
    warning: '#eab308',
    error: '#ef4444',
    info: '#3b82f6',
    running: '#8b5cf6',
    queued: '#f59e0b',
    completed: '#22c55e',
    failed: '#ef4444',
  },

  // Neutral grays
  neutral: {
    50: '#fafafa',
    100: '#f4f4f5',
    200: '#e4e4e7',
    300: '#d4d4d8',
    400: '#a1a1aa',
    500: '#71717a',
    600: '#52525b',
    700: '#3f3f46',
    800: '#27272a',
    900: '#18181b',
  },
};

// ============================================
// GRADIENTS - Reusable gradient definitions
// ============================================

export const gradients = {
  // Primary gradients
  primary: 'bg-gradient-to-r from-blue-500 to-purple-600',
  primaryHover: 'bg-gradient-to-r from-blue-600 to-purple-700',

  // Background gradients
  bgLight: 'bg-gradient-to-br from-blue-50 via-white to-purple-50',
  bgSubtle: 'bg-gradient-to-br from-gray-50 via-white to-blue-50',
  bgDark: 'bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900',

  // Card gradients
  cardGold: 'bg-gradient-to-br from-yellow-50 to-yellow-100',
  cardSilver: 'bg-gradient-to-br from-gray-50 to-gray-100',
  cardBronze: 'bg-gradient-to-br from-orange-50 to-orange-100',

  // Button gradients
  btnPrimary: 'bg-gradient-to-r from-blue-500 to-purple-500',
  btnSuccess: 'bg-gradient-to-r from-green-500 to-emerald-500',
  btnWarning: 'bg-gradient-to-r from-yellow-500 to-orange-500',
  btnDanger: 'bg-gradient-to-r from-red-500 to-rose-500',

  // Metric gradients
  metricPositive: 'bg-gradient-to-r from-emerald-400 to-cyan-400',
  metricNegative: 'bg-gradient-to-r from-rose-400 to-orange-400',
  metricNeutral: 'bg-gradient-to-r from-gray-400 to-slate-400',
};

// ============================================
// TYPOGRAPHY
// ============================================

export const typography = {
  // Font families
  fontFamily: {
    sans: 'Inter, system-ui, -apple-system, sans-serif',
    mono: 'JetBrains Mono, Fira Code, Consolas, monospace',
  },

  // Font sizes
  fontSize: {
    xs: '0.75rem',    // 12px
    sm: '0.875rem',   // 14px
    base: '1rem',     // 16px
    lg: '1.125rem',   // 18px
    xl: '1.25rem',    // 20px
    '2xl': '1.5rem',  // 24px
    '3xl': '1.875rem',// 30px
    '4xl': '2.25rem', // 36px
    '5xl': '3rem',    // 48px
  },

  // Line heights
  lineHeight: {
    tight: 1.25,
    normal: 1.5,
    relaxed: 1.75,
  },
};

// ============================================
// SPACING & SIZING
// ============================================

export const spacing = {
  // Component padding
  cardPadding: 'p-6',
  sectionPadding: 'p-8',
  containerPadding: 'px-4 sm:px-6 lg:px-8',

  // Gaps
  gridGap: 'gap-6',
  stackGap: 'space-y-4',
  inlineGap: 'space-x-4',

  // Border radius
  radius: {
    sm: 'rounded',
    md: 'rounded-lg',
    lg: 'rounded-xl',
    xl: 'rounded-2xl',
    full: 'rounded-full',
  },
};

// ============================================
// SHADOWS & EFFECTS
// ============================================

export const effects = {
  // Shadows
  shadow: {
    sm: 'shadow-sm',
    md: 'shadow-md',
    lg: 'shadow-lg',
    xl: 'shadow-xl',
    '2xl': 'shadow-2xl',
  },

  // Glassmorphism
  glass: 'bg-white/70 backdrop-blur-lg border border-white/20 shadow-xl',
  glassDark: 'bg-gray-900/80 backdrop-blur-lg border border-gray-700/50 shadow-xl',

  // Hover effects
  hoverScale: 'hover:scale-105 transition-transform duration-300',
  hoverLift: 'hover:-translate-y-1 hover:shadow-xl transition-all duration-300',
  hoverGlow: 'hover:shadow-lg hover:shadow-blue-500/20 transition-all duration-300',
};

// ============================================
// ANIMATION PRESETS
// ============================================

export const animations = {
  // Transitions
  fast: 'transition-all duration-150',
  normal: 'transition-all duration-300',
  slow: 'transition-all duration-500',

  // Keyframes (defined in globals.css)
  pulse: 'animate-pulse',
  spin: 'animate-spin',
  bounce: 'animate-bounce',
  fadeIn: 'animate-fade-in',
  slideUp: 'animate-slide-up',
};

// ============================================
// COMPONENT PRESETS
// ============================================

export const components = {
  // Cards
  card: 'bg-white/70 backdrop-blur-lg border border-white/20 shadow-xl rounded-xl p-6',
  cardHover: 'bg-white/70 backdrop-blur-lg border border-white/20 shadow-xl rounded-xl p-6 hover:shadow-2xl hover:scale-105 transition-all duration-300',

  // Buttons
  btn: {
    base: 'px-4 py-2 rounded-lg font-medium transition-all duration-300',
    primary: 'px-6 py-3 bg-gradient-to-r from-blue-500 to-purple-500 text-white rounded-lg font-medium hover:shadow-lg hover:scale-105 transition-all',
    secondary: 'px-6 py-3 bg-white/70 backdrop-blur-lg border border-gray-200 rounded-lg font-medium hover:shadow-lg hover:scale-105 transition-all',
    ghost: 'px-4 py-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-all',
  },

  // Inputs
  input: 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all',
  select: 'px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent',

  // Badges
  badge: {
    base: 'px-2 py-0.5 text-xs font-medium rounded-full',
    success: 'bg-green-100 text-green-800',
    warning: 'bg-yellow-100 text-yellow-800',
    error: 'bg-red-100 text-red-800',
    info: 'bg-blue-100 text-blue-800',
    purple: 'bg-purple-100 text-purple-800',
  },
};

// ============================================
// LAYOUT PRESETS
// ============================================

export const layout = {
  // Container
  container: 'max-w-7xl mx-auto px-4 sm:px-6 lg:px-8',
  containerWide: 'max-w-screen-2xl mx-auto px-4 sm:px-6 lg:px-8',

  // Grid layouts
  grid: {
    cols2: 'grid grid-cols-1 md:grid-cols-2 gap-6',
    cols3: 'grid grid-cols-1 md:grid-cols-3 gap-6',
    cols4: 'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6',
    dashboard: 'grid grid-cols-1 lg:grid-cols-3 gap-8',
  },

  // Flex layouts
  flex: {
    center: 'flex items-center justify-center',
    between: 'flex items-center justify-between',
    start: 'flex items-center justify-start',
    col: 'flex flex-col',
  },
};

// ============================================
// COMPETITION-SPECIFIC TOKENS
// ============================================

export const kaggle = {
  // Medal colors
  medals: {
    gold: { bg: 'bg-yellow-100', text: 'text-yellow-900', border: 'border-yellow-200' },
    silver: { bg: 'bg-gray-100', text: 'text-gray-900', border: 'border-gray-200' },
    bronze: { bg: 'bg-orange-100', text: 'text-orange-900', border: 'border-orange-200' },
  },

  // Ranking tiers
  tiers: {
    grandmaster: '#d4af37',
    master: '#c0c0c0',
    expert: '#cd7f32',
    contributor: '#4a90d9',
    novice: '#22c55e',
  },

  // Competition status
  status: {
    active: { bg: 'bg-green-100', text: 'text-green-800', dot: 'bg-green-500' },
    upcoming: { bg: 'bg-blue-100', text: 'text-blue-800', dot: 'bg-blue-500' },
    ended: { bg: 'bg-gray-100', text: 'text-gray-600', dot: 'bg-gray-400' },
  },
};

// ============================================
// METRIC DISPLAY HELPERS
// ============================================

export const metrics = {
  // Score formatting
  formatScore: (score: number, precision: number = 3): string => {
    return score.toFixed(precision);
  },

  // Score color based on value (higher is better)
  getScoreColor: (score: number, thresholds = { good: 0.6, excellent: 0.8 }): string => {
    if (score >= thresholds.excellent) return 'text-green-600';
    if (score >= thresholds.good) return 'text-blue-600';
    return 'text-gray-600';
  },

  // Improvement indicator
  getImprovementIndicator: (current: number, previous: number): { icon: string; color: string; text: string } => {
    const diff = current - previous;
    const percent = previous !== 0 ? ((diff / previous) * 100).toFixed(1) : '0';

    if (diff > 0) return { icon: '+', color: 'text-green-600', text: `+${percent}%` };
    if (diff < 0) return { icon: '-', color: 'text-red-600', text: `${percent}%` };
    return { icon: '=', color: 'text-gray-500', text: '0%' };
  },
};

// ============================================
// FULL THEME EXPORT
// ============================================

export const theme = {
  colors,
  gradients,
  typography,
  spacing,
  effects,
  animations,
  components,
  layout,
  kaggle,
  metrics,
};

export default theme;
