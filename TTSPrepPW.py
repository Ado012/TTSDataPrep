


import os

import Converter
import HallucinationRemover
import Punctuator
import SpeechRecognizerWXDiarizer
import SentenceSplitterWX
import AlignerWX
import AudioClipper
import Converter
import whisperx

device = "cuda"
compute_type = "float16"  # change to "int8" if low on GPU mem (may reduce accuracy)


#rename long youtube files

#list files in directory
filelist = os.listdir('./PreProcessedAudio/')
model = whisperx.load_model("large-v2", device, compute_type=compute_type, language='en', asr_options={"suppress_numerals": True})
for entry in filelist:
    SpeechRecognizerWXDiarizer.SpeechRecognizer(entry, model)



#AudioClipper

filelist = os.listdir('./RawTranscripts/')

traininglist = []
validationlist = []

for entry in filelist:
    metadata = AudioClipper.AudioClipper(entry)

    traininglist.extend(metadata[0])
    validationlist.extend(metadata[1])



with open("train.txt", 'w') as f:
    for entry in traininglist:
        f.write(f"{entry}\n")
        print(f"{entry}\n")
        print("row")

with open("validation.txt", 'w') as f:
    for entry in validationlist:
        f.write(f"{entry}\n")
        print(f"{entry}\n")
        print("row")
# MetaDataGenerator




#Converter
filelist = os.listdir('./SplitAudio/')
for entry in filelist:
    Converter.Converter(entry)







import HallucinationRemover

#traintranscript = pd.read_csv('train.txt', sep="|", header=None)

# Using readlines()
traintranscript = open('train.txt', 'r')
traintranscript = traintranscript.readlines()

HallucinationRemover.HallucinationRemover(traintranscript, "train")

#validationtranscript = pd.read_csv('validation.txt', sep="|", header=None)

# Using readlines()
validationtranscript = open('validation.txt', 'r')
validationtranscript = validationtranscript.readlines()

HallucinationRemover.HallucinationRemover(validationtranscript, "validation")




import QualityControlWX

#traintranscript = pd.read_csv('train.txt', sep="|", header=None)

# Using readlines()
traintranscript = open('train_cleaned.txt', 'r')
traintranscript = traintranscript.readlines()

QualityControlWX.QualityControl(traintranscript, "train")

#validationtranscript = pd.read_csv('validation.txt', sep="|", header=None)

# Using readlines()
validationtranscript = open('validation_cleaned.txt', 'r')
validationtranscript = validationtranscript.readlines()

QualityControlWX.QualityControl(validationtranscript, "validation")
