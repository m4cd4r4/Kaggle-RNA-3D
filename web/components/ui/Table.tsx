/**
 * Table Component - Data tables with sorting and styling
 *
 * Usage:
 *   <Table>
 *     <TableHeader>
 *       <TableRow>
 *         <TableHead>Name</TableHead>
 *       </TableRow>
 *     </TableHeader>
 *     <TableBody>
 *       <TableRow>
 *         <TableCell>Data</TableCell>
 *       </TableRow>
 *     </TableBody>
 *   </Table>
 */

import React from 'react';

interface TableProps {
  children: React.ReactNode;
  className?: string;
}

export function Table({ children, className = '' }: TableProps) {
  return (
    <div className={`overflow-x-auto ${className}`}>
      <table className="min-w-full divide-y divide-gray-200">
        {children}
      </table>
    </div>
  );
}

export function TableHeader({ children, className = '' }: TableProps) {
  return (
    <thead className={`bg-gray-50 ${className}`}>
      {children}
    </thead>
  );
}

export function TableBody({ children, className = '' }: TableProps) {
  return (
    <tbody className={`bg-white divide-y divide-gray-200 ${className}`}>
      {children}
    </tbody>
  );
}

interface TableRowProps {
  children: React.ReactNode;
  onClick?: () => void;
  className?: string;
  hover?: boolean;
}

export function TableRow({ children, onClick, className = '', hover = true }: TableRowProps) {
  const hoverClass = hover ? 'hover:bg-gray-50' : '';
  const clickableClass = onClick ? 'cursor-pointer' : '';

  return (
    <tr
      className={`${hoverClass} ${clickableClass} ${className}`}
      onClick={onClick}
    >
      {children}
    </tr>
  );
}

interface TableCellProps {
  children: React.ReactNode;
  className?: string;
  align?: 'left' | 'center' | 'right';
}

export function TableHead({ children, className = '', align = 'left' }: TableCellProps) {
  const alignClass = {
    left: 'text-left',
    center: 'text-center',
    right: 'text-right',
  };

  return (
    <th
      className={`px-6 py-3 text-xs font-medium text-gray-500 uppercase tracking-wider ${alignClass[align]} ${className}`}
    >
      {children}
    </th>
  );
}

export function TableCell({ children, className = '', align = 'left' }: TableCellProps) {
  const alignClass = {
    left: 'text-left',
    center: 'text-center',
    right: 'text-right',
  };

  return (
    <td className={`px-6 py-4 whitespace-nowrap text-sm text-gray-900 ${alignClass[align]} ${className}`}>
      {children}
    </td>
  );
}

interface SortableTableHeadProps {
  children: React.ReactNode;
  sortKey: string;
  currentSort?: { key: string; direction: 'asc' | 'desc' };
  onSort?: (key: string) => void;
  className?: string;
}

export function SortableTableHead({
  children,
  sortKey,
  currentSort,
  onSort,
  className = '',
}: SortableTableHeadProps) {
  const isActive = currentSort?.key === sortKey;
  const direction = isActive ? currentSort?.direction : undefined;

  return (
    <th
      className={`px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100 ${className}`}
      onClick={() => onSort?.(sortKey)}
    >
      <div className="flex items-center space-x-1">
        <span>{children}</span>
        <span className="text-gray-400">
          {direction === 'asc' && '↑'}
          {direction === 'desc' && '↓'}
          {!isActive && '⇅'}
        </span>
      </div>
    </th>
  );
}

interface DataTableProps<T> {
  data: T[];
  columns: {
    key: string;
    header: string;
    render?: (item: T) => React.ReactNode;
    align?: 'left' | 'center' | 'right';
    sortable?: boolean;
  }[];
  onRowClick?: (item: T) => void;
  emptyMessage?: string;
  className?: string;
}

export function DataTable<T extends Record<string, any>>({
  data,
  columns,
  onRowClick,
  emptyMessage = 'No data available',
  className = '',
}: DataTableProps<T>) {
  const [sortConfig, setSortConfig] = React.useState<{ key: string; direction: 'asc' | 'desc' } | null>(null);

  const handleSort = (key: string) => {
    setSortConfig(current => {
      if (current?.key === key) {
        return { key, direction: current.direction === 'asc' ? 'desc' : 'asc' };
      }
      return { key, direction: 'asc' };
    });
  };

  const sortedData = React.useMemo(() => {
    if (!sortConfig) return data;

    return [...data].sort((a, b) => {
      const aVal = a[sortConfig.key];
      const bVal = b[sortConfig.key];

      if (aVal < bVal) return sortConfig.direction === 'asc' ? -1 : 1;
      if (aVal > bVal) return sortConfig.direction === 'asc' ? 1 : -1;
      return 0;
    });
  }, [data, sortConfig]);

  if (data.length === 0) {
    return (
      <div className="text-center py-12 text-gray-500">
        {emptyMessage}
      </div>
    );
  }

  return (
    <Table className={className}>
      <TableHeader>
        <TableRow hover={false}>
          {columns.map(column => (
            column.sortable ? (
              <SortableTableHead
                key={column.key}
                sortKey={column.key}
                currentSort={sortConfig || undefined}
                onSort={handleSort}
              >
                {column.header}
              </SortableTableHead>
            ) : (
              <TableHead key={column.key} align={column.align}>
                {column.header}
              </TableHead>
            )
          ))}
        </TableRow>
      </TableHeader>
      <TableBody>
        {sortedData.map((item, index) => (
          <TableRow
            key={index}
            onClick={() => onRowClick?.(item)}
            hover={!!onRowClick}
          >
            {columns.map(column => (
              <TableCell key={column.key} align={column.align}>
                {column.render ? column.render(item) : item[column.key]}
              </TableCell>
            ))}
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
}
