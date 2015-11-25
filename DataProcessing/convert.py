import argparse
import csv
import subprocess
import os

#debuging use
def visualize(notes):
    key = ['C','C#','D','Eb','E','F','F#','G','Ab','A','Bb','B']
    pitches = notes[0:12]
    newNotes = ['', '', '', '', '', '', '', '', '', '', '', '', key[notes[12]]]
    for i in range(0,12):
        if pitches[i] >= 1: newNotes[i] = key[i]
    return newNotes

#notes = list of midi pitches (0-127)
#newNotes = [n, n, n, n, n, n, n, n, n, n, n, n, bass]
def formatNotes(notes):
    notes = list(set(notes))
    newNotes = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 128]
    minNote = 128
    for note in notes:
        if minNote > note:
            minNote = note
            newNotes[12] = note % 12
#        newNotes[note % 12] = 1                        #format 0
        newNotes[note % 12] = newNotes[note % 12] + 1   #format 1
    return newNotes

def readcsv(filePath, sid, debug):
    with open(filePath, newline='') as file:
        #CSV -> List
        RR = list(csv.reader(file, delimiter=',', skipinitialspace=True))
        #L = Lyric (annotated chord list from MIDI)
        CL = list(filter(lambda x: (x[2] == 'Lyric_t'), RR))
        CL = list(map(lambda x: [int(x[1]), x[2], x[3]], CL))
        #Keep only 'Note_<off/on>_c' rows
        R = list(filter(lambda x: (x[2] == 'Note_on_c') or (x[2] == 'Note_off_c'), RR))
        #Keep only columns 2, 3, 5, 6
        R = list(map(lambda x: [int(x[1]), x[2], int(x[4]), int(x[5])], R))
        #Sort by time, then by velocity
        R = sorted(R, key=(lambda x: (x[0], x[3])))
        eList = dict()
        heldNotes = []
        prevTime = 0
        hold = False
        for row in R:
            if (prevTime != row[0] and hold == True):
                #Play heldNotes
                currNotes = []
                currNotes.extend(heldNotes) #shallow copy
                if debug: print(currNotes)
                eList.update(dict({prevTime:currNotes}))
            if (row[1] == 'Note_off_c' or (row[1] == 'Note_on_c' and row[3] == 0)):
                if row[2] in heldNotes: heldNotes.remove(row[2])
                hold = False
                prevTime = row[0]
            elif (row[1] == 'Note_on_c'):
                heldNotes.append(row[2])
                hold = True
                prevTime = row[0]
            if debug: print(row)
        eList2 = []
        i = 1
        W = []
        chordLbl = 'N' #Default: no chord label
        CL_index = 0
        for time, values in sorted(eList.items()):
            #Change currently selected chord label
            if CL_index < len(CL) and time == CL[CL_index][0]:
                chordLbl = CL[CL_index][2]
                CL_index = CL_index + 1
            x = [sid, i]
            if debug: x.extend(visualize(formatNotes(values)))
            else: x.extend(formatNotes(values))
            #x.append(metric)
            x.append(chordLbl)
            W.append(x)
            i = i + 1
        return W

def writecsv(filePath, mode, W):
    with open(filePath, mode, newline='') as file:
        writer = csv.writer(file)
        writer.writerows(W)
        return

parser = argparse.ArgumentParser()
parser.add_argument('inputPath', help='MIDI file or Dir containing MIDI files')
parser.add_argument('outputFile', help='Output csv file')
parser.add_argument('-d', dest='debug', action='store_const',
                    const=True, default=False,
                    help='Debug mode. Use notes instead of numbers for .csv')
args = parser.parse_args()

#convert single file
if os.path.isfile(args.inputPath):
    if args.inputPath.endswith('.mid'):
        fileTitle = args.inputPath.split(sep='.')[0]
        midiToCSV = ['Midicsv.exe', args.inputPath, 'temp.csv']
        subprocess.call(midiToCSV)
        W = readcsv('temp.csv', fileTitle, args.debug)
        writecsv(args.outputFile, 'w', W)
    subprocess.call('rm temp.csv')
#convert multiple files
elif os.path.isdir(args.inputPath):
    #remove outputFile if exists
    if os.path.isfile(args.outputFile): subprocess.call('rm ' + args.outputFile)
    for file in sorted(os.listdir(args.inputPath)):
        if file.endswith('.mid'):
            fileTitle = file.split(sep='.')[0]
            midiToCSV = ['Midicsv.exe', args.inputPath + '/' + file, 'temp.csv']
            subprocess.call(midiToCSV)
            W = readcsv('temp.csv', fileTitle, args.debug)
            writecsv(args.outputFile, 'a', W)
    subprocess.call('rm temp.csv')
else:
    print('Invalid input path')


