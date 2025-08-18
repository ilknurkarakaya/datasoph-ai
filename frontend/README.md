# DataSoph AI Frontend - Claude-Style Interface

A modern, responsive React frontend with Claude-inspired design and functionality.

## 🚀 Features

### ✨ Claude-Style Interface
- **Left Sidebar**: Chat history management with collapsible design
- **New Chat Button**: Create fresh conversations instantly
- **Chat History**: Auto-saved conversations with titles and timestamps
- **Responsive Design**: Adapts to mobile, tablet, and desktop

### 📁 File Upload System
- **Plus Button**: Claude-style file attachment in input area
- **Drag & Drop**: Drop files anywhere in the chat area
- **File Preview**: See attached files before sending
- **Supported Formats**: CSV, Excel, JSON, TXT files
- **File Size Limit**: Up to 50MB per file
- **Visual Feedback**: Upload progress and error handling

### 💬 Enhanced Chat Experience
- **Real-time Messaging**: Smooth message flow with typing indicators
- **File Attachments**: Files displayed in message bubbles
- **Code Highlighting**: Syntax highlighting for code blocks
- **Copy to Clipboard**: Easy code copying functionality
- **Message Timestamps**: Clear time display for each message

### 🎨 Modern UI/UX
- **Dark Theme**: Claude-inspired dark color scheme
- **Smooth Animations**: Fade-in, slide, and scale animations
- **Custom Scrollbars**: Styled scrollbars matching the theme
- **Inter Font**: Professional typography with system fallbacks
- **Responsive Layout**: Mobile-first responsive design

## 🛠️ Technical Stack

- **React 18** with TypeScript
- **Tailwind CSS** for styling
- **Custom Hooks** for state management
- **Local Storage** for chat persistence
- **Axios** for API communication
- **React Syntax Highlighter** for code display

## 📱 Responsive Breakpoints

- **Mobile**: < 768px (overlay sidebar)
- **Tablet**: 768px - 1024px (toggleable sidebar)
- **Desktop**: > 1024px (persistent sidebar)

## 🎯 Key Components

### Layout Components
- `MainLayout`: Overall app layout with sidebar toggle
- `Sidebar`: Chat history and navigation
- `ChatInterface`: Main chat area with drag & drop

### Chat Components
- `MessageBubble`: Individual message display with file support
- `InputArea`: Message input with file upload integration
- `ChatHistoryItem`: Individual chat item in sidebar

### File Upload Components
- `FileUploadButton`: Plus button for file selection
- `DragDropZone`: Full-screen drag & drop overlay
- `FilePreview`: File display in input area

### Custom Hooks
- `useChatHistory`: Chat management and localStorage
- `useFileUpload`: File upload handling and validation
- `useDragAndDrop`: Drag and drop functionality

## 🚀 Getting Started

1. **Install Dependencies**
   ```bash
   npm install
   ```

2. **Start Development Server**
   ```bash
   npm start
   ```

3. **Build for Production**
   ```bash
   npm run build
   ```

## 🔧 Configuration

### Environment Variables
- API endpoints configured in `src/services/api.ts`
- Default backend URL: `http://localhost:8000/api/v1`

### Tailwind Configuration
- Custom Claude colors in `tailwind.config.js`
- Inter font family with system fallbacks
- Custom animations and utilities

## 📝 API Integration

### Chat API
```typescript
POST /api/v1/chat
{
  "message": "string",
  "user_id": "string",
  "file_id": "string?" // optional
}
```

### File Upload API
```typescript
POST /api/v1/upload
Content-Type: multipart/form-data
file: File
```

## 🎨 Design System

### Colors
- **Background**: `#1a1a1a`
- **Surface**: `#2d2d2d`
- **Border**: `#404040`
- **Text**: `#e5e5e5`
- **Accent**: `#3b82f6`

### Typography
- **Font Family**: Inter, system-ui, sans-serif
- **Weights**: 300, 400, 500, 600, 700, 800
- **Line Heights**: Optimized for readability

## 🚀 Features Roadmap

- [ ] Real-time collaboration
- [ ] Voice messages
- [ ] Advanced file analysis
- [ ] Export conversations
- [ ] Theme customization
- [ ] Keyboard shortcuts

## 📄 License

MIT License - see LICENSE file for details. 