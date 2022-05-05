#!/bin/bash

# echo "*** Recording now, please speak ***"
# arecord --format=S16_LE --duration=5 --rate=16000 --file-type=wav test.wav

echo "*** Processing... ***"
API_KEY="YOUR_GOOGLE_API_KEY" # REPLACE content with your Google API Key!
curl -X POST --data-binary @test.wav --header 'Content-Type: audio/l16; rate=16000;' "https://www.google.com/speech-api/v2/recognize?output=json&lang=en-us&key=${API_KEY}" > converted.json

echo "*** Display converted text ***"
cat converted.json

# Clean the voice file
rm test.wav
# rm converted.txt

python ./voicePassword.py