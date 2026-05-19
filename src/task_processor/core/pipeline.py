"""Core pipeline orchestrator"""

import os
import json
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
from pathlib import Path


logger = logging.getLogger(__name__)


class Pipeline:
    """Task pipeline orchestrator"""
    
    def __init__(self, config: 'PipelineConfig' = None):
        """Initialize pipeline"""
        self.config = config
        self.metrics = {}
        self.errors = []
        
    def discover_tasks(self, task_dir: str) -> List[Dict[str, Any]]:
        """
        Discover tasks from directory
        
        Args:
            task_dir: Directory containing tasks
            
        Returns:
            List of discovered tasks
        """
        tasks = []
        task_dir = Path(task_dir)
        
        if not task_dir.exists():
            logger.error(f"Task directory not found: {task_dir}")
            return tasks
        
        # Find all Task_* folders
        for item in sorted(task_dir.iterdir()):
            if item.is_dir() and item.name.startswith('Task_'):
                log_file = item / 'log.txt'
                if log_file.exists():
                    tasks.append({
                        'name': item.name,
                        'path': str(item),
                        'log_file': str(log_file),
                        'version': self._extract_version(item.name)
                    })
        
        # Sort by version number
        tasks.sort(key=lambda x: x['version'])
        logger.info(f"Discovered {len(tasks)} tasks")
        return tasks
    
    def _extract_version(self, task_name: str) -> tuple:
        """
        Extract version number from task name
        
        Args:
            task_name: Task name (e.g., 'Task_gggggg_1.0000')
            
        Returns:
            Version tuple for sorting
        """
        try:
            version = task_name.split('_')[-1]
            parts = version.split('.')
            return tuple(int(p) for p in parts)
        except:
            return (0, 0)
    
    def parse_task_metadata(self, log_file: str) -> Dict[str, Any]:
        """
        Parse task metadata from log file
        
        Args:
            log_file: Path to log file
            
        Returns:
            Metadata dictionary
        """
        metadata = {}
        
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract key-value pairs
            lines = content.split('\n')
            current_key = None
            current_value = []
            
            for line in lines:
                if ':' in line and not line.startswith(' '):
                    if current_key:
                        metadata[current_key] = '\n'.join(current_value).strip()
                    key, value = line.split(':', 1)
                    current_key = key.strip()
                    current_value = [value.strip()]
                elif current_key and line.strip():
                    current_value.append(line.strip())
            
            if current_key:
                metadata[current_key] = '\n'.join(current_value).strip()
            
            logger.info(f"Parsed metadata: {len(metadata)} fields")
            return metadata
        except Exception as e:
            logger.error(f"Error parsing metadata: {e}")
            return {}
    
    def execute(self, task_dir: str, output_dir: str) -> Dict[str, Any]:
        """
        Execute pipeline on all tasks
        
        Args:
            task_dir: Input task directory
            output_dir: Output directory for results
            
        Returns:
            Pipeline metrics
        """
        # Create output directory
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Discover tasks
        tasks = self.discover_tasks(task_dir)
        
        if not tasks:
            logger.warning("No tasks found")
            return self.metrics
        
        # Process each task
        start_time = datetime.now()
        successful = 0
        failed = 0
        
        for task in tasks:
            try:
                logger.info(f"Processing task: {task['name']}")
                
                # Parse metadata
                metadata = self.parse_task_metadata(task['log_file'])
                
                # Create result
                result = {
                    'task_name': task['name'],
                    'timestamp': datetime.now().isoformat(),
                    'metadata': metadata,
                    'status': 'completed'
                }
                
                # Save result
                task_output_dir = output_path / task['name']
                task_output_dir.mkdir(parents=True, exist_ok=True)
                
                result_file = task_output_dir / 'result.json'
                with open(result_file, 'w', encoding='utf-8') as f:
                    json.dump(result, f, indent=2)
                
                logger.info(f"Saved result: {result_file}")
                successful += 1
                
            except Exception as e:
                logger.error(f"Task failed: {task['name']} - {e}")
                self.errors.append({'task': task['name'], 'error': str(e)})
                failed += 1
        
        # Calculate metrics
        end_time = datetime.now()
        self.metrics = {
            'total_tasks': len(tasks),
            'successful': successful,
            'failed': failed,
            'success_rate': successful / len(tasks) if tasks else 0,
            'duration_seconds': (end_time - start_time).total_seconds(),
            'timestamp': start_time.isoformat()
        }
        
        logger.info(f"Pipeline completed: {successful}/{len(tasks)} successful")
        return self.metrics
