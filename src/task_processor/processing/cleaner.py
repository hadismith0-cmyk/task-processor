"""
Data cleaning and normalization module
"""

import re
import logging
from typing import List, Dict, Optional
import unicodedata
import html


logger = logging.getLogger(__name__)


class TextCleaner:
    """Text cleaning and normalization utilities"""
    
    @staticmethod
    def normalize_unicode(text: str) -> str:
        """
        Normalize Unicode characters
        
        Args:
            text: Input text
            
        Returns:
            Normalized text
        """
        if not isinstance(text, str):
            return text
        return unicodedata.normalize('NFKC', text)
    
    @staticmethod
    def decode_html_entities(text: str) -> str:
        """
        Decode HTML entities
        
        Args:
            text: Text with HTML entities
            
        Returns:
            Decoded text
        """
        if not isinstance(text, str):
            return text
        return html.unescape(text)
    
    @staticmethod
    def remove_html_tags(text: str) -> str:
        """
        Remove HTML tags from text
        
        Args:
            text: Text with HTML
            
        Returns:
            Text without HTML tags
        """
        if not isinstance(text, str):
            return text
        return re.sub(r'<[^>]+>', '', text)
    
    @staticmethod
    def remove_urls(text: str) -> str:
        """
        Remove URLs from text
        
        Args:
            text: Text with URLs
            
        Returns:
            Text without URLs
        """
        if not isinstance(text, str):
            return text
        return re.sub(r'https?://\S+|www\.\S+', '', text)
    
    @staticmethod
    def remove_emails(text: str) -> str:
        """
        Remove email addresses from text
        
        Args:
            text: Text with emails
            
        Returns:
            Text without emails
        """
        if not isinstance(text, str):
            return text
        return re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '', text)
    
    @staticmethod
    def remove_special_chars(text: str, keep_chars: str = "") -> str:
        """
        Remove special characters
        
        Args:
            text: Input text
            keep_chars: Characters to keep (in addition to alphanumeric)
            
        Returns:
            Text with special chars removed
        """
        if not isinstance(text, str):
            return text
        pattern = f'[^a-zA-Z0-9\\s{re.escape(keep_chars)}]'
        return re.sub(pattern, '', text)
    
    @staticmethod
    def normalize_whitespace(text: str) -> str:
        """
        Normalize whitespace
        
        Args:
            text: Input text
            
        Returns:
            Text with normalized whitespace
        """
        if not isinstance(text, str):
            return text
        # Replace multiple spaces with single space
        text = re.sub(r'\s+', ' ', text)
        # Strip leading/trailing whitespace
        return text.strip()
    
    @staticmethod
    def remove_control_chars(text: str) -> str:
        """
        Remove control characters
        
        Args:
            text: Input text
            
        Returns:
            Text without control characters
        """
        if not isinstance(text, str):
            return text
        return ''.join(char for char in text if unicodedata.category(char)[0] != 'C')
    
    @staticmethod
    def clean_text(
        text: str,
        normalize_unicode: bool = True,
        decode_html: bool = True,
        remove_html: bool = True,
        remove_urls_flag: bool = False,
        remove_emails_flag: bool = False,
        normalize_ws: bool = True,
        lowercase: bool = False
    ) -> str:
        """
        Comprehensive text cleaning
        
        Args:
            text: Input text
            normalize_unicode: Normalize Unicode
            decode_html: Decode HTML entities
            remove_html: Remove HTML tags
            remove_urls_flag: Remove URLs
            remove_emails_flag: Remove emails
            normalize_ws: Normalize whitespace
            lowercase: Convert to lowercase
            
        Returns:
            Cleaned text
        """
        if not isinstance(text, str):
            return text
        
        if normalize_unicode:
            text = TextCleaner.normalize_unicode(text)
        
        if decode_html:
            text = TextCleaner.decode_html_entities(text)
        
        if remove_html:
            text = TextCleaner.remove_html_tags(text)
        
        if remove_urls_flag:
            text = TextCleaner.remove_urls(text)
        
        if remove_emails_flag:
            text = TextCleaner.remove_emails(text)
        
        text = TextCleaner.remove_control_chars(text)
        
        if normalize_ws:
            text = TextCleaner.normalize_whitespace(text)
        
        if lowercase:
            text = text.lower()
        
        return text


class LanguageDetector:
    """Language detection and filtering"""
    
    COMMON_STOPWORDS = {
        'en': ['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'is', 'are'],
        'es': ['el', 'la', 'de', 'que', 'y', 'a', 'en', 'un', 'ser', 'se'],
        'fr': ['le', 'de', 'un', 'et', 'à', 'être', 'en', 'que', 'pour', 'dans'],
    }
    
    @staticmethod
    def detect_language(text: str, default: str = 'en') -> str:
        """
        Detect language of text
        
        Args:
            text: Input text
            default: Default language if detection fails
            
        Returns:
            Language code (e.g., 'en', 'es', 'fr')
        """
        try:
            from textblob import TextBlob
            blob = TextBlob(str(text))
            return blob.detect_language()
        except ImportError:
            logger.warning("textblob not installed for language detection")
            return default
        except Exception as e:
            logger.debug(f"Language detection failed: {e}")
            return default
    
    @staticmethod
    def filter_by_language(texts: List[str], language: str = 'en') -> List[str]:
        """
        Filter texts by language
        
        Args:
            texts: List of texts
            language: Language code to filter for
            
        Returns:
            Filtered texts
        """
        filtered = []
        for text in texts:
            if LanguageDetector.detect_language(text) == language:
                filtered.append(text)
        
        logger.info(f"Language filter: {len(texts)} -> {len(filtered)} texts")
        return filtered


class NoiseRemover:
    """Remove noise from data"""
    
    @staticmethod
    def remove_repeated_chars(text: str, max_repeat: int = 3) -> str:
        """
        Remove repeated characters
        
        Args:
            text: Input text
            max_repeat: Maximum allowed repetitions
            
        Returns:
            Text with repeated chars removed
        """
        if not isinstance(text, str):
            return text
        return re.sub(f'(.)\{{max_repeat},}}', r'\1' * max_repeat, text)
    
    @staticmethod
    def filter_by_length(
        texts: List[str],
        min_length: int = 10,
        max_length: int = 10000
    ) -> List[str]:
        """
        Filter texts by length
        
        Args:
            texts: List of texts
            min_length: Minimum text length
            max_length: Maximum text length
            
        Returns:
            Filtered texts
        """
        filtered = [
            text for text in texts
            if min_length <= len(text) <= max_length
        ]
        logger.info(f"Length filter: {len(texts)} -> {len(filtered)} texts")
        return filtered
    
    @staticmethod
    def remove_empty_lines(text: str) -> str:
        """
        Remove empty lines from text
        
        Args:
            text: Input text
            
        Returns:
            Text without empty lines
        """
        if not isinstance(text, str):
            return text
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        return '\n'.join(lines)


class DataValidator:
    """Validate data quality"""
    
    @staticmethod
    def is_valid_text(text: str, min_length: int = 5) -> bool:
        """
        Check if text is valid
        
        Args:
            text: Text to validate
            min_length: Minimum length
            
        Returns:
            True if valid
        """
        if not isinstance(text, str):
            return False
        
        cleaned = text.strip()
        if len(cleaned) < min_length:
            return False
        
        # Check for excessive noise
        special_ratio = len(re.findall(r'[^a-zA-Z0-9\s]', cleaned)) / len(cleaned)
        if special_ratio > 0.5:
            return False
        
        return True
    
    @staticmethod
    def validate_texts(texts: List[str]) -> Dict[str, any]:
        """
        Validate list of texts
        
        Args:
            texts: List of texts
            
        Returns:
            Validation report
        """
        valid = sum(1 for text in texts if DataValidator.is_valid_text(text))
        
        return {
            "total": len(texts),
            "valid": valid,
            "invalid": len(texts) - valid,
            "validity_rate": valid / len(texts) if texts else 0,
        }
