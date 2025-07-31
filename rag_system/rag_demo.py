"""
DATASOPH AI - RAG System Demo
Interactive demo for the RAG (Retrieval-Augmented Generation) system
"""

import os
import sys
from pathlib import Path
from rag_pipeline import RAGPipeline

def main():
    """Interactive RAG system demo"""
    print("🔍 DATASOPH AI - RAG System Demo")
    print("=" * 60)
    print("This demo shows how the RAG system processes documents and answers questions.")
    print("You can upload documents and ask questions about their content.")
    print("-" * 60)
    
    # Initialize RAG pipeline
    rag = RAGPipeline()
    
    # Show system info
    stats = rag.get_system_stats()
    print(f"🤖 RAG System: {stats['rag_system']}")
    print(f"🔗 API Connected: {stats['api_connected']}")
    print(f"📄 Supported file types: {', '.join(stats['supported_file_types'])}")
    print(f"📏 Chunk size: {stats['chunk_size']}")
    print(f"🔄 Chunk overlap: {stats['chunk_overlap']}")
    print("-" * 60)
    
    print("Available commands:")
    print("- 'upload <file_path>' - Upload a document")
    print("- 'ask <question>' - Ask a question about uploaded documents")
    print("- 'stats' - Show system statistics")
    print("- 'reset' - Reset the system")
    print("- 'demo' - Run automatic demo")
    print("- 'quit' - Exit")
    print("-" * 60)
    
    while True:
        try:
            user_input = input("\n🔍 RAG> ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("\n👋 Goodbye! Thanks for using DATASOPH AI RAG System!")
                break
            
            elif user_input.lower() == 'stats':
                stats = rag.get_system_stats()
                print(f"\n📊 System Statistics:")
                print(f"   RAG System: {stats['rag_system']}")
                print(f"   API Connected: {stats['api_connected']}")
                print(f"   Vector Store: {stats['vector_store']['collection_name']}")
                print(f"   Total Documents: {stats['vector_store']['total_documents']}")
                print(f"   Embedding Model: {stats['vector_store']['embedding_model']}")
            
            elif user_input.lower() == 'reset':
                success = rag.reset_system()
                if success:
                    print("✅ System reset successfully!")
                else:
                    print("❌ Failed to reset system")
            
            elif user_input.lower() == 'demo':
                run_automatic_demo(rag)
            
            elif user_input.startswith('upload '):
                file_path = user_input[7:].strip()
                if os.path.exists(file_path):
                    print(f"📤 Uploading {file_path}...")
                    result = rag.upload_documents([file_path])
                    
                    if result["success"]:
                        print(f"✅ Upload successful!")
                        print(f"   Documents processed: {result['documents_processed']}")
                        print(f"   Chunks created: {result['chunks_created']}")
                        if "summary" in result:
                            summary = result["summary"]
                            print(f"   Total characters: {summary.get('total_characters', 0)}")
                            print(f"   Average chunk size: {summary.get('average_chunk_size', 0):.1f}")
                    else:
                        print(f"❌ Upload failed: {result.get('error', 'Unknown error')}")
                else:
                    print(f"❌ File not found: {file_path}")
            
            elif user_input.startswith('ask '):
                question = user_input[4:].strip()
                if question:
                    print(f"🤔 Searching for answer to: '{question}'")
                    result = rag.ask_question(question)
                    
                    if result["success"]:
                        print(f"✅ Answer:")
                        print(f"   {result['answer']}")
                        if result.get('sources'):
                            print(f"   Sources: {', '.join(result['sources'])}")
                        print(f"   Context documents: {result.get('context_documents', 0)}")
                    else:
                        print(f"❌ Error: {result.get('error', 'Unknown error')}")
                else:
                    print("❌ Please provide a question")
            
            elif not user_input:
                continue
            
            else:
                print("❌ Unknown command. Type 'help' for available commands.")
        
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye! Thanks for using DATASOPH AI RAG System!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")


def run_automatic_demo(rag):
    """Run automatic demo with sample documents"""
    print("\n🎬 Running Automatic Demo...")
    print("-" * 40)
    
    # Create sample documents
    sample_docs = create_sample_documents()
    
    # Upload documents
    print("📤 Uploading sample documents...")
    for doc_name, content in sample_docs.items():
        with open(doc_name, 'w') as f:
            f.write(content)
    
    try:
        result = rag.upload_documents(list(sample_docs.keys()))
        
        if result["success"]:
            print(f"✅ Uploaded {result['documents_processed']} documents")
            print(f"   Created {result['chunks_created']} chunks")
            
            # Ask sample questions
            sample_questions = [
                "What is machine learning?",
                "What are the main types of data analysis?",
                "How does the RAG system work?",
                "What file formats are supported?"
            ]
            
            print("\n🤔 Asking sample questions...")
            for question in sample_questions:
                print(f"\nQ: {question}")
                result = rag.ask_question(question)
                
                if result["success"]:
                    print(f"A: {result['answer'][:200]}...")
                else:
                    print(f"A: {result.get('error', 'No answer available')}")
            
            print("\n✅ Demo completed successfully!")
        
        else:
            print(f"❌ Demo failed: {result.get('error', 'Unknown error')}")
    
    finally:
        # Clean up sample files
        for doc_name in sample_docs.keys():
            if os.path.exists(doc_name):
                os.unlink(doc_name)


def create_sample_documents():
    """Create sample documents for demo"""
    return {
        "machine_learning.txt": """
Machine Learning Fundamentals

Machine learning is a subset of artificial intelligence that enables computers to learn and improve from experience without being explicitly programmed. It focuses on developing algorithms that can access data and use it to learn for themselves.

Key Concepts:
1. Supervised Learning: Learning from labeled data
2. Unsupervised Learning: Finding patterns in unlabeled data
3. Reinforcement Learning: Learning through interaction with environment

Applications:
- Image recognition
- Natural language processing
- Recommendation systems
- Fraud detection
- Medical diagnosis

Machine learning algorithms can be categorized into:
- Classification algorithms
- Regression algorithms
- Clustering algorithms
- Dimensionality reduction
        """,
        
        "data_analysis.txt": """
Data Analysis Methods

Data analysis is the process of inspecting, cleaning, transforming, and modeling data to discover useful information and support decision-making.

Types of Data Analysis:
1. Descriptive Analysis: Summarizing data characteristics
2. Diagnostic Analysis: Understanding why something happened
3. Predictive Analysis: Forecasting future outcomes
4. Prescriptive Analysis: Recommending actions

Common Techniques:
- Statistical analysis
- Data visualization
- Hypothesis testing
- Correlation analysis
- Regression analysis

Tools and Technologies:
- Python (pandas, numpy, scikit-learn)
- R programming language
- SQL for data querying
- Tableau for visualization
- Power BI for business intelligence
        """,
        
        "rag_system.txt": """
RAG System Overview

Retrieval-Augmented Generation (RAG) is an AI framework that combines information retrieval with text generation to provide more accurate and contextual responses.

How RAG Works:
1. Document Processing: Upload and chunk documents
2. Vector Embedding: Convert text to numerical vectors
3. Storage: Store embeddings in vector database
4. Retrieval: Find relevant documents for queries
5. Generation: Generate answers using retrieved context

Benefits:
- More accurate responses
- Up-to-date information
- Source attribution
- Reduced hallucinations
- Better context understanding

Supported File Types:
- PDF documents
- Word documents (DOCX)
- Text files (TXT)
- CSV data files
- JSON data files

The system uses ChromaDB for vector storage and OpenAI embeddings for semantic search.
        """
    }


if __name__ == "__main__":
    main() 