# a3.py
# ssd74, jv442
# Sources/people consulted: NONE
# March 15th, 2022
# Skeleton by Prof. Lee, LJL2, Mar 9, 2022

"""See CS1110 Spring '22 A3 writeup."""

import sample_lists as sl
from freq import Freq


def percent_short(tokenlist, k):
    """Returns: percentage (as float between 0 and 100) of tokens in tokenlist
    that are of length <=k.

    Precondition: k [float] is >= 0. tokenlist is a non-empty list of strings.
    """
    count = 0
    for token in tokenlist:
        if len(token) <= k:
             count = count+1
    return (count/len(tokenlist))*100

def print_trend(results, labels):
    """
    Precondition:  `labels` is a list of strings where each string is a label for
    the corresponding entry in list `results` (which is a same-length list of
    numbers (floats or ints)).
    WARNING: it is possible for there to be repeated values in either `results`
    or `labels`.


    Prints info about `results` and `labels` in the following format (does
    not return anything)

    <label[0]>: <round(results[0], 2)>
    <label[1]>: <round(results[1], 2)>
    ... [etc.]

    The call round(x, 2) rounds to two decimal places.
    """
    for i in range(len(results)):
        rounded = round(results[i], 2)
        print(str(labels[i]) + ": " + str(rounded))


def type_token_ratio(tokenlist):
    """Returns, as a float,

         100*(1 - (# of types in tokenlist/# of tokens in tokenlist))

    Precondition: tokenlist is a non-empty list of strings."""
    num_types = 0
    num_tokens = len(tokenlist)
    for i in range(len(tokenlist)):
        temp = tokenlist[i]
        if tokenlist.index(temp) == i:
            num_types = num_types + 1
    return 100*(1-(num_types/num_tokens))


def percent_avg_or_shorter(tokenlist, tokenlistlist):
    """Returns: percentage (as float between 0 and 100) of tokens in tokenlist
    that are of length <=k, where k is the average token length across
    all the tokens in tokenlistlist.

    Example:
     if tokenlist were ["a", "b", "ccccc", "dd"]
     and tokenlistlist were
        [ ["abcd", "abcd", "abcd"],
          ["a", "b", "ccccc", "dd"],
          ["ef"]
        ]
     then k should be (3*4+2*1 +1*5 + 2*2)/8 = 2.875
     and this function should return 3/4 = .75

    Precondition: tokenlist is a non-empty list of strings.
    tokenlistlist is a non-empty list of non-empty lists of non-empty strings.
    tokenlist is in tokenlistlist
    """

    avg_length = 0
    for i in range(len(tokenlistlist)):
        for j in range(len(tokenlistlist[i])):
            avg_length += len(tokenlistlist[i][j])

    total = 0
    for row in tokenlistlist:
        total += len(row)
    k = avg_length/total
    return percent_short(tokenlist, k)


def zipf(tokenlist, n):
    """Returns: percentage (as float between 0 and 100) of tokens in tokenlist
    that are of the top n most common types in tokenlist.

    Examples:
        zipf(["a", "a", "a", "a", "b",  "b",  "b", "c", "c", "d"], 1) --> 40
          because 4 of the 10 tokens are "a", the single most common type

        zipf(["a", "a", "a", "a", "b",  "b",  "b", "c", "c", "d"], 2) --> 70
         because the 2 most common types are "a" and "b", of which there are 7
         out of the 10 tokens in the input list

        zipf(["a", "a", "b", "b"], 1) --> 50
         It doesn't matter which of 'a' and 'b' are considered "the most common"
         here; 2 out of 4 list items = 50%.

    Precondition: n [int] is > 0, <= the number of distinct wordtypes in tokenlist
        tokenlist is a non-empty list of strings
    """
    dic = {}
    for i in range(len(tokenlist)):
        temp = tokenlist[i]
        if tokenlist.index(temp) == i:
            dic[temp] = tokenlist.count(temp)

    Freqlist = []
    for key in dic:
        new_Freq = Freq(key, dic[key])
        Freqlist.append(new_Freq)
    Freqlist.sort(reverse=True)

    num_freq = 0
    for j in range(n):
        num_freq += Freqlist[j].freq

    return (num_freq/len(tokenlist))*100
