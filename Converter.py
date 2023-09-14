

from pydub import AudioSegment
import os


def match_target_amplitude(sound, target_dBFS):
    change_in_dBFS = target_dBFS - sound.dBFS
    return sound.apply_gain(change_in_dBFS)


audiopath = './SplitAudio/'
finishedaudiopath = './FinishedAudio/'


def Converter(audiofile):
    loadedaudiofile = audiopath + audiofile
    audio = AudioSegment.from_file(loadedaudiofile)
    audiomono = audio.set_channels(1) #convert to mono
    audiomonosampled = audiomono.set_frame_rate(22050) #set bitrate

    audionormalized = match_target_amplitude(audiomonosampled, -25.0) #normalize volume

    clipfilename = finishedaudiopath + audiofile #construct file name
    cwd = os.getcwd()
    print(cwd)
    audionormalized.export(clipfilename, format="wav") #export finished file