/**
 * Card Component - Reusable card with glassmorphism effect
 *
 * Usage:
 *   <Card>Content</Card>
 *   <Card variant="hover" className="custom-class">Content</Card>
 */

import React from 'react';
import { components, effects } from '@/lib/theme';

interface CardProps {
  children: React.ReactNode;
  variant?: 'default' | 'hover' | 'glass' | 'solid';
  className?: string;
  onClick?: () => void;
}

export function Card({ children, variant = 'default', className = '', onClick }: CardProps) {
  const baseClasses = 'rounded-xl p-6';

  const variantClasses = {
    default: components.card,
    hover: components.cardHover,
    glass: effects.glass + ' rounded-xl p-6',
    solid: 'bg-white shadow-lg rounded-xl p-6',
  };

  return (
    <div
      className={`${baseClasses} ${variantClasses[variant]} ${className}`}
      onClick={onClick}
    >
      {children}
    </div>
  );
}

interface StatCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  icon?: React.ReactNode;
  trend?: {
    value: number;
    label: string;
  };
  color?: 'blue' | 'purple' | 'green' | 'yellow' | 'red';
}

export function StatCard({ title, value, subtitle, icon, trend, color = 'blue' }: StatCardProps) {
  const colorClasses = {
    blue: 'from-blue-500 to-cyan-500',
    purple: 'from-purple-500 to-pink-500',
    green: 'from-green-500 to-emerald-500',
    yellow: 'from-yellow-500 to-orange-500',
    red: 'from-red-500 to-rose-500',
  };

  return (
    <Card variant="hover">
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <p className="text-sm font-medium text-gray-600 mb-1">{title}</p>
          <p className="text-3xl font-bold text-gray-900">{value}</p>
          {subtitle && <p className="text-sm text-gray-500 mt-1">{subtitle}</p>}
          {trend && (
            <div className={`mt-2 flex items-center text-sm ${trend.value >= 0 ? 'text-green-600' : 'text-red-600'}`}>
              <span className="font-medium">{trend.value >= 0 ? '+' : ''}{trend.value}%</span>
              <span className="ml-2 text-gray-500">{trend.label}</span>
            </div>
          )}
        </div>
        {icon && (
          <div className={`p-3 bg-gradient-to-br ${colorClasses[color]} rounded-lg text-white`}>
            {icon}
          </div>
        )}
      </div>
    </Card>
  );
}

interface MetricCardProps {
  name: string;
  value: number;
  previousValue?: number;
  format?: 'decimal' | 'percentage' | 'integer';
  precision?: number;
}

export function MetricCard({ name, value, previousValue, format = 'decimal', precision = 3 }: MetricCardProps) {
  const formatValue = (val: number) => {
    switch (format) {
      case 'percentage':
        return `${(val * 100).toFixed(precision)}%`;
      case 'integer':
        return Math.round(val).toString();
      default:
        return val.toFixed(precision);
    }
  };

  const improvement = previousValue !== undefined ? value - previousValue : null;
  const improvementPercent = improvement !== null && previousValue !== 0
    ? ((improvement / previousValue) * 100).toFixed(1)
    : null;

  return (
    <Card>
      <div className="text-center">
        <p className="text-sm font-medium text-gray-600 mb-2">{name}</p>
        <p className="text-2xl font-bold text-gray-900">{formatValue(value)}</p>
        {improvement !== null && (
          <div className={`mt-1 text-sm font-medium ${improvement >= 0 ? 'text-green-600' : 'text-red-600'}`}>
            {improvement >= 0 ? '↑' : '↓'} {Math.abs(improvement).toFixed(precision)}
            {improvementPercent && ` (${improvement >= 0 ? '+' : ''}${improvementPercent}%)`}
          </div>
        )}
      </div>
    </Card>
  );
}
