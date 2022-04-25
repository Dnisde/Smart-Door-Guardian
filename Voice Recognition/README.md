This is the voice to text convertion module. It captures user's voice input over a microphone
and convert the voice to text by using Google Cloud Speech-To-Text API. The converted text is stored in file <em>converted.txt</em>.

Before run the voice2text.sh script, please make sure that:
- You're running on a Raspberry Pi (Pi 3 or later version) 
- Pi has a functioning microphone
- Pi is connected to internet
- In the script, put your Google API key for the variable <em>API_KEY</em>
- Run the following command: 
```
chmod 755 voice2text.sh
```
