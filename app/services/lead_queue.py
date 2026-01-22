import threading
import queue
from typing import List
from app.services.scrape import run_scrape_job

# Thread-safe FIFO queue
LEAD_QUEUE = queue.Queue()

# Worker function that runs in a separate thread
def queue_worker():
    print("🟢 Lead Queue Worker started")
    while True:
        # Get next job (blocking)
        hashtags, max_profiles = LEAD_QUEUE.get()
        try:
            print(f"📥 Processing queued job: {hashtags}")
            run_scrape_job(hashtags, max_profiles)
            print(f"✅ Finished job: {hashtags}")
        except Exception as e:
            print(f"❌ Error in queued job: {e}")
        finally:
            LEAD_QUEUE.task_done()


# Start the worker thread (daemon=True so it exits when FastAPI shuts down)
worker_thread = threading.Thread(target=queue_worker, daemon=True)
worker_thread.start()


# Function to enqueue a new job
def enqueue_scrape_job(hashtags: List[str], max_profiles: int):
    LEAD_QUEUE.put((hashtags, max_profiles))
    print(f"🟢 Job queued: {hashtags}")
