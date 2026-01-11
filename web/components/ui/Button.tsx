/**
 * Button Component - Reusable button with multiple variants
 *
 * Usage:
 *   <Button variant="primary" onClick={handleClick}>Click me</Button>
 *   <Button variant="ghost" size="sm">Small button</Button>
 */

import React from 'react';

interface ButtonProps {
  children: React.ReactNode;
  variant?: 'primary' | 'secondary' | 'ghost' | 'success' | 'warning' | 'danger' | 'outline';
  size?: 'sm' | 'md' | 'lg';
  className?: string;
  onClick?: () => void;
  disabled?: boolean;
  type?: 'button' | 'submit' | 'reset';
  fullWidth?: boolean;
}

export function Button({
  children,
  variant = 'primary',
  size = 'md',
  className = '',
  onClick,
  disabled = false,
  type = 'button',
  fullWidth = false,
}: ButtonProps) {
  const baseClasses = 'font-medium rounded-lg transition-all duration-300 focus:outline-none focus:ring-2 focus:ring-offset-2';

  const variantClasses = {
    primary: 'bg-gradient-to-r from-blue-500 to-purple-500 text-white hover:shadow-lg hover:scale-105 focus:ring-blue-500',
    secondary: 'bg-white/70 backdrop-blur-lg border border-gray-200 text-gray-700 hover:shadow-lg hover:scale-105 focus:ring-gray-300',
    ghost: 'text-gray-600 hover:text-gray-900 hover:bg-gray-100 focus:ring-gray-300',
    success: 'bg-gradient-to-r from-green-500 to-emerald-500 text-white hover:shadow-lg hover:scale-105 focus:ring-green-500',
    warning: 'bg-gradient-to-r from-yellow-500 to-orange-500 text-white hover:shadow-lg hover:scale-105 focus:ring-yellow-500',
    danger: 'bg-gradient-to-r from-red-500 to-rose-500 text-white hover:shadow-lg hover:scale-105 focus:ring-red-500',
    outline: 'border-2 border-blue-500 text-blue-500 hover:bg-blue-50 focus:ring-blue-500',
  };

  const sizeClasses = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-6 py-3 text-base',
    lg: 'px-8 py-4 text-lg',
  };

  const disabledClasses = disabled ? 'opacity-50 cursor-not-allowed hover:scale-100' : '';
  const widthClasses = fullWidth ? 'w-full' : '';

  return (
    <button
      type={type}
      className={`${baseClasses} ${variantClasses[variant]} ${sizeClasses[size]} ${disabledClasses} ${widthClasses} ${className}`}
      onClick={onClick}
      disabled={disabled}
    >
      {children}
    </button>
  );
}

interface IconButtonProps {
  icon: React.ReactNode;
  onClick?: () => void;
  variant?: 'default' | 'primary' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  className?: string;
  tooltip?: string;
}

export function IconButton({ icon, onClick, variant = 'default', size = 'md', className = '', tooltip }: IconButtonProps) {
  const sizeClasses = {
    sm: 'p-1.5',
    md: 'p-2',
    lg: 'p-3',
  };

  const variantClasses = {
    default: 'text-gray-600 hover:text-gray-900 hover:bg-gray-100',
    primary: 'text-blue-600 hover:text-blue-700 hover:bg-blue-50',
    danger: 'text-red-600 hover:text-red-700 hover:bg-red-50',
  };

  return (
    <button
      onClick={onClick}
      className={`rounded-lg transition-all duration-200 ${sizeClasses[size]} ${variantClasses[variant]} ${className}`}
      title={tooltip}
    >
      {icon}
    </button>
  );
}
