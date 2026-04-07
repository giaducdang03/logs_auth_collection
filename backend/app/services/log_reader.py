import logging
import os
from datetime import datetime, timedelta
from typing import List, Optional
from app.utils.log_parser import SSHLogParser
from app.utils.exceptions import LogParsingException


logger = logging.getLogger(__name__)


class LogReaderService:
    """Service for reading and parsing SSH logs"""
    
    def __init__(self, log_file_path: str = "/var/log/auth.log", offset_file: str = "/state/.log_offset"):
        self.log_file_path = log_file_path
        self.offset_file = offset_file
    
    def get_last_offset(self) -> int:
        """Get the last read offset from tracking file"""
        if os.path.exists(self.offset_file):
            try:
                with open(self.offset_file, "r") as f:
                    offset = int(f.read().strip())
                    logger.debug("Loaded last log offset %s from %s", offset, self.offset_file)
                    return offset
            except Exception as exc:
                logger.warning("Failed to read offset file %s, starting from 0: %s", self.offset_file, exc)
                return 0
        logger.debug("Offset file %s not found, starting from 0", self.offset_file)
        return 0
    
    def save_offset(self, offset: int):
        """Save current read offset to tracking file"""
        try:
            with open(self.offset_file, "w") as f:
                f.write(str(offset))
            logger.debug("Saved log offset %s to %s", offset, self.offset_file)
        except Exception as e:
            raise LogParsingException(f"Failed to save offset: {str(e)}")
    
    def read_new_logs(self, initial_days: int = 2, large_file_mb: int = 20) -> List[str]:
        """Read new logs; on first run with large files, keep only the last N days."""
        logger.info("Reading SSH logs from %s", self.log_file_path)

        if not os.path.exists(self.log_file_path):
            logger.error("Log file not found at %s", self.log_file_path)
            raise LogParsingException(f"Log file not found: {self.log_file_path}")
        
        try:
            last_offset = self.get_last_offset()
            new_logs = []
            file_size_bytes = os.path.getsize(self.log_file_path)
            size_threshold_bytes = max(1, large_file_mb) * 1024 * 1024
            is_initial_large_read = last_offset == 0 and file_size_bytes > size_threshold_bytes
            cutoff_time = datetime.now() - timedelta(days=max(1, initial_days))

            logger.info(
                "Log read mode=%s file_size_bytes=%s last_offset=%s offset_file=%s",
                "initial-large" if is_initial_large_read else ("incremental" if last_offset > 0 else "full"),
                file_size_bytes,
                last_offset,
                self.offset_file,
            )
            
            with open(self.log_file_path, "r") as f:
                # Normal incremental mode: read from last offset.
                if last_offset > 0:
                    logger.debug("Seeking to last offset %s in %s", last_offset, self.log_file_path)
                    f.seek(last_offset)

                    for line in f:
                        stripped_line = line.strip()
                        if stripped_line:
                            new_logs.append(stripped_line)

                # First run with a large file: keep only parseable lines from the last N days.
                else:
                    if is_initial_large_read:
                        logger.info(
                            "Initial large log file detected; keeping only parseable lines newer than %s",
                            cutoff_time.isoformat(),
                        )

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

            logger.info(
                "Finished reading SSH logs from %s: %s new lines collected, next offset=%s",
                self.log_file_path,
                len(new_logs),
                current_offset,
            )
            
            return new_logs
        
        except Exception as e:
            logger.exception("Failed while reading SSH logs from %s", self.log_file_path)
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
