# Task Processor - Data Pipeline Orchestration System

## Overview

Task Processor is a comprehensive Python-based data pipeline orchestration system designed to automate data extraction, cleaning, deduplication, and analysis workflows.

## Features

### 🎯 Core Features
- **Automatic Task Discovery** - Finds all tasks in directory structure
- **Version-Based Sorting** - Processes tasks in numerical order (1.0000 → 1.0004)
- **Metadata Extraction** - Parses task metadata from log.txt files
- **JSON Result Generation** - Creates structured output for each task
- **Real-time Monitoring** - Tracks pipeline execution metrics
- **Error Analytics** - Comprehensive logging and error collection
- **Modular Architecture** - Easy to extend with new processing stages

### 🧹 Data Cleaning & Normalization
- Unicode normalization (NFKC)
- HTML entity decoding
- HTML tag removal
- Noise removal
- Language detection
- Length filtering
- Stopword and spam filtering

### 🔄 Deduplication
- Exact deduplication (MD5 hashing)
- Fuzzy deduplication (SequenceMatcher)
- Semantic deduplication (embedding similarity)
- Duplicate statistics and reporting

### 📺 Observability & Monitoring
- Real-time progress tracking
- Pipeline metrics dashboard
- Error analytics
- Throughput monitoring
- Success rate reporting
- Stage-level diagnostics

## Installation

```bash
git clone https://github.com/hadismith0-cmyk/task-processor.git
cd task-processor
pip install -r requirements.txt
```

## Quick Start

### Using Python API

```python
from task_processor.core.pipeline import Pipeline
from task_processor.config.config import PipelineConfig

# Create configuration
config = PipelineConfig(
    name="my-pipeline",
    task_dir="./tasks",
    output_dir="./results"
)

# Create and execute pipeline
pipeline = Pipeline(config)
metrics = pipeline.execute("./tasks", "./results")

print(metrics)
```

### Using CLI

```bash
python -m task_processor.cli.cli --task-dir ./tasks --output-dir ./results --name my-pipeline
```

## Project Structure

```
task-processor/
├── src/task_processor/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   └── pipeline.py              # Main pipeline orchestrator
│   ├── config/
│   │   ├── __init__.py
│   │   └── config.py                # Configuration management
│   ├── monitoring/
│   │   ├── __init__.py
│   │   └── metrics.py               # Metrics collection
│   ├── processing/
│   │   ├── __init__.py
│   │   ├── cleaner.py               # Text cleaning
│   │   └── deduplicator.py          # Deduplication
│   └── cli/
│       ├── __init__.py
│       └── cli.py                   # Command-line interface
├── requirements.txt                 # Python dependencies
└── README.md
```

## Task Structure

Tasks should be organized as follows:

```
tasks/
├── Task_gggggg_1.0000/
│   ├── DataFiles/
│   ├── JsonExample/
│   └── log.txt
└── Task_ghjjj_1.0004/
    ├── DataFiles/
    ├── JsonExample/
    └── log.txt
```

### log.txt Format

```
TASK: mechanics
SEQUENCE: 1
STATUS: New
CREATED: 2026-05-18T04:54:28.170Z

DETAIL: Task description

PROMPT: Task prompt

TMAX: 512MB
MIN REFINED: 64MB

LINKS:
https://example.com
https://example2.com
```

## Data Processing Pipeline

1. **Task Discovery** → Finds all `Task_*` folders
2. **Version Sorting** → Processes in order (1.0000, 1.0004, etc.)
3. **Metadata Extraction** → Parses log.txt content
4. **Result Generation** → Creates JSON output
5. **Metrics Collection** → Tracks performance metrics
6. **Error Reporting** → Logs any failures

## Output Format

For each task, a `result.json` file is generated:

```json
{
  "task_name": "Task_gggggg_1.0000",
  "timestamp": "2026-05-19T04:54:28.170Z",
  "metadata": {
    "TASK": "mechanics",
    "SEQUENCE": "1",
    "STATUS": "New",
    "DETAIL": "Task description",
    "PROMPT": "Task prompt",
    "TMAX": "512MB",
    "MIN REFINED": "64MB",
    "LINKS": "https://example.com\nhttps://example2.com"
  },
  "status": "completed"
}
```

## Performance Metrics

The pipeline generates comprehensive metrics:

```python
{
    "total_tasks": 10,
    "successful": 10,
    "failed": 0,
    "success_rate": 1.0,
    "duration_seconds": 23.45,
    "timestamp": "2026-05-19T04:54:28.170Z"
}
```

## Configuration

Create a `config.yaml`:

```yaml
name: my-pipeline
task_dir: ./tasks
output_dir: ./results
processing:
  clean_text: true
  remove_duplicates: true
monitoring:
  collect_metrics: true
  log_level: INFO
```

## API Reference

### Pipeline

```python
Pipeline(config: PipelineConfig)
  .discover_tasks(task_dir: str) -> List[Dict]
  .parse_task_metadata(log_file: str) -> Dict
  .execute(task_dir: str, output_dir: str) -> Dict
```

### TextCleaner

```python
TextCleaner.clean_text(text: str) -> str
TextCleaner.normalize_unicode(text: str) -> str
TextCleaner.remove_html_tags(text: str) -> str
TextCleaner.remove_urls(text: str) -> str
```

### Deduplicator

```python
Deduplicator.exact_dedup(items: List[str]) -> Tuple[List[str], Dict]
Deduplicator.fuzzy_dedup(items: List[str], threshold: float) -> Tuple[List[str], Dict]
```

### MetricsCollector

```python
MetricsCollector()
  .start() -> None
  .end() -> Dict
  .record_task(task_name: str, status: str, duration: float) -> None
  .get_summary() -> Dict
```

## Performance Requirements

- **Memory**: MIN REFINED: 64MB | TMAX: 512MB
- **Processing**: Optimized for large-scale data processing
- **Throughput**: Real-time metrics tracking

## Contributing

Contributions are welcome! Please submit pull requests or open issues.

## License

MIT License

## Author

Hadi Smith - [@hadismith0-cmyk](https://github.com/hadismith0-cmyk)

## Support

For issues and questions, please open an issue on GitHub.
