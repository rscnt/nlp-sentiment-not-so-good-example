from __future__ import division
from collections import Counter # Counter() is a dict for counting
from collections import defaultdict
from numpy import mean

# List of positive words:
pos_words = ["love"]
# List of negative words:
neg_words = ["hate"]
# List of target words:
targets = ["bieber"]
sentiment_words = pos_words+neg_words

def PMI(c_xy, c_x, c_y, N):
    # Computes PMI(x, y) where
    # c_xy is the number of times x co-occurs with y
    # c_x is the number of times x occurs.
    # c_y is the number of times y occurs.
    # N is the number of observations.
    return 0; # replace this
    
#Do a simple error check using value computed by hand
if(PMI(2,4,3,12) != 1): # these numbers are from our y,z example
    print("Warning: PMI is incorrectly defined")
else:
    print("PMI check passed")

#remove any keys from counts dictionary unless their count is above min_threshold
#if max_threshold is set, also remove anything whose count is equal to or above that threshold 
def filter_o_counts(counts, min_threshold, max_threshold=0):
    if (max_threshold > 0):
        return Counter({w : counts[w] for w in counts.keys() if counts[w] > min_threshold and counts[w] < max_threshold})
    else:
        return Counter({w : counts[w] for w in counts.keys() if counts[w] > min_threshold})

#remove any co-occ. counts if they are not above threshold 
def filter_co_counts(co_counts, threshold)                       :
     return {w: filter_o_counts(co_counts[w], threshold) for w in co_counts.keys()}

# Define the data structures used to store the counts:
o_counts = Counter(); # Occurrence counts
co_counts = defaultdict(Counter); # Co-occurrence counts:
  #This will be indexed by target words. co_counts[target] will contain
  #a dictionary of co-occurrence counts of target with each sentiment word.

N = 0 #This will store the total number of observations (tweets)
      # You should add code to the block below so that N has the
      # correct value when the block finishes.
# Load the data:
with open("tweets_en.txt") as f: #The tweets file contains one tweet per line.
    for line in f:
        words = set(line.strip().split()) #remove duplicate words
        for word in words:
            o_counts[word] += 1 # Store occurence counts for all words
            # but only get co-occurrence counts for target/sentiment word pairs
            if word in targets:
                for word2 in words:
                    if word2 in sentiment_words:
                        co_counts[word][word2] += 1 # Store co-occurence counts
print("Total number of tweets: {}".format(N))

#For a Counter c, c.most_common(n) returns a sorted list of the n most common 
#items in c. If no n is given, it returns all items, sorted by decreasing frequency
print("Counts of positive words:")
print(Counter({w : o_counts[w] for w in pos_words}).most_common())
print("Counts of negative words:")
print(Counter({w : o_counts[w] for w in neg_words}).most_common())
print("Counts of target words:")
print(Counter({w : o_counts[w] for w in targets}).most_common())
for target in targets:
    print("{} co counts: {}".format(target, co_counts[target].most_common()))


#filter out co-occurrences with too few counts if you want
#co_counts = filter_co_counts(co_counts, 2)

for target in targets:
    target_count = o_counts[target]
    posPMIs = []
    negPMIs = []
    # compute PMI between target and each positive word, and
    # add it to the list of positive sentiment PMI values
    for pos in pos_words:
        if(pos in co_counts[target]): # Check if the words actually co-occur
            # If so, compute PMI and append to the list
            posPMIs.append(PMI(co_counts[target][pos],target_count,o_counts[pos],N)); 
    # same for negative sentiment words
    for neg in neg_words:
       if(neg in co_counts[target]): 
           negPMIs.append(PMI(co_counts[target][neg],target_count,o_counts[neg],N));
#uncomment the following line when posPMIs and negPMIs are no longer empty.
    print("{} {:.2f} (pos), {:.2f} (neg)".format((target+":").ljust(12), mean(posPMIs), mean(negPMIs)))

