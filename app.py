import os
import json
import random
import subprocess
import openai
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

# Permanent transaction memory database log to ensure zero duplicated uploads
HISTORY_FILE = "processed_history.txt"

# Silicon Valley Identity Store: Verified Premium Sources verified by user
SOURCE_CHANNELS = [
    "https://youtube.com",
    "https://youtube.com",
    "https://youtube.com",
    "https://youtube.com",
    "https://youtube.com"
]

def get_already_processed_ids():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return [line.strip() for line in f.readlines()]
    return []

def save_processed_id(video_id):
    with open(HISTORY_FILE, "a") as f:
        f.write(f"{video_id}\n")

def fetch_latest_video_from_random_source():
    print("[INFO] Selecting a random target domain from premium child-entertainment logs...")
    selected_channel = random.choice(SOURCE_CHANNELS)
    print(f"[INFO] Operational scope assigned to source: {selected_channel}")
    
    # Executing localized extraction of the current trending metadata stream
    cmd = ["yt-dlp", "--playlist-items", "1", "--get-id", f"{selected_channel}/videos"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    video_id = result.stdout.strip()
    
    if not video_id:
        raise Exception(f"[FATAL ERROR] API/Scraper communication failure on: {selected_channel}")
        
    # Memory Interception: Block already rendered assets
    processed_ids = get_already_processed_ids()
    if video_id in processed_ids:
        print(f"[MEMORY SUPPRESSION] Asset ID {video_id} found in history. Execution halted to protect channel authority.")
        return None

    return video_id

def download_and_slice(video_url):
    print("[INFO] Executing high-bandwidth packet ingestion from source nodes...")
    subprocess.run(["yt-dlp", "-f", "bestvideo+bestaudio/best", "-o", "raw_source.mp4", video_url])
    
    print("[INFO] Slicing source stream into isolated 5-second sub-buffers...")
    subprocess.run(["ffmpeg", "-i", "raw_source.mp4", "-c", "copy", "-map", "0", "-segment_time", "5", "-f", "segment", "segment_%03d.mp4"])
    
    segments = [f for f in os.listdir() if f.startswith("segment_") and f.endswith(".mp4")]
    random.shuffle(segments)
    return segments

def apply_advanced_transformations(segments):
    print("[INFO] Processing audio-visual parameters (Klasky-Invert Matrix, 1.2x Pitch Matrix, 1.5x Volume Gain)...")
    processed_files = []
    
    # Silicon Valley Duration Engine: Configured specifically for 2:00 to 8:30 min variations
    # 24 clips minimum * 5s = 120s (2 mins) | 102 clips maximum * 5s = 510s (8.5 mins)
    target_count = random.randint(24, 102)
    print(f"[METRIC ENGINE] Target array length assigned: {target_count} clip structures.")
    
    for i, clip in enumerate(segments[:target_count]):
        output_clip = f"transformed_fx_{i}.mp4"
        ffmpeg_cmd = [
            "ffmpeg", "-i", clip,
            "-vf", "lutrgb=r=negate:g=negate:b=negate,scale=1920:1080", 
            "-af", "asetrate=44100*1.2,atempo=1.0,volume=1.5",
            "-c:v", "libx264", "-c:a", "aac", output_clip
        ]
        subprocess.run(ffmpeg_cmd)
        processed_files.append(output_clip)
        
    return processed_files

def compile_final_longform(processed_files):
    print("[INFO] Packaging isolated elements into unified master broadcast matrix...")
    with open("render_list.txt", "w") as f:
        for file in processed_files:
            f.write(f"file '{file}'\n")
            
    subprocess.run(["ffmpeg", "-f", "concat", "-safe", "0", "-i", "render_list.txt", "-c", "copy", "final_render_output.mp4"])
    print("[SUCCESS] Production pipeline render completed.")

def generate_ai_metadata():
    print("[INFO] Querying Generative AI for high-CPM USA metadata generation optimization...")
    openai.api_key = os.getenv("OPENAI_API_KEY")
    prompt = "Act as an expert YouTube SEO manager. Generate one highly clickable viral Title, a detailed Description filled with trending high-CPM tags for a premium USA kids visual edit video."
    
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices.message['content']

def upload_and_cleanup(metadata_text, video_id):
    print("[INFO] Establishing OAuth2 authenticated channel interface protocol...")
    
    client_secret_data = json.loads(os.getenv("YOUTUBE_API_SECRET"))
    token_data = json.loads(os.getenv("YOUTUBE_TOKEN"))
    
    credentials = Credentials.from_authorized_user_info(token_data)
    
    if credentials.expired and credentials.refresh_token:
        print("[INFO] Credential token lifecycle expired. Refresh protocol initiated...")
        credentials.refresh(Request())
        
    youtube = build("youtube", "v3", credentials=credentials)
    
    body = {
        "snippet": {
            "title": "Viral Kids Cartoons Multi-FX Transformation", 
            "description": "Automated Content Pipeline Optimization - Premium Production Matrix.",
            "tags": ["cartoons", "kids", "animation", "viral"],
            "categoryId": "1" # Film & Animation Scope
        },
        "status": {
            "privacyStatus": "public" # Directly pushes to live feed
        }
    }
    
    media = MediaFileUpload("final_render_output.mp4", chunksize=-1, resumable=True)
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
    
    response = request.execute()
    new_video_url = f"https://www.youtube.com/watch?v={response.get('id')}"
    print(f"[SUCCESS] Transmission completed. Target link live: {new_video_url}")
    
    # Save target signature into history data array before clean loop execution
    save_processed_id(video_id)
    
    print("[CLEANUP ENGINE] Finalizing disk storage scrub protocol. Erasing active cache memory...")
    files_to_clean = ["raw_source.mp4", "final_render_output.mp4", "render_list.txt"]
    for file in files_to_clean:
        if os.path.exists(file):
            os.remove(file)
            
    # Purge all remaining segment files immediately
    for item in os.listdir():
        if item.startswith("segment_") or item.startswith("transformed_fx_"):
            os.remove(item)
    print("[SUCCESS] Hardware workspace memory cleared and structurally optimized.")

def main():
    try:
        video_id = fetch_latest_video_from_random_source()
        if video_id is None:
            return  # Clean termination if duplicate is detected by memory filter

        video_url = f"https://www.youtube.com/watch?v={video_id}"
        segments = download_and_slice(video_url)
        fx_clips = apply_advanced_transformations(segments)
        compile_final_longform(fx_clips)
        metadata = generate_ai_metadata()
        upload_and_cleanup(metadata, video_id)
        print("[SYSTEM] Pipeline cycle completed successfully.")
    except Exception as e:
        print(f"[PROTECTED FAULT] Error trace handled: {str(e)}")

if __name__ == "__main__":
    main()
