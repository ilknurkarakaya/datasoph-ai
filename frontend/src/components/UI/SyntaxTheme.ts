// Custom DataSoph AI Syntax Highlighting Themes
export const dataSophTheme = {
  'code[class*="language-"]': {
    color: '#e1e4e8',
    background: 'none',
    fontFamily: 'ui-monospace, SFMono-Regular, "SF Mono", Consolas, "Liberation Mono", Menlo, monospace',
    fontSize: '14px',
    lineHeight: '1.5',
    whiteSpace: 'pre',
    wordSpacing: 'normal',
    wordBreak: 'normal',
    wordWrap: 'normal',
    tabSize: '4',
    hyphens: 'none'
  },
  'pre[class*="language-"]': {
    color: '#e1e4e8',
    background: '#1a1e23',
    fontFamily: 'ui-monospace, SFMono-Regular, "SF Mono", Consolas, "Liberation Mono", Menlo, monospace',
    fontSize: '14px',
    lineHeight: '1.5',
    whiteSpace: 'pre',
    wordSpacing: 'normal',
    wordBreak: 'normal',
    wordWrap: 'normal',
    tabSize: '4',
    hyphens: 'none',
    padding: '1rem',
    margin: '0',
    overflow: 'auto',
    borderRadius: '0'
  },
  ':not(pre) > code[class*="language-"]': {
    background: '#1a1e23',
    padding: '0.2em 0.4em',
    borderRadius: '3px',
    whiteSpace: 'normal'
  },
  comment: {
    color: '#6a737d',
    fontStyle: 'italic'
  },
  prolog: {
    color: '#6a737d',
    fontStyle: 'italic'
  },
  doctype: {
    color: '#6a737d',
    fontStyle: 'italic'
  },
  cdata: {
    color: '#6a737d',
    fontStyle: 'italic'
  },
  punctuation: {
    color: '#e1e4e8'
  },
  '.namespace': {
    opacity: '0.7'
  },
  property: {
    color: '#79b8ff'
  },
  tag: {
    color: '#85e89d'
  },
  boolean: {
    color: '#f97583'
  },
  number: {
    color: '#f97583'
  },
  constant: {
    color: '#f97583'
  },
  symbol: {
    color: '#f97583'
  },
  deleted: {
    color: '#f97583'
  },
  selector: {
    color: '#85e89d'
  },
  'attr-name': {
    color: '#ffab70'
  },
  string: {
    color: '#9ecbff'
  },
  char: {
    color: '#9ecbff'
  },
  builtin: {
    color: '#79b8ff'
  },
  inserted: {
    color: '#85e89d'
  },
  operator: {
    color: '#f97583'
  },
  entity: {
    color: '#79b8ff',
    cursor: 'help'
  },
  url: {
    color: '#79b8ff'
  },
  '.language-css .token.string': {
    color: '#9ecbff'
  },
  '.style .token.string': {
    color: '#9ecbff'
  },
  variable: {
    color: '#ffab70'
  },
  atrule: {
    color: '#b392f0'
  },
  'attr-value': {
    color: '#9ecbff'
  },
  function: {
    color: '#b392f0'
  },
  'class-name': {
    color: '#ffab70'
  },
  keyword: {
    color: '#f97583',
    fontWeight: 'bold'
  },
  regex: {
    color: '#85e89d'
  },
  important: {
    color: '#f97583',
    fontWeight: 'bold'
  },
  bold: {
    fontWeight: 'bold'
  },
  italic: {
    fontStyle: 'italic'
  },
  // Python-specific styling
  'token.decorator': {
    color: '#ffab70'
  },
  'token.triple-quoted-string': {
    color: '#9ecbff',
    fontStyle: 'italic'
  },
  // SQL-specific styling
  'token.sql-keyword': {
    color: '#f97583',
    fontWeight: 'bold',
    textTransform: 'uppercase'
  },
  // R-specific styling
  'token.r-operator': {
    color: '#f97583'
  },
  'token.r-assignment': {
    color: '#f97583',
    fontWeight: 'bold'
  },
  // JavaScript/TypeScript specific
  'token.template-string': {
    color: '#9ecbff'
  },
  'token.template-punctuation': {
    color: '#f97583'
  }
};

// Light theme variant for DataSoph AI
export const dataSophLightTheme = {
  'code[class*="language-"]': {
    color: '#24292e',
    background: 'none',
    fontFamily: 'ui-monospace, SFMono-Regular, "SF Mono", Consolas, "Liberation Mono", Menlo, monospace',
    fontSize: '14px',
    lineHeight: '1.5',
    whiteSpace: 'pre',
    wordSpacing: 'normal',
    wordBreak: 'normal',
    wordWrap: 'normal',
    tabSize: '4',
    hyphens: 'none'
  },
  'pre[class*="language-"]': {
    color: '#24292e',
    background: '#f6f8fa',
    fontFamily: 'ui-monospace, SFMono-Regular, "SF Mono", Consolas, "Liberation Mono", Menlo, monospace',
    fontSize: '14px',
    lineHeight: '1.5',
    whiteSpace: 'pre',
    wordSpacing: 'normal',
    wordBreak: 'normal',
    wordWrap: 'normal',
    tabSize: '4',
    hyphens: 'none',
    padding: '1rem',
    margin: '0',
    overflow: 'auto',
    borderRadius: '0',
    border: '1px solid #e1e4e8'
  },
  ':not(pre) > code[class*="language-"]': {
    background: '#f6f8fa',
    padding: '0.2em 0.4em',
    borderRadius: '3px',
    whiteSpace: 'normal',
    border: '1px solid #e1e4e8'
  },
  comment: {
    color: '#6a737d',
    fontStyle: 'italic'
  },
  prolog: {
    color: '#6a737d',
    fontStyle: 'italic'
  },
  doctype: {
    color: '#6a737d',
    fontStyle: 'italic'
  },
  cdata: {
    color: '#6a737d',
    fontStyle: 'italic'
  },
  punctuation: {
    color: '#24292e'
  },
  '.namespace': {
    opacity: '0.7'
  },
  property: {
    color: '#005cc5'
  },
  tag: {
    color: '#22863a'
  },
  boolean: {
    color: '#d73a49'
  },
  number: {
    color: '#005cc5'
  },
  constant: {
    color: '#005cc5'
  },
  symbol: {
    color: '#d73a49'
  },
  deleted: {
    color: '#d73a49'
  },
  selector: {
    color: '#22863a'
  },
  'attr-name': {
    color: '#6f42c1'
  },
  string: {
    color: '#032f62'
  },
  char: {
    color: '#032f62'
  },
  builtin: {
    color: '#005cc5'
  },
  inserted: {
    color: '#22863a'
  },
  operator: {
    color: '#d73a49'
  },
  entity: {
    color: '#005cc5',
    cursor: 'help'
  },
  url: {
    color: '#005cc5'
  },
  '.language-css .token.string': {
    color: '#032f62'
  },
  '.style .token.string': {
    color: '#032f62'
  },
  variable: {
    color: '#e36209'
  },
  atrule: {
    color: '#6f42c1'
  },
  'attr-value': {
    color: '#032f62'
  },
  function: {
    color: '#6f42c1'
  },
  'class-name': {
    color: '#6f42c1'
  },
  keyword: {
    color: '#d73a49',
    fontWeight: 'bold'
  },
  regex: {
    color: '#22863a'
  },
  important: {
    color: '#d73a49',
    fontWeight: 'bold'
  },
  bold: {
    fontWeight: 'bold'
  },
  italic: {
    fontStyle: 'italic'
  }
};

// High contrast theme for accessibility
export const dataSophHighContrastTheme = {
  'code[class*="language-"]': {
    color: '#ffffff',
    background: 'none',
    fontFamily: 'ui-monospace, SFMono-Regular, "SF Mono", Consolas, "Liberation Mono", Menlo, monospace',
    fontSize: '14px',
    lineHeight: '1.6',
    whiteSpace: 'pre',
    wordSpacing: 'normal',
    wordBreak: 'normal',
    wordWrap: 'normal',
    tabSize: '4',
    hyphens: 'none'
  },
  'pre[class*="language-"]': {
    color: '#ffffff',
    background: '#000000',
    fontFamily: 'ui-monospace, SFMono-Regular, "SF Mono", Consolas, "Liberation Mono", Menlo, monospace',
    fontSize: '14px',
    lineHeight: '1.6',
    whiteSpace: 'pre',
    wordSpacing: 'normal',
    wordBreak: 'normal',
    wordWrap: 'normal',
    tabSize: '4',
    hyphens: 'none',
    padding: '1rem',
    margin: '0',
    overflow: 'auto',
    borderRadius: '0',
    border: '2px solid #ffffff'
  },
  ':not(pre) > code[class*="language-"]': {
    background: '#000000',
    color: '#ffffff',
    padding: '0.2em 0.4em',
    borderRadius: '3px',
    whiteSpace: 'normal',
    border: '1px solid #ffffff'
  },
  comment: {
    color: '#00ff00',
    fontStyle: 'italic'
  },
  punctuation: {
    color: '#ffffff'
  },
  property: {
    color: '#00ffff'
  },
  tag: {
    color: '#ffff00'
  },
  boolean: {
    color: '#ff0080'
  },
  number: {
    color: '#ff0080'
  },
  constant: {
    color: '#ff0080'
  },
  string: {
    color: '#00ff00'
  },
  char: {
    color: '#00ff00'
  },
  builtin: {
    color: '#00ffff'
  },
  operator: {
    color: '#ff0080'
  },
  variable: {
    color: '#ffff00'
  },
  function: {
    color: '#00ffff'
  },
  'class-name': {
    color: '#ffff00'
  },
  keyword: {
    color: '#ff0080',
    fontWeight: 'bold'
  },
  regex: {
    color: '#00ff00'
  },
  important: {
    color: '#ff0080',
    fontWeight: 'bold'
  },
  bold: {
    fontWeight: 'bold'
  },
  italic: {
    fontStyle: 'italic'
  }
};

// Export theme selector utility
export const getThemeByName = (themeName: string) => {
  switch (themeName.toLowerCase()) {
    case 'datasoph-light':
      return dataSophLightTheme;
    case 'datasoph-high-contrast':
      return dataSophHighContrastTheme;
    case 'datasoph-dark':
    default:
      return dataSophTheme;
  }
}; 