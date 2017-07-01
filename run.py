from pysynth_s import make_wav
import random

notes = ['c','c#','d','d#','e', 'f','f#','g','g#','a','a#', 'b', 'b#']

# intervals with their chance to appear
intervals = [
    (0, 0.6),
    (3, 0.6),
    (4, 0.4),
    (5, 0.5),
    (7, 0.7),
    (8, 0.3),
    (9, 0.3),
    (12, 0.5),
]


# lengths with their chance to appear
notelengths = [ # adjust right values to set music speed. larger left numbers - faster. larger right - more chance
    (1, 0.2),
    (2, 0.4),
    (4, 0.5),
    (8, 0.4),
    (16, 0.0)
    ]


chc = 0.95 # chance of chord instead of single note
lcc = 0.5 # chance to change note|chord length
npcc = 0.1 # chance to meet not primary chord
pc = 0.0 # chance of pause instead of sound

tonelimit = 4 * 12

primary_chord = 1 # 1 = minor, -1 = major

def rnd_pass(prop):
    random.seed()
    r = random.randint(0,1000)
    return r / 1000.0 < prop

def make_song(length):
    random.seed()
    song = []
    # select initial tone
    tone = random.randint(0,6) * 2 + 12 * random.randint(0,5)
    slc = 0  # total sequence length counter
    passed = False
    while not passed:
        nl = notelengths[random.randint(0,len(notelengths)-1)]
        if rnd_pass(nl[1]):
            nl = nl[0] # set note length
            passed = True
    chordtype = primary_chord

    while slc < length:
        ffc = 0 # frame fullness counter
        if int(slc) == slc:
            strong = True # make the first sound of the frame strong
        else:
            strong = False
        # should we change note length?
        if rnd_pass(lcc):
            passed = False
            while not passed:
                random.seed()
                nl = notelengths[random.randint(0, len(notelengths) - 1)]
                if rnd_pass(nl[1]):
                    nl = nl[0]  # set note length
                    passed = True
        slc += 1/nl
        if rnd_pass(pc):  # use pause
            song.append(make_pause(nl))
        else:  # make sound
            if not rnd_pass(chc): #use single note
                # select new interval
                passed = False
                while not passed:
                    random.seed()
                    iv = intervals[random.randint(0, len(intervals) - 1)]
                    if rnd_pass(iv[1]):
                        iv = iv[0]  # set note length
                        passed = True
                if tone - iv < 0 or (tone + iv < tonelimit and rnd_pass(0.5)):
                    tone += iv
                else:
                    tone -= iv
                octave = (tone // 12) + 1
                note = notes[tone % 12]
                song.append(make_note(note,octave,nl,strong))
            else: # use chord
                chord_iv_passed = False
                while not chord_iv_passed:
                    random.seed()
                    # select new interval
                    passed = False
                    while not passed:
                        random.seed()
                        iv = intervals[random.randint(0, len(intervals) - 1)]
                        if rnd_pass(iv[1]):
                            iv = iv[0]  # set note length
                            passed = True
                    if tone - iv < 0 or (tone + iv < tonelimit and rnd_pass(0.5)):
                        tone += iv
                    else:
                        tone -= iv
                    octave = (tone // 12) + 1
                    if not (tone % 12) % 2:
                        chord_iv_passed = True
                        if rnd_pass(npcc):
                            chordtype = -primary_chord
                        else:
                            chordtype = primary_chord
                        if chordtype > 0:  # make minor chord
                            chord = make_chord(minorchords[(tone % 12)//2],octave,nl,strong)
                        else:
                            chord = make_chord(majorchords[(tone % 12)//2],octave,nl,strong)

                song.append(chord)

    return song


def make_pause(l):
    return make_note('r', 0, l)

def make_note(name, o, l, strong = False):
    if name == 'r':
        return [['r', l]]
    note = [[name + str(o), l]]
    if strong:
        note[0][0] += '*'
    return note

def make_chord(name, o, l, strong = False):
    note = []
    if name == 'C':
        note.append('c' + str(o))
        note.append('e' + str(o))
        note.append('g' + str(o))
    elif name == 'Cm':
        note.append('c' + str(o))
        note.append('eb' + str(o))
        note.append('g' + str(o))
    elif name == 'D':
        note.append('d' + str(o))
        note.append('f#' + str(o))
        note.append('a' + str(o))
    elif name == 'Dm':
        note.append('d' + str(o))
        note.append('f' + str(o))
        note.append('a' + str(o))
    elif name == 'E':
        note.append('e' + str(o))
        note.append('g#' + str(o))
        note.append('b' + str(o))
    elif name == 'Em':
        note.append('e' + str(o))
        note.append('g' + str(o))
        note.append('b' + str(o))
    elif name == 'F':
        note.append('f' + str(o))
        note.append('a' + str(o))
        note.append('c' + str(o+1))
    elif name == 'Fm':
        note.append('f' + str(o))
        note.append('ab' + str(o))
        note.append('c' + str(o+1))
    elif name == 'G':
        note.append('g' + str(o))
        note.append('b' + str(o))
        note.append('d' + str(o+1))
    elif name == 'Gm':
        note.append('g' + str(o))
        note.append('bb' + str(o))
        note.append('d' + str(o+1))
    elif name == 'A':
        note.append('a' + str(o))
        note.append('c#' + str(o+1))
        note.append('e' + str(o+1))
    elif name == 'Am':
        note.append('a' + str(o))
        note.append('c' + str(o+1))
        note.append('e' + str(o+1))
    else:
        return [['r',l]]
    chord = []
    for n in note:
        if strong:
            n += '*'
        chord.append([n, l])
    return chord

majorchords = ['C','D','E','F','G', 'A']
minorchords = ['Cm','Dm','Em','Fm','Gm', 'Am']

randsong = make_song(20)
print(randsong)

make_wav(randsong, bpm=120, transpose=1, boost=1.15, repeat=0, fn="tst.wav")