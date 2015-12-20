import textwrap
import midi
import sys

if len(sys.argv) != 2:
    print "Specify file for conversion!"
    exit()

pattern = midi.read_midifile(sys.argv[1])

TIME_DISCRETIZATION = 50.0 # ms

WRAPPER = textwrap.TextWrapper(width=140, break_long_words=False, break_on_hyphens=False)

I = 0
for track in pattern:
    if track[0] != midi.EndOfTrackEvent():
        notes = []
        delays = []
        for event in track:
            if type(event) is midi.NoteOnEvent:
                notes.append(event.data[0])
                delays.append(int(round(event.tick/TIME_DISCRETIZATION)))
            elif type(event) is midi.NoteOffEvent:
                notes.append(0)
                delays.append(int(round(event.tick/TIME_DISCRETIZATION)))
        if len(notes) != 0:
            print "\n".join(WRAPPER.wrap("byte[] notes " + str(I) + " = {" + ", ".join([str(x).rjust(2) for x in notes]) + "};"))
            print "\n".join(WRAPPER.wrap("byte[] delays" + str(I) + " = {" + ", ".join([str(x).rjust(2) for x in delays]) + "};"))
            I += 1
