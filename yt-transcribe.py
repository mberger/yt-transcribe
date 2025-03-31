import yt_dlp
from pydub import AudioSegment
import whisper
import os
import re

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
        info = ydl.extract_info(url, download=True)  # Extract metadata and download
        title = info.get('title', 'unknown_title')   # Get video title

    # Sanitize filename (remove unsafe characters)
    safe_title = re.sub(r'[\\/*?:"<>|]', '', title)
    
    return 'audio.mp3', safe_title

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
    audio_file, video_title = download_audio_from_youtube(video_url)
    transcript = transcribe_audio(audio_file)
    
    # Use video title for filename
    filename = f'transcript_{video_title}.md'
    
    save_transcript_to_markdown(transcript, filename)
    print(f"Transcript saved to {filename}")
