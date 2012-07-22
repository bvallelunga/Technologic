import shutil
import os
import datetime

def synthesizer(genre, data):

    sounds = r'sounds'
    entry_time = str(datetime.datetime.now().strftime(r"%H-%M-%S_%m-%d-%Y"))
    destination = open(r'products/%s_%s.mp3' % (genre, entry_time), 'wb')

    for loop in data:

        loop['beat'] = 100 if loop['beat'] > 100 else loop['beat']

        filename = os.path.join(sounds, '%i.mp3' % loop['beat'])

        shutil.copyfileobj(open(filename, 'rb'), destination)

    destination.close()

    return "%s Techno Song Created\n\nPath to file: products/%s_%s.mp3" % (genre.title(), genre, entry_time )