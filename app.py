from flask import Flask, render_template, request
from generator import generate_video

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    video_path = None

    if request.method == "POST":
        prompt = request.form["prompt"]
        video_path = generate_video(prompt)

    return render_template("index.html", video_path=video_path)

if __name__ == "__main__":
    app.run(debug=True, port=5001)