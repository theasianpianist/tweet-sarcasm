from evaluate import tweetscore
import os
import sqlite3
from timeit import default_timer as timer

def tweetToList(path):
    tweetList = []
    files = os.listdir(path)
    x = 1
    for file in files:
        print("Parsing file " + str(x) + " of " + str(len(files)))
        #with open(path + "\\" + file) as f:
        content = [line.rstrip("\n") for line in open(path + "\\" + file)]
        length = len(content)
        for tweet in content:
            temp = parseTweet(tweet, file)
            if len(temp) > 1:
                tweetList.append(temp)
        x += 1
    print("Done parsing")
    return tweetList

def evalTweets(tweetList):
    print("Scoring Tweets")
    x = 1
    tweetStartTime = -1
    length = str(len(tweetList))
    for tweetInfo in tweetList:
        if x % 1000 == 0 and tweetStartTime == -1:
            tweetStartTime = x
            start = timer()
        print("Scoring Tweet " + str(x) + " of " + length)
        try:
            try:
                tweet = tweetInfo[1]
                score = tweetscore(tweet)
                tweetList[x-1].append(score)
            except IndexError:
                pass
        except UnicodeError:
            pass
        if x % 1000 == 0 and x > tweetStartTime:
            end = timer()
            tweetStartTime = -1
            print(str(end - start) + "for 1000 tweets")
        x += 1
    return tweetList

def parseTweet(tweet, fileName):
    parsedTweet = tweet.split("[@@-@@]")
    try:
        for x in range(1, 8):
            temp = parsedTweet[1]
            parsedTweet.remove(temp)
    except IndexError:
        pass
    for x in parsedTweet:
        x = unicode(x, errors="ignore")
    parsedTweet.append(fileName.strip(".tweets"))
    return parsedTweet

def scoreTweets(path):
    toDatabase(evalTweets(tweetToList(path)))

def writeTweetsExcludingScore(path):
    toDatabase(tweetToList(path))

def toDatabase(tweetList):
    conn= sqlite3.connect("phones.db")
    conn.text_factory = str
    c = conn.cursor()
    c.execute('''CREATE TABLE tweets
            (tweetID text, tweet text, product text, sarcasm real)''')
    for tweet in tweetList:
        if len(tweet) == 4:
            c.execute("INSERT INTO tweets VALUES (?, ?, ?, ?)", (tweet[0], tweet[1], tweet[2], tweet[3]))
    conn.commit()
    conn.close()
    print("Database populated")

def encoding():
    for tweetInfo in tweetList:
        try:
            tweetInfo[2].decode('utf-8')
            print ("string is UTF-8")
        except UnicodeError:
            print ("string is not UTF-8")

if __name__ == "__main__":
    scoreTweets("D:\Documents\Code\Tweet_Sarcasm PY2\Sarcasm_detector-master\Sarcasm_detector-master\data\\phones")
    #print(parseTweet("20110711204304595[@@-@@]145765552[@@-@@]Tue Jul 12 00:43:03 +0000 2011[@@-@@]0[@@-@@]65[@@-@@]4023[@@-@@]86[@@-@@]68[@@-@@]crackberry: BlackBerry Bold 9900 passes through the FCC - http://t.co/uTSrgHZ?"))