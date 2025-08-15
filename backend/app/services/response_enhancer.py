"""
Simple Response Enhancer - Minimal formatting
"""
import re

def enhance_response(text: str) -> str:
    """Simple text enhancement"""
    # Convert **bold** to HTML
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    
    # Convert *italic* to HTML
    text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', text)
    
    # Convert code blocks
    text = re.sub(r'```(.*?)```', r'<pre><code>\1</code></pre>', text, flags=re.DOTALL)
    
    return text