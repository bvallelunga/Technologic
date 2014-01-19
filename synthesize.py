"""
# made in laborate (http://laborate.io) (http://laborate.io)
# 'song' is a Python list (or tuple) in which the song is defined,
#   the format is [['note', value]]

# Notes are 'a' through 'g' of course,
# optionally with '#' or 'b' appended for sharps or flats.
# Finally the octave number (defaults to octave 4 if not given).
# An asterisk at the end makes the note a little louder (useful for the beat).
# 'r' is a rest.

# Note value is a number:
# 1 = Whole Note; 2 = Half Note; 4 = Quarter Note, etc.
# Dotted notes can be written in two ways:
# 1.33 = -2 = dotted half
# 2.66 = -4 = dotted quarter
# 5.33 = -8 = dotted eighth
"""
import datetime
from random import randint
import os
from hurry.filesize import size

def synthesizer(genre, data, spacer):

    entry_time = str(datetime.datetime.now().strftime(r"%H-%M-%S_%m-%d-%Y"))
    techno_song = []
    counter = 0

    ##########################################################################
    # Compute and print piano key frequency table
    ##########################################################################
    pitchhz = {}
    keys_s = ('a', 'a#', 'b', 'c', 'c#', 'd', 'd#', 'e', 'f', 'f#', 'g', 'g#')
    keys_f = ('a', 'bb', 'b', 'c', 'db', 'd', 'eb', 'e', 'f', 'gb', 'g', 'ab')

    print "  Duration (Minutes)        Key Number                Scientific Name       Frequency (Hz)"
    print spacer

    for beat in data:
        k = 88 if beat['beat'] > 88 else beat['beat']
        note_length = pow(beat['duration'], -1)
        freq = 27.5 * 2.**(k/12.)
        oct = (k+9) // 12
        sharp = randint(1, 10)
        sharp = "*" if sharp == 1 else ""
        note = '%s%s%u' % (keys_s[k%12], sharp, oct)
        print "\t%.2f\t\t%10u\t\t%15s\t\t%14.2f" % (beat['duration'], k+1, note.upper(), freq)
        pitchhz[note] = freq
        note = '%s%u' % (keys_f[k%12], oct)
        pitchhz[note] = freq
        techno_song.append((note, note_length))
        counter = counter + 1

    ##########################################################################
    #### Main program starts below
    ##########################################################################
    # Some parameters:

    # Beats (quarters) per minute
    # e.g. bpm = 95

    # Octave shift (neg. integer -> lower; pos. integer -> higher)
    # e.g. transpose = 0

    # Pause between notes as a fraction (0. = legato and e.g., 0.5 = staccato)
    # e.g. pause = 0.05

    # Volume boost for asterisk notes (1. = no boost)
    # e.g. boost = 1.2

    # Output file name
    #fn = 'pysynth_output.wav'

    # Other parameters:

    # Influences the decay of harmonics over frequency. Lowering the
    # value eliminates even more harmonics at high frequencies.
    # Suggested range: between 3. and 5., depending on the frequency response
    #  of speakers/headphones used
    harm_max = 4.
    ##########################################################################

    import wave, math, struct

    def make_wav(song,bpm=120,transpose=0,pause=0.00,boost=5.1,fn='products/%s_%s.wav' % (genre, entry_time)):
        f=wave.open(fn,'w')

        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(44100)
        f.setcomptype('NONE','Not Compressed')

        bpmfac = 120./bpm

        def length(l):
            try:
                return 88200./l*bpmfac
            except ZeroDivisionError:
                return 88200./l*bpmfac + 1

        def waves2(hz,l):
            a=44100./hz
            b=float(l)/44100.*hz
            return [a,round(b)]

        def sixteenbit(x):
            return struct.pack('h', round(32000*x))

        def asin(x):
            return math.sin(2.*math.pi*x)

        def render2(a,b,vol):
            b2 = (1.-pause)*b
            l=waves2(a,b2)
            ow=""
            q=int(l[0]*l[1])

            # harmonics are frequency-dependent:
            lf = math.log(a)
            lf_fac = (lf-3.) / harm_max
            if lf_fac > 1: harm = 0
            else: harm = 2. * (1-lf_fac)
            decay = 2. / lf
            t = (lf-3.) / (8.5-3.)
            volfac = 1. + .8 * t * math.cos(math.pi/5.3*(lf-3.))

            for x in range(q):
                fac=1.
                if x<100: fac=x/80.
                if 100<=x<300: fac=1.25-(x-100)/800.
                if x>q-400: fac=1.-((x-q+400)/400.)
                s = float(x)/float(q)
                dfac =  1. - s + s * decay
                ow=ow+sixteenbit((asin(float(x)/l[0])
                                  +harm*asin(float(x)/(l[0]/2.))
                                  +.5*harm*asin(float(x)/(l[0]/4.)))/4.*fac*vol*dfac*volfac)
            fill = max(int(ex_pos - curpos - q), 0)
            f.writeframesraw((ow)+(sixteenbit(0)*fill))
            return q + fill

        ##########################################################################
        # Write to output file (in WAV format)
        ##########################################################################

        curpos = 0
        ex_pos = 0.

        for nn, x in enumerate(song):
            if not nn % 10:
                print "Writing Beat: %u out of %u" % (nn+1,len(song))
            if x[0]!='r':
                if x[0][-1] == '*':
                    vol = boost
                    note = x[0][:-1]
                else:
                    vol = 1.
                    note = x[0]

                try:
                    a=pitchhz[note]
                except:
                    a=pitchhz[note + '4']	# default to fourth octave
                a = a * 2**transpose
                if x[1] < 0:
                    b=length(-2.*x[1]/3.)
                else:
                    b=length(x[1])
                ex_pos = ex_pos + b
                curpos = curpos + render2(a,b,vol)

            if x[0]=='r':
                b=length(x[1])
                ex_pos = ex_pos + b
                f.writeframesraw(sixteenbit(0)*int(b))
                curpos = curpos + int(b)

        duration = f.getnframes()/f.getframerate()
        f.writeframes('')
        f.close()

        print "\n%s\n" % spacer
        print "File Name:   %s_%s" % (genre, entry_time)
        print "Extension:   .wav"
        print "Duration:    %i seconds" % duration
        print "File Size:   %s" % size(os.path.getsize(fn))
        print "In Folder:   products"
        print "Location:    %s" % fn
        print "\n%s\n" % spacer

    print "\n%s" % spacer

    ##########################################################################
    # Synthesize demo songs
    ##########################################################################

    print "\nCompiling Techno Song... (this might take a minute)\n"
    print "%s\n" % spacer

    make_wav(techno_song)
