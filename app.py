"""
Hub Demo Addon - Stremio addon made to test the Addon Hub.

Upload this single file to a GitHub repository (e.g. demo_addon.py) and paste
its raw URL into the hub's /configure page:

    https://github.com/<user>/<repo>/blob/main/demo_addon.py

All video links are public demo MP4 files (no googlevideo).
"""

from flask import Flask, Response, jsonify

try:
    from Crypto.Cipher import AES

    HAVE_CRYPTO = True
except ImportError:
    HAVE_CRYPTO = False

app = Flask(__name__)

MOVIES = [
    {
        "id": "demohub.bigbuckbunny",
        "name": "Big Buck Bunny",
        "release": "2008",
        "description": "A big rabbit takes revenge on three bullying rodents. Blender Foundation's classic demo film.",
        "video": "https://archive.org/download/BigBuckBunny_124/Content/big_buck_bunny_720p_surround.mp4",
        "quality": "720p MP4 (archive.org)",
        "color": ("#8b5cf6", "#4c1d95"),
        "imdb": "tt1254207",
    },
    {
        "id": "demohub.elephantsdream",
        "name": "Elephants Dream",
        "release": "2006",
        "description": "Two strange characters explore a capricious and seemingly infinite machine. Blender's first open movie.",
        "video": "https://archive.org/download/ElephantsDream/ed_1024_512kb.mp4",
        "quality": "1024p MP4 (archive.org)",
        "color": ("#d946ef", "#701a75"),
        "imdb": "tt1858465",
    },
    {
        "id": "demohub.sintel",
        "name": "Sintel",
        "release": "2010",
        "description": "A lonely young woman searches for a dragon she once befriended. Blender's third open movie.",
        "video": "https://archive.org/download/Sintel/sintel-2048-surround.mp4",
        "quality": "2048p MP4 (archive.org)",
        "color": ("#f59e0b", "#7c2d12"),
        "imdb": "tt1727585",
    },
    {
        "id": "demohub.tearsofsteel",
        "name": "Tears of Steel",
        "release": "2012",
        "description": "A group of warriors and scientists gather to fight robots in future Amsterdam. Blender's fourth open movie.",
        "video": "https://download.blender.org/demo/movies/ToS/tears_of_steel_720p.mov",
        "quality": "720p MOV (blender.org)",
        "color": ("#38bdf8", "#0c4a6e"),
        "imdb": "tt2537216",
    },
]

FALLBACK_STREAMS = [
    {
        "title": "Demo Clip - Flower (MDN, small)",
        "url": "https://mdn.github.io/shared-assets/videos/flower.mp4",
    },
    {
        "title": "Demo Clip - Big Buck Bunny 10s (test-videos.co.uk)",
        "url": "https://test-videos.co.uk/vids/bigbuckbunny/mp4/h264/1080/Big_Buck_Bunny_1080_10s_5MB.mp4",
    },
    {
        "title": "Demo Clip - Big Buck Bunny short (W3Schools)",
        "url": "https://www.w3schools.com/html/mov_bbb.mp4",
    },
]


def _find_movie(movie_id):
    for movie in MOVIES:
        if movie["id"] == movie_id or movie["imdb"] == movie_id:
            return movie
    return None


def _poster_svg(movie):
    color1, color2 = movie["color"]
    title = movie["name"]
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="300" height="440" viewBox="0 0 300 440">
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{color1}"/>
      <stop offset="100%" stop-color="{color2}"/>
    </linearGradient>
  </defs>
  <rect width="300" height="440" rx="16" fill="url(#g)"/>
  <circle cx="150" cy="170" r="58" fill="rgba(255,255,255,0.14)"/>
  <polygon points="132,140 132,200 182,170" fill="#ffffff" opacity="0.9"/>
  <text x="150" y="300" text-anchor="middle" font-family="Arial, sans-serif" font-size="24" font-weight="bold" fill="#ffffff">{title}</text>
  <text x="150" y="332" text-anchor="middle" font-family="Arial, sans-serif" font-size="16" fill="rgba(255,255,255,0.75)">Hub Demo Addon</text>
</svg>"""


@app.route("/")
def landing():
    return Response(
        """<!doctype html><html><head><meta charset="utf-8"><title>Hub Demo Addon</title></head>
<body style="background:#0b0817;color:#eceaf6;font-family:sans-serif;text-align:center;padding:60px;">
<h1>&#129513; Hub Demo Addon</h1>
<p>This addon exists to test the <b>Stremio Addon Hub</b>.</p>
<p><a style="color:#c4b5fd;" href="manifest.json">manifest.json</a> &middot;
<a style="color:#c4b5fd;" href="catalog/movie/demo.json">catalog</a> &middot;
<a style="color:#c4b5fd;" href="health.json">health</a></p>
</body></html>""",
        mimetype="text/html",
    )


def _metahub_background(movie):
    return f"https://images.metahub.space/background/medium/{movie['imdb']}/img"


@app.route("/manifest.json")
def manifest():
    return jsonify({
        "id": "community.hubdemo",
        "version": "1.0.0",
        "name": "Hub Demo Addon",
        "description": "Demo addon with public test videos, made to validate the Stremio Addon Hub. Relative URLs (/logo.svg) are rewritten to absolute by the hub.",
        "logo": "/logo.svg",
        "background": "/poster/demohub.tearsofsteel.svg",
        "resources": ["catalog", "stream", "meta"],
        "types": ["movie"],
        "catalogs": [{
            "type": "movie",
            "id": "demo",
            "name": "Demo Movies",
            "extra": [],
        }],
        "contactEmail": "hubdemo@example.com",
    })


@app.route("/logo.svg")
def logo():
    svg = """<svg xmlns="http://www.w3.org/2000/svg" width="120" height="120" viewBox="0 0 120 120">
  <defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="#8b5cf6"/><stop offset="100%" stop-color="#d946ef"/>
  </linearGradient></defs>
  <rect width="120" height="120" rx="28" fill="url(#g)"/>
  <polygon points="48,38 48,82 86,60" fill="#ffffff" opacity="0.95"/>
</svg>"""
    return Response(svg, mimetype="image/svg+xml")


@app.route("/catalog/movie/demo.json")
def catalog():
    return jsonify({
        "metas": [
            {
                "id": movie["id"],
                "type": "movie",
                "name": movie["name"],
                "releaseInfo": movie["release"],
                "description": movie["description"],
                "poster": f"/poster/{movie['id']}.svg",
                "posterShape": "poster",
                "background": f"/poster/{movie['id']}.svg",
            }
            for movie in MOVIES
        ]
    })


@app.route("/meta/movie/<movie_id>.json")
def meta(movie_id):
    movie = _find_movie(movie_id)
    if not movie:
        return jsonify({"meta": None}), 404
    return jsonify({
        "meta": {
            "id": movie["id"],
            "type": "movie",
            "name": movie["name"],
            "releaseInfo": movie["release"],
            "description": movie["description"],
            "poster": f"/poster/{movie['id']}.svg",
            "background": f"/poster/{movie['id']}.svg",
            "imdb_id": movie["imdb"],
        }
    })


@app.route("/poster/<movie_id>.svg")
def poster(movie_id):
    movie = _find_movie(movie_id)
    if not movie:
        return Response("not found", mimetype="text/plain"), 404
    return Response(_poster_svg(movie), mimetype="image/svg+xml")


@app.route("/stream/movie/<movie_id>.json")
def streams(movie_id):
    result = []
    movie = _find_movie(movie_id)
    if movie:
        result.append({
            "title": f"{movie['name']} ({movie['release']}) - {movie['quality']}",
            "url": movie["video"],
        })
    result.extend(FALLBACK_STREAMS)
    return jsonify({"streams": result})


@app.route("/health.json")
def health():
    payload = {"status": "ok", "pycryptodome": {"installed": HAVE_CRYPTO}}
    if HAVE_CRYPTO:
        cipher = AES.new(b"0123456789abcdef", AES.MODE_ECB)
        encrypted = cipher.encrypt(b"hub demo addon..")
        payload["pycryptodome"]["aes_roundtrip"] = cipher.decrypt(encrypted).decode("ascii")
    return jsonify(payload)


if __name__ == "__main__":
    import os

    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "7000")), threaded=True)
