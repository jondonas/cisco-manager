import random
import datetime
import time
list1 = [1, 2, 3, 4, 5, 6, 7, 8]


def unordered(alist):
    while alist != [1, 2, 3, 4, 5, 6, 7, 8]:
        return True
    return False


def bogosort(somelist):
    start = datetime.datetime.now()
    print "running"
    a = 0
    while unordered(somelist):
	time.sleep(0.01)
        random.shuffle(somelist)
        print a
        a += 1
    print datetime.datetime.now() - start
    print "BOGONIGHT MOTHERFUCKER"

random.shuffle(list1)
bogosort(list1)
