import threading
import random
import time
import csv
from time import localtime
from steem.steem import Steem
from steem.steem import BroadcastingError

vote_delay = 1740

def feed():
    authors= list_load('authors.txt')
    upvote_history= list_load('upvotehistory.txt')
    steem = Steem(wif=posting_key)
    for comment in steem.stream_comments():
        if comment.author in authors:
            if len(comment.title) > 0:
                if comment.identifier in upvote_history:
                    continue
                upvote_history.append(comment.identifier)
                list_save('upvotehistory.txt', upvote_history)
                print(timestamp_builder(), comment.identifier, \
                    ": thread started, vote in ", vote_delay, " seconds ...")
                workerThread = threading.Thread(name=comment.identifier, \
                    target=worker, args=(comment,))
                workerThread.start()

def worker(worker_comment):
    time.sleep(vote_delay)
    try:
      for (k,v) in enumerate(account):
        print(timestamp_builder(), worker_comment.identifier, " <--- voted ",v)
        worker_steem = Steem(wif=posting_key[k])
        upvote_comment = worker_steem.get_content(worker_comment.identifier)
        upvote_comment.vote(100, v)
    except BroadcastingError as e:
      print(str(E))

def list_save(listfile,  listvar):
    with open(listfile, 'w') as writestuff:
        writestuff.write('\n'.join(listvar))
        writestuff.write('\n')

def list_load(listfile):
    with open(listfile, 'r') as readstuff:
        listvar= []
        reader= csv.reader(readstuff)
        for rows in reader:
            v= rows[0]
            listvar.append(v)
    return listvar

def timestamp_builder():
    lt = localtime()
    timestamp = time.strftime("%d/%m/%Y-%H:%M:%S ", lt)
    return timestamp

account= list_load('accounts.txt')
posting_key= list_load('wif.txt')

if __name__ == "__main__":
    while True:
        try:
            feed()
        except (KeyboardInterrupt, SystemExit):
            print("Quit")
            break
        except Exception as e:
            print("Exception ... Restart")
            traceback.print_exc()