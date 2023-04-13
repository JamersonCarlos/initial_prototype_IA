import schedule
import time
import threading


def job_thread(job):
    schedule.every().monday.at("01:00").do(job)

    while True:
        schedule.run_pending()
        time.sleep(28800)

def start_thread(job):
    threading.Thread(target=job_thread,args=[job]).start()
