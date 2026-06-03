# ==========================================
# 2. PYTHON BACKEND FLASK FLUSH ARCHITECTURE
# ==========================================

import os
import time
import threading
import requests
import io
from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from gtts import gTTS

app = Flask(__name__)
CORS(app)  # Cross-Origin resource sharing restriction bypass setup for GitHub Pages

# ⚠️ APNA RENDER WEB SERVICE KA POORA URL DEPLOYMENT KE BAAD YAHAN ENGINE MEIN UPDATE KAREIN
RENDER_APP_URL = "https://audio-tspd.onrender.com"

# Render Server Anti-Sleep Mechanism Framework
def self_ping():
    time.sleep(30)  # Server initial up execution buffer time window delay
    while True:
        try:
            requests.get(RENDER_APP_URL)
            print("[System Bot] Self-ping delivery verified. Server system is kept awake.")
        except Exception as e:
            print(f"[System Bot] Ping failed safely: {e}")
        time.sleep(600)  # Exact 10 minutes = 600 seconds loop delay intervals

@app.route('/ping', methods=['GET'])
def ping():
    return "Render automation system status: Fully operational and active.", 200

@app.route('/generate-audio', methods=['POST'])
def generate_audio():
    try:
        data = request.get_json()
        text_to_speak = data.get('text', '')
        
        if not text_to_speak:
            return jsonify({"error": "Null character stream error: No text payload received by backend API."}), 400
            
        # Hard drive space optimization: Directly write and read audio buffer stream logs from device RAM storage memory cells
        mp3_fp = io.BytesIO()
        tts = gTTS(text=text_to_speak, lang='en', slow=False) 
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)
        
        return send_file(mp3_fp, mimetype="audio/mp3")
        
    except Exception as e:
        print(f"[Backend Core Error Log]: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Separate threading daemon task registration loops running concurrently
    threading.Thread(target=self_ping, daemon=True).start()
    
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
