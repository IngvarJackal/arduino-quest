import textwrap
import midi
import sys

if len(sys.argv) != 2:
    print "Specify file for conversion!"
    exit()

pattern = midi.read_midifile(sys.argv[1])

TIME_DISCRETIZATION = 50.0 # ms

NOTE_SHIFT = 58-69
TRACKS = []
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
            TRACKS += [max(0, x+NOTE_SHIFT) for x in notes]
            TRACKS += [255]
            TRACKS += delays
            TRACKS += [255]

with open(sys.argv[1].split(".")[0].upper() + ".SND", "wb") as out:
    out.write(b"".join([chr(x) for x in TRACKS]))
