"""
Initialize the BackgroundScheduler and define the scheduled cleanup job.
"""
from src.services.medicine_service import cleanup_expired_medicines
from apscheduler.schedulers.background import BackgroundScheduler
import logging 
import asyncio


scheduler = BackgroundScheduler()


def start_scheduler():
    try:
        logging.getLogger("apscheduler").setLevel(logging.INFO)
        scheduler.add_job(cleanup_expired_medicines, "cron", hour=0, minute=0)
        scheduler.start()
        logging.info("[SCHEDULER] Background Scheduler started successfully... Cleanup will run every midnight")
    except Exception as e:
        logging.error(f"[SCHEDULER ERROR] Failed to start scheduler: {e}")


async def stop_scheduler_on_shutdown():
    try:
        logging.info("[SCHEDULER] Shutdown Signal Received... Stopping Scheduler Gracefully")
        scheduler.shutdown(wait=False)  # Immediately shutdown without waiting
        logging.info("[SCHEDULER] Scheduler Stopped")
    except Exception as e:
        logging.error(f"[SCHEDULER ERROR] Failed to shutdown: {e}")
