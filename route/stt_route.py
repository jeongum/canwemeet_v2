import re
import sys
import datetime
import time
import pyaudio
from google.cloud import speech
from six.moves import queue
from flask import Flask,url_for, render_template, request, Blueprint, session, jsonify
EXIT_FLAG = True

stt_route = Blueprint('stt_route',__name__)

class ResumableMicrophoneStream:
    """Opens a recording stream as a generator yielding the audio chunks."""
    streaming_limit = 300000  # 5 minutes
    sample_rate = 16000
    chunk_size = int(sample_rate / 10)  # 100m
    def __init__(self):
        self._num_channels = 1
        self._buff = queue.Queue()
        self.closed = True
        self.start_time = self.get_current_time_to_ms()
        self.restart_counter = 0
        self.audio_input = []
        self.last_audio_input = []
        self.result_end_time = 0
        self.is_final_end_time = 0
        self.final_request_end_time = 0
        self.bridging_offset = 0
        self.last_transcript_was_final = False
        self.new_stream = True
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            channels=self._num_channels,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=self.chunk_size,
            # Run the audio stream asynchronously to fill the buffer object.
            # This is necessary so that the input device's buffer doesn't
            # overflow while the calling thread makes network requests, etc.
            stream_callback=self._fill_buffer,
        )

    def __enter__(self):

        self.closed = False
        return self

    def __exit__(self, type, value, traceback):

        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        # Signal the generator to terminate so that the client's
        # streaming_recognize method will not block the process termination.
        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_buffer(self, in_data, *args, **kwargs):
        """Continuously collect data from the audio stream, into the buffer."""
        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self):
        """Stream Audio from microphone to API and to local buffer"""
        while not self.closed:
            data = []

            if self.new_stream and self.last_audio_input:
                chunk_time = self.streaming_limit / len(self.last_audio_input)

                if chunk_time != 0:
                    if self.bridging_offset < 0:
                        self.bridging_offset = 0

                    if self.bridging_offset > self.final_request_end_time:
                        self.bridging_offset = self.final_request_end_time

                    chunks_from_ms = round(
                        (self.final_request_end_time - self.bridging_offset)
                        / chunk_time
                    )

                    self.bridging_offset = round(
                        (len(self.last_audio_input) - chunks_from_ms) * chunk_time
                    )

                    for i in range(chunks_from_ms, len(self.last_audio_input)):
                        data.append(self.last_audio_input[i])

                self.new_stream = False

            # Use a blocking get() to ensure there's at least one chunk of
            # data, and stop iteration if the chunk is None, indicating the
            # end of the audio stream.
            chunk = self._buff.get()
            self.audio_input.append(chunk)

            if chunk is None:
                return
            data.append(chunk)
            # Now consume whatever other data's still buffered.
            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                    self.audio_input.append(chunk)

                except queue.Empty:
                    break

            yield b"".join(data)

    def get_current_time_to_ms(self):
        """Return Current Time in MS."""
        return int(round(time.time() * 1000))

    def get_current_time_to_str(self):
        now = datetime.datetime.now()
        return now.strftime('%A, %d %B %Y %H:%M:%S')

class SpeechToText:
    global EXIT_FLAG
    def __init__(self):
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code="ko-KR",
            # max_alternatives=1,
            # audio_channel_count=2,    # The number of channels 
            # enable_separate_recognition_per_channel=True # audio_channel_count > 1 to get each channel recognized separately.
        )
        self.streaming_config = speech.StreamingRecognitionConfig(
            config=config, interim_results=True
        )

    def run(self):
        client = speech.SpeechClient()
        mic_manager = ResumableMicrophoneStream()
        # start STT 
        sys.stdout.write("==start stt==!\n")
        with mic_manager as stream:
            stream.audio_input = []
            audio_generator = stream.generator()
            requests = (
                speech.StreamingRecognizeRequest(audio_content=content)
                for content in audio_generator
            )
            responses = client.streaming_recognize(
                requests=requests, config=self.streaming_config
            )
            self.listen_print_loop(request, responses, stream)
            if EXIT_FLAG:
                return 

            if stream.result_end_time > 0:
                stream.final_request_end_time = stream.is_final_end_time
                stream.result_end_time = 0
                stream.last_audio_input = []
                stream.last_audio_input = stream.audio_input
                stream.audio_input = []
                stream.restart_counter = stream.restart_counter + 1

            if not stream.last_transcript_was_final:
                sys.stdout.write("\n")

    def listen_print_loop(self, request, responses, stream):
        for response in responses:
            if stream.get_current_time_to_ms() - stream.start_time > stream.streaming_limit:
                stream.start_time = stream.get_current_time_to_ms()
                break
            if not response.results:
                continue

            result = response.results[0]
            if not result.alternatives:
                continue

            transcript = result.alternatives[0].transcript
            result_seconds = 0

            if result.result_end_time.seconds:
                result_seconds = result.result_end_time.seconds

            stream.result_end_time = int((result_seconds * 1000) + (result_seconds / 1000000))
            # return and store at the end of the speech 
            if EXIT_FLAG:
                break 
            else:
                if result.is_final:
                    current_time = stream.get_current_time_to_str()
                    sys.stdout.write(current_time + ": " + transcript + "\n")
                    stream.is_final_end_time = stream.result_end_time
                    stream.last_transcript_was_final = True
                else:
                    stream.last_transcript_was_final = False

@stt_route.route('/stt', methods =['POST'])
def transcript():
    global EXIT_FLAG
    if 'start_stt' in request.form:
        EXIT_FLAG = not(EXIT_FLAG)
        stt = SpeechToText()
        stt.run()
    elif 'end_stt' in request.form:
        sys.stdout.write("==end stt!==\n")
        EXIT_FLAG = not(EXIT_FLAG)
    return render_template('chat/index.html')
