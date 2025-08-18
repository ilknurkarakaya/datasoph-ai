import React, { useState } from 'react';
import { 
  Play, 
  Square, 
  Plus, 
  Save, 
  Download, 
  Code, 
  FileText,
  Terminal,
  Database,
  Zap,
  Loader2,
  CheckCircle,
  AlertCircle
} from 'lucide-react';
import { ViewType } from '../../types/navigation.ts';

interface CodeEnvironmentProps {
  files: any[];
  onNavigate: (view: ViewType) => void;
}

interface CodeCell {
  id: string;
  type: 'code' | 'markdown';
  content: string;
  output?: string;
  isRunning?: boolean;
  hasError?: boolean;
}

const CodeEnvironment: React.FC<CodeEnvironmentProps> = ({
  files,
  onNavigate
}) => {
  const [cells, setCells] = useState<CodeCell[]>([
    {
      id: '1',
      type: 'markdown',
      content: '# Data Analysis Notebook\n\nThis notebook contains your data analysis workflow. Add code cells below to start analyzing your data.'
    },
    {
      id: '2', 
      type: 'code',
      content: '# Import libraries\nimport pandas as pd\nimport numpy as np\nimport matplotlib.pyplot as plt\nimport seaborn as sns\n\n# Configure plotting\nplt.style.use(\'seaborn\')\nsns.set_palette("husl")\n\nprint("Libraries loaded successfully!")',
      output: 'Libraries loaded successfully!'
    }
  ]);

  const [selectedLanguage, setSelectedLanguage] = useState('python');
  const [notebookName, setNotebookName] = useState('Untitled Notebook');

  const languages = [
    { id: 'python', name: 'Python', icon: '🐍' },
    { id: 'r', name: 'R', icon: '📊' },
    { id: 'sql', name: 'SQL', icon: '🗃️' }
  ];

  const sampleCode = {
    python: `# Load and explore data
df = pd.read_csv('your_data.csv')
print(f"Dataset shape: {df.shape}")
print("\\nFirst 5 rows:")
df.head()`,
    r: `# Load and explore data
library(readr)
library(dplyr)

df <- read_csv('your_data.csv')
cat("Dataset dimensions:", dim(df), "\\n")
head(df)`,
    sql: `-- Explore data structure
SELECT 
  COUNT(*) as total_rows,
  COUNT(DISTINCT customer_id) as unique_customers
FROM your_table
LIMIT 10;`
  };

  const addCell = (type: 'code' | 'markdown', afterId?: string) => {
    const newCell: CodeCell = {
      id: Date.now().toString(),
      type,
      content: type === 'code' ? sampleCode[selectedLanguage as keyof typeof sampleCode] : '# New markdown cell\n\nAdd your content here...'
    };

    if (afterId) {
      const index = cells.findIndex(cell => cell.id === afterId);
      const newCells = [...cells];
      newCells.splice(index + 1, 0, newCell);
      setCells(newCells);
    } else {
      setCells([...cells, newCell]);
    }
  };

  const updateCell = (id: string, content: string) => {
    setCells(cells.map(cell => 
      cell.id === id ? { ...cell, content } : cell
    ));
  };

  const runCell = async (id: string) => {
    setCells(cells.map(cell => 
      cell.id === id ? { ...cell, isRunning: true, hasError: false } : cell
    ));

    // Simulate code execution
    await new Promise(resolve => setTimeout(resolve, 1000 + Math.random() * 2000));

    const cell = cells.find(c => c.id === id);
    if (cell && cell.type === 'code') {
      // Generate mock output based on code content
      let output = '';
      if (cell.content.includes('df.shape')) {
        output = 'Dataset shape: (12847, 23)\n\nFirst 5 rows:\n   customer_id  age  income  purchase_amount\n0          1   25   45000           1250\n1          2   34   52000           2100\n2          3   28   48000           1750\n3          4   45   67000           3200\n4          5   31   51000           1900';
      } else if (cell.content.includes('import')) {
        output = 'Libraries loaded successfully!';
      } else if (cell.content.includes('describe')) {
        output = '       age        income  purchase_amount\ncount  12847.0    12847.0       12847.0\nmean    35.2      54230.5        2156.3\nstd      8.7      15420.8         987.2\nmin     18.0      25000.0         500.0\nmax     65.0      95000.0        5000.0';
      } else {
        output = `Executed successfully!\n${Math.random() > 0.8 ? '[Warning] Consider adding error handling' : ''}`;
      }

      setCells(cells.map(cell => 
        cell.id === id ? { 
          ...cell, 
          isRunning: false, 
          output, 
          hasError: Math.random() > 0.9 
        } : cell
      ));
    }
  };

  const deleteCell = (id: string) => {
    setCells(cells.filter(cell => cell.id !== id));
  };

  return (
    <div className="h-full flex bg-gray-50">
      {/* Sidebar */}
      <div className="w-80 bg-white border-r border-gray-200 flex flex-col">
        {/* Header */}
        <div className="p-4 border-b border-gray-200">
          <input
            type="text"
            value={notebookName}
            onChange={(e) => setNotebookName(e.target.value)}
            className="text-lg font-semibold text-gray-900 bg-transparent border-none outline-none w-full"
          />
          <p className="text-sm text-gray-600">Interactive code environment</p>
        </div>

        {/* Language Selector */}
        <div className="p-4 border-b border-gray-200">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Language
          </label>
          <select
            value={selectedLanguage}
            onChange={(e) => setSelectedLanguage(e.target.value)}
            className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            {languages.map((lang) => (
              <option key={lang.id} value={lang.id}>
                {lang.icon} {lang.name}
              </option>
            ))}
          </select>
        </div>

        {/* Available Datasets */}
        <div className="p-4 border-b border-gray-200">
          <h3 className="text-sm font-medium text-gray-700 mb-3">Available Datasets</h3>
          <div className="space-y-2">
            {files.length === 0 ? (
              <div className="text-center py-4">
                <Database className="w-8 h-8 text-gray-400 mx-auto mb-2" />
                <p className="text-sm text-gray-600">No datasets uploaded</p>
                <button 
                  onClick={() => onNavigate('data')}
                  className="text-xs text-blue-600 hover:text-blue-700 mt-1"
                >
                  Upload data
                </button>
              </div>
            ) : (
              files.slice(0, 5).map((file) => (
                <div key={file.id} className="flex items-center gap-2 p-2 bg-gray-50 rounded-lg">
                  <FileText className="w-4 h-4 text-gray-500" />
                  <div className="flex-1 min-w-0">
                    <div className="text-sm font-medium text-gray-900 truncate">
                      {file.name}
                    </div>
                    <div className="text-xs text-gray-500">
                      {(file.size / 1024).toFixed(1)} KB
                    </div>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>

        {/* Code Snippets */}
        <div className="flex-1 p-4">
          <h3 className="text-sm font-medium text-gray-700 mb-3">Code Snippets</h3>
          <div className="space-y-2">
            {[
              { name: 'Load Data', code: 'df = pd.read_csv("file.csv")' },
              { name: 'Data Info', code: 'df.info()' },
              { name: 'Summary Stats', code: 'df.describe()' },
              { name: 'Plot Distribution', code: 'df.hist(figsize=(12, 8))' },
              { name: 'Correlation Matrix', code: 'sns.heatmap(df.corr(), annot=True)' }
            ].map((snippet) => (
              <button
                key={snippet.name}
                onClick={() => addCell('code')}
                className="w-full text-left p-2 bg-gray-50 hover:bg-gray-100 rounded-lg text-sm"
              >
                <div className="font-medium text-gray-900">{snippet.name}</div>
                <div className="text-xs text-gray-600 font-mono">{snippet.code}</div>
              </button>
            ))}
          </div>
        </div>

        {/* Actions */}
        <div className="p-4 border-t border-gray-200">
          <div className="space-y-2">
            <button 
              onClick={() => onNavigate('chat')}
              className="w-full px-3 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm"
            >
              <Zap className="w-4 h-4 inline mr-2" />
              Ask AI for Code
            </button>
            <div className="grid grid-cols-2 gap-2">
              <button className="px-3 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors text-sm">
                <Save className="w-4 h-4 inline mr-1" />
                Save
              </button>
              <button className="px-3 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors text-sm">
                <Download className="w-4 h-4 inline mr-1" />
                Export
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Main Notebook Area */}
      <div className="flex-1 flex flex-col">
        {/* Toolbar */}
        <div className="bg-white border-b border-gray-200 p-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <button
                onClick={() => addCell('code')}
                className="px-3 py-2 bg-blue-50 text-blue-700 rounded-lg hover:bg-blue-100 transition-colors text-sm"
              >
                <Plus className="w-4 h-4 inline mr-1" />
                Code
              </button>
              <button
                onClick={() => addCell('markdown')}
                className="px-3 py-2 bg-gray-50 text-gray-700 rounded-lg hover:bg-gray-100 transition-colors text-sm"
              >
                <Plus className="w-4 h-4 inline mr-1" />
                Markdown
              </button>
              <div className="w-px h-6 bg-gray-300" />
              <button className="px-3 py-2 bg-green-50 text-green-700 rounded-lg hover:bg-green-100 transition-colors text-sm">
                <Play className="w-4 h-4 inline mr-1" />
                Run All
              </button>
            </div>

            <div className="flex items-center gap-2 text-sm text-gray-600">
              <div className="w-2 h-2 bg-green-500 rounded-full"></div>
              <span>Kernel Ready</span>
            </div>
          </div>
        </div>

        {/* Notebook Cells */}
        <div className="flex-1 overflow-auto p-6 space-y-4">
          {cells.map((cell, index) => (
            <div key={cell.id} className="bg-white rounded-lg border border-gray-200 overflow-hidden">
              {/* Cell Header */}
              <div className="flex items-center justify-between p-3 bg-gray-50 border-b border-gray-200">
                <div className="flex items-center gap-2">
                  <span className="text-sm text-gray-500">
                    {cell.type === 'code' ? `[${index}]` : 'MD'}
                  </span>
                  <span className="text-sm font-medium text-gray-700">
                    {cell.type === 'code' ? `${selectedLanguage.toUpperCase()} Code` : 'Markdown'}
                  </span>
                  {cell.isRunning && (
                    <Loader2 className="w-4 h-4 text-blue-600 animate-spin" />
                  )}
                  {cell.hasError && (
                    <AlertCircle className="w-4 h-4 text-red-600" />
                  )}
                  {cell.output && !cell.isRunning && !cell.hasError && (
                    <CheckCircle className="w-4 h-4 text-green-600" />
                  )}
                </div>
                
                <div className="flex items-center gap-1">
                  {cell.type === 'code' && (
                    <button
                      onClick={() => runCell(cell.id)}
                      disabled={cell.isRunning}
                      className="p-1 text-gray-500 hover:text-green-600 disabled:opacity-50"
                    >
                      <Play className="w-4 h-4" />
                    </button>
                  )}
                  <button
                    onClick={() => deleteCell(cell.id)}
                    className="p-1 text-gray-500 hover:text-red-600"
                  >
                    <Square className="w-4 h-4" />
                  </button>
                </div>
              </div>

              {/* Cell Content */}
              <div className="p-4">
                <textarea
                  value={cell.content}
                  onChange={(e) => updateCell(cell.id, e.target.value)}
                  className={`w-full resize-none border-none outline-none font-mono text-sm ${
                    cell.type === 'code' ? 'bg-gray-900 text-green-400 p-3 rounded' : 'bg-white text-gray-900'
                  }`}
                  rows={Math.max(3, cell.content.split('\n').length)}
                  placeholder={cell.type === 'code' ? 'Enter your code here...' : 'Enter markdown content...'}
                />
              </div>

              {/* Cell Output */}
              {cell.output && (
                <div className="border-t border-gray-200 bg-gray-50 p-4">
                  <div className="text-xs text-gray-500 mb-2">Output:</div>
                  <pre className="text-sm text-gray-900 font-mono whitespace-pre-wrap bg-white p-3 rounded border">
                    {cell.output}
                  </pre>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default CodeEnvironment; 