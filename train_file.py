from apscheduler.schedulers.background import BackgroundScheduler
import time


def foo():
    print(f"time = {time.time()}")


scheduler = BackgroundScheduler()
scheduler.add_job(foo, "interval", seconds=3)
scheduler.start()

time.sleep(30)
scheduler.shutdown()