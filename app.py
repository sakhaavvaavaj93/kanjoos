from flask import Flask
import threading
import os

app = Flask(__name__)

@app.route('/')
def health_check():
    return "Kalyani Music Bot is actively running on Hugging Face!"

def run_web_server():
    # Hugging Face mandates running on 0.0.0.0 and port 7860
    app.run(host="0.0.0.0", port=7860)

if __name__ == "__main__":
    # Launch web framework asynchronously to prevent blocking the polling stream
    threading.Thread(target=run_web_server, daemon=True).start()
    
    # Execute the repository's internal main loop module launcher
    os.system("python3 -m modules")
