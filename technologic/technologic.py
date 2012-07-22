'''
This system will create music based off of y=mx+b equations.
There are two sets of equations:
    1) x is time and y is audio sound (higher y = high pitch) (low y = big bass)
    2) x is time and y is the duration of the sound in set 1 (may have 1+ equations > piecewise function)
    BOTH sets will stop at the duration. Duration in seconds
'''

from genres import genres
from combine import synthesizer

def logic(genre = "fast", duration = 90):

    print "Creating song characteristics\n"

    data = genres(genre, float(duration))

    print "Combining beats\n"

    synthesize = synthesizer(genre, data)

    print synthesize


logic("slow")