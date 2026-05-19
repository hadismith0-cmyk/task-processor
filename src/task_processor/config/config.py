"""Pipeline configuration management"""

import yaml
import json
import os
from typing import Dict, Any, Optional
from pathlib import Path
import logging


logger = logging.getLogger(__name__)


class PipelineConfig:
    """Pipeline configuration"""
    
    def __init__(
        self,
        name: str = "default",
        task_dir: str = "./tasks",
        output_dir: str = "./results",
        config_dict: Optional[Dict[str, Any]] = None
    ):
        """Initialize configuration"""
        self.name = name
        self.task_dir = task_dir
        self.output_dir = output_dir
        self.config = config_dict or {}
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'name': self.name,
            'task_dir': self.task_dir,
            'output_dir': self.output_dir,
            **self.config
        }
    
    def save_yaml(self, path: str) -> None:
        """Save configuration as YAML"""
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, 'w') as f:
            yaml.dump(self.to_dict(), f)
        
        logger.info(f"Config saved: {path}")
    
    def load_yaml(self, path: str) -> None:
        """Load configuration from YAML"""
        with open(path, 'r') as f:
            data = yaml.safe_load(f)
        
        self.name = data.get('name', self.name)
        self.task_dir = data.get('task_dir', self.task_dir)
        self.output_dir = data.get('output_dir', self.output_dir)
        self.config = data
        
        logger.info(f"Config loaded: {path}")
    
    def validate(self) -> bool:
        """Validate configuration"""
        if not self.name:
            logger.error("Pipeline name is required")
            return False
        
        return True
