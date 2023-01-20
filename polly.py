"""
    Here we will use the Amazon Polly to convert the text to speech.
"""
import boto3
import pyaudio

polly_client = boto3.client(service_name='polly', region_name='us-east-1', use_ssl=True)

# Use module
PY_AUDIO = pyaudio.PyAudio()


def text_to_speech(text_to_convert):
    # Convert the text to speech
    response = polly_client.synthesize_speech(Text=text_to_convert, OutputFormat='pcm', VoiceId="Lucia")

    stream_data(response['AudioStream'])


def stream_data(stream):
    """
        Consumes a stream in chunks to produce the response's output
    """

    chunk = 1024
    if stream:
        polly_stream = PY_AUDIO.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            output=True,
        )

        # this is a blocking call...
        while True:
            data = stream.read(chunk)
            polly_stream.write(data)
            # If there's no more data to read, stop streaming
            if not data:
                stream.close()
                polly_stream.stop_stream()
                polly_stream.close()
                break
