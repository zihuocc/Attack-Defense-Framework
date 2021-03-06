#!/usr/bin/env python
# encoding:utf-8

import sys
import thread
import threading
import time
import datetime
from Queue import Queue

# Job control
jobs = Queue()
WORKER_NUMBER = 30
EXPLOIT_TIMEOUT = 10
ROUND_TIME = 60 * 9
CTF_START_TIME = datetime.datetime(2018, 9, 16, 9, 0, 0, 0)

def d(message):
    sys.stdout.write("[DEBUG]: %s\n" % (message))

def worker(wid):
    while True:
        job = jobs.get()
        d("[WORKER[%d]] %s" % (wid, job))
        result = Exploit(job['host'], job['port'], 5).run()
        if result[0]:
            d("[WORKER(%d)] Got flag: %s" % (wid, flag))
            mysubmit_flag(
                job['challenge'], 
                "%s:%d" % (job['host'],job['port']),
                "UNKNOWN",
                flag,
            )
        else:
            d("[WORKER(%d)] Got flag: %s" % (wid, flag))


def start_workers():
    for i in range(WORKER_NUMBER):
        t = threading.Thread(target=worker, args=(i,))
        t.daemon = True
        t.start()

# Start works
start_workers()

# Job dispatcher
while True:
    round_start_time = datetime.datetime.now()
    print round_start_time
    round_number = (round_start_time - CTF_START_TIME).seconds * 1.0 / ROUND_TIME
    d("The %d round started" % (round_number))
    # Generate jobs
    d("Loading victims...")
    with open("targets") as f:
        for line in f:
            '''
            challenge,host,port,hostname
            '''
            items = line.split(",")
            job = dict()
            job['challenge'] = items[0]
            job['host'] = items[1]
            job['port'] = int(items[2])
            job['hostname'] = items[3]
            jobs.put(job)
            print job
    round_end_time = datetime.datetime.now()
    # Ensure sync with offical round

    d("Sleeping %d second for the next round" % (ROUND_TIME - (round_end_time - round_start_time).seconds))
    sleep_time = ROUND_TIME - (round_end_time - round_start_time).seconds
    sleeped_time = 0
    for i in range(sleep_time):
        time.sleep(1)
        d("%d/%d => %s" % (sleeped_time, sleep_time, datetime.datetime.now()))
        sleeped_time += 1
