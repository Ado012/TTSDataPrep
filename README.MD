This software prepares training data for MrQ's fork of tortoiseTTS.

It is designed to take raw audio files and convert it to clips and annotation files that can be directly plugged into the ai-voice-cloning software to be processed. 

This project is currently a WIP but the code is sufficient and tested to perform its functions. It just needs a little setup. 


Files: 

TTSPrepPW: The master file which runs all the other scripts. 


SpeechRecognizerWXDiarizer: Input: Audio files (.wav). Output: Raw Transcripts. 
Takes audio files and transcribes them and seperates them by speaker. 

AudioClipper: Input: Raw Transcripts, Audio files. Output: Split audio

HallucinationRemover:Retests audio files to ensure annotations are correct. 


QualityControl: Various tests for transcript errors. 


converter: Input: Audio files. Output: Processed audio files
Converts audio files to proper format. 





