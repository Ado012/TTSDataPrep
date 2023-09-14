#!/usr/bin/env python3

from pydub import AudioSegment

import pandas as pd

alignedtranscriptpath = './RawTranscripts/'
rawaudiopath = './PreProcessedAudio/'
splitaudiopath = './SplitAudio/'

def AudioClipper(transcript):

    splitname = transcript.split('.')
    basename = splitname[0]
    transcriptname = alignedtranscriptpath + basename + '.txt'
    audioname = rawaudiopath + basename + '.wav'
    print(transcript)
    print(audioname)

    traininglist = []
    validationlist = []
    datasetentrycount = 0


    sound = AudioSegment.from_file(audioname)
    df = pd.read_csv(transcriptname, sep =' ',header =None)

    for index, row in df.iterrows():
        begin = float(row[1]) * 1000 #look to see if this is converted correctly
        end = float(row[2]) * 1000

        clipsize = end - begin
#cannot be too long or shorter than 0.6 seconds
        if (clipsize > 11000 or clipsize < 1500 ):
            print("AUDIOCLIPPER: discarding clip due to length")

        else:
            audioclip = sound[begin:end]
            clipname = basename + "_" + str(row[0]) + ".wav"
            clipfilename = splitaudiopath + basename + "_" + str(row[0]) + ".wav"
            metadataline = clipname + "|" + " " + row[3]
            #print("row")
            #print(row[3])
            #print("metadataline")
            #print(metadataline)
            audioclip.export(clipfilename, format="wav")
            print("AUDIOCLIPPER: creating new clip fragment")



                # distribute metadata across training and validation sets
            if (datasetentrycount >= 5):
                validationlist.append(metadataline)
                datasetentrycount = 0
            else:
                traininglist.append(metadataline)

            datasetentrycount = datasetentrycount + 1



    return [traininglist, validationlist]
