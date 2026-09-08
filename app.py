import os
import json
import random
import subprocess
import urllib.request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

def download_and_slice(video_url):
    clean_url = video_url.strip().replace(" ", "")
    print(f"[INFO] Initializing robust hybrid ingestion layer for URL: {clean_url}")
    
    # Silicon Valley Layer 1: Simulated high-end edge client headers
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
    ]
    chosen_agent = random.choice(user_agents)
    
    # Layer 2: Execute direct authenticated stream capture using strict browser network masks
    download_cmd = [
        "yt-dlp",
        "--no-warnings",
        "--geo-bypass",
        "--user-agent", chosen_agent,
        "--referer", "https://google.com",
        "--extractor-args", "youtube:player_client=android,web",
        "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        "-o", "raw_source.mp4",
        clean_url
    ]
    
    print("[INFO] Executing primary ingestion workflow loop...")
    subprocess.run(download_cmd)
    
    # Layer 3: Ultimate Invidious Proxy Network Fallback Strategy
    if not os.path.exists("raw_source.mp4") or os.path.getsize("raw_source.mp4") == 0:
        print("[WARNING] Primary extraction intercepted by security gate. Routing via proxy network nodes...")
        
        if "youtu.be/" in clean_url:
            v_id = clean_url.split("youtu.be/")[-1].split("?")[0]
        elif "v=" in clean_url:
            v_id = clean_url.split("v=")[-1].split("&")[0]
        else:
            v_id = clean_url
            
        proxy_url = f"https://perennialte.ch{v_id}&itag=22"
        try:
            req = urllib.request.Request(proxy_url, headers={'User-Agent': chosen_agent})
            with urllib.request.urlopen(req, timeout=30) as response:
                with open("raw_source.mp4", "wb") as f:
                    f.write(response.read())
            print("[SUCCESS] Media array captured clean via proxy bypass channel.")
        except Exception as proxy_err:
            print(f"[ERROR] Proxy node returned validation error: {str(proxy_err)}")

    if not os.path.exists("raw_source.mp4") or os.path.getsize("raw_source.mp4") == 0:
        raise Exception("[FATAL NETWORK EXCEPTION] All ingestion pipelines blocked by security blocks. Workspace asset null.")
        
    print("[INFO] Initializing high-precision 5-second matrix boundary slicing...")
    subprocess.run(["ffmpeg", "-y", "-i", "raw_source.mp4", "-c", "copy", "-map", "0", "-segment_time", "5", "-f", "segment", "segment_%03d.mp4"])
    
    segments = [f for f in os.listdir() if f.startswith("segment_") and f.endswith(".mp4")]
    if not segments:
        raise Exception("[FATAL BUFFER ERROR] Slicing architecture returned zero valid media structures.")

    while len(segments) < 108:
        segments += segments
        
    random.shuffle(segments)
    return segments

def apply_fx_and_render_mashup(segments):
    print("[INFO] Deploying Multi-FX rendering filters (Klasky-Invert Matrix, 1.2x Pitch Matrix, 1.5x Volume Amplification)...")
    processed_files = []
    
    # Dynamically scales video duration bounds natively between 2:00 and 9:00 minutes
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
        subprocess.run(ffmpeg_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
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
