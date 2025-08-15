"""
Simple File Memory - Minimal implementation
"""
from typing import Dict, Any

class SimpleFileMemory:
    def __init__(self):
        self.files: Dict[str, Dict[str, Any]] = {}
    
    def store(self, file_id: str, data: Dict[str, Any]):
        """Store file data"""
        self.files[file_id] = data
    
    def get(self, file_id: str) -> Dict[str, Any]:
        """Get file data"""
        return self.files.get(file_id, {})
    
    def clear(self):
        """Clear all files"""
        self.files.clear()

# Global instance
memory = SimpleFileMemory()