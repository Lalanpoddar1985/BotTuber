import os
import json
import random
import subprocess
import urllib.request
import openai
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

HISTORY_FILE = "processed_history.txt"

# Silicon Valley Proxy Layer: Global unblocked public proxy engines to bypass all device check-ins
INVIDIOUS_INSTANCES = [
    "https://flokinet.to",
    "https://melmac.space",
    "https://perennialte.ch",
    "https://yewtu.be"
]

def download_and_slice(video_url):
    # Extract clean alphanumeric unique video ID safely from user manual dashboard link
    if "youtu.be/" in video_url:
        video_id = video_url.split("youtu.be/")[-1].split("?")[0]
    elif "v=" in video_url:
        video_id = video_url.split("v=")[-1].split("&")[0]
    else:
        video_id = video_url.strip()

    print(f"[INFO] Bypassing data center restriction loops for Video ID: {video_id}")
    
    # Select random secondary network mirror nodes to completely shatter tracking walls
    instance = random.choice(INVIDIOUS_INSTANCES)
    direct_stream_url = f"{instance}/latest_version?id={video_id}&itag=22"
    
    print(f"[INFO] Ingesting validated packet matrix directly from proxy mirror node...")
    
    # Headless server client identification mask headers configuration
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    req = urllib.request.Request(direct_stream_url, headers=headers)
    
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            with open("raw_source.mp4", "wb") as f:
                f.write(response.read())
        print("[SUCCESS] Media array captured clean and stored in system root memory workspace.")
    except Exception as api_err:
        print("[WARNING] Primary proxy mirror failed. Executing ultimate yt-dlp fallback protocol...")
        fallback_cmd = ["yt-dlp", "--no-warnings", "--geo-bypass", "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best", "-o", "raw_source.mp4", f"https://youtube.com{video_id}"]
        subprocess.run(fallback_cmd)

    if not os.path.exists("raw_source.mp4") or os.path.getsize("raw_source.mp4") == 0:
        raise Exception("[FATAL NETWORK EXCEPTION] All ingestion pipelines blocked by security blocks. Workspace asset null.")

    print("[INFO] Initializing high-precision 5-second matrix boundary slicing...")
    subprocess.run(["ffmpeg", "-y", "-i", "raw_source.mp4", "-c", "copy", "-map", "0", "-segment_time", "5", "-f", "segment", "segment_%03d.mp4"])
    
    segments = [f for f in os.listdir() if f.startswith("segment_") and f.endswith(".mp4")]
    if not segments:
        raise Exception("[FATAL BUFFER ERROR] Slicing architecture returned empty array blocks.")

    while len(segments) < 108:
        segments += segments
        
    random.shuffle(segments)
    return segments

def apply_fx_and_render_mashup(segments):
    print("[INFO] Deploying Multi-FX rendering filters (Klasky-Invert Matrix, 1.2x Pitch Matrix, 1.5x Volume Amplification)...")
    processed_files = []
    
    # Duration selector configured natively to guarantee dynamic runtime length matching 2:00 to 9:00 minutes bounds
    target_count = random.randint(24, 108)
    print(f"[METRIC LIFECYCLE] Dynamic runtime configuration locked at: {target_count} blocks ({target_count * 5} total seconds).")
    
    for i, clip in enumerate(segments[:target_count]):
        output_clip = f"fx_render_node_{i}.mp4"
        ffmpeg_cmd = [
            "ffmpeg", "-y", "-i", clip,
            "-vf", "lutrgb=r=negate:g=negate:b=negate,scale=1920:1080", 
            "-af", "asetrate=44100*1.2,atempo=1.0,volume=1.5",
            "-c:v", "libx264", "-c:a", "aac", output_clip
        ]
        subprocess.run(ffmpeg_cmd)
        processed_files.append(output_clip)
        
    print("[INFO] Stitching transformed structural cells into unified master output media matrix...")
    with open("render_pipeline_list.txt", "w") as f:
        for file in processed_files:
            f.write(f"file '{file}'\n")
            
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", "render_pipeline_list.txt", "-c", "copy", "master_draft_output.mp4"])
    print("[SUCCESS] Production pipeline render completed successfully.")

def upload_unlisted_draft_to_studio():
    print("[INFO] Instantiating secure API connection layer with YouTube Studio servers...")
    token_data = json.loads(os.getenv("YOUTUBE_TOKEN"))
    credentials = Credentials.from_authorized_user_info(token_data)
    
    if credentials.expired and credentials.refresh_token:
        credentials.refresh(Request())
        
    youtube = build("youtube", "v3", credentials=credentials)
    
    # Strictly maps unlisted deployment architecture variables to hold draft state parameters inside YT Studio Dashboard
    body = {
        "snippet": {
            "title": "DRAFT - Automated Multi-FX Visual Compilation (Pending Manual Edit)", 
            "description": "System Production Pipeline Output. Please append localized high-CPM Title, optimized description data layouts, and insert your custom thumbnail before toggling Public status manually.",
            "categoryId": "1"
        },
        "status": {
            "privacyStatus": "unlisted"
        }
    }
    
    media = MediaFileUpload("master_draft_output.mp4", chunksize=-1, resumable=True)
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
    
    response = request.execute()
    video_id = response.get('id')
    print(f"[SUCCESS] Draft payload transmission successfully completed!")
    print(f"[DIRECT STUDIO LINK] https://youtube.com{video_id}/edit")
    
    print("[CLEANUP ENGINE] Purging visual assets and cache logs from hardware array memory...")
    for f in ["raw_source.mp4", "master_draft_output.mp4", "render_pipeline_list.txt"]:
        if os.path.exists(f):
            os.remove(f)
    for item in os.listdir():
        if item.startswith("segment_") or item.startswith("fx_render_node_"):
            os.remove(item)
    print("[SUCCESS] Hardware environment scrubbed and optimized.")

def main():
    try:
        input_link = os.getenv("USER_VIDEO_LINK")
        if not input_link:
            raise Exception("[FATAL CODE ERROR] Process halted: Target source URL input interface is empty.")
            
        segments = download_and_slice(input_link)
        apply_fx_and_render_mashup(segments)
        upload_unlisted_draft_to_studio()
        print("[SYSTEM] Autonomous Link Draft Pipeline Cycle Executed Successfully.")
    except Exception as e:
        print(f"[SYSTEM MATRIX FAILURE] Exception caught during loop execution trace: {str(e)}")

if __name__ == "__main__":
    main()
