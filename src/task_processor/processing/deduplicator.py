"""
Data deduplication module
"""

import hashlib
from typing import List, Dict, Set, Tuple
import logging


logger = logging.getLogger(__name__)


class Deduplicator:
    """Data deduplication utilities"""
    
    @staticmethod
    def exact_hash(text: str) -> str:
        """
        Generate MD5 hash for exact deduplication
        
        Args:
            text: Text to hash
            
        Returns:
            MD5 hash string
        """
        if not isinstance(text, str):
            text = str(text)
        return hashlib.md5(text.encode()).hexdigest()
    
    @staticmethod
    def exact_dedup(items: List[str]) -> Tuple[List[str], Dict[str, int]]:
        """
        Remove exact duplicates
        
        Args:
            items: List of items
            
        Returns:
            Tuple of (unique items, duplicate counts)
        """
        seen: Dict[str, int] = {}
        unique: List[str] = []
        
        for item in items:
            hash_val = Deduplicator.exact_hash(item)
            if hash_val not in seen:
                seen[hash_val] = 0
                unique.append(item)
            seen[hash_val] += 1
        
        # Return duplicates info (count - 1 since first occurrence isn't a duplicate)
        duplicates = {k: v - 1 for k, v in seen.items() if v > 1}
        logger.info(f"Removed {sum(duplicates.values())} exact duplicates from {len(items)} items")
        return unique, duplicates
    
    @staticmethod
    def fuzzy_dedup(items: List[str], threshold: float = 0.95) -> Tuple[List[str], Dict[str, List[str]]]:
        """
        Remove fuzzy duplicates (similar items)
        
        Args:
            items: List of items
            threshold: Similarity threshold (0-1)
            
        Returns:
            Tuple of (deduplicated items, similarity groups)
        """
        try:
            from difflib import SequenceMatcher
            
            unique: List[str] = []
            groups: Dict[str, List[str]] = {}
            
            for item in items:
                is_duplicate = False
                for existing in unique:
                    ratio = SequenceMatcher(None, item, existing).ratio()
                    if ratio >= threshold:
                        if existing not in groups:
                            groups[existing] = []
                        groups[existing].append(item)
                        is_duplicate = True
                        break
                
                if not is_duplicate:
                    unique.append(item)
            
            logger.info(f"Fuzzy dedup: {len(items)} items -> {len(unique)} unique items")
            return unique, groups
        except Exception as e:
            logger.error(f"Fuzzy deduplication failed: {e}")
            return items, {}
    
    @staticmethod
    def semantic_dedup(
        items: List[str],
        embeddings: List[List[float]] = None,
        threshold: float = 0.95
    ) -> Tuple[List[str], Dict[int, List[int]]]:
        """
        Remove semantic duplicates using embeddings
        
        Args:
            items: List of items
            embeddings: Pre-computed embeddings (optional)
            threshold: Similarity threshold
            
        Returns:
            Tuple of (unique items, duplicate indices)
        """
        if embeddings is None:
            logger.warning("No embeddings provided for semantic deduplication")
            return items, {}
        
        try:
            from sklearn.metrics.pairwise import cosine_similarity
            import numpy as np
            
            similarity_matrix = cosine_similarity(embeddings)
            unique_indices: Set[int] = set(range(len(items)))
            duplicates: Dict[int, List[int]] = {}
            
            for i in range(len(items)):
                if i not in unique_indices:
                    continue
                
                similar_indices = []
                for j in range(i + 1, len(items)):
                    if j not in unique_indices:
                        continue
                    
                    if similarity_matrix[i][j] >= threshold:
                        similar_indices.append(j)
                        unique_indices.discard(j)
                
                if similar_indices:
                    duplicates[i] = similar_indices
            
            unique_items = [items[i] for i in sorted(unique_indices)]
            logger.info(f"Semantic dedup: {len(items)} items -> {len(unique_items)} unique items")
            return unique_items, duplicates
        except ImportError:
            logger.warning("sklearn not installed for semantic deduplication")
            return items, {}
        except Exception as e:
            logger.error(f"Semantic deduplication failed: {e}")
            return items, {}


class DuplicateDetector:
    """Detect various types of duplicates"""
    
    @staticmethod
    def find_exact_duplicates(items: List[str]) -> Dict[str, List[int]]:
        """
        Find exact duplicates with their indices
        
        Args:
            items: List of items
            
        Returns:
            Dict mapping items to list of indices
        """
        index_map: Dict[str, List[int]] = {}
        
        for idx, item in enumerate(items):
            hash_val = Deduplicator.exact_hash(item)
            if hash_val not in index_map:
                index_map[hash_val] = []
            index_map[hash_val].append(idx)
        
        # Return only duplicates
        return {k: v for k, v in index_map.items() if len(v) > 1}
    
    @staticmethod
    def get_duplicate_stats(items: List[str]) -> Dict[str, any]:
        """
        Get duplicate statistics
        
        Args:
            items: List of items
            
        Returns:
            Statistics dictionary
        """
        duplicates = DuplicateDetector.find_exact_duplicates(items)
        
        total_duplicates = sum(len(indices) - 1 for indices in duplicates.values())
        
        return {
            "total_items": len(items),
            "unique_items": len(items) - total_duplicates,
            "duplicate_items": total_duplicates,
            "duplicate_groups": len(duplicates),
            "duplication_rate": total_duplicates / len(items) if items else 0,
        }
