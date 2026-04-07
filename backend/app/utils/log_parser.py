import re
from datetime import datetime
from typing import Optional, Dict, Any
import socket


class SSHLogParser:
    """Parse SSH logs from /var/log/auth.log"""
    
    # Sample patterns to match
    PATTERNS = [
        # Accepted password/publickey
        r"(\w+\s+\d+\s+\d+:\d+:\d+).*sshd\[\d+\]:\s+(Accepted|Failed)\s+(\w+)\s+for\s+(?:invalid user\s+)?(\S+)\s+from\s+(\S+)",
        # Invalid user
        r"(\w+\s+\d+\s+\d+:\d+:\d+).*sshd\[\d+\]:\s+(Invalid user)\s+(\S+)\s+from\s+(\S+)",
    ]
    
    @staticmethod
    def parse_timestamp(timestamp_str: str, year: int = None) -> datetime:
        """Parse timestamp from syslog format (e.g., 'Mar  6 15:30:45')"""
        if year is None:
            year = datetime.now().year
        
        try:
            dt = datetime.strptime(f"{timestamp_str} {year}", "%b %d %H:%M:%S %Y")
            return dt
        except ValueError:
            return datetime.now()
    
    @staticmethod
    def extract_ssh_key(raw_log: str) -> Optional[str]:
        """Extract SSH key info from log line (e.g., ssh2: ED25519 SHA256:...)"""
        # Pattern: ssh2: ED25519 SHA256:OzMsdVj2smLr5dl5GQSXRJmdruwtf5Mfc18VRz7+IzQ
        match = re.search(r"ssh2:\s+(\S+\s+\S+:\S+)$", raw_log)
        if match:
            return match.group(1).strip()
        
        # Alternative pattern without ssh2: prefix (some versions)
        match = re.search(r"((?:ED25519|RSA|ECDSA|ssh-ed25519|ssh-rsa|ecdsa-sha2-nistp256)\s+SHA256:\S+)$", raw_log)
        if match:
            return match.group(1).strip()
        
        return None
    
    @staticmethod
    def parse_log_line(raw_log: str) -> Optional[Dict[str, Any]]:
        """
        Parse a single SSH log line
        Returns dict with: username, ip_address, login_time, status, auth_method, ssh_key, raw_log
        """
        
        # Pattern 1: Accepted/Failed password/publickey for existing user
        # Mar  6 15:30:50 ubuntu sshd[1235]: Accepted publickey for ubuntu from 10.0.0.5 port 22
        match1 = re.search(
            r"(\w+\s+\d+\s+\d+:\d+:\d+).*sshd\[\d+\]:\s+(Accepted|Failed)\s+(\w+)\s+for\s+(?:invalid user\s+)?(\S+)\s+from\s+(\S+)",
            raw_log
        )
        
        if match1:
            timestamp_str, status, auth_method, username, ip_address = match1.groups()
            ssh_key = SSHLogParser.extract_ssh_key(raw_log)
            
            return {
                "username": username,
                "ip_address": ip_address,
                "login_time": SSHLogParser.parse_timestamp(timestamp_str),
                "status": "success" if status == "Accepted" else "failed",
                "auth_method": auth_method.lower(),
                "ssh_key": ssh_key,
                "raw_log": raw_log.strip(),
            }
        
        # Pattern 2: Invalid user
        # Mar  6 15:30:45 ubuntu sshd[1234]: Invalid user admin from 192.168.1.100 port 54321
        match2 = re.search(
            r"(\w+\s+\d+\s+\d+:\d+:\d+).*sshd\[\d+\]:\s+Invalid user\s+(\S+)\s+from\s+(\S+)",
            raw_log
        )
        
        if match2:
            timestamp_str, username, ip_address = match2.groups()
            ssh_key = SSHLogParser.extract_ssh_key(raw_log)
            
            return {
                "username": username,
                "ip_address": ip_address,
                "login_time": SSHLogParser.parse_timestamp(timestamp_str),
                "status": "failed",
                "auth_method": "unknown",
                "ssh_key": ssh_key,
                "raw_log": raw_log.strip(),
            }
        
        # Pattern 3: Failed password (verbose format)
        # Mar  6 15:31:00 ubuntu sshd[1236]: Failed password for user1 from 10.0.0.10 port 22 ssh2
        match3 = re.search(
            r"(\w+\s+\d+\s+\d+:\d+:\d+).*sshd\[\d+\]:\s+Failed password for\s+(?:invalid user\s+)?(\S+)\s+from\s+(\S+)",
            raw_log
        )
        
        if match3:
            timestamp_str, username, ip_address = match3.groups()
            ssh_key = SSHLogParser.extract_ssh_key(raw_log)
            
            return {
                "username": username,
                "ip_address": ip_address,
                "login_time": SSHLogParser.parse_timestamp(timestamp_str),
                "status": "failed",
                "auth_method": "password",
                "ssh_key": ssh_key,
                "raw_log": raw_log.strip(),
            }
        
        return None
