import requests
import time
import os

CLOUDCONVERT_API_KEY = ""
OPENAI_API_KEY = ""
VIDEO_PATH = "./07. Checkout Page Sign-Ups.mp4"
AUDIO_PATH = "audio.mp3"
CLOUDCONVERT_URL = "https://api.cloudconvert.com/v2"
OPENAI_URL = "https://api.openai.com/v1"

def upload_to_cloudconvert(video_path):
    """Uploads the video to CloudConvert and returns the file ID."""
    print(f"\n[Uploading File] Video Path: {video_path}")

    url = f"{CLOUDCONVERT_URL}/import/upload"
    headers = {"Authorization": f"Bearer {CLOUDCONVERT_API_KEY}"}

    response = requests.post(url, json={"filename": os.path.basename(video_path)}, headers=headers)
    response.raise_for_status()

    upload_data = response.json()["data"]
    print(f"[Debug] API Response: {upload_data}")

    upload_url = upload_data["result"]["form"]["url"]
    parameters = upload_data["result"]["form"]["parameters"]

    print(f"[Signed URL Received] Upload URL: {upload_url}")

    with open(video_path, "rb") as file:
        files = {"file": file}
        upload_response = requests.post(upload_url, files=files, data=parameters)

    upload_response.raise_for_status()
    print(f"[Upload Successful] File ID: {upload_data['id']}")

    return upload_data["id"]

def check_file_status(file_id):
    """Checks the status of the uploaded file."""
    url = f"{CLOUDCONVERT_URL}/tasks/{file_id}"
    headers = {"Authorization": f"Bearer {CLOUDCONVERT_API_KEY}"}

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    job_data = response.json()
    print(f"\n[File Status] File ID: {file_id}")
    print(f"Status: {job_data['data']['status']}")

def start_conversion(file_id, output_format="mp3"):
    """Starts a CloudConvert job to convert the file."""
    url = f"{CLOUDCONVERT_URL}/jobs"

    headers = {"Authorization": f"Bearer {CLOUDCONVERT_API_KEY}", "Content-Type": "application/json"}

    data = {
        "tasks": {
            "convert": {
                "operation": "convert",
                "input": [file_id],  # ✅ FIXED: input should be a list
                "output_format": output_format
            }
        }
    }

    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()

    job_data = response.json()["data"]
    job_id = job_data["id"]
    print(f"[Conversion Job Created] Job ID: {job_id}")

    return job_id

def get_job_status(job_id):
    """Checks the status of the conversion job."""
    url = f"{CLOUDCONVERT_URL}/jobs/{job_id}"

    headers = {"Authorization": f"Bearer {CLOUDCONVERT_API_KEY}"}

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    return response.json()["data"]

def create_export_task(file_id):
    """Creates an export task to generate a downloadable URL."""
    url = f"{CLOUDCONVERT_URL}/jobs"

    headers = {"Authorization": f"Bearer {CLOUDCONVERT_API_KEY}", "Content-Type": "application/json"}

    data = {
        "tasks": {
            "export": {
                "operation": "export/url",
                "input": [file_id]  # ✅ FIXED: input should be a list
            }
        }
    }

    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()

    job_data = response.json()["data"]
    job_id = job_data["id"]
    print(f"\n✅ [Export Job Created] Job ID: {job_id}")

    return job_id

def get_export_download_url(job_id):
    """Finds the export task and extracts the download URL."""
    url = f"{CLOUDCONVERT_URL}/jobs/{job_id}"
    headers = {"Authorization": f"Bearer {CLOUDCONVERT_API_KEY}"}

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    job_data = response.json()["data"]

    for task in job_data["tasks"]:
        if task["operation"] == "export/url" and task["status"] == "finished":
            download_url = task["result"]["files"][0]["url"]
            print(f"\n✅ [Download Ready] MP3 File URL: {download_url}")
            return download_url

    print("[❌] Export task not finished yet. Please wait and try again.")
    return None

def download_audio(audio_url, output_path="audio.mp3"):
    """Downloads the converted MP3 file from CloudConvert."""
    print(f"\n⬇️ [Downloading] {output_path} from URL...")

    response = requests.get(audio_url)
    response.raise_for_status()

    with open(output_path, "wb") as file:
        file.write(response.content)

    print(f"✅ [Download Complete] File saved as: {output_path}")
    return output_path

def transcribe_audio(audio_path):
    print(audio_path)
    """Sends the audio file to OpenAI Whisper for transcription."""
    print(f"\n🎙️ [Transcribing Audio] File: {audio_path}")

    url = f"{OPENAI_URL}/audio/transcriptions"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }
    
    with open(audio_path, "rb") as audio_file:
        files = {"file": audio_file, "model": (None, "whisper-1")}
        response = requests.post(url, headers=headers, files=files)

    response.raise_for_status()
    
    transcript = response.json()["text"]
    print(f"✅ [Transcription Complete] Text: {transcript}...")  # Show first 100 chars

    return transcript

def summarize_text(text):
    """Sends the extracted text to OpenAI GPT for summarization."""
    print(f"\n📖 [Summarizing Text] Length: {len(text)} characters")

    url = f"{OPENAI_URL}/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-4",
        "messages": [
            {"role": "system", "content": "Summarize this transcript:"},
            {"role": "user", "content": text}
        ]
    }

    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()

    summary = response.json()["choices"][0]["message"]["content"]
    print(f"✅ [Summarization Complete] Summary: {summary}..")  # Show first 100 chars

    return summary


if __name__ == "__main__":
    print("\n================ STARTING PROCESS =================")

    file_id = upload_to_cloudconvert(VIDEO_PATH)
    print(f"[File Uploaded] File ID: {file_id}")
    
    job_id = start_conversion(file_id, "mp3")

    if job_id:
        print(f"\n[Job Created Successfully] Job ID: {job_id}")
    else:
        print("\n[Failed] Could not start conversion.")

    time.sleep(10)  

    job_data = get_job_status(job_id)

    converted_task_id = None
    for task in job_data["tasks"]:
        if task["operation"] == "convert" and task["status"] == "finished":
            converted_task_id = task["id"]
            break

    if not converted_task_id:
        print("[❌] No finished conversion task found. Exiting export process.")
        exit(1)  
        
    export_job_id = create_export_task(converted_task_id)
    audio_url = get_export_download_url(export_job_id)  
    audio_path = download_audio(audio_url)
    transcript = transcribe_audio(audio_path)
    summary = summarize_text(transcript)
    print("\n================ FINAL OUTPUT =================")
    print("\n🔊 **Transcription:**\n", transcript)
    print("\n📝 **Summary:**\n", summary)


    print("\n================ PROCESS COMPLETE =================")

