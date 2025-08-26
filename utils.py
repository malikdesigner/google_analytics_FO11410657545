#utils.py
"""
UTILITY FUNCTIONS MODULE
Helper functions and utilities for the enhanced search simulator
"""

import sys
import json
import logging
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

def setup_enhanced_logging():
    """Setup enhanced logging configuration"""
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('enhanced_search_simulator.log', encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ],
        force=True
    )

def create_enhanced_sample_data(output_file: str = "enhanced_search_data.json") -> str:
    """Create enhanced sample search data"""
    
    sample_data = [
        {"keyword": "supply list 2024-2025", "site": "https://getschoolsupplieslist.com/"},
        {"keyword": "causes lip swelling smileee", "site": "https://smileee.co.uk/"},
        {"keyword": "barber shop software", "site": "https://www.thecut.co/"},
        {"keyword": "artificial intelligence tutorials", "site": "https://www.tensorflow.org"},
        {"keyword": "python web scraping guide", "site": "https://docs.python.org"},
        {"keyword": "machine learning courses online", "site": "https://www.coursera.org"},
        {"keyword": "best laptops for programming", "site": "https://www.techradar.com"},
        {"keyword": "data science job opportunities", "site": "https://www.indeed.com"},
        {"keyword": "react native development", "site": "https://reactnative.dev"},
        {"keyword": "cloud computing basics", "site": "https://aws.amazon.com"},
        {"keyword": "digital marketing strategies", "site": "https://www.hubspot.com"},
        {"keyword": "cybersecurity best practices", "site": "https://www.cisco.com"}
    ]
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(sample_data, f, indent=2, ensure_ascii=False)
    
    return output_file

def validate_search_data(data: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """Validate search data format and content"""
    
    validated_data = []
    
    for i, item in enumerate(data):
        if isinstance(item, dict) and "keyword" in item and "site" in item:
            if item["keyword"].strip() and item["site"].strip():
                # Validate URL format
                try:
                    from urllib.parse import urlparse
                    parsed = urlparse(item["site"])
                    if parsed.scheme and parsed.netloc:
                        validated_data.append(item)
                    else:
                        logging.warning(f"Invalid URL format at index {i}: {item['site']}")
                except Exception as e:
                    logging.warning(f"URL parsing failed at index {i}: {item['site']} - {e}")
            else:
                logging.warning(f"Empty keyword or site at index {i}")
        else:
            logging.warning(f"Invalid item format at index {i}")
    
    return validated_data

def load_json_data(file_path: str) -> List[Dict[str, str]]:
    """Load and validate JSON data from file"""
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        logging.info(f"Loaded {len(data)} items from {file_path}")
        
        validated_data = validate_search_data(data)
        logging.info(f"Validated {len(validated_data)} search tasks")
        
        return validated_data
        
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
        raise
    except json.JSONDecodeError as e:
        logging.error(f"JSON decode error in {file_path}: {e}")
        raise
    except Exception as e:
        logging.error(f"Error loading data from {file_path}: {e}")
        raise

def save_json_data(data: Any, file_path: str, indent: int = 2):
    """Save data to JSON file"""
    
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=indent, ensure_ascii=False, default=str)
        
        logging.info(f"Data saved to {file_path}")
        
    except Exception as e:
        logging.error(f"Failed to save data to {file_path}: {e}")
        raise

def calculate_success_rate(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Calculate success rate and other metrics"""
    
    total = len(results)
    successful = sum(1 for r in results if r.get("success", False))
    
    metrics = {
        "total_searches": total,
        "successful_searches": successful,
        "failed_searches": total - successful,
        "success_rate": (successful / total) * 100 if total > 0 else 0,
        "failure_rate": ((total - successful) / total) * 100 if total > 0 else 0
    }
    
    return metrics

def calculate_performance_metrics(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Calculate detailed performance metrics"""
    
    if not results:
        return {}
    
    # Basic metrics
    success_metrics = calculate_success_rate(results)
    
    # Duration metrics
    durations = [r.get("duration", 0) for r in results if r.get("duration")]
    if durations:
        duration_metrics = {
            "avg_duration": sum(durations) / len(durations),
            "min_duration": min(durations),
            "max_duration": max(durations),
            "total_duration": sum(durations)
        }
    else:
        duration_metrics = {}
    
    # Activity metrics
    all_activities = []
    for result in results:
        activities = result.get("human_like_activities", [])
        all_activities.extend(activities)
    
    activity_metrics = {
        "total_activities": len(all_activities),
        "avg_activities_per_session": len(all_activities) / len(results) if results else 0
    }
    
    # Model integration metrics
    model_integrated = sum(1 for r in results if r.get("models_integrated", False))
    integration_metrics = {
        "model_integration_count": model_integrated,
        "model_integration_rate": (model_integrated / len(results)) * 100 if results else 0
    }
    
    # Combine all metrics
    performance_metrics = {
        **success_metrics,
        **duration_metrics,
        **activity_metrics,
        **integration_metrics,
        "analysis_timestamp": datetime.now().isoformat()
    }
    
    return performance_metrics

def generate_summary_report(results: List[Dict[str, Any]], output_file: str):
    """Generate a human-readable summary report"""
    
    metrics = calculate_performance_metrics(results)
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("ENHANCED HUMAN-LIKE SEARCH SIMULATION REPORT\n")
            f.write("=" * 50 + "\n\n")
            
            f.write(f"Generated: {metrics.get('analysis_timestamp', 'Unknown')}\n")
            f.write(f"Report Version: Enhanced Human-like v2.0 Modular\n\n")
            
            f.write("PERFORMANCE SUMMARY:\n")
            f.write(f"  Total Searches: {metrics.get('total_searches', 0)}\n")
            f.write(f"  Successful: {metrics.get('successful_searches', 0)}\n")
            f.write(f"  Failed: {metrics.get('failed_searches', 0)}\n")
            f.write(f"  Success Rate: {metrics.get('success_rate', 0):.1f}%\n\n")
            
            if metrics.get('avg_duration'):
                f.write("TIMING METRICS:\n")
                f.write(f"  Average Duration: {metrics.get('avg_duration', 0):.1f}s\n")
                f.write(f"  Minimum Duration: {metrics.get('min_duration', 0):.1f}s\n")
                f.write(f"  Maximum Duration: {metrics.get('max_duration', 0):.1f}s\n")
                f.write(f"  Total Duration: {metrics.get('total_duration', 0):.1f}s\n\n")
            
            f.write("HUMAN-LIKE BEHAVIOR METRICS:\n")
            f.write(f"  Total Activities: {metrics.get('total_activities', 0)}\n")
            f.write(f"  Average Activities per Session: {metrics.get('avg_activities_per_session', 0):.1f}\n\n")
            
            f.write("MODEL INTEGRATION:\n")
            f.write(f"  Sessions with Model Integration: {metrics.get('model_integration_count', 0)}\n")
            f.write(f"  Model Integration Rate: {metrics.get('model_integration_rate', 0):.1f}%\n\n")
            
            # Persona distribution
            persona_dist = {}
            for result in results:
                persona_type = result.get("persona", {}).get("type", "unknown")
                persona_dist[persona_type] = persona_dist.get(persona_type, 0) + 1
            
            if persona_dist:
                f.write("PERSONA DISTRIBUTION:\n")
                for persona, count in persona_dist.items():
                    percentage = (count / len(results)) * 100 if results else 0
                    f.write(f"  {persona}: {count} ({percentage:.1f}%)\n")
                f.write("\n")
            
            # Error analysis
            errors = [r.get("error") for r in results if r.get("error")]
            if errors:
                f.write("ERROR ANALYSIS:\n")
                error_counts = {}
                for error in errors:
                    error_type = str(error)[:50] + "..." if len(str(error)) > 50 else str(error)
                    error_counts[error_type] = error_counts.get(error_type, 0) + 1
                
                for error, count in sorted(error_counts.items(), key=lambda x: x[1], reverse=True):
                    f.write(f"  {error}: {count}\n")
        
        logging.info(f"Summary report generated: {output_file}")
        
    except Exception as e:
        logging.error(f"Failed to generate summary report: {e}")
        raise

def format_duration(seconds: float) -> str:
    """Format duration in seconds to human-readable format"""
    
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f}m"
    else:
        hours = seconds / 3600
        return f"{hours:.1f}h"

def get_timestamp() -> str:
    """Get current timestamp in ISO format"""
    return datetime.now().isoformat()

def ensure_directory_exists(file_path: str):
    """Ensure the directory for the file path exists"""
    
    directory = Path(file_path).parent
    directory.mkdir(parents=True, exist_ok=True)

def backup_file(file_path: str) -> str:
    """Create a backup of the file with timestamp"""
    
    if not Path(file_path).exists():
        return ""
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"{file_path}.backup_{timestamp}"
    
    try:
        import shutil
        shutil.copy2(file_path, backup_path)
        logging.info(f"Backup created: {backup_path}")
        return backup_path
    except Exception as e:
        logging.warning(f"Failed to create backup: {e}")
        return ""

def clean_old_backups(directory: str, pattern: str = "*.backup_*", keep_count: int = 5):
    """Clean old backup files, keeping only the most recent ones"""
    
    try:
        backup_files = list(Path(directory).glob(pattern))
        if len(backup_files) > keep_count:
            # Sort by modification time, newest first
            backup_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
            
            # Remove old backups
            for backup in backup_files[keep_count:]:
                backup.unlink()
                logging.info(f"Removed old backup: {backup}")
    
    except Exception as e:
        logging.warning(f"Failed to clean old backups: {e}")

def log_system_info():
    """Log system information for debugging"""
    
    try:
        import platform
        import psutil
        
        logging.info(f"System: {platform.system()} {platform.release()}")
        logging.info(f"Python: {platform.python_version()}")
        logging.info(f"CPU Count: {psutil.cpu_count()}")
        logging.info(f"Memory: {psutil.virtual_memory().total // (1024**3)}GB")
        
    except ImportError:
        logging.info("System info logging requires psutil package")
    except Exception as e:
        logging.debug(f"Failed to log system info: {e}")

def validate_config(config: Dict[str, Any]) -> Dict[str, Any]:
    """Validate and normalize configuration"""
    
    default_config = {
        "browser_timeout": 30000,
        "page_timeout": 25000,
        "max_retries": 3,
        "delay_range": (1, 5),
        "scroll_amount_range": (200, 600),
        "hover_duration_range": (1, 4),
        "typing_speed_range": (0.05, 0.2)
    }
    
    # Merge with defaults
    validated_config = {**default_config, **config}
    
    # Validate ranges
    for key in ["delay_range", "scroll_amount_range", "hover_duration_range", "typing_speed_range"]:
        if key in validated_config:
            value = validated_config[key]
            if isinstance(value, (list, tuple)) and len(value) == 2:
                validated_config[key] = tuple(sorted(value))
            else:
                logging.warning(f"Invalid range for {key}, using default")
                validated_config[key] = default_config[key]
    
    return validated_config

def emergency_save(data: Any, prefix: str = "emergency") -> str:
    """Save data with emergency filename"""
    
    timestamp = int(time.time())
    filename = f"{prefix}_{timestamp}.json"
    
    try:
        save_json_data(data, filename)
        return filename
    except Exception as e:
        logging.error(f"Emergency save failed: {e}")
        return ""

class ProgressTracker:
    """Simple progress tracking utility"""
    
    def __init__(self, total: int, description: str = "Processing"):
        self.total = total
        self.current = 0
        self.description = description
        self.start_time = time.time()
    
    def update(self, increment: int = 1):
        """Update progress"""
        self.current += increment
        self._log_progress()
    
    def _log_progress(self):
        """Log current progress"""
        if self.total > 0:
            percentage = (self.current / self.total) * 100
            elapsed = time.time() - self.start_time
            
            if self.current > 0:
                eta = (elapsed / self.current) * (self.total - self.current)
                eta_str = format_duration(eta)
            else:
                eta_str = "Unknown"
            
            logging.info(f"{self.description}: {self.current}/{self.total} "
                        f"({percentage:.1f}%) - ETA: {eta_str}")
    
    def complete(self):
        """Mark as complete"""
        self.current = self.total
        elapsed = time.time() - self.start_time
        logging.info(f"{self.description} completed in {format_duration(elapsed)}")

def check_dependencies() -> Dict[str, bool]:
    """Check if required dependencies are available"""
    
    dependencies = {
        "playwright": False,
        "asyncio": False,
        "json": False,
        "logging": False,
        "random": False,
        "time": False,
        "datetime": False,
        "pathlib": False,
        "typing": False,
        "urllib": False,
        "playwright_stealth": False
    }
    
    for dep in dependencies:
        try:
            if dep == "playwright_stealth":
                import playwright_stealth
            else:
                __import__(dep)
            dependencies[dep] = True
        except ImportError:
            dependencies[dep] = False
    
    return dependencies