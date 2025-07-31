"""
DATASOPH AI - RAG System Tests
Test cases for document processing, vector storage, and RAG pipeline
"""

import unittest
from unittest.mock import patch, MagicMock
import tempfile
import os
import json
from pathlib import Path

# Import RAG components
from document_processor import DocumentProcessor
from vector_store import VectorStore
from rag_pipeline import RAGPipeline


class TestDocumentProcessor(unittest.TestCase):
    """Test cases for DocumentProcessor"""
    
    def setUp(self):
        """Set up test environment"""
        self.processor = DocumentProcessor(chunk_size=500, chunk_overlap=100)
    
    def test_initialization(self):
        """Test DocumentProcessor initialization"""
        self.assertIsNotNone(self.processor)
        self.assertEqual(self.processor.chunk_size, 500)
        self.assertEqual(self.processor.chunk_overlap, 100)
        self.assertIn('.pdf', self.processor.supported_extensions)
        self.assertIn('.docx', self.processor.supported_extensions)
        self.assertIn('.txt', self.processor.supported_extensions)
    
    def test_process_txt_document(self):
        """Test processing TXT document"""
        # Create test TXT file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("This is a test document.\n\nIt has multiple paragraphs.\n\nThis is the third paragraph.")
            file_path = f.name
        
        try:
            documents = self.processor.process_document(file_path)
            
            self.assertIsInstance(documents, list)
            self.assertGreater(len(documents), 0)
            
            for doc in documents:
                self.assertIsInstance(doc.page_content, str)
                self.assertIn('source', doc.metadata)
                self.assertIn('chunk_id', doc.metadata)
                self.assertIn('file_type', doc.metadata)
            
        finally:
            os.unlink(file_path)
    
    def test_process_csv_document(self):
        """Test processing CSV document"""
        # Create test CSV file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write("name,age,city\nJohn,25,New York\nJane,30,Los Angeles\nBob,35,Chicago")
            file_path = f.name
        
        try:
            documents = self.processor.process_document(file_path)
            
            self.assertIsInstance(documents, list)
            self.assertGreater(len(documents), 0)
            
            # Check that CSV content is properly formatted
            content = documents[0].page_content
            self.assertIn("CSV Document", content)
            self.assertIn("Shape", content)
            self.assertIn("Columns", content)
            
        finally:
            os.unlink(file_path)
    
    def test_process_json_document(self):
        """Test processing JSON document"""
        # Create test JSON file
        test_data = {"name": "test", "value": 123, "items": ["a", "b", "c"]}
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(test_data, f)
            file_path = f.name
        
        try:
            documents = self.processor.process_document(file_path)
            
            self.assertIsInstance(documents, list)
            self.assertGreater(len(documents), 0)
            
            # Check that JSON content is properly formatted
            content = documents[0].page_content
            self.assertIn("JSON Document", content)
            self.assertIn("test", content)
            
        finally:
            os.unlink(file_path)
    
    def test_process_multiple_documents(self):
        """Test processing multiple documents"""
        # Create test files
        files = []
        try:
            # Create TXT file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
                f.write("Test document 1")
                files.append(f.name)
            
            # Create CSV file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
                f.write("col1,col2\nval1,val2")
                files.append(f.name)
            
            documents = self.processor.process_multiple_documents(files)
            
            self.assertIsInstance(documents, list)
            self.assertGreater(len(documents), 0)
            
        finally:
            for file_path in files:
                if os.path.exists(file_path):
                    os.unlink(file_path)
    
    def test_get_document_summary(self):
        """Test document summary generation"""
        # Create test documents
        from langchain.schema import Document
        test_docs = [
            Document(page_content="Test content 1", metadata={"source": "test1.txt"}),
            Document(page_content="Test content 2", metadata={"source": "test2.txt"})
        ]
        
        summary = self.processor.get_document_summary(test_docs)
        
        self.assertIn("total_documents", summary)
        self.assertIn("total_chunks", summary)
        self.assertIn("total_characters", summary)
        self.assertEqual(summary["total_documents"], 2)
        self.assertEqual(summary["total_chunks"], 2)


class TestVectorStore(unittest.TestCase):
    """Test cases for VectorStore"""
    
    def setUp(self):
        """Set up test environment"""
        self.vector_store = VectorStore(persist_directory="./test_vectorstore")
    
    def test_initialization(self):
        """Test VectorStore initialization"""
        self.assertIsNotNone(self.vector_store)
        self.assertEqual(self.vector_store.collection_name, "datasoph_documents")
        self.assertIsNotNone(self.vector_store.collection)
    
    def test_add_documents(self):
        """Test adding documents to vector store"""
        from langchain.schema import Document
        
        test_docs = [
            Document(page_content="Test document 1", metadata={"source": "test1.txt"}),
            Document(page_content="Test document 2", metadata={"source": "test2.txt"})
        ]
        
        success = self.vector_store.add_documents(test_docs)
        self.assertTrue(success)
    
    def test_similarity_search(self):
        """Test similarity search"""
        # First add some documents
        from langchain.schema import Document
        
        test_docs = [
            Document(page_content="This is about machine learning", metadata={"source": "ml.txt"}),
            Document(page_content="This is about data science", metadata={"source": "ds.txt"}),
            Document(page_content="This is about artificial intelligence", metadata={"source": "ai.txt"})
        ]
        
        self.vector_store.add_documents(test_docs)
        
        # Test search
        results = self.vector_store.similarity_search("machine learning", k=2)
        
        self.assertIsInstance(results, list)
        self.assertLessEqual(len(results), 2)
        
        for doc, score in results:
            self.assertIsInstance(doc.page_content, str)
            self.assertIsInstance(score, float)
    
    def test_get_collection_stats(self):
        """Test getting collection statistics"""
        stats = self.vector_store.get_collection_stats()
        
        self.assertIn("collection_name", stats)
        self.assertIn("total_documents", stats)
        self.assertIn("embedding_model", stats)
        self.assertIn("api_connected", stats)
    
    def test_reset_collection(self):
        """Test resetting collection"""
        success = self.vector_store.reset_collection()
        self.assertTrue(success)
    
    def tearDown(self):
        """Clean up after tests"""
        try:
            self.vector_store.delete_collection()
        except:
            pass


class TestRAGPipeline(unittest.TestCase):
    """Test cases for RAGPipeline"""
    
    def setUp(self):
        """Set up test environment"""
        self.rag = RAGPipeline()
    
    def test_initialization(self):
        """Test RAGPipeline initialization"""
        self.assertIsNotNone(self.rag)
        self.assertIsNotNone(self.rag.document_processor)
        self.assertIsNotNone(self.rag.vector_store)
        self.assertEqual(self.rag.chunk_size, 1000)
        self.assertEqual(self.rag.chunk_overlap, 200)
    
    def test_upload_documents(self):
        """Test uploading documents"""
        # Create test file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("This is a test document for RAG pipeline testing.")
            file_path = f.name
        
        try:
            result = self.rag.upload_documents([file_path])
            
            self.assertIn("success", result)
            if result["success"]:
                self.assertIn("documents_processed", result)
                self.assertIn("chunks_created", result)
                self.assertIn("summary", result)
            
        finally:
            os.unlink(file_path)
    
    def test_ask_question(self):
        """Test asking questions"""
        # First upload a document
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("This document contains information about artificial intelligence and machine learning.")
            file_path = f.name
        
        try:
            # Upload document
            self.rag.upload_documents([file_path])
            
            # Ask question
            result = self.rag.ask_question("What is this document about?")
            
            self.assertIn("success", result)
            if result["success"]:
                self.assertIn("answer", result)
                self.assertIn("sources", result)
                self.assertIn("question", result)
            
        finally:
            os.unlink(file_path)
    
    def test_mock_answer(self):
        """Test mock answer generation"""
        result = self.rag._mock_answer("What is this document about?")
        
        self.assertIn("success", result)
        self.assertIn("answer", result)
        self.assertIn("sources", result)
        self.assertIn("question", result)
        self.assertTrue(result["success"])
    
    def test_get_system_stats(self):
        """Test getting system statistics"""
        stats = self.rag.get_system_stats()
        
        self.assertIn("rag_system", stats)
        self.assertIn("api_connected", stats)
        self.assertIn("chunk_size", stats)
        self.assertIn("chunk_overlap", stats)
        self.assertIn("vector_store", stats)
        self.assertIn("supported_file_types", stats)
    
    def test_reset_system(self):
        """Test resetting the system"""
        success = self.rag.reset_system()
        self.assertTrue(success)
    
    def test_export_system_info(self):
        """Test exporting system information"""
        info = self.rag.export_system_info()
        
        self.assertIn("system_stats", info)
        self.assertIn("vector_store_info", info)
        self.assertIn("export_timestamp", info)


def run_rag_tests():
    """Run all RAG system tests"""
    print("🧪 Running RAG System Tests...")
    print("=" * 60)
    
    # Create test suite
    suite = unittest.TestSuite()
    
    # Add test classes
    suite.addTest(unittest.makeSuite(TestDocumentProcessor))
    suite.addTest(unittest.makeSuite(TestVectorStore))
    suite.addTest(unittest.makeSuite(TestRAGPipeline))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 60)
    print(f"📊 Test Results:")
    print(f"   Tests run: {result.testsRun}")
    print(f"   Failures: {len(result.failures)}")
    print(f"   Errors: {len(result.errors)}")
    
    if result.failures:
        print("\n❌ Failures:")
        for test, traceback in result.failures:
            print(f"   - {test}: {traceback}")
    
    if result.errors:
        print("\n❌ Errors:")
        for test, traceback in result.errors:
            print(f"   - {test}: {traceback}")
    
    if not result.failures and not result.errors:
        print("\n✅ All RAG system tests passed!")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    run_rag_tests() 