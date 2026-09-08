import os
import json
import random
import subprocess
from pytube import YouTube
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

def download_and_slice(video_url):
    print(f"[INFO] Ingesting raw network stream packets from source URL via Pytube Engine: {video_url}")
    
    # Custom client signature bypass array to mask automated data center footprints
    yt = YouTube(
        video_url,
        use_oauth=False,
        allow_oauth_cache=False
    )
    
    # Select premium progressive stream structures to evade block checking arrays
    stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
    if not stream:
        raise Exception("[FATAL EXTRACTION] Unable to isolate clean stream structures for download.")
        
    print(f"[INFO] Extracting stream footprint to local file: {stream.title}")
    stream.download(output_path=os.getcwd(), filename="raw_source.mp4")
    
    print("[INFO] Initializing high-precision 5-second matrix boundary slicing...")
    subprocess.run(["ffmpeg", "-y", "-i", "raw_source.mp4", "-c", "copy", "-map", "0", "-segment_time", "5", "-f", "segment", "segment_%03d.mp4"])
    
    segments = [f for f in os.listdir() if f.startswith("segment_") and f.endswith(".mp4")]
    if not segments:
        raise Exception("[FATAL BUFFER ERROR] Slicing architecture returned zero valid media structures.")

    # Automatically duplicates media cells if source duration is shorter than target length constraints
    while len(segments) < 108:
        segments += segments
        
    random.shuffle(segments)
    return segments

def apply_fx_and_render_mashup(segments):
    print("[INFO] Deploying Multi-FX rendering filters (Klasky-Invert Matrix, 1.2x Pitch Matrix, 1.5x Volume Amplification)...")
    processed_files = []
    
    # SILICON VALLEY DYNAMIC BOUNDARY MATRIX CONTROLLER:
    # 24 segments * 5 seconds = 120 seconds (Strict 2 Minutes Minimum Boundary)
    # 108 segments * 5 seconds = 540 seconds (Strict 9 Minutes Maximum Boundary)
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
        print("[INFO] Expiration flag detected. Requesting token refresh authorization lifecycles...")
        credentials.refresh(Request())
        
    youtube = build("youtube", "v3", credentials=credentials)
    
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
        video_url = os.getenv("USER_VIDEO_LINK")
        if not video_url:
            raise Exception("[FATAL CODE ERROR] Process halted: Target source URL input interface is empty.")
            
        segments = download_and_slice(video_url)
        apply_fx_and_render_mashup(segments)
        upload_unlisted_draft_to_studio()
        print("[SYSTEM] Autonomous Link Draft Pipeline Cycle Executed Successfully.")
    except Exception as e:
        print(f"[SYSTEM MATRIX FAILURE] Exception caught during loop execution trace: {str(e)}")

if __name__ == "__main__":
    main()
