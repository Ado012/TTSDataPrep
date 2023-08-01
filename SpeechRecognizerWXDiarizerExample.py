#!/usr/bin/env python3

path = './RawTranscripts/'
pathaudio = './PreProcessedAudio/'



#get unique speakers
def unique(speakerlist):

    # initialize a null list
    unique_list = []

    # traverse for all elements
    for x in speakerlist:
        # check if exists in unique_list or not
        if x not in unique_list:
            unique_list.append(x)
    # print list
    return unique_list


# Python code to count the number of occurrences
def countX(lst, x):
    count = 0
    for ele in lst:
        if (ele == x):
            count = count + 1
    return count


def SpeechRecognizer(audiofile, model):
    import whisperx
    import gc
    import torch

    device = "cuda"

    count = 0
    batch_size = 4  # reduce if low on GPU mem
    speakerlist = []


    print(audiofile)
    loadedAudioFile = pathaudio + audiofile
    audio = whisperx.load_audio(loadedAudioFile)
    result = model.transcribe(audio, batch_size=batch_size)

    gc.collect()
    torch.cuda.empty_cache()

    model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=device)
    result = whisperx.align(result["segments"], model_a, metadata, audio, device, return_char_alignments=False)

    diarize_model = whisperx.DiarizationPipeline(use_auth_token='YOUR_TOKEN', device=device)

    diarize_segments = diarize_model(loadedAudioFile)

    result = whisperx.assign_word_speakers(diarize_segments, result)


    gc.collect()
    torch.cuda.empty_cache()


    print(diarize_segments)
    print(result["segments"])  # segments are now assigned speaker IDs


    splitname = audiofile.split('.')
    splitname = splitname[0]
    transcriptname = path + splitname + '.txt'
    clipsize = len(result["segments"])
    clipsize2 = clipsize - 5

    print(clipsize)
    print(transcriptname)

    while (count < clipsize):
        print(count)
        try:
            speaker = result["segments"][count]["speaker"]
            speakerlist.append(speaker)
        except KeyError:
            print("Key not present")
        count = count + 1

    uniquelist = unique(speakerlist)

    primarySpeaker = uniquelist[0]
    maxOccurence = 0

    for x in uniquelist:
        occurences = countX(speakerlist, x)
        if occurences > maxOccurence:
            primarySpeaker = x
            maxOccurence = occurences


    count = 0

    with open(transcriptname, 'a') as f:
        while count < (clipsize):
            try:
                currentSpeaker = result["segments"][count]["speaker"]

                if (currentSpeaker == primarySpeaker):
                    entryText = result["segments"][count]["text"]
                    entryTimeBegin = result["segments"][count]["start"]
                    entryTimeEnd = result["segments"][count]["end"]

                    countstr = str(count)
                    entryTimeBegin = str(entryTimeBegin)
                    entryTimeEnd = str(entryTimeEnd)

                    if (entryText[0] == ' '):
                        entryText = entryText[1:]

                    f.write(countstr + " " + entryTimeBegin + " " + entryTimeEnd + " \"" + entryText + "\"")
                    f.write("\n")
                print("SpeechRecognizer:")
                print(result["segments"][count]["speaker"])
                print(result["segments"][count]["text"])
                print(count)
                count = count + 1

            except KeyError:
                print("Key not present")
                count = count + 1
                continue


