import schedule
import time

from service import get_fetched_data

def job():
    get_fetched_data()

schedule.every().hour.do(job)

while True:
    schedule.run_pending()
    time.sleep(1 )
