


def HallucinationRemover(transcript, inputname):

    import shutil
    pathaudio = './FinishedAudio/'
    pathrejectaudio = './RejectAudio/'

    remove_list = []

    for transcriptcount, entry in enumerate(transcript):  # can't directly subscript entries from pandas dataframes in loop for some reason, will have to access through the whole transcript

        splitentry = entry.split('|')
        audioname = splitentry[0]
        loadedAudioFile = pathaudio + audioname
        transcribedtext = splitentry[1]
        transcribedtextbag = transcribedtext.split(' ')

        transcribedtextsize = len(transcribedtext)

        if (transcribedtextsize > 199): #remove text entries which are too long
            remove_list.append(transcriptcount)
            loadedrejectedaudio = pathrejectaudio + audioname
            shutil.move(loadedAudioFile, loadedrejectedaudio)
            continue


        repeatdetected = 0
        print("HallucinationRemover: Analyzing Line" + str(transcriptcount))

        for wordcount, word in enumerate(transcribedtextbag):
            if wordcount == 0:
                potentialrepeatword = word
            else:
                if potentialrepeatword == word:
                    repeatdetected = repeatdetected + 1

                else:
                    potentialrepeatword = word
                    repeatdetected = 0

            if repeatdetected > 2:
                remove_list.append(transcriptcount)
                loadedrejectedaudio = pathrejectaudio + audioname
                shutil.move(loadedAudioFile, loadedrejectedaudio)
                break

            elif potentialrepeatword == 'the' and repeatdetected > 0:
                remove_list.append(transcriptcount)
                loadedrejectedaudio = pathrejectaudio + audioname
                shutil.move(loadedAudioFile, loadedrejectedaudio)
                break





    transcriptcleaned = [a for i, a in enumerate(transcript) if i not in remove_list] #remove bad entries from transcript

    cleanedoutputname = inputname + "_cleaned.txt"

    f = open(cleanedoutputname, 'a')
    for item in transcriptcleaned:
        f.write(item)
    f.close()