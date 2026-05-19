"""Monitoring and metrics collection"""

import logging
import time
from typing import Dict, Any, List
from datetime import datetime


logger = logging.getLogger(__name__)


class MetricsCollector:
    """Collect pipeline metrics"""
    
    def __init__(self):
        """Initialize metrics collector"""
        self.metrics: Dict[str, Any] = {}
        self.start_time = None
        self.errors: List[Dict[str, Any]] = []
        
    def start(self) -> None:
        """Start metrics collection"""
        self.start_time = time.time()
        self.metrics['start_time'] = datetime.now().isoformat()
        logger.info("Metrics collection started")
    
    def end(self) -> Dict[str, Any]:
        """End metrics collection"""
        if self.start_time:
            duration = time.time() - self.start_time
            self.metrics['duration_seconds'] = duration
            self.metrics['end_time'] = datetime.now().isoformat()
            logger.info(f"Metrics collection ended - Duration: {duration:.2f}s")
        
        return self.metrics
    
    def record_task(self, task_name: str, status: str, duration: float) -> None:
        """Record task metrics"""
        if 'tasks' not in self.metrics:
            self.metrics['tasks'] = []
        
        self.metrics['tasks'].append({
            'name': task_name,
            'status': status,
            'duration_seconds': duration,
            'timestamp': datetime.now().isoformat()
        })
    
    def record_error(self, task_name: str, error_message: str) -> None:
        """Record error"""
        self.errors.append({
            'task': task_name,
            'error': error_message,
            'timestamp': datetime.now().isoformat()
        })
    
    def get_summary(self) -> Dict[str, Any]:
        """Get metrics summary"""
        tasks = self.metrics.get('tasks', [])
        total_tasks = len(tasks)
        successful = sum(1 for t in tasks if t['status'] == 'completed')
        failed = total_tasks - successful
        
        return {
            'total_tasks': total_tasks,
            'successful': successful,
            'failed': failed,
            'success_rate': successful / total_tasks if total_tasks > 0 else 0,
            'errors': self.errors,
            'duration_seconds': self.metrics.get('duration_seconds', 0)
        }
