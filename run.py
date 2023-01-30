import ffmpeg
from whisper_streaming import WhisperStreaming
from whisper.audio import SAMPLE_RATE


if __name__ == '__main__':
    out, _ = (
        ffmpeg.input("sample.mp3", threads=0)
        .output("-", format="s16le", acodec="pcm_s16le", ac=1, ar=16000)
        .run(cmd="ffmpeg", capture_stdout=True, capture_stderr=True)
    )

    whisper_streaming = WhisperStreaming()
    sender_buffer = out
    while len(sender_buffer) > 0:
        set_data = sender_buffer[:SAMPLE_RATE*5*2]
        whisper_streaming.set_data(set_data)
        sender_buffer = sender_buffer[SAMPLE_RATE*5*2:]

    whisper_streaming.get_result()['text']