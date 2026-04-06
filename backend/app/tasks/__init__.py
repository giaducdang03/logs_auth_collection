from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services.log_reader import LogReaderService
from app.services.log_service import LogService
from app.config import get_settings
import logging

logger = logging.getLogger(__name__)
settings = get_settings()


def collect_logs():
    """Background task to collect and parse SSH logs"""
    db: Session = SessionLocal()
    try:
        log_reader = LogReaderService(settings.log_file_path)
        
        # Read new logs since last offset
        new_log_lines = log_reader.read_new_logs(
            initial_days=settings.log_reader_initial_days,
            large_file_mb=settings.log_reader_large_file_mb,
        )
        
        if not new_log_lines:
            logger.debug("No new logs to process")
            return
        
        # Parse logs
        parsed_logs = log_reader.parse_logs(new_log_lines)
        
        # Store logs in database
        created_count = 0
        skipped_count = 0
        
        for log_data in parsed_logs:
            try:
                result = LogService.create_log(db, log_data)
                if result:
                    created_count += 1
                else:
                    skipped_count += 1
            except Exception as e:
                logger.error(f"Failed to store log: {str(e)}")
                skipped_count += 1
        
        logger.info(f"Log collection completed: {created_count} created, {skipped_count} skipped")
    
    except Exception as e:
        logger.error(f"Log collection failed: {str(e)}")
    
    finally:
        db.close()


def start_scheduler(run_on_startup: bool = True):
    """Start the background task scheduler and optionally run once immediately"""
    if run_on_startup:
        logger.info("Running initial log collection on app startup")
        collect_logs()

    scheduler = BackgroundScheduler()
    
    # Schedule log collection every N minutes
    interval_minutes = settings.log_reader_interval_minutes
    scheduler.add_job(
        collect_logs,
        'interval',
        minutes=interval_minutes,
        id='log_collector',
        name='SSH Log Collector',
        replace_existing=True
    )
    
    scheduler.start()
    logger.info(f"Log collector scheduler started (interval: {interval_minutes} minutes)")
    
    return scheduler
