'''
This system will create music based off of y=mx+b equations.
There are two sets of equations:
    1) x is time and y is audio sound (higher y = high pitch) (low y = big bass)
    2) x is time and y is the duration of the sound in set 1 (may have 1+ equations > piecewise function)
    BOTH sets will stop at the duration. Duration in seconds
'''

from genres import genres
from synthesize import synthesizer


def logic(genre = "fast", duration = 90):

    spacer = "------------------------------------------------------------------------------------------------"

    print "\n%s" % spacer

    print "\nGenerating Song Characteristics\n"

    print spacer

    data = genres(genre, float(duration))

    synthesize = synthesizer(genre, data, spacer)

    return synthesize


logic("slow", 30)