from pytube import YouTube
from pydub import AudioSegment
import whisper
import os

def download_audio_from_youtube(url):
    yt = YouTube(url)
    video = yt.streams.filter(only_audio=True).first()
    out_file = video.download(filename='audio')
    base, ext = os.path.splitext(out_file)
    new_file = base + '.mp3'
    AudioSegment.from_file(out_file).export(new_file, format='mp3')
    os.remove(out_file)  # remove the original file
    return new_file

def transcribe_audio(audio_file):
    model = whisper.load_model("base")
    result = model.transcribe(audio_file)
    return result['text']

def save_transcript_to_markdown(transcript, filename):
    with open(filename, 'w') as f:
        f.write("# Transcript\n\n")
        f.write(transcript)

if __name__ == "__main__":
    video_url = input("Enter the YouTube video URL: ")
    audio_file = download_audio_from_youtube(video_url)
    transcript = transcribe_audio(audio_file)
    save_transcript_to_markdown(transcript, 'transcript.md')
    print("Transcript saved to transcript.md")
