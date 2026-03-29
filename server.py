from flask import Flask, request, jsonify
from flask_cors import CORS
from agent import run_agent
import json
import os

app = Flask(__name__)
CORS(app)
# @app.route("/")
# def home():
#     return "Auto Agent Backend is Running 🚀"

@app.route("/run", methods=["POST"])
def run():
    data = request.json
    task = data.get("task")

    result = run_agent(task)
    return jsonify(result)

@app.route("/logs", methods=["GET"])
def logs():
    try:
        with open("agent_log.json", "r") as f:
            return jsonify(json.load(f))
    except:
        return jsonify({"logs": "No logs yet"})

if __name__ == "__main__":
    app.run(port=5000)
    #app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))