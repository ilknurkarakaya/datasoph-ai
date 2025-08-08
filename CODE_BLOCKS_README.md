# DataSoph AI - Professional Code Blocks

A comprehensive, Claude-style code block system built specifically for DataSoph AI with advanced features for data science workflows.

## 🌟 Features

### Core Features
- **Syntax Highlighting**: 20+ languages with custom DataSoph themes
- **Copy to Clipboard**: One-click code copying with visual feedback
- **Download as File**: Save code with proper file extensions
- **Execute Code**: Run Python, SQL, R, and JavaScript code (integration ready)
- **Line Numbers**: Optional line numbering for better readability
- **Language Detection**: Automatic language identification and icon display

### Data Science Specific
- **Analysis Context**: Display dataset info, complexity levels, runtime estimates
- **Template Library**: Pre-built templates for common data science tasks
- **Enhanced Metadata**: Memory usage, dataset dimensions, analysis type
- **Notebook Integration**: One-click export to Jupyter notebooks
- **Script Generation**: Save analysis scripts with metadata headers

### Professional UI/UX
- **Claude-Style Design**: Professional dark theme with modern aesthetics
- **Responsive Layout**: Mobile-optimized code viewing
- **Accessibility**: Keyboard navigation, screen reader support, high contrast mode
- **Progressive Enhancement**: Works without JavaScript, enhanced with it

## 🚀 Quick Start

### Basic Usage

```tsx
import { CodeBlock } from '@/components/UI';

// Simple code block
<CodeBlock
  code="print('Hello, DataSoph!')"
  language="python"
  executable={true}
/>

// Enhanced data science code block
import { DataScienceCodeBlock } from '@/components/UI';

<DataScienceCodeBlock
  code={pythonAnalysisCode}
  language="python"
  title="Customer Segmentation Analysis"
  analysisType="eda"
  complexity="intermediate"
  estimatedRuntime="5-10 minutes"
  datasetInfo={{
    name: "customers.csv",
    rows: 50000,
    columns: 12
  }}
  executable={true}
/>
```

### AI Message Integration

```tsx
import { AIMessage } from '@/components/UI';

// Automatically parses and renders code blocks in AI responses
<AIMessage 
  content={aiResponseWithCode} 
  executable={true} 
/>
```

## 📦 Component Reference

### CodeBlock

The main code block component with syntax highlighting and actions.

```tsx
interface CodeBlockProps {
  code: string;                    // Source code to display
  language: string;                // Programming language
  title?: string;                  // Optional title
  fileName?: string;               // Optional filename
  executable?: boolean;            // Show execute button
  showLineNumbers?: boolean;       // Show line numbers (default: true)
  className?: string;              // Additional CSS classes
}
```

**Supported Languages:**
- Python, JavaScript, TypeScript, SQL, R
- Java, C++, C#, PHP, Ruby, Go, Rust, Swift
- HTML, CSS, JSON, YAML, XML, Markdown
- Bash/Shell scripts

### DataScienceCodeBlock

Enhanced code block with data science context and metadata.

```tsx
interface DataScienceCodeBlockProps extends CodeBlockProps {
  datasetInfo?: {
    name: string;
    rows: number;
    columns: number;
    size?: string;
  };
  analysisType?: 'eda' | 'modeling' | 'visualization' | 'statistics' | 'preprocessing' | 'feature-engineering';
  complexity?: 'beginner' | 'intermediate' | 'advanced';
  estimatedRuntime?: string;
  memoryUsage?: string;
}
```

### InlineCode

For inline code snippets within text.

```tsx
// Simple inline code
<InlineCode>pandas.DataFrame</InlineCode>

// With language context
<InlineCode language="python">df.head()</InlineCode>
```

### AIMessage

Intelligent message parser that detects and renders code blocks in AI responses.

```tsx
interface AIMessageProps {
  content: string;        // Message content with embedded code blocks
  executable?: boolean;   // Enable execution buttons
}
```

**Markdown Code Block Detection:**
```markdown
```python Data Analysis
import pandas as pd
df = pd.read_csv('data.csv')
print(df.shape)
```

The parser automatically detects:
- Language specification
- Optional titles after language
- Filename detection (files with extensions)
- Inline code with `backticks`

## 🎨 Themes and Styling

### Built-in Themes

```tsx
import { getThemeByName } from '@/components/UI';

const themes = {
  'datasoph-dark': 'Default dark theme',
  'datasoph-light': 'Professional light theme', 
  'datasoph-high-contrast': 'Accessibility-focused theme'
};

// Apply theme
const theme = getThemeByName('datasoph-dark');
```

### Custom CSS Classes

```css
/* Available CSS custom properties */
.code-block-container {
  --code-bg: #1a1e23;
  --code-border: #374151;
  --code-text: #e1e4e8;
  --code-accent: #3b82f6;
}

/* Responsive breakpoints */
@media (max-width: 768px) {
  .code-block-container {
    margin: 0.75rem -1rem;
    border-radius: 0;
  }
}
```

## 📚 Code Templates

Pre-built templates for common data science workflows.

```tsx
import { getTemplatesByLanguage, getTemplatesByCategory } from '@/components/UI';

// Get all Python templates
const pythonTemplates = getTemplatesByLanguage('python');

// Get all EDA templates across languages
const edaTemplates = getTemplatesByCategory('data-analysis');

// Template structure
interface CodeTemplate {
  name: string;
  description: string;
  code: string;
  language: string;
  category: 'data-analysis' | 'machine-learning' | 'visualization' | 'statistics' | 'preprocessing';
  complexity: 'beginner' | 'intermediate' | 'advanced';
  estimatedRuntime?: string;
  memoryUsage?: string;
}
```

### Available Templates

**Python Templates:**
- `dataAnalysis`: Comprehensive EDA workflow
- `machineLearning`: End-to-end ML pipeline
- `visualization`: Data visualization suite

**SQL Templates:**
- `exploration`: Data profiling queries
- `analytics`: Customer analytics and BI

**R Templates:**
- `statistics`: Statistical analysis workflow

## 🔧 Integration Guide

### 1. Installation

Already included in DataSoph AI. Dependencies:
- `react-syntax-highlighter`: Syntax highlighting
- `prism-react-renderer`: Advanced highlighting features
- `lucide-react`: Icons

### 2. ChatInterface Integration

```tsx
// In your chat message rendering
{message.type === 'assistant' ? (
  <AIMessage content={message.content} executable={true} />
) : (
  <div>{message.content}</div>
)}
```

### 3. Custom Execution Handler

```tsx
// Implement code execution
const handleCodeExecution = async (code: string, language: string) => {
  // Send to your backend execution service
  const result = await executeCode(code, language);
  return result;
};

// Pass to components
<CodeBlock 
  code={code}
  language={language}
  executable={true}
  onExecute={handleCodeExecution}
/>
```

## 🎯 Data Science Features

### Analysis Context

```tsx
<DataScienceCodeBlock
  code={code}
  language="python"
  analysisType="eda"
  complexity="intermediate"
  estimatedRuntime="5-10 minutes"
  memoryUsage="< 1GB"
  datasetInfo={{
    name: "sales_data.csv",
    rows: 100000,
    columns: 15,
    size: "25MB"
  }}
/>
```

### Quick Actions

- **🚀 Run Analysis**: Execute code with DataSoph AI
- **📋 Add to Notebook**: Export to Jupyter notebook
- **💾 Save as Script**: Download with metadata headers

### Complexity Indicators

- **🟢 Beginner**: Basic operations, well-documented
- **🔵 Intermediate**: Moderate complexity, some domain knowledge required  
- **🔴 Advanced**: Complex algorithms, expert-level understanding needed

## 📱 Mobile Experience

- Responsive design adapts to mobile screens
- Touch-friendly buttons and interactions
- Horizontal scrolling for wide code blocks
- Optimized font sizes for readability

## ♿ Accessibility

- **Keyboard Navigation**: Full keyboard support
- **Screen Readers**: Proper ARIA labels and structure
- **High Contrast**: Dedicated high contrast theme
- **Reduced Motion**: Respects user motion preferences
- **Color Blind Friendly**: Carefully chosen color palettes

## 🔒 Security

- **Code Sandboxing**: All execution is sandboxed (implementation dependent)
- **Input Validation**: Code content is sanitized
- **XSS Prevention**: Proper content escaping
- **CSP Compliance**: Content Security Policy compatible

## 🚀 Performance

- **Lazy Loading**: Syntax highlighter loads on demand
- **Code Splitting**: Components are bundled separately
- **Memoization**: Expensive operations are cached
- **Virtual Scrolling**: Large code blocks scroll efficiently

## 🧪 Testing

```bash
# Run component tests
npm test

# Visual regression testing
npm run test:visual

# Accessibility testing
npm run test:a11y
```

## 📈 Analytics

Track code block usage:

```tsx
// Built-in analytics hooks
const { trackCodeCopy, trackCodeExecution } = useCodeAnalytics();

// Automatic tracking of:
// - Code copies
// - Download actions
// - Execution attempts
// - Language popularity
// - Template usage
```

## 🛠️ Customization

### Custom Language Support

```tsx
// Add custom language
const customLanguageConfig = {
  'datalog': {
    icon: '🔍',
    displayName: 'Datalog',
    executable: false,
    fileExtension: 'dl'
  }
};
```

### Custom Themes

```tsx
// Create custom theme
const myTheme = {
  'code[class*="language-"]': {
    color: '#your-color',
    background: '#your-bg'
  },
  // ... other styles
};
```

## 🤝 Contributing

1. Follow existing code style and patterns
2. Add tests for new features
3. Update documentation
4. Ensure accessibility compliance
5. Test across different devices and browsers

## 📄 License

Part of DataSoph AI - MIT License

---

## 🎉 Examples

### Complete Integration Example

```tsx
import React from 'react';
import { AIMessage, CodeBlock, DataScienceCodeBlock } from '@/components/UI';

const DataAnalysisChat = () => {
  const aiResponse = `Here's your analysis:

\`\`\`python Sales Analysis
import pandas as pd
df = pd.read_csv('sales.csv')
print(df.describe())
\`\`\`

Use \`df.head()\` to see the first few rows.`;

  return (
    <div className="chat-container">
      {/* AI message with embedded code */}
      <AIMessage content={aiResponse} executable={true} />
      
      {/* Standalone enhanced code block */}
      <DataScienceCodeBlock
        code="# Advanced ML Pipeline"
        language="python"
        analysisType="modeling"
        complexity="advanced"
        datasetInfo={{ name: "data.csv", rows: 50000, columns: 10 }}
        executable={true}
      />
    </div>
  );
};
```

This creates a professional, feature-rich code block system that enhances the DataSoph AI experience with Claude-level quality and data science specific functionality. 