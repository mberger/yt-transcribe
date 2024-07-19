import yt_dlp
from pydub import AudioSegment
import whisper
import os
from datetime import datetime

def download_audio_from_youtube(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': 'audio.%(ext)s',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    
    return 'audio.mp3'

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
    
    # Get the current date
    current_date = datetime.now().strftime("%Y-%m-%d")
    # Create filename with date
    filename = f'transcript_{current_date}.md'
    
    save_transcript_to_markdown(transcript, filename)
    print(f"Transcript saved to {filename}")
