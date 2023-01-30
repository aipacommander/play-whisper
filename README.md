# 遊ぶ


酔っ払ってこれを書いている


## 環境

- M1 mac

## 準備

```bash
$ docker build -t whisper . --platform linux/arm64
$ docker run --rm -v $(pwd):/workspace -it whisper /bin/bash
```

## 準備2(Dockerコンテナ内)

文字起こししたいyoutube動画を落とす

```bash
$ yt-dlp -x --audio-format mp3 https://youtu.be/vR5GXyklvm4
$ mv ${ダウンロードしたファイル名} sample.mp3
```

## スクリプト実行(Dockerコンテナ内)

```python
import ffmpeg
out, _ = (
    ffmpeg.input("sample.mp3", threads=0)
    .output("-", format="s16le", acodec="pcm_s16le", ac=1, ar=16000)
    .run(cmd="ffmpeg", capture_stdout=True, capture_stderr=True)
)


from whisper_streaming import WhisperStreaming

whisper_streaming = WhisperStreaming()
sender_buffer = out

from whisper.audio import SAMPLE_RATE
while len(sender_buffer) > 0:
    set_data = sender_buffer[:SAMPLE_RATE*5*2]
    whisper_streaming.set_data(set_data)
    sender_buffer = sender_buffer[SAMPLE_RATE*5*2:]

whisper_streaming.get_result()['text']
```

