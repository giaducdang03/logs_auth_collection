"""
Script to seed fake SSH logs into the database
Run with: python -m scripts.seed_data
"""

import sys
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
import random

# Add parent directory to path
sys.path.insert(0, "/backend")

from app.database import SessionLocal, Base, engine
from app.models import User, SSHLog
from app.utils.auth_utils import hash_password


def seed_users(db: Session):
    """Create test users"""
    users = [
        ("admin", "admin123"),
        ("testuser", "testpass123"),
    ]
    
    for username, password in users:
        existing = db.query(User).filter(User.username == username).first()
        if not existing:
            user = User(
                username=username,
                password_hash=hash_password(password),
                is_active=True
            )
            db.add(user)
    
    db.commit()
    print("✓ Users seeded")


def seed_ssh_logs(db: Session):
    """Create fake SSH logs"""
    usernames = ["ubuntu", "root", "admin", "user1", "attacker", "deploy"]
    ips = [
        "192.168.1.100",
        "192.168.1.101",
        "10.0.0.5",
        "10.0.0.10",
        "172.16.0.50",
        "203.0.113.45",
        "198.51.100.23",
    ]
    statuses = ["success", "failed"]
    auth_methods = ["password", "publickey", "unknown"]
    
    base_time = datetime.utcnow()
    
    # Generate 150 fake logs over the last 7 days
    for i in range(150):
        # Random time within last 7 days
        days_ago = random.randint(0, 7)
        hours_ago = random.randint(0, 23)
        minutes_ago = random.randint(0, 59)
        
        login_time = base_time - timedelta(days=days_ago, hours=hours_ago, minutes=minutes_ago)
        
        username = random.choice(usernames)
        ip_address = random.choice(ips)
        status = random.choice(statuses)
        auth_method = random.choice(auth_methods)
        
        # Create appropriate raw_log based on status
        if status == "success":
            raw_log = f"{login_time.strftime('%b %d %H:%M:%S')} ubuntu sshd[1234]: Accepted {auth_method} for {username} from {ip_address} port 22"
        else:
            raw_log = f"{login_time.strftime('%b %d %H:%M:%S')} ubuntu sshd[1234]: Failed password for {username} from {ip_address} port 22 ssh2"
        
        log_entry = SSHLog(
            username=username,
            ip_address=ip_address,
            login_time=login_time,
            status=status,
            auth_method=auth_method,
            ssh_key=None,
            raw_log=raw_log,
        )
        
        # Check for duplicates before adding
        existing = db.query(SSHLog).filter(
            SSHLog.username == username,
            SSHLog.ip_address == ip_address,
            SSHLog.login_time == login_time,
            SSHLog.status == status
        ).first()
        
        if not existing:
            db.add(log_entry)
    
    db.commit()
    print("✓ SSH logs seeded (150 entries)")


def main():
    """Main seed function"""
    print("Starting database seeding...")
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    print("✓ Database tables created")
    
    db = SessionLocal()
    try:
        seed_users(db)
        seed_ssh_logs(db)
        print("\n✅ Database seeding completed successfully!")
        print("\nTest credentials:")
        print("  - Username: admin, Password: admin123")
        print("  - Username: testuser, Password: testpass123")
    except Exception as e:
        print(f"\n❌ Seeding failed: {str(e)}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    main()
