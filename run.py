import ffmpeg
from whisper_streaming import WhisperStreaming
from whisper.audio import SAMPLE_RATE
import sys


if __name__ == '__main__':
    mp3_filename = sys.argv[1]
    out, _ = (
        ffmpeg.input(mp3_filename, threads=0)
        .output("-", format="s16le", acodec="pcm_s16le", ac=1, ar=16000)
        .run(cmd="ffmpeg", capture_stdout=True, capture_stderr=True)
    )

    whisper_streaming = WhisperStreaming()
    sender_buffer = out
    buffer_len = SAMPLE_RATE * 5 * 2
    while len(sender_buffer) > 0:
        set_data = sender_buffer[:buffer_len]
        whisper_streaming.set_data(set_data)
        sender_buffer = sender_buffer[buffer_len:]

    print(whisper_streaming.get_result()['text'])
