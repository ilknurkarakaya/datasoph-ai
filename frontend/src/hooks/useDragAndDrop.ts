import { useState, useCallback, useRef } from 'react';

// v5.0 - Force sidebar colors for drag & drop overlay
export const useDragAndDrop = () => {
  const [isDragging, setIsDragging] = useState(false);
  const [isOver, setIsOver] = useState(false);
  const dragCounter = useRef(0);

  const handleDragEnter = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    
    dragCounter.current++;
    
    if (e.dataTransfer.items && e.dataTransfer.items.length > 0) {
      setIsDragging(true);
    }
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    
    dragCounter.current--;
    
    if (dragCounter.current === 0) {
      setIsDragging(false);
      setIsOver(false);
    }
  }, []);

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    
    if (e.dataTransfer.items && e.dataTransfer.items.length > 0) {
      setIsOver(true);
    }
  }, []);

  const handleDrop = useCallback((e: React.DragEvent, onFileDrop: (files: File[]) => void) => {
    e.preventDefault();
    e.stopPropagation();
    
    setIsDragging(false);
    setIsOver(false);
    dragCounter.current = 0;
    
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      const files = Array.from(e.dataTransfer.files);
      onFileDrop(files);
    }
  }, []);

  const reset = useCallback(() => {
    setIsDragging(false);
    setIsOver(false);
    dragCounter.current = 0;
  }, []);

  return {
    isDragging,
    isOver,
    handleDragEnter,
    handleDragLeave,
    handleDragOver,
    handleDrop,
    reset,
  };
}; 