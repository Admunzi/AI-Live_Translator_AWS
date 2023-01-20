"""
    Here we will use the Amazon Transcribe to transcribe the audio to text.

"""

from translate import translate_text
from polly import text_to_speech

import asyncio
# This example uses the sounddevice library to get an audio stream from the
# microphone. It's not a dependency of the project but can be installed with
# `python -m pip install amazon-transcribe aiofile`
# `pip install sounddevice`.
import sounddevice

from amazon_transcribe.client import TranscribeStreamingClient
from amazon_transcribe.handlers import TranscriptResultStreamHandler
from amazon_transcribe.model import TranscriptEvent, TranscriptResultStream


class MyEventHandler(TranscriptResultStreamHandler):
    def __init__(self, transcript_result_stream: TranscriptResultStream, language_input, language_output):
        super().__init__(transcript_result_stream)
        self.language_input = language_input
        self.language_output = language_output

    async def handle_transcript_event(self, transcript_event: TranscriptEvent):
        # This handler can be implemented to handle transcriptions as needed.
        # Here's an example to get started.
        results = transcript_event.transcript.results

        if len(results) > 0:
            if len(results[0].alternatives) > 0:
                transcript = results[0].alternatives[0].transcript

                if hasattr(results[0], "is_partial") and results[0].is_partial == False:
                    print("Transcript:", transcript)

                    translated_text = translate_text(transcript, self.language_input, self.language_output)
                    print("Translated text:", translated_text)

                    text_to_speech(translated_text)


async def mic_stream():
    # This function wraps the raw input stream from the microphone forwarding
    # the blocks to an asyncio.Queue.
    loop = asyncio.get_event_loop()
    input_queue = asyncio.Queue()

    def callback(indata, frame_count, time_info, status):
        loop.call_soon_threadsafe(input_queue.put_nowait, (bytes(indata), status))

    stream = sounddevice.RawInputStream(
        channels=1,
        samplerate=16000,
        callback=callback,
        blocksize=1024 * 2,
        dtype="int16",
    )
    # Initiate the audio stream and asynchronously yield the audio chunks
    # as they become available.
    with stream:
        while True:
            indata, status = await input_queue.get()
            yield indata, status


async def write_chunks(stream):
    # This connects the raw audio chunks generator coming from the microphone
    # and passes them along to the transcription stream.
    async for chunk, status in mic_stream():
        await stream.input_stream.send_audio_event(audio_chunk=chunk)
    await stream.input_stream.end_stream()


async def basic_transcribe(language_input, language_output):
    # Setup up our client with our chosen AWS region
    client = TranscribeStreamingClient(region="us-east-1")

    # Start transcription to generate our async stream
    stream = await client.start_stream_transcription(
        language_code=language_input,
        media_sample_rate_hz=16000,
        media_encoding="pcm"
    )

    # Instantiate our handler and start processing events
    handler = MyEventHandler(stream.output_stream, language_input, language_output)
    await asyncio.gather(write_chunks(stream), handler.handle_events())


def transcribe_audio(language_input, language_output):
    loop = asyncio.get_event_loop()
    task = loop.create_task(basic_transcribe(language_input, language_output))
    loop.run_until_complete(task)
    loop.close()

    return task.result()
