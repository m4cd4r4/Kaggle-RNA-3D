/**
 * Badge Component - Status indicators and labels
 *
 * Usage:
 *   <Badge variant="success">Completed</Badge>
 *   <Badge variant="warning" size="sm">Pending</Badge>
 */

import React from 'react';

interface BadgeProps {
  children: React.ReactNode;
  variant?: 'default' | 'success' | 'warning' | 'error' | 'info' | 'purple' | 'cyan';
  size?: 'sm' | 'md' | 'lg';
  className?: string;
  dot?: boolean;
}

export function Badge({ children, variant = 'default', size = 'md', className = '', dot = false }: BadgeProps) {
  const baseClasses = 'inline-flex items-center font-medium rounded-full';

  const variantClasses = {
    default: 'bg-gray-100 text-gray-800',
    success: 'bg-green-100 text-green-800',
    warning: 'bg-yellow-100 text-yellow-800',
    error: 'bg-red-100 text-red-800',
    info: 'bg-blue-100 text-blue-800',
    purple: 'bg-purple-100 text-purple-800',
    cyan: 'bg-cyan-100 text-cyan-800',
  };

  const sizeClasses = {
    sm: 'px-2 py-0.5 text-xs',
    md: 'px-2.5 py-1 text-sm',
    lg: 'px-3 py-1.5 text-base',
  };

  const dotColors = {
    default: 'bg-gray-500',
    success: 'bg-green-500',
    warning: 'bg-yellow-500',
    error: 'bg-red-500',
    info: 'bg-blue-500',
    purple: 'bg-purple-500',
    cyan: 'bg-cyan-500',
  };

  return (
    <span className={`${baseClasses} ${variantClasses[variant]} ${sizeClasses[size]} ${className}`}>
      {dot && <span className={`w-1.5 h-1.5 rounded-full mr-1.5 ${dotColors[variant]}`}></span>}
      {children}
    </span>
  );
}

interface StatusBadgeProps {
  status: 'running' | 'queued' | 'completed' | 'failed' | 'pending' | 'active' | 'upcoming' | 'ended';
  showDot?: boolean;
  className?: string;
}

export function StatusBadge({ status, showDot = true, className = '' }: StatusBadgeProps) {
  const statusConfig = {
    running: { label: 'Running', variant: 'info' as const },
    queued: { label: 'Queued', variant: 'warning' as const },
    completed: { label: 'Completed', variant: 'success' as const },
    failed: { label: 'Failed', variant: 'error' as const },
    pending: { label: 'Pending', variant: 'default' as const },
    active: { label: 'Active', variant: 'success' as const },
    upcoming: { label: 'Upcoming', variant: 'info' as const },
    ended: { label: 'Ended', variant: 'default' as const },
  };

  const config = statusConfig[status];

  return (
    <Badge variant={config.variant} dot={showDot} className={className}>
      {config.label}
    </Badge>
  );
}

interface MedalBadgeProps {
  rank: 1 | 2 | 3 | number;
  size?: 'sm' | 'md' | 'lg';
  className?: string;
}

export function MedalBadge({ rank, size = 'md', className = '' }: MedalBadgeProps) {
  const medals = {
    1: { emoji: '🥇', color: 'bg-yellow-100 text-yellow-900 border border-yellow-200' },
    2: { emoji: '🥈', color: 'bg-gray-100 text-gray-900 border border-gray-200' },
    3: { emoji: '🥉', color: 'bg-orange-100 text-orange-900 border border-orange-200' },
  };

  const medal = rank <= 3 ? medals[rank as 1 | 2 | 3] : null;

  const sizeClasses = {
    sm: 'px-2 py-0.5 text-xs',
    md: 'px-2.5 py-1 text-sm',
    lg: 'px-3 py-1.5 text-base',
  };

  if (!medal) {
    return (
      <span className={`inline-flex items-center font-medium rounded-full bg-blue-100 text-blue-800 ${sizeClasses[size]} ${className}`}>
        #{rank}
      </span>
    );
  }

  return (
    <span className={`inline-flex items-center font-medium rounded-full ${medal.color} ${sizeClasses[size]} ${className}`}>
      <span className="mr-1">{medal.emoji}</span>
      #{rank}
    </span>
  );
}

interface TierBadgeProps {
  tier: 'grandmaster' | 'master' | 'expert' | 'contributor' | 'novice';
  className?: string;
}

export function TierBadge({ tier, className = '' }: TierBadgeProps) {
  const tierConfig = {
    grandmaster: { label: 'Grandmaster', color: 'bg-yellow-500 text-white' },
    master: { label: 'Master', color: 'bg-gray-400 text-white' },
    expert: { label: 'Expert', color: 'bg-orange-600 text-white' },
    contributor: { label: 'Contributor', color: 'bg-blue-500 text-white' },
    novice: { label: 'Novice', color: 'bg-green-500 text-white' },
  };

  const config = tierConfig[tier];

  return (
    <span className={`inline-flex items-center px-3 py-1 text-xs font-bold rounded-full ${config.color} ${className}`}>
      {config.label}
    </span>
  );
}
