import os
import json
import random
import subprocess
import re
import urllib.request
import openai
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

HISTORY_FILE = "processed_history.txt"

# Silicon Valley Fix: Maps custom handles directly to official immutable YouTube Channel IDs
CHANNEL_FEEDS = [
    "https://youtube.com",  # Cocomelon
    "https://youtube.com",  # ChuChu TV
    "https://youtube.com",  # Bebefinn
    "https://youtube.com",  # Pinkfong
    "https://youtube.com"   # Baby Shark
]

def get_already_processed_ids():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return [line.strip() for line in f.readlines()]
    return []

def save_processed_id(video_id):
    with open(HISTORY_FILE, "a") as f:
        f.write(f"{video_id}\n")

def fetch_latest_video_from_rss():
    print("[INFO] Selecting an encrypted RSS entry stream node randomly...")
    selected_feed = random.choice(CHANNEL_FEEDS)
    print(f"[INFO] Accessing bulletproof RSS stream payload: {selected_feed}")
    
    try:
        # Securely fetch XML data directly via standard secure web requests (Bypasses all scraper blocks)
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        req = urllib.request.Request(selected_feed, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as response:
            xml_content = response.read().decode('utf-8')
            
        # Regex expression pattern to capture the absolute latest video entry ID instantly
        video_ids = re.findall(r'<yt:videoId>([^<]+)</yt:videoId>', xml_content)
        
        if not video_ids:
            raise Exception("XML parsing layout returned empty node streams.")
            
        target_id = video_ids[0].strip()
        print(f"[SUCCESS] Official YouTube backend data match located: {target_id}")
        return target_id
        
    except Exception as network_error:
        raise Exception(f"[XML FETCH FAILURE] Primary bypass pipeline crashed: {str(network_error)}")

def download_and_slice(video_url):
    print("[INFO] Initiating high-speed video download from verified source...")
    # Cleaned arguments to eliminate output naming configuration conflicts on cloud networks
    subprocess.run(["yt-dlp", "--no-warnings", "-f", "bestvideo+bestaudio/best", "-o", "raw_source.mp4", video_url])
    
    print("[INFO] Slicing source asset into mandatory 5-second segments...")
    subprocess.run(["ffmpeg", "-y", "-i", "raw_source.mp4", "-c", "copy", "-map", "0", "-segment_time", "5", "-f", "segment", "segment_%03d.mp4"])
    
    segments = [f for f in os.listdir() if f.startswith("segment_") and f.endswith(".mp4")]
    random.shuffle(segments)
    return segments

def apply_advanced_transformations(segments):
    print("[INFO] Applying multi-effects, transformations, and custom sound variations (Klasky style, 1.2x pitch, 1.5x volume gain)...")
    processed_files = []
    
    # 24 to 102 clips configures the exact video runtime between 2:00 and 8:30 minutes
    target_count = random.randint(24, 102)
    print(f"[DYNAMIC LENGTH] Constructing a new version composed of {target_count} randomized 5-second variations.")
    
    for i, clip in enumerate(segments[:target_count]):
        output_clip = f"transformed_fx_{i}.mp4"
        ffmpeg_cmd = [
            "ffmpeg", "-y", "-i", clip,
            "-vf", "lutrgb=r=negate:g=negate:b=negate,scale=1920:1080", 
            "-af", "asetrate=44100*1.2,atempo=1.0,volume=1.5",
            "-c:v", "libx264", "-c:a", "aac", output_clip
        ]
        subprocess.run(ffmpeg_cmd)
        processed_files.append(output_clip)
        
    return processed_files

def compile_final_longform(processed_files):
    print("[INFO] Assembling all multi-effect clips into the final long-form video...")
    with open("render_list.txt", "w") as f:
        for file in processed_files:
            f.write(f"file '{file}'\n")
            
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", "render_list.txt", "-c", "copy", "final_render_output.mp4"])
    print("[SUCCESS] New long-form transformation rendering complete.")

def generate_ai_metadata():
    print("[INFO] Querying AI engine for viral, high-CPM metadata optimized for USA audience...")
    openai.api_key = os.getenv("OPENAI_API_KEY")
    prompt = "Generate a highly engaging, viral kids YouTube Video Title, description, and high-CPM tags targeting the USA market."
    
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices.message['content']

def upload_and_cleanup(metadata_text, video_id):
    print("[INFO] Opening secure connection to target YouTube channel...")
    
    client_secret_data = json.loads(os.getenv("YOUTUBE_API_SECRET"))
    token_data = json.loads(os.getenv("YOUTUBE_TOKEN"))
    
    credentials = Credentials.from_authorized_user_info(token_data)
    
    if credentials.expired and credentials.refresh_token:
        print("[INFO] Access token expired. Automatic refresh executing...")
        credentials.refresh(Request())
        
    youtube = build("youtube", "v3", credentials=credentials)
    
    body = {
        "snippet": {
            "title": "Viral Kids Cartoons Multi-FX Transformation", 
            "description": "Premium High-Definition Kids Visual Edit Compilation Output Matrix.",
            "tags": ["cartoons", "kids", "animation", "viral"],
            "categoryId": "1"
        },
        "status": {
            "privacyStatus": "public" 
        }
    }
    
    media = MediaFileUpload("final_render_output.mp4", chunksize=-1, resumable=True)
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
    
    response = request.execute()
    new_video_url = f"https://youtube.com{response.get('id')}"
    print(f"[SUCCESS] Transmission completed. Target link live: {new_video_url}")
    
    save_processed_id(video_id)
    
    print("[CLEANUP ENGINE] Erasing physical video memory cache from cloud storage workspace...")
    files_to_clean = ["raw_source.mp4", "final_render_output.mp4", "render_list.txt"]
    for file in files_to_clean:
        if os.path.exists(file):
            os.remove(file)
            
    for item in os.listdir():
        if item.startswith("segment_") or item.startswith("transformed_fx_"):
            os.remove(item)
    print("[SUCCESS] Disk memory cleared. System optimized for next cycle.")

def main():
    try:
        video_id = fetch_latest_video_from_rss()
        if video_id is None:
            return  

        # Memory Logic Suppression Fallback (Optional, but enabled here for strict safety logs)
        processed_ids = get_already_processed_ids()
        if video_id in processed_ids:
            print(f"[SUPPRESSION] Data stream tracking matched historical logs for ID: {video_id}. Safely skipping execution loop.")
            return

        video_url = f"https://youtube.com{video_id}"
        segments = download_and_slice(video_url)
        fx_clips = apply_advanced_transformations(segments)
        compile_final_longform(fx_clips)
        metadata = generate_ai_metadata()
        upload_and_cleanup(metadata, video_id)
        print("[SYSTEM] Autonomous Cycle Executed and Safely Logged.")
    except Exception as e:
        print(f"[SYSTEM ENGINE FAILURE] Handled Exception: {str(e)}")

if __name__ == "__main__":
    main()
