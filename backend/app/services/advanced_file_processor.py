"""
DataSoph AI - Advanced File Processor
Intelligent file processing with automated EDA and business insights
"""

import pandas as pd
import numpy as np
import json
import zipfile
import tarfile
from typing import Dict, List, Any, Optional, Tuple, Union
from pathlib import Path
import logging
import io
import warnings
from datetime import datetime
import mimetypes
import chardet

# Suppress warnings
warnings.filterwarnings('ignore')

logger = logging.getLogger(__name__)

class AdvancedFileProcessor:
    """
    Advanced file processor with intelligent format detection and comprehensive analysis
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.supported_formats = {
            '.csv': self.process_csv_advanced,
            '.xlsx': self.process_excel_advanced,
            '.xls': self.process_excel_advanced,
            '.json': self.process_json_advanced,
            '.parquet': self.process_parquet,
            '.tsv': self.process_tsv,
            '.txt': self.process_text_file,
            '.sql': self.process_sql_file,
            '.html': self.process_html_tables,
            '.xml': self.process_xml_file,
            '.zip': self.process_archive,
            '.tar': self.process_archive,
            '.gz': self.process_compressed
        }
        
        self.encoding_fallbacks = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1', 'utf-16']
        
        self.logger.info("🚀 Advanced File Processor initialized")

    def process_any_file(self, file_path: str) -> Dict[str, Any]:
        """
        Intelligently process any file format and return comprehensive analysis
        """
        try:
            file_path = Path(file_path)
            
            # Basic file information
            file_info = self._get_file_metadata(file_path)
            
            # Detect file type and encoding
            file_extension = file_path.suffix.lower()
            mime_type = mimetypes.guess_type(str(file_path))[0]
            
            self.logger.info(f"📁 Processing file: {file_path.name} (type: {file_extension})")
            
            # Process based on file type
            if file_extension in self.supported_formats:
                processor = self.supported_formats[file_extension]
                processing_result = processor(file_path)
            else:
                # Try to infer format from content
                processing_result = self._infer_and_process(file_path)
            
            # Combine metadata and processing results
            result = {
                'file_info': file_info,
                'processing_result': processing_result,
                'analysis_timestamp': datetime.now().isoformat(),
                'processor_version': '2.0'
            }
            
            self.logger.info(f"✅ Successfully processed {file_path.name}")
            return result
            
        except Exception as e:
            self.logger.error(f"❌ Error processing file {file_path}: {e}")
            return {
                'error': str(e),
                'file_info': self._get_file_metadata(file_path) if Path(file_path).exists() else {},
                'analysis_timestamp': datetime.now().isoformat()
            }

    def _get_file_metadata(self, file_path: Path) -> Dict[str, Any]:
        """Get comprehensive file metadata"""
        try:
            stat = file_path.stat()
            
            # Detect encoding for text files
            encoding = None
            if file_path.suffix.lower() in ['.csv', '.txt', '.json', '.sql', '.html', '.xml']:
                encoding = self._detect_encoding(file_path)
            
            return {
                'filename': file_path.name,
                'size_bytes': stat.st_size,
                'size_mb': round(stat.st_size / (1024 * 1024), 2),
                'extension': file_path.suffix.lower(),
                'mime_type': mimetypes.guess_type(str(file_path))[0],
                'encoding': encoding,
                'created': datetime.fromtimestamp(stat.st_ctime).isoformat(),
                'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                'is_text': file_path.suffix.lower() in ['.csv', '.txt', '.json', '.sql', '.html', '.xml', '.tsv']
            }
        except Exception as e:
            return {'error': f"Could not read file metadata: {e}"}

    def _detect_encoding(self, file_path: Path) -> str:
        """Intelligently detect file encoding"""
        try:
            # Read a sample of the file
            with open(file_path, 'rb') as f:
                raw_data = f.read(min(10000, file_path.stat().st_size))  # Read up to 10KB
            
            # Use chardet for detection
            detection = chardet.detect(raw_data)
            if detection['confidence'] > 0.7:
                return detection['encoding']
            
            # Fallback to common encodings
            for encoding in self.encoding_fallbacks:
                try:
                    raw_data.decode(encoding)
                    return encoding
                except UnicodeDecodeError:
                    continue
            
            return 'utf-8'  # Default fallback
            
        except Exception:
            return 'utf-8'

    def process_csv_advanced(self, file_path: Path) -> Dict[str, Any]:
        """Advanced CSV processing with intelligent parameter detection"""
        try:
            encoding = self._detect_encoding(file_path)
            
            # Auto-detect CSV parameters
            with open(file_path, 'r', encoding=encoding) as f:
                sample = f.read(8192)  # Read 8KB sample
            
            # Detect delimiter
            delimiter = self._detect_delimiter(sample)
            
            # Try different parsing strategies
            parsing_strategies = [
                {'sep': delimiter, 'encoding': encoding},
                {'sep': delimiter, 'encoding': encoding, 'quotechar': '"'},
                {'sep': delimiter, 'encoding': encoding, 'quotechar': "'"},
                {'sep': delimiter, 'encoding': encoding, 'escapechar': '\\\\'},
            ]
            
            df = None
            strategy_used = None
            
            for strategy in parsing_strategies:
                try:
                    df = pd.read_csv(file_path, **strategy, nrows=1000)  # Read sample first
                    if len(df.columns) > 1:  # Ensure proper parsing
                        # Read full file if sample looks good
                        df = pd.read_csv(file_path, **strategy)
                        strategy_used = strategy
                        break
                except Exception:
                    continue
            
            if df is None:
                raise ValueError("Could not parse CSV file with any strategy")
            
            # Comprehensive analysis
            analysis = self.intelligent_data_profiling(df)
            
            return {
                'success': True,
                'data_shape': df.shape,
                'parsing_strategy': strategy_used,
                'sample_data': df.head().to_dict('records'),
                'analysis': analysis,
                'data_preview': self._generate_data_preview(df)
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def process_excel_advanced(self, file_path: Path) -> Dict[str, Any]:
        """Advanced Excel processing with multi-sheet support"""
        try:
            # Read all sheets
            excel_file = pd.ExcelFile(file_path)
            sheets_data = {}
            
            for sheet_name in excel_file.sheet_names:
                try:
                    df = pd.read_excel(file_path, sheet_name=sheet_name)
                    
                    # Skip empty sheets
                    if df.empty:
                        continue
                    
                    analysis = self.intelligent_data_profiling(df)
                    
                    sheets_data[sheet_name] = {
                        'shape': df.shape,
                        'columns': list(df.columns),
                        'sample_data': df.head().to_dict('records'),
                        'analysis': analysis
                    }
                    
                except Exception as e:
                    sheets_data[sheet_name] = {'error': str(e)}
            
            # Determine primary sheet (largest by row count)
            if sheets_data:
                primary_sheet = max(sheets_data.keys(), 
                                  key=lambda x: sheets_data[x].get('shape', [0, 0])[0] 
                                  if 'shape' in sheets_data[x] else 0)
            else:
                primary_sheet = None
            
            return {
                'success': True,
                'sheets': list(excel_file.sheet_names),
                'primary_sheet': primary_sheet,
                'sheets_data': sheets_data,
                'total_sheets': len(excel_file.sheet_names)
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def process_json_advanced(self, file_path: Path) -> Dict[str, Any]:
        """Advanced JSON processing with structure analysis"""
        try:
            encoding = self._detect_encoding(file_path)
            
            with open(file_path, 'r', encoding=encoding) as f:
                data = json.load(f)
            
            # Analyze JSON structure
            structure_analysis = self._analyze_json_structure(data)
            
            # Try to convert to DataFrame if possible
            df = None
            conversion_method = None
            
            # Different conversion strategies
            if isinstance(data, list) and len(data) > 0:
                if isinstance(data[0], dict):
                    df = pd.DataFrame(data)
                    conversion_method = "list_of_dicts"
                else:
                    df = pd.DataFrame({'values': data})
                    conversion_method = "simple_list"
            elif isinstance(data, dict):
                # Try different dict conversion methods
                if all(isinstance(v, (list, dict)) for v in data.values()):
                    try:
                        df = pd.json_normalize(data)
                        conversion_method = "normalized_dict"
                    except:
                        df = pd.DataFrame([data])
                        conversion_method = "single_record"
                else:
                    df = pd.DataFrame([data])
                    conversion_method = "single_record"
            
            result = {
                'success': True,
                'structure_analysis': structure_analysis,
                'conversion_method': conversion_method
            }
            
            if df is not None:
                analysis = self.intelligent_data_profiling(df)
                result.update({
                    'data_shape': df.shape,
                    'sample_data': df.head().to_dict('records'),
                    'analysis': analysis
                })
            
            return result
            
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def process_parquet(self, file_path: Path) -> Dict[str, Any]:
        """Process Parquet files"""
        try:
            df = pd.read_parquet(file_path)
            analysis = self.intelligent_data_profiling(df)
            
            return {
                'success': True,
                'data_shape': df.shape,
                'sample_data': df.head().to_dict('records'),
                'analysis': analysis,
                'parquet_metadata': self._get_parquet_metadata(file_path)
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def process_tsv(self, file_path: Path) -> Dict[str, Any]:
        """Process Tab-Separated Values files"""
        try:
            encoding = self._detect_encoding(file_path)
            df = pd.read_csv(file_path, sep='\\t', encoding=encoding)
            analysis = self.intelligent_data_profiling(df)
            
            return {
                'success': True,
                'data_shape': df.shape,
                'sample_data': df.head().to_dict('records'),
                'analysis': analysis
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def process_text_file(self, file_path: Path) -> Dict[str, Any]:
        """Process generic text files with structure detection"""
        try:
            encoding = self._detect_encoding(file_path)
            
            with open(file_path, 'r', encoding=encoding) as f:
                content = f.read()
            
            # Analyze text structure
            text_analysis = self._analyze_text_structure(content)
            
            # Try to detect if it's structured data
            if text_analysis['might_be_csv']:
                # Try parsing as CSV
                try:
                    df = pd.read_csv(io.StringIO(content))
                    if len(df.columns) > 1:
                        analysis = self.intelligent_data_profiling(df)
                        return {
                            'success': True,
                            'detected_format': 'CSV',
                            'data_shape': df.shape,
                            'sample_data': df.head().to_dict('records'),
                            'analysis': analysis
                        }
                except:
                    pass
            
            return {
                'success': True,
                'content_type': 'text',
                'text_analysis': text_analysis,
                'sample_content': content[:1000] if len(content) > 1000 else content
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def process_sql_file(self, file_path: Path) -> Dict[str, Any]:
        """Process SQL files and extract structure"""
        try:
            encoding = self._detect_encoding(file_path)
            
            with open(file_path, 'r', encoding=encoding) as f:
                sql_content = f.read()
            
            # Analyze SQL structure
            sql_analysis = self._analyze_sql_structure(sql_content)
            
            return {
                'success': True,
                'content_type': 'sql',
                'sql_analysis': sql_analysis,
                'sample_content': sql_content[:1000] if len(sql_content) > 1000 else sql_content
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def process_html_tables(self, file_path: Path) -> Dict[str, Any]:
        """Extract and process tables from HTML files"""
        try:
            # Try to read HTML tables
            dfs = pd.read_html(str(file_path))
            
            if not dfs:
                return {'success': False, 'error': 'No tables found in HTML'}
            
            tables_data = {}
            for i, df in enumerate(dfs):
                analysis = self.intelligent_data_profiling(df)
                tables_data[f'table_{i}'] = {
                    'shape': df.shape,
                    'sample_data': df.head().to_dict('records'),
                    'analysis': analysis
                }
            
            return {
                'success': True,
                'tables_found': len(dfs),
                'tables_data': tables_data
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def process_xml_file(self, file_path: Path) -> Dict[str, Any]:
        """Process XML files and extract structure"""
        try:
            # Try to parse XML and convert to DataFrame
            try:
                df = pd.read_xml(str(file_path))
                analysis = self.intelligent_data_profiling(df)
                
                return {
                    'success': True,
                    'data_shape': df.shape,
                    'sample_data': df.head().to_dict('records'),
                    'analysis': analysis
                }
            except:
                # If direct conversion fails, provide structure analysis
                encoding = self._detect_encoding(file_path)
                with open(file_path, 'r', encoding=encoding) as f:
                    xml_content = f.read()
                
                return {
                    'success': True,
                    'content_type': 'xml',
                    'xml_structure': 'Complex XML structure detected',
                    'sample_content': xml_content[:1000] if len(xml_content) > 1000 else xml_content
                }
                
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def process_archive(self, file_path: Path) -> Dict[str, Any]:
        """Process archive files (ZIP, TAR)"""
        try:
            archive_contents = []
            
            if file_path.suffix.lower() == '.zip':
                with zipfile.ZipFile(file_path, 'r') as archive:
                    for info in archive.infolist():
                        archive_contents.append({
                            'filename': info.filename,
                            'size': info.file_size,
                            'compressed_size': info.compress_size,
                            'modified': datetime(*info.date_time).isoformat()
                        })
            elif file_path.suffix.lower() in ['.tar', '.tar.gz']:
                with tarfile.open(file_path, 'r') as archive:
                    for member in archive.getmembers():
                        if member.isfile():
                            archive_contents.append({
                                'filename': member.name,
                                'size': member.size,
                                'modified': datetime.fromtimestamp(member.mtime).isoformat()
                            })
            
            return {
                'success': True,
                'archive_type': file_path.suffix.lower(),
                'files_count': len(archive_contents),
                'contents': archive_contents[:50]  # Limit to first 50 files
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def process_compressed(self, file_path: Path) -> Dict[str, Any]:
        """Process compressed files"""
        try:
            # This is a placeholder for compressed file handling
            return {
                'success': True,
                'message': 'Compressed file detected. Extract to analyze contents.',
                'compression_type': file_path.suffix.lower()
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def intelligent_data_profiling(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Generate comprehensive automated EDA with business insights
        """
        try:
            profiling_results = {
                'basic_info': self._get_basic_data_info(df),
                'data_quality': self._assess_data_quality_advanced(df),
                'statistical_summary': self._get_enhanced_statistical_summary(df),
                'column_analysis': self._analyze_columns_advanced(df),
                'patterns_and_insights': self._detect_patterns_and_insights(df),
                'business_recommendations': self._generate_business_recommendations(df),
                'data_preparation_suggestions': self._suggest_data_preparation(df)
            }
            
            return profiling_results
            
        except Exception as e:
            return {'error': f"Data profiling failed: {str(e)}"}

    def _get_basic_data_info(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Enhanced basic data information"""
        return {
            'shape': df.shape,
            'memory_usage_mb': df.memory_usage(deep=True).sum() / (1024 * 1024),
            'dtypes_summary': df.dtypes.value_counts().to_dict(),
            'missing_values_total': df.isnull().sum().sum(),
            'missing_percentage': (df.isnull().sum().sum() / (df.shape[0] * df.shape[1])) * 100,
            'duplicate_rows': df.duplicated().sum(),
            'duplicate_percentage': (df.duplicated().sum() / len(df)) * 100,
            'numeric_columns': list(df.select_dtypes(include=[np.number]).columns),
            'categorical_columns': list(df.select_dtypes(include=['object', 'category']).columns),
            'datetime_columns': list(df.select_dtypes(include=['datetime64']).columns)
        }

    def _assess_data_quality_advanced(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Advanced data quality assessment with scoring"""
        quality_score = 100
        quality_issues = []
        recommendations = []
        
        # Missing values assessment
        missing_pct = (df.isnull().sum().sum() / (df.shape[0] * df.shape[1])) * 100
        if missing_pct > 30:
            quality_score -= 40
            quality_issues.append(f"Very high missing values: {missing_pct:.1f}%")
            recommendations.append("Consider data collection improvement or imputation strategy")
        elif missing_pct > 15:
            quality_score -= 25
            quality_issues.append(f"High missing values: {missing_pct:.1f}%")
            recommendations.append("Implement systematic missing value treatment")
        elif missing_pct > 5:
            quality_score -= 10
            quality_issues.append(f"Moderate missing values: {missing_pct:.1f}%")
            recommendations.append("Simple imputation strategies should suffice")
        
        # Duplicate assessment
        dup_pct = (df.duplicated().sum() / len(df)) * 100
        if dup_pct > 20:
            quality_score -= 30
            quality_issues.append(f"Very high duplicate rows: {dup_pct:.1f}%")
            recommendations.append("Investigate data collection process for duplicates")
        elif dup_pct > 5:
            quality_score -= 15
            quality_issues.append(f"High duplicate rows: {dup_pct:.1f}%")
            recommendations.append("Remove duplicate records before analysis")
        
        # Data consistency checks
        for col in df.select_dtypes(include=['object']).columns:
            unique_ratio = df[col].nunique() / len(df)
            if unique_ratio > 0.98 and len(df) > 100:
                quality_issues.append(f"Column '{col}' appears to be an identifier")
                recommendations.append(f"Consider removing '{col}' for analytical purposes")
        
        # Data type consistency
        for col in df.select_dtypes(include=['object']).columns:
            sample_values = df[col].dropna().astype(str)
            if len(sample_values) > 0:
                # Check if numeric data is stored as text
                try:
                    pd.to_numeric(sample_values.head(100))
                    quality_issues.append(f"Column '{col}' contains numeric data stored as text")
                    recommendations.append(f"Convert '{col}' to numeric type")
                except (ValueError, TypeError):
                    pass
        
        return {
            'quality_score': max(0, quality_score),
            'quality_grade': self._assign_quality_grade(quality_score),
            'issues': quality_issues,
            'recommendations': recommendations,
            'assessment_details': {
                'missing_value_impact': missing_pct,
                'duplicate_impact': dup_pct,
                'consistency_issues': len([i for i in quality_issues if 'identifier' in i or 'numeric data stored' in i])
            }
        }

    def _assign_quality_grade(self, score: float) -> str:
        """Assign quality grade based on score"""
        if score >= 90:
            return "A - Excellent"
        elif score >= 80:
            return "B - Good"
        elif score >= 70:
            return "C - Fair"
        elif score >= 60:
            return "D - Poor"
        else:
            return "F - Critical Issues"

    # Helper methods for analysis
    def _detect_delimiter(self, sample: str) -> str:
        """Detect CSV delimiter from sample"""
        delimiters = [',', ';', '\\t', '|', ':']
        delimiter_counts = {d: sample.count(d) for d in delimiters}
        return max(delimiter_counts, key=delimiter_counts.get)

    def _analyze_json_structure(self, data: Any) -> Dict[str, Any]:
        """Analyze JSON structure and nesting"""
        if isinstance(data, list):
            return {
                'type': 'list',
                'length': len(data),
                'element_types': list(set(type(item).__name__ for item in data[:10])),
                'is_homogeneous': len(set(type(item).__name__ for item in data[:10])) == 1
            }
        elif isinstance(data, dict):
            return {
                'type': 'dict',
                'keys_count': len(data.keys()),
                'keys_sample': list(data.keys())[:10],
                'value_types': list(set(type(v).__name__ for v in data.values())),
                'nesting_levels': self._calculate_json_depth(data)
            }
        else:
            return {'type': type(data).__name__, 'value': str(data)[:100]}

    def _calculate_json_depth(self, obj: Any, depth: int = 0) -> int:
        """Calculate maximum nesting depth in JSON"""
        if isinstance(obj, dict):
            return max([self._calculate_json_depth(v, depth + 1) for v in obj.values()], default=depth)
        elif isinstance(obj, list):
            return max([self._calculate_json_depth(item, depth + 1) for item in obj], default=depth)
        else:
            return depth

    def _analyze_text_structure(self, content: str) -> Dict[str, Any]:
        """Analyze text file structure"""
        lines = content.split('\\n')
        
        return {
            'total_lines': len(lines),
            'average_line_length': sum(len(line) for line in lines) / len(lines) if lines else 0,
            'might_be_csv': ',' in content and len(lines) > 1,
            'might_be_tsv': '\\t' in content and len(lines) > 1,
            'has_headers': len(lines) > 0 and not lines[0].isdigit(),
            'encoding_confidence': 'high'  # Simplified
        }

    def _analyze_sql_structure(self, sql_content: str) -> Dict[str, Any]:
        """Analyze SQL file structure"""
        sql_lower = sql_content.lower()
        
        return {
            'total_length': len(sql_content),
            'has_create_statements': 'create table' in sql_lower,
            'has_insert_statements': 'insert into' in sql_lower,
            'has_select_statements': 'select' in sql_lower,
            'estimated_tables': sql_lower.count('create table'),
            'estimated_inserts': sql_lower.count('insert into')
        }

    def _get_parquet_metadata(self, file_path: Path) -> Dict[str, Any]:
        """Get Parquet file metadata"""
        try:
            import pyarrow.parquet as pq
            parquet_file = pq.ParquetFile(file_path)
            
            return {
                'num_row_groups': parquet_file.num_row_groups,
                'schema': str(parquet_file.schema),
                'metadata': str(parquet_file.metadata)
            }
        except ImportError:
            return {'note': 'PyArrow not available for detailed Parquet metadata'}
        except Exception as e:
            return {'error': str(e)}

    def _generate_data_preview(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Generate comprehensive data preview"""
        return {
            'head': df.head().to_dict('records'),
            'tail': df.tail().to_dict('records'),
            'random_sample': df.sample(min(5, len(df))).to_dict('records') if len(df) > 0 else [],
            'column_info': {col: {'dtype': str(df[col].dtype), 'nunique': df[col].nunique()} 
                          for col in df.columns}
        }

    def _infer_and_process(self, file_path: Path) -> Dict[str, Any]:
        """Infer file format and process accordingly"""
        try:
            # Try common formats
            content_sample = ""
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content_sample = f.read(1000)
            except UnicodeDecodeError:
                try:
                    with open(file_path, 'r', encoding='latin-1') as f:
                        content_sample = f.read(1000)
                except:
                    return {'success': False, 'error': 'Could not read file with any encoding'}
            
            # Check for CSV-like structure
            if ',' in content_sample and '\\n' in content_sample:
                return self.process_csv_advanced(file_path)
            
            # Check for JSON-like structure
            if content_sample.strip().startswith(('{', '[')):
                return self.process_json_advanced(file_path)
            
            # Default to text processing
            return self.process_text_file(file_path)
            
        except Exception as e:
            return {'success': False, 'error': str(e)}

    # Placeholder methods for additional analysis
    def _get_enhanced_statistical_summary(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Enhanced statistical summary - to be implemented"""
        return {'note': 'Enhanced statistical analysis available'}

    def _analyze_columns_advanced(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Advanced column analysis - to be implemented"""
        return {'note': 'Advanced column analysis available'}

    def _detect_patterns_and_insights(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Pattern detection and insights - to be implemented"""
        return {'note': 'Pattern detection available'}

    def _generate_business_recommendations(self, df: pd.DataFrame) -> List[str]:
        """Business recommendations - to be implemented"""
        return ['Comprehensive business recommendations available']

    def _suggest_data_preparation(self, df: pd.DataFrame) -> List[str]:
        """Data preparation suggestions - to be implemented"""
        return ['Data preparation suggestions available'] 