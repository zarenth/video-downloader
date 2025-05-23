from flask import Flask, request, jsonify
from yt_dlp import YoutubeDL
import traceback

app = Flask(__name__)

YDL_OPTIONS = {
    'quiet': True,
    'skip_download': True,
    'nocheckcertificate': True,
    'ignoreerrors': True,
}

@app.route("/info", methods=["GET"])
def get_video_info():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "Missing 'url' parameter"}), 400

    try:
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)

        if not info:
            return jsonify({"error": "Failed to extract info"}), 500

        audio_video_formats = [
            {
                "format_id": f.get("format_id"),
                "ext": f.get("ext"),
                "format_note": f.get("format_note"),
                "filesize": f.get("filesize"),
                "url": f.get("url"),
                "acodec": f.get("acodec"),
                "vcodec": f.get("vcodec")
            }
            for f in info.get("formats", [])
            if f.get("vcodec") != "none" or f.get("acodec") != "none"
        ]

        return jsonify({
            "title": info.get("title"),
            "thumbnail": info.get("thumbnail"),
            "formats": audio_video_formats
        })

    except Exception as e:
        return jsonify({"error": str(e), "trace": traceback.format_exc()}), 500

if __name__ == "__main__":
    app.run(debug=True)
