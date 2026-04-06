import os
from datetime import datetime, timedelta
from typing import List, Optional
from app.utils.log_parser import SSHLogParser
from app.utils.exceptions import LogParsingException


class LogReaderService:
    """Service for reading and parsing SSH logs"""
    
    def __init__(self, log_file_path: str = "/var/log/auth.log"):
        self.log_file_path = log_file_path
        self.offset_file = ".log_offset"
    
    def get_last_offset(self) -> int:
        """Get the last read offset from tracking file"""
        if os.path.exists(self.offset_file):
            try:
                with open(self.offset_file, "r") as f:
                    return int(f.read().strip())
            except Exception:
                return 0
        return 0
    
    def save_offset(self, offset: int):
        """Save current read offset to tracking file"""
        try:
            with open(self.offset_file, "w") as f:
                f.write(str(offset))
        except Exception as e:
            raise LogParsingException(f"Failed to save offset: {str(e)}")
    
    def read_new_logs(self, initial_days: int = 2, large_file_mb: int = 20) -> List[str]:
        """Read new logs; on first run with large files, keep only the last N days."""
        if not os.path.exists(self.log_file_path):
            raise LogParsingException(f"Log file not found: {self.log_file_path}")
        
        try:
            last_offset = self.get_last_offset()
            new_logs = []
            file_size_bytes = os.path.getsize(self.log_file_path)
            size_threshold_bytes = max(1, large_file_mb) * 1024 * 1024
            is_initial_large_read = last_offset == 0 and file_size_bytes > size_threshold_bytes
            cutoff_time = datetime.now() - timedelta(days=max(1, initial_days))
            
            with open(self.log_file_path, "r") as f:
                # Normal incremental mode: read from last offset.
                if last_offset > 0:
                    f.seek(last_offset)

                    for line in f:
                        stripped_line = line.strip()
                        if stripped_line:
                            new_logs.append(stripped_line)

                # First run with a large file: keep only parseable lines from the last N days.
                else:
                    for line in f:
                        stripped_line = line.strip()
                        if not stripped_line:
                            continue

                        if is_initial_large_read:
                            parsed_line = SSHLogParser.parse_log_line(stripped_line)
                            if not parsed_line:
                                continue
                            if parsed_line["login_time"] < cutoff_time:
                                continue

                        new_logs.append(stripped_line)
                
                # Save current offset
                current_offset = f.tell()
                self.save_offset(current_offset)
            
            return new_logs
        
        except Exception as e:
            raise LogParsingException(f"Failed to read log file: {str(e)}")
    
    @staticmethod
    def parse_logs(log_lines: List[str]) -> List[dict]:
        """Parse log lines into structured data"""
        parsed_logs = []
        
        for line in log_lines:
            if not line.strip():
                continue
            
            parsed = SSHLogParser.parse_log_line(line)
            if parsed:
                parsed_logs.append(parsed)
        
        return parsed_logs
