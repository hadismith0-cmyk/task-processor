"""Command-line interface"""

import argparse
import logging
from pathlib import Path
from task_processor.core.pipeline import Pipeline
from task_processor.config.config import PipelineConfig
from task_processor.monitoring.metrics import MetricsCollector


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(description='Task Processor - Data Pipeline Orchestration')
    
    parser.add_argument('--task-dir', default='./tasks', help='Input task directory')
    parser.add_argument('--output-dir', default='./results', help='Output directory')
    parser.add_argument('--name', default='task-processor', help='Pipeline name')
    
    args = parser.parse_args()
    
    # Create config
    config = PipelineConfig(
        name=args.name,
        task_dir=args.task_dir,
        output_dir=args.output_dir
    )
    
    if not config.validate():
        logger.error("Configuration validation failed")
        return 1
    
    # Create pipeline
    pipeline = Pipeline(config)
    
    # Create metrics collector
    metrics = MetricsCollector()
    metrics.start()
    
    # Execute pipeline
    try:
        result = pipeline.execute(args.task_dir, args.output_dir)
        logger.info(f"Pipeline completed successfully")
        logger.info(f"Summary: {result['total_tasks']} total, {result['successful']} successful, {result['failed']} failed")
        logger.info(f"Duration: {result['duration_seconds']:.2f} seconds")
    except Exception as e:
        logger.error(f"Pipeline execution failed: {e}")
        return 1
    finally:
        metrics.end()
        summary = metrics.get_summary()
        logger.info(f"Metrics: {summary}")
    
    return 0


if __name__ == '__main__':
    exit(main())
