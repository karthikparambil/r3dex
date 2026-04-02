from flask import Flask, render_template, request, jsonify, redirect, url_for
import json
import os
from datetime import datetime

app = Flask(__name__)

# In-memory data (Core requirement: No database)
CHALLENGES = {#--------machines--------#
    "Omni": {"flag": "r3dx{omni_user_flag}", "root_flag": "r3dx{omni_root_flag}", "is_machine": True},
    "Spectre": {"flag": "r3dx{spectre_user_flag}", "root_flag": "r3dx{spectre_root_flag}", "is_machine": True},
    "Skulllock": {"flag": "r3dx{midnight_walk}", "is_machine": False},#--------challenges-------#
    "phantomfest": {"flag": "r3dx{crypt_k33p3r}", "is_machine": False},
    "secret note": {"flag": "r3dx{j4ck_sk3ll1ngt0n_l0v3s_h4ll0w33n}", "is_machine": False},
    "ghost mansion": {"flag": "r3dx{h4un73d_m4ns10n_gh0s7_m4s73r}", "is_machine": False},
}

CREATORS = [
    {
        "username": "r3dex",
        "name": "Karthik",
        "profile_link": "https://github.com/karthikparambil",
        "bio": "Pentester, CTF Enthusiast and Developer.",
        "challenges": ["skulllock", "secret note", "phantomfest", "ghost mansion"]
    },
    {
        "username": "mxshub",
        "name": "Mushab",
        "profile_link": "https://github.com/MuhammadMushab",
        "bio": "Security researcher and creator of crypto challenges.",
        "challenges": ["Cloud-Break", "Kernel-Panic"]
    }
]

SUBMISSIONS_FILE = 'submissions.json'

def save_submission(data):
    submissions = []
    if os.path.exists(SUBMISSIONS_FILE):
        with open(SUBMISSIONS_FILE, 'r') as f:
            try:
                submissions = json.load(f)
            except json.JSONDecodeError:
                submissions = []
    
    data['timestamp'] = datetime.now().isoformat()
    submissions.append(data)
    
    with open(SUBMISSIONS_FILE, 'w') as f:
        json.dump(submissions, f, indent=4)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contribute')
def contribute():
    return render_template('contribute.html', creators=CREATORS)

@app.route('/contribute/submit')
def submit_page():
    return render_template('submit.html')

@app.route('/api/validate-flag', methods=['POST'])
def validate_flag():
    data = request.json
    name = data.get('name')
    flag = data.get('flag')
    is_root = data.get('is_root', False)
    
    challenge = CHALLENGES.get(name)
    if not challenge:
        return jsonify({"success": False, "message": "Challenge not found"}), 404
    
    correct_flag = challenge.get('root_flag') if is_root else challenge.get('flag')
    if flag == correct_flag:
        return jsonify({"success": True, "message": "Correct flag!"})
    else:
        return jsonify({"success": False, "message": "Incorrect flag."})

@app.route('/api/submit', methods=['POST'])
def submit_content():
    data = request.json
    save_submission(data)
    return jsonify({"success": True, "message": "Submission received!"})

if __name__ == '__main__':
    app.run(debug=True, port=5001)
