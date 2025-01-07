### Sample-Right - Batch fix incorrect samplerate header information
---
Occasionally some audio recording devices stamp files with the wrong samplerate despite the underlying audio being recorded as intended (an example being Grace Design m108 on MacOS with firmware prior to 1.12). As a result, DAWs and audio players play back the files at the wrong speed. This python script is designed to quickly fix these issues for one or more audio files by only changing the samplerate information in the wave header.

**Supported file type**: wav

#### Usage:
sample-right.py <correct_samplerate> <file_pattern>
#### Example (correcting the samplerate header information for all wav files in the folder to 88.2k):
```sh
sample-right.py 88200 "*.wav"
```

#### Test File
Included in the repository is a wave file (from _The Open Goldberg Variations_ performed by Kimiko Ishizaka) with audio samples recorded at 44.1k but incorrectly stamped 48k. To fix:
```sh
sample-right.py 44100 goldberg-test.wav
```
