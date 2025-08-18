/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      fontFamily: {
        'system': ['Inter', 'system-ui', '-apple-system', 'BlinkMacSystemFont', '"Segoe UI"', 'Roboto', '"Helvetica Neue"', 'Arial', 'sans-serif'],
        'mono': ['"SF Mono"', 'Monaco', '"Cascadia Code"', '"Roboto Mono"', 'Consolas', '"Courier New"', 'monospace'],
      },
      fontSize: {
        'xs': ['12px', '1.4'],
        'sm': ['14px', '1.4'],
        'base': ['16px', '1.5'],
        'lg': ['18px', '1.5'],
        'xl': ['20px', '1.5'],
        '2xl': ['24px', '1.4'],
        '3xl': ['28px', '1.3'],
      },
      fontWeight: {
        'light': '300',
        'normal': '400',
        'medium': '500',
        'semibold': '600',
        'bold': '700',
        'extrabold': '800',
      },
      colors: {
        gray: {
          50: 'rgb(var(--gray-50-rgb) / <alpha-value>)',
          100: 'rgb(var(--gray-100-rgb) / <alpha-value>)',
          200: 'rgb(var(--gray-200-rgb) / <alpha-value>)',
          300: 'rgb(var(--gray-300-rgb) / <alpha-value>)',
          400: 'rgb(var(--gray-400-rgb) / <alpha-value>)',
          500: 'rgb(var(--gray-500-rgb) / <alpha-value>)',
          600: 'rgb(var(--gray-600-rgb) / <alpha-value>)',
          700: 'rgb(var(--gray-700-rgb) / <alpha-value>)',
          800: 'rgb(var(--gray-800-rgb) / <alpha-value>)',
          900: 'rgb(var(--gray-900-rgb) / <alpha-value>)',
        },
        'sidebar': {
          'bg': 'var(--sidebar-bg)',
          'border': 'var(--sidebar-border)',
        },
        'main': {
          'bg': 'var(--main-bg)',
        },
        'text': {
          'primary': 'var(--text-primary)',
          'secondary': 'var(--text-secondary)',
        },
        'avatar': {
          'user': 'var(--user-avatar)',
          'ai': 'var(--ai-avatar)',
        },
        'input': {
          'border': 'var(--input-border)',
          'focus': 'var(--input-focus)',
        },
        blue: {
          50: '#dbeafe',
          100: '#bfdbfe',
          200: '#93c5fd',
          300: '#60a5fa',
          400: '#3b82f6',
          500: '#0969da',
          600: '#0550ae',
          700: '#0969da',
          800: '#1e40af',
          900: '#1e3a8a',
        },
        green: {
          50: '#f0fff4',
          100: '#c6f6d5',
          200: '#9ae6b4',
          300: '#68d391',
          400: '#48bb78',
          500: '#38a169',
          600: '#2f855a',
          700: '#276749',
          800: '#22543d',
          900: '#1c4532',
        },
        orange: {
          50: '#fff7ed',
          100: '#fed7aa',
          200: '#fdb882',
          300: '#fd9b5a',
          400: '#fc7c3b',
          500: '#ed8936',
          600: '#dd6b20',
          700: '#c05621',
          800: '#9c4221',
          900: '#7b341e',
        },
        red: {
          50: '#fef5f5',
          100: '#fed7d7',
          200: '#feb2b2',
          300: '#fc8181',
          400: '#f56565',
          500: '#e53e3e',
          600: '#c53030',
          700: '#9b2c2c',
          800: '#822727',
          900: '#63171b',
        },
      },
      spacing: {
        '18': '4.5rem',
        '88': '22rem',
        '128': '32rem',
      },
      maxWidth: {
        'claude': '48rem',
        '8xl': '88rem',
      },
      borderRadius: {
        'lg': '0.75rem',
        'xl': '1rem',
      },
      animation: {
        'fade-in': 'fadeIn 0.3s ease-out',
        'slide-in': 'slideIn 0.3s ease-out',
        'spin': 'spin 1s linear infinite',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0', transform: 'translateY(0.5rem)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        slideIn: {
          '0%': { opacity: '0', transform: 'translateX(-1rem)' },
          '100%': { opacity: '1', transform: 'translateX(0)' },
        },
        spin: {
          '0%': { transform: 'rotate(0deg)' },
          '100%': { transform: 'rotate(360deg)' },
        },
      },
      transitionDuration: {
        '150': '150ms',
        '200': '200ms',
        '300': '300ms',
      },
      transitionTimingFunction: {
        'ease': 'ease',
        'ease-out': 'cubic-bezier(0, 0, 0.2, 1)',
      },
      boxShadow: {
        'sm': '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
        'md': '0 4px 6px -1px rgba(0, 0, 0, 0.05)',
        'lg': '0 10px 15px -3px rgba(0, 0, 0, 0.05)',
        'focus': '0 0 0 3px rgba(66, 153, 225, 0.1)',
        'focus-blue': '0 0 0 3px rgba(66, 153, 225, 0.05)',
      },
      backdropBlur: {
        xs: '2px',
      },
      screens: {
        'xs': '475px',
        'claude': '768px',
      },
    },
  },
  plugins: [],
} 