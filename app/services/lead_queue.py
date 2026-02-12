import threading
import queue
from app.constants.batch_status import BatchStatus
from app.crud.scraping_batch import update_batch_status
from app.db.database import SessionLocal
from app.services.scrape import run_scrape_job

# Thread-safe FIFO queue
LEAD_QUEUE = queue.Queue()

def queue_worker():
    print("🟢 Lead Queue Worker started")
    while True:
        hashtag, max_profiles, batch_id , user_id = LEAD_QUEUE.get()
        try:
            with SessionLocal() as db:
                update_batch_status(db,batch_id, status=BatchStatus.RUNNING.value)
            isSuccess = run_scrape_job(hashtag, max_profiles, batch_id , user_id)
            if isSuccess:
                print(f"✅ Finished job: {hashtag} (batch_id={batch_id})")
        except Exception as e:
            print(f"❌ Error in queued job: {e}")
        finally:
            LEAD_QUEUE.task_done()

# Start worker thread
worker_thread = threading.Thread(target=queue_worker, daemon=True)
worker_thread.start()

# Function to enqueue a new job
def enqueue_scrape_job(hashtag: str, max_profiles: int, batch_id: int,user_id:int):
    LEAD_QUEUE.put((hashtag, max_profiles, batch_id,user_id))
    print(f"🟢 Job queued: {hashtag} (batch_id={batch_id})")
