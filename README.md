# Live Translator

The program will transcribe the voice to text, translate the text to the target language, and then convert the text to speech.

## This program will use the following AWS services:
- Amazon Transcribe (transcribe voice to text)
- Amazon Translate (translate the text to the target language)
- Amazon Polly (text to Speech)

## Prerequisites
- AWS Account
- AWS CLI
- Python 3.6 or later

## Setup
- Create a new IAM user with the following permissions:
  - AmazonTranscribeFullAccess
  - AmazonTranslateFullAccess
  - AmazonPollyFullAccess

- Configure the AWS CLI with the new user credentials
- Install the required Python packages:
  - `pip install -r requirements.txt`

## Usage
- Run the program
- Select the source language
- Select the target language
- Speak into the microphone
