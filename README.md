# Text-to-Transcribe

## **🔍 Code Overview: Video to Text Transcription Pipeline**

This Python script automates the process of **converting a video into text** using **CloudConvert** for file conversion and **OpenAI Whisper** for transcription. It follows a structured pipeline to:

1. **📤 Upload a video file to CloudConvert**
2. **🎬 Convert the video into an MP3 audio file**
3. **📦 Export the MP3 file and retrieve the download link**
4. **⬇️ Download the MP3 file locally**
5. **🎙️ Transcribe the audio using OpenAI Whisper**
6. **📝 Summarize the transcribed text using OpenAI GPT**
7. **✅ Display the final transcription and summary**

---

## **🚀 Step-by-Step Breakdown:**
### **1️⃣ Upload Video to CloudConvert**
- The script starts by **uploading a video file** to CloudConvert.
- It requests a **signed upload URL** and sends the video file to that URL.
- The API responds with a unique **file ID** for further processing.

### **2️⃣ Convert Video to MP3 Audio**
- The script **initiates a conversion job** using CloudConvert.
- It waits for the **job to complete** before proceeding.
- Once finished, the API provides a **converted task ID**.

### **3️⃣ Export & Download MP3 File**
- The script **creates an export task** to generate a downloadable URL for the MP3 file.
- It **retrieves the download link** from CloudConvert.
- The MP3 file is then **downloaded locally**.

### **4️⃣ Transcribe Audio with OpenAI Whisper**
- The downloaded MP3 file is sent to **OpenAI Whisper** for **speech-to-text transcription**.
- The API responds with a **full transcript** of the audio content.

### **5️⃣ Summarize the Transcription with OpenAI GPT**
- The transcribed text is sent to **OpenAI GPT** for summarization.
- The API returns a **short, concise summary** of the transcript.

### **6️⃣ Display the Final Output**
- The script **prints the full transcription** and the **generated summary**.
- The process completes successfully.

---

## **🔹 Features & Enhancements**
✅ **Automated Workflow:** Fully automated pipeline for video-to-text conversion.  
✅ **Error Handling:** Uses structured error handling (`handle_request_errors()`) to catch failures.  
✅ **Logging & Debugging:** Logs the status of each step, making it easier to debug.  
✅ **Environment Variables:** Securely loads API keys using `.env` (instead of hardcoding).  
✅ **Efficient API Requests:** Uses `time.sleep()` to avoid excessive API polling.  

---

## **🌟 Why This is Useful**
This script is useful for **content creators, journalists, researchers, and developers** who need to **extract text from video/audio** for:
- **Creating captions or subtitles**
- **Generating notes from lectures**
- **Summarizing meeting recordings**
- **Automating podcast transcriptions**

🚀 **With this tool, you can transcribe and summarize videos in just a few steps!** 🚀
