


def QualityControl(transcript,inputname):


    pathaudio = './FinishedAudio/'
    pathrejectaudio = './RejectAudio/'
    import os
    import shutil
    import whisperx
    import gc
    import torch

    device = "cuda"
    compute_type = "float16"  # change to "int8" if low on GPU mem (may reduce accuracy)

    model = whisperx.load_model("large-v2", device, compute_type=compute_type, language='en',asr_options={"suppress_numerals": True})
    remove_list = []

    #comparefile = open("comparisonresults.txt", "a")  # append mode

    for transcriptcount, entry in enumerate(transcript): #can't directly subscript entries from pandas dataframes in loop for some reason, will have to access through the whole transcript
        splitentry = entry.split('|')
        audioname = splitentry[0]
        transcribedtext = splitentry[1]
        #audiofile = audioname + ".wav"
        loadedAudioFile = pathaudio + audioname
        # initial prompt because Whisper sometimes goes into no punctuation mode.
        secondtranscript = model.transcribe(loadedAudioFile) #analyze audio clip

        clipsize = len(secondtranscript["segments"]) #measure number of text segments in audio clip?
        count = 0
        while count < clipsize: #put together total text of audio clip
            sentence = secondtranscript["segments"][count]["text"]
            if (count == 0):
                sentencecollection = sentence
            else:
                sentencecollection = sentencecollection + " " + sentence

            count = count + 1
        secondtranscript = sentencecollection.split(" ") #split the second transcript to get a word count
        firsttranscript = transcribedtext
        firsttranscript = firsttranscript.split(" ") #split the first transcript
        firstcount = len(firsttranscript)
        secondcount = len(secondtranscript)
        predictiondifference = firstcount - secondcount #compare the first and second transcript
        predictiondifference = abs(predictiondifference)

        print("Analyzed transcript")
        #print(firsttranscript)
        #print(firstcount)
        #print(secondtranscript)
        #print(secondcount)
        # Append-adds at last
        #comparefile.write(audioname + "\n")
        #comparefile.write(str(firsttranscript) + "\n")
        #comparefile.write(str(firstcount) + "\n")
        #comparefile.write(str(secondtranscript) + "\n")
        #comparefile.write(str(secondcount) + "\n")
        #comparefile.write("-------------\n")


        if (predictiondifference > 0): #if the word counts differ too much get rid of the audio clip.
            #print("Bad Entry Detected")
            #print(transcript[transcriptcount])
            remove_list.append(transcriptcount)
            loadedrejectedaudio = pathrejectaudio + audioname
            shutil.move(loadedAudioFile, loadedrejectedaudio)
            #print("New Entry at Position")
            #print(transcript[transcriptcount])

        transcriptplace = str(transcriptcount)
        print("Analyzed line: " + transcriptplace)

    #comparefile.close()


    transcriptcleaned = [a for i, a in enumerate(transcript) if i not in remove_list] #remove bad entries from transcript

    cleanedoutputname = inputname + "_cleaned2.txt"

    f = open(cleanedoutputname, 'a')
    for item in transcriptcleaned:
        f.write(item)
    f.close()

    gc.collect()
    torch.cuda.empty_cache()


    return transcript

