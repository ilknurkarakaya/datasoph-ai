import React from 'react';

interface VisualizationBlockProps {
  type: 'chart' | 'graph' | 'plot' | 'table';
  data: any;
  title?: string;
  description?: string;
}

const VisualizationBlock: React.FC<VisualizationBlockProps> = ({
  type,
  data,
  title,
  description
}) => {
  return (
    <div className="bg-gray-50 dark:bg-gray-800 rounded-lg p-6 mb-4">
      {title && (
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
          {title}
        </h3>
      )}
      {description && (
        <p className="text-gray-600 dark:text-gray-300 mb-4">
          {description}
        </p>
      )}
      <div className="bg-white dark:bg-gray-700 rounded border p-4">
        <div className="text-center text-gray-500 dark:text-gray-400">
          <div className="mb-2">📊</div>
          <div>Visualization: {type}</div>
          <div className="text-xs mt-2 font-mono bg-gray-100 dark:bg-gray-600 p-2 rounded">
            {JSON.stringify(data, null, 2).substring(0, 200)}
            {JSON.stringify(data, null, 2).length > 200 ? '...' : ''}
          </div>
        </div>
      </div>
    </div>
  );
};

export default VisualizationBlock; 