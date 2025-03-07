# # """
# # Initialize the BackgroundScheduler and define the scheduled cleanup job.
# # """
# # from src.services.medicine_service import cleanup_expired_medicines
# # from apscheduler.schedulers.background import BackgroundScheduler
# # import logging 
# # import asyncio


# # scheduler = BackgroundScheduler()


# # def start_scheduler():
# #     try:
# #         logging.getLogger("apscheduler").setLevel(logging.INFO)
# #         scheduler.add_job(cleanup_expired_medicines, "cron", hour=0, minute=0)
# #         scheduler.start()
# #         logging.info("[SCHEDULER] Scheduler started successfully")
# #     except Exception as e:
# #         logging.error(f"[SCHEDULER ERROR] Failed to start scheduler: {e}")


# # def stop_scheduler_on_shutdown():
# #     try:
# #         logging.info("[SCHEDULER] Shutdown Signal Received... Stopping Scheduler Gracefully")
# #         if scheduler.running:
# #             scheduler.shutdown(wait=True)  # Graceful shutdown ✅
# #             logging.info("[SCHEDULER] Scheduler Stopped")
# #     except Exception as e:
# #         logging.error(f"[SCHEDULER ERROR] Failed to shutdown: {e}")


# from apscheduler.schedulers.background import BackgroundScheduler
# from src.services.medicine_service import send_inventory_warning  # Replace with actual email sending function
# import logging

# scheduler = BackgroundScheduler()

# def start_scheduler():
#     try:
#         logging.getLogger("apscheduler").setLevel(logging.INFO)

#         # Add job to run every 5 minutes (for testing)
#         scheduler.add_job(
#             send_inventory_warning,  # Replace with your actual email-sending function
#             "interval",  # Interval trigger
#             minutes=5  # Run every 5 minutes
#         )

#         # Start the scheduler
#         scheduler.start()

#         logging.info("[SCHEDULER] Scheduler started successfully")
#     except Exception as e:
#         logging.error(f"[SCHEDULER ERROR] Failed to start scheduler: {e}")

# def stop_scheduler_on_shutdown():
#     try:
#         logging.info("[SCHEDULER] Shutdown Signal Received... Stopping Scheduler Gracefully")

#         if scheduler.running:
#             scheduler.shutdown(wait=True)  # Graceful shutdown
#             logging.info("[SCHEDULER] Scheduler Stopped")
#     except Exception as e:
#         logging.error(f"[SCHEDULER ERROR] Failed to shutdown: {e}")
