# RAG Chat Interface

A modern React-based chat interface for the RAG system that works like ChatGPT, Gemini, or Grok.

## Features

- Real-time chat interface with typing indicators
- Source citation for all answers
- Responsive design that works on desktop and mobile
- Example queries to get started quickly
- Smooth animations and transitions

## Tech Stack

- React 18 with Hooks
- Vite for fast development
- Axios for API requests
- Font Awesome for icons

## How to Run

1. **Install dependencies**:
   ```bash
   npm install
   ```

2. **Start the development server**:
   ```bash
   npm run start
   ```

3. **Build for production**:
   ```bash
   npm run build
   ```

4. **Preview the production build**:
   ```bash
   npm run serve
   ```

## Configuration

The frontend is configured to proxy API requests to `http://localhost:8000`. You can change this in [vite.config.js](vite.config.js).

## Project Structure

```
frontend/
├── public/                 # Static assets
├── src/
│   ├── components/         # React components
│   │   ├── ChatInterface.jsx
│   │   └── ChatInterface.css
│   ├── App.jsx             # Main App component
│   ├── App.css             # App styles
│   └── main.jsx            # Entry point
├── index.html              # HTML template
├── vite.config.js          # Vite configuration
└── package.json            # Project dependencies
```

## API Integration

The chat interface communicates with the RAG API through the following endpoints:

- `POST /query` - Send a question and receive an answer with sources

## Customization

You can customize the look and feel by modifying:
- [ChatInterface.css](src/components/ChatInterface.css) - Chat interface styles
- [App.css](src/App.css) - Global styles
- [vite.config.js](vite.config.js) - Build and proxy configuration

## Deployment

To deploy the frontend:

1. Build the project:
   ```bash
   npm run build
   ```

2. The built files will be in the `dist/` directory, which can be served by any static file server.