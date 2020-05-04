from mido import MidiFile
import argparse
major = [0,2,4,5,7,9,11]
markings = ['=', '=','=','.','=','.','=','.','=','.','=','.','=','=',':','=','=','.','=','.','=','=', '=']
letter_notes_sharp = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']
letter_notes_flat = ['A', 'Bb', 'B', 'C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab']

def midi_to_letter(note):
    return letter_notes_sharp[(note+3)%12]

def letter_to_midi(letter):
    octave = letter[-1]
    hasAcc = ""

    if octave.isnumeric():
        octave = int(octave)
        if len(letter) == 3:
            hasAcc = letter[1]
    else:
        octave = 4
        if len(letter) == 2:
            hasAcc = letter[-1]

    let = letter[0].upper() + hasAcc
    ind = letter_notes_sharp.index(let) if hasAcc == "#" else letter_notes_flat.index(let)
    return ind + (12 * (octave+2)) - 3



def conv(s):
    if s.isnumeric():
        return int(s)
    else:
        return letter_to_midi(s)

def print_neck(offsets):
    for i in range(frets):
        print(markings[i] + '==', end = '')
    print("=")
    for i in range(strings):
        out = 'X  ' if offsets[i] <= -1 else "|  "
        for o in range(frets):
            out += "o  " if o+1 == offsets[i] else "-  "
        out += " " if offsets[i] <= -1 else midi_to_letter(tuning[i]+offsets[i])
        print(out)


def from_pairs(pairs):
    ret = [-1] * strings
    for pair in pairs:
        ret[pair[0]] = pair_to_fret(pair)
    return ret

def pair_to_fret(pair):
    return pair[1] - tuning[pair[0]]

def ok_strings(note):
    return [i  for i in range(strings) if tuning[i] <= note and tuning[i]+frets >= note]

#print(ok_strings(67))

def maxDiff(a):
    a.sort()
    vmin = a[0]
    dmax = 0
    for i in range(len(a)):
        if (a[i] < vmin):
            vmin = a[i]
        elif (a[i] - vmin > dmax):
            dmax = a[i] - vmin
    return dmax

def generate_ordered_notes(notes, acc, n):

    newl = []
    for s in ok_strings(notes[n]):
        addition = [(s,notes[n])]
        for i in acc if acc != [] else (range(0) if newl.append(addition) is None else range(0)):
            bad = [1 for pair in i if s == pair[0]]
            if bad == []:
                newl.append(addition+i)


    if n+1 == len(notes):
        #print(newl)
        return newl
    return generate_ordered_notes(notes, newl, n+1)


def best(ordered):
    m,n =  min([((maxDiff([pair_to_fret(b) for b in a])),a) for a in ordered])
    l =  n
    return n

parser = argparse.ArgumentParser(description="midi to tab converter")
parser.add_argument('-f', '--file', help='-f <file>')
parser.add_argument('-t', '--tuning', nargs="+", help='-t 64 59 55 50 45 40    for standard tuning, input notes are in midi')
parser.add_argument('-fr', '--frets', help="-fr <number of frets>   standart=23")
parser.add_argument('-a', '--append', nargs="+", action='append',help="-a <notes for chord 1> ... -a <notes for chord n> to append a chord to the end of your mdid sequence")
tuning = []

frets = 23

args = parser.parse_args()

if args.frets is not None:
    frets = int(args.frets)
markings = markings + ["=" for _ in range(frets-23)]
if args.tuning is not None:
    tuning = [conv(a) for a in args.tuning]

else:
     tuning = [64, 59, 55, 50, 45, 40]
strings = len(tuning)

mid = MidiFile(args.file)
chords = []
chord = []
note_on = 0
for track in mid.tracks:
    for msg in track:
        if msg.type == 'note_on':
            note_on += 1
            chord.append(msg.note)
        elif msg.type == 'note_off':
            note_on -= 1
        else:
            continue
        if note_on == 0:
            chords.append(chord)
            chord = []
if args.append is not None:
    chords.extend([[conv(b) for b in a] for a in args.append])

for chord in chords:
    print_neck(from_pairs(best(generate_ordered_notes(chord,[],0))))
for i in range(frets):
    print("===", end = '')
print("=")
