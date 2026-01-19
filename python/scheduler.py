"""
Scheduler for automatic daily updates at 8:00 AM
"""

import schedule
import time
import logging
from datetime import datetime
import sys

from update_dashboard import update_dashboard

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('../data/scheduler.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


def scheduled_update():
    """Wrapper function for scheduled updates"""
    logger.info("=" * 60)
    logger.info("SCHEDULED UPDATE TRIGGERED")
    logger.info(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 60)

    try:
        update_dashboard()
        logger.info("Scheduled update completed successfully")

    except Exception as e:
        logger.error(f"Scheduled update failed: {str(e)}")


def run_scheduler():
    """Main scheduler loop"""
    logger.info("=" * 60)
    logger.info("DASHBOARD SCHEDULER STARTED")
    logger.info(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("Schedule: Daily at 08:00 AM")
    logger.info("=" * 60)

    # Schedule daily update at 8:00 AM
    schedule.every().day.at("08:00").do(scheduled_update)

    # Also run immediately on startup
    logger.info("Running initial update...")
    scheduled_update()

    # Keep the scheduler running
    logger.info("Scheduler is now running. Press Ctrl+C to stop.")

    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute

    except KeyboardInterrupt:
        logger.info("=" * 60)
        logger.info("SCHEDULER STOPPED BY USER")
        logger.info(f"Stop time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("=" * 60)


def main():
    """Entry point for scheduler"""
    try:
        run_scheduler()

    except Exception as e:
        logger.error(f"Scheduler error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
