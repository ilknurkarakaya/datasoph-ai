import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import DataSophApp from './App.tsx';

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);
root.render(
  <React.StrictMode>
    <DataSophApp />
  </React.StrictMode>
); 
