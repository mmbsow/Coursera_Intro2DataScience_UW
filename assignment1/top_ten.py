import sys
import json
import re


def main():
    tweet_file = open(sys.argv[1])

    # dictionary holding the hashtags with their counts
    hashtags = {}
        
    # parse twitter output
    for line in tweet_file.readlines():

        # decode json and get the text part of the tweet
        try:
            tweet = json.loads(line)
            
            entities = tweet.get('entities', None)
            if entities:
                hashlist = entities.get('hashtags', [])
                for hasht in hashlist:
                    tag = hasht.get('text', None)
                    if tag:
                        tag = tag.encode('utf-8').lower()
                        hashtags[tag] = hashtags.get(tag, 0) + 1
        except:
            pass

    # now sort dictionary by counts
    sorted_hashtags = sorted(hashtags.items(), key=lambda h: h[1], reverse=True)

    # finally, print the sentiment score for the line
    for i in range(min(len(sorted_hashtags), 10)):
        tag = sorted_hashtags[i]
        print '%s %d' % (tag[0], tag[1])


if __name__ == '__main__':
    main()
