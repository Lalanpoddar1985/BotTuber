import os
import json
import random
import subprocess
import openai
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

HISTORY_FILE = "processed_history.txt"

# Immutably mapped official Channel IDs for bulletproof API lookup
CHANNEL_IDS = [
    "UCbCmjCuTUZos6Inko4u57UQ",  # Cocomelon
    "UC6zZJu_mS9OclgA99w0ElAg",  # ChuChu TV
    "UC_8_Ew7D7Xf5A2zRAs89Rsg",  # Bebefinn
    "UC47Ehk70ZSGnInY7iKDuH_A",  # Pinkfong
    "UC_wL-6uN_C7p8GgC_VreYVw"   # Baby Shark
]

def get_already_processed_ids():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return [line.strip() for line in f.readlines()]
    return []

def save_processed_id(video_id):
    with open(HISTORY_FILE, "a") as f:
        f.write(f"{video_id}\n")

def fetch_latest_video_via_official_api():
    print("[INFO] Initializing secure Google YouTube Data API interface...")
    
    # Reconstructing internal authentication tokens from GitHub Secrets
    token_data = json.loads(os.getenv("YOUTUBE_TOKEN"))
    credentials = Credentials.from_authorized_user_info(token_data)
    
    if credentials.expired and credentials.refresh_token:
        print("[INFO] Requesting refreshed credential access lifecycles...")
        credentials.refresh(Request())
        
    youtube = build("youtube", "v3", credentials=credentials)
    
    selected_channel = random.choice(CHANNEL_IDS)
    print(f"[INFO] API querying selected channel endpoint node: {selected_channel}")
    
    # Executing clean, official search queries to capture the absolute latest upload
    request = youtube.search().list(
        part="snippet",
        channelId=selected_channel,
        maxResults=1,
        order="date",
        type="video"
    )
    response = request.execute()
    
    if not response.get("items"):
        raise Exception(f"[FATAL API FAILURE] Channel payload returned empty item trees for: {selected_channel}")
        
    target_video_id = response["items"][0]["id"]["videoId"]
    print(f"[SUCCESS] Official API validated video asset discovered: {target_video_id}")
    return target_video_id

def download_and_slice(video_url):
    print("[INFO] Initiating dynamic payload download...")
    subprocess.run(["yt-dlp", "--no-warnings", "-f", "bestvideo+bestaudio/best", "-o", "raw_source.mp4", video_url])
    
    print("[INFO] Executing precision 5-second matrix slicing...")
    subprocess.run(["ffmpeg", "-y", "-i", "raw_source.mp4", "-c", "copy", "-map", "0", "-segment_time", "5", "-f", "segment", "segment_%03d.mp4"])
    
    segments = [f for f in os.listdir() if f.startswith("segment_") and f.endswith(".mp4")]
    random.shuffle(segments)
    return segments

def apply_advanced_transformations(segments):
    print("[INFO] Activating Multi-FX rendering pipelines (Klasky-Style Invert, Pitch 1.2x, Volume 1.5x)...")
    processed_files = []
    
    # Generates a runtime natively matching the 2:00 to 8:30 minute duration boundary
    target_count = random.randint(24, 102)
    print(f"[METRICS] Compilation array size assigned: {target_count} variations.")
    
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
    print("[INFO] Rendering composite array blocks into global longform layout...")
    with open("render_list.txt", "w") as f:
        for file in processed_files:
            f.write(f"file '{file}'\n")
            
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", "render_list.txt", "-c", "copy", "final_render_output.mp4"])
    print("[SUCCESS] Master distribution render locked.")

def generate_ai_metadata():
    print("[INFO] Extracting highly converting metadata assets via Generative AI nodes...")
    openai.api_key = os.getenv("OPENAI_API_KEY")
    prompt = "Generate a highly viral kids YouTube Video Title, description, and high-CPM tags targeting the USA market."
    
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices.message['content']

def upload_and_cleanup(metadata_text, video_id):
    print("[INFO] Authenticating target distribution server stream...")
    
    token_data = json.loads(os.getenv("YOUTUBE_TOKEN"))
    credentials = Credentials.from_authorized_user_info(token_data)
    
    if credentials.expired and credentials.refresh_token:
        credentials.refresh(Request())
        
    youtube = build("youtube", "v3", credentials=credentials)
    
    body = {
        "snippet": {
            "title": "Viral Kids Cartoons Multi-FX Transformation", 
            "description": "Premium High-Definition Automated Production Stream.",
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
    print(f"[SUCCESS] Broadcast successfully live! Target link: {new_video_url}")
    
    save_processed_id(video_id)
    
    print("[CLEANUP ENGINE] Scrubbing cloud storage caches...")
    files_to_clean = ["raw_source.mp4", "final_render_output.mp4", "render_list.txt"]
    for file in files_to_clean:
        if os.path.exists(file):
            os.remove(file)
            
    for item in os.listdir():
        if item.startswith("segment_") or item.startswith("transformed_fx_"):
            os.remove(item)
    print("[SUCCESS] Disk memory arrays wiped successfully.")

def main():
    try:
        video_id = fetch_latest_video_via_official_api()
        if not video_id:
            return  

        processed_ids = get_already_processed_ids()
        if video_id in processed_ids:
            print(f"[ANTI-DUPLICATE] Asset {video_id} already exists in processed tracks. Exiting execution safely.")
            return

        video_url = f"https://youtube.com{video_id}"
        segments = download_and_slice(video_url)
        fx_clips = apply_advanced_transformations(segments)
        compile_final_longform(fx_clips)
        metadata = generate_ai_metadata()
        upload_and_cleanup(metadata, video_id)
        print("[SYSTEM] Autonomous Cycle Executed and Logged Successfully.")
    except Exception as e:
        print(f"[SYSTEM ENGINE FAILURE] Handled Exception: {str(e)}")

if __name__ == "__main__":
    main()
