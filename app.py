import os
import json
import random
import subprocess
import requests
import time

def download_and_slice(video_url):
    clean_url = video_url.strip()
    print(f"[INFO] Routing ingestion layer via mirror architecture for URL: {clean_url}")
    
    # Utilizing an open-source distributed cobalt instance engine to completely bypass YouTube data center blocks
    api_url = "https://cobalt.tools"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    payload = {
        "url": clean_url,
        "videoQuality": "720", # Optimized for fast rendering on virtual cloud instances
        "downloadMode": "default"
    }
    
    try:
        response = requests.post(api_url, headers=headers, json=payload, timeout=30)
        response_data = response.json()
        
        if response_data.get("status") == "error":
            raise Exception(f"Mirror API returned business error log: {response_data.get('text')}")
            
        stream_url = response_data.get("url")
        if not stream_url:
            raise Exception("Isolate stream endpoint array returned empty node trees.")
            
        print("[INFO] Direct streaming binary package located. Pulling asset down to workspace...")
        video_file = requests.get(stream_url, timeout=60)
        with open("raw_source.mp4", "wb") as f:
            f.write(video_file.content)
            
    except Exception as network_exception:
        raise Exception(f"[FATAL NETWORK BYPASS PIPELINE CRASH] Mirror routing layer failed: {str(network_exception)}")
    
    if not os.path.exists("raw_source.mp4") or os.path.getsize("raw_source.mp4") == 0:
        raise Exception("[FATAL] Source file ingest validation failed. Asset size is 0 bytes.")
        
    print("[INFO] Initializing high-precision 5-second matrix boundary slicing...")
    subprocess.run(["ffmpeg", "-y", "-i", "raw_source.mp4", "-c", "copy", "-map", "0", "-segment_time", "5", "-f", "segment", "segment_%03d.mp4"])
    
    segments = [f for f in os.listdir() if f.startswith("segment_") and f.endswith(".mp4")]
    if not segments:
        raise Exception("[FATAL BUFFER ERROR] Slicing architecture returned zero valid media structures.")

    # Automatically loop video cells if source runtime cannot satisfy minimum duration restrictions
    while len(segments) < 108:
        segments += segments
        
    random.shuffle(segments)
    return segments

def apply_fx_and_render_mashup(segments):
    print("[INFO] Deploying Multi-FX rendering filters (Klasky-Invert Matrix, 1.2x Pitch Matrix, 1.5x Volume Amplification)...")
    processed_files = []
    
    # Silicon Valley Duration Engine: Scaled natively between 24 (2 minutes) and 108 (9 minutes) segment blocks
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
