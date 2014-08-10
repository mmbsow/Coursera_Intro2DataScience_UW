import sys
import json
import re

STATES = {
    'AK': 'Alaska',
    'AL': 'Alabama',
    'AR': 'Arkansas',
    'AS': 'American Samoa',
    'AZ': 'Arizona',
    'CA': 'California',
    'CO': 'Colorado',
    'CT': 'Connecticut',
    'DC': 'District of Columbia',
    'DE': 'Delaware',
    'FL': 'Florida',
    'GA': 'Georgia',
    'GU': 'Guam',
    'HI': 'Hawaii',
    'IA': 'Iowa',
    'ID': 'Idaho',
    'IL': 'Illinois',
    'IN': 'Indiana',
    'KS': 'Kansas',
    'KY': 'Kentucky',
    'LA': 'Louisiana',
    'MA': 'Massachusetts',
    'MD': 'Maryland',
    'ME': 'Maine',
    'MI': 'Michigan',
    'MN': 'Minnesota',
    'MO': 'Missouri',
    'MP': 'Northern Mariana Islands',
    'MS': 'Mississippi',
    'MT': 'Montana',
    'NA': 'National',
    'NC': 'North Carolina',
    'ND': 'North Dakota',
    'NE': 'Nebraska',
    'NH': 'New Hampshire',
    'NJ': 'New Jersey',
    'NM': 'New Mexico',
    'NV': 'Nevada',
    'NY': 'New York',
    'OH': 'Ohio',
    'OK': 'Oklahoma',
    'OR': 'Oregon',
    'PA': 'Pennsylvania',
    'PR': 'Puerto Rico',
    'RI': 'Rhode Island',
    'SC': 'South Carolina',
    'SD': 'South Dakota',
    'TN': 'Tennessee',
    'TX': 'Texas',
    'UT': 'Utah',
    'VA': 'Virginia',
    'VI': 'Virgin Islands',
    'VT': 'Vermont',
    'WA': 'Washington',
    'WI': 'Wisconsin',
    'WV': 'West Virginia',
    'WY': 'Wyoming'
}

def getAfinnDicts(afinnFile):
    # build 2 dictionaries of scores from AFINN file:
    # one with single words, one for 2 words
    single_words = {}
    double_words = {}
    for line in afinnFile:
        term, score = line.split('\t')
        if re.findall(r'\w+ \w+', term):
            double_words[term] = int(score)
        else:
            single_words[term] = int(score)

    return (single_words, double_words)

def getTweetScore(tweet, single_words, double_words):
    tweet_score = []
    
    # get scores for single-word term (ex: "fun")
    tweet_score = [ single_words.get(s, 0) for s in re.split(r'\W+', tweet) if s ]

    # append scores for multi-word term (ex: "no fun")
    for term, score in double_words.items():
        tweet_score = tweet_score + [ score for d in re.findall(r'\b%s\b' % term, tweet) ]

    return sum(tweet_score)

def getUSstate(place, location):
    if not place and not location:
        return None

    p = str(place).strip().lower()
    l = str(location).strip().lower()

    for shortName, fullName in STATES.items():
        if p in [shortName.lower(), fullName.lower()] or \
           l in [shortName.lower(), fullName.lower()]:
            return shortName

    return None
            
def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    
    # get dictionaries of sentiment scores
    single_words, double_words = getAfinnDicts(sent_file)

    # create dictionary keeping the list of new terms and a tuple (score, count of occurrences)
    stateScores = {}
    
    # parse twitter output
    for line in tweet_file.readlines():
        text = None
        sent_score = 0
        state = None

        # decode json and get the text part of the tweet
        try:
            tweet = json.loads(line)
            text = tweet.get('text', None)

            # determine the US state for the tweet
            place = tweet.get('place', None)
            user = tweet.get('user', None)
            location = None if not user else user.get('location', None)
            state = getUSstate(place, location)
        except:
            text = None

        # if tweet is valid and has a valid US state, compute score
        if text and state:
            text = text.encode('utf-8').lower()
            tweet_score = getTweetScore(text, single_words, double_words)

            numbers = stateScores.get(state, (0.0, 0.0))
            stateScores[state] = (numbers[0] + sent_score, numbers[1] + 1.0)

    
    statesList = [ (s, v[0]/v[1]) for s,v in stateScores.items() ]
    sorted_states = sorted(statesList, key = lambda s: s[1], reverse=True)
##    for s in sorted_states:
##        print '%s %f' % (s[0], s[1])
    if sorted_states:
        topState = sorted_states[0]
        print '%s' % topState[0]
    else:
        print 'no state found'


if __name__ == '__main__':
    main()
