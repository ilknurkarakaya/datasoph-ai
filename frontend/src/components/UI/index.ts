// UI Components Exports
export { default as CodeBlock } from './CodeBlock';
export { default as InlineCode } from './InlineCode';
export { default as DataScienceCodeBlock } from './DataScienceCodeBlock';
export { default as DropdownMenu } from './DropdownMenu';
export { default as VisualizationBlock } from './VisualizationBlock';

// Message parsing utilities
export { 
  AIMessage, 
  MessageWithCodeBlocks, 
  parseMessageWithCode, 
  processInlineCode 
} from './MessageParser';

// Code templates and themes
export { 
  codeTemplates, 
  getTemplatesByLanguage, 
  getTemplatesByCategory, 
  getAllTemplates 
} from './CodeTemplates';

export { 
  dataSophTheme, 
  dataSophLightTheme, 
  dataSophHighContrastTheme, 
  getThemeByName 
} from './SyntaxTheme';

// Type exports
export type { CodeTemplate } from './CodeTemplates'; 