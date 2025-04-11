
from flask import Flask, request, Response
import random
import os

app = Flask(__name__)

gamer_types = [
    {
        "title": "FPS Freak",
        "desc": "Loves fast reflexes, shooters, and explosions.",
        "image": "/static/images/fps.jpg"
    },
    {
        "title": "MMO Grinder",
        "desc": "Strategic, loyal, and always leveling up.",
        "image": "/static/images/mmo.jpg"
    },
    {
        "title": "Stealth Assassin",
        "desc": "Patient, tactical, and lives in the shadows.",
        "image": "/static/images/stealth.jpg"
    }
]

@app.route('/', methods=['GET'])
def index():
    return Response("""<!DOCTYPE html>
<html lang='en'>
<head>
    <meta charset='UTF-8'>
    <meta name='viewport' content='width=device-width, initial-scale=1.0'>
    <meta property='og:title' content='What Kind of Gamer Are You?' />
    <meta property='og:description' content='Click to reveal your gamer type!' />
    <meta property='og:image' content='/static/images/cover.jpg' />
    <meta name='fc:frame' content='vNext' />
    <meta name='fc:frame:button:1' content='Reveal My Type' />
    <meta name='fc:frame:post_url' content='https://gamer-frame.onrender.com/reveal' />
    <link rel='stylesheet' href='/static/css/style.css'>
    <title>Gamer Frame</title>
</head>
<body>
    <div class='container'>
        <h1>🎮 What Kind of Gamer Are You?</h1>
        <img src='/static/images/cover.jpg' alt='Cover Image' class='cover-img'/>
        <form action='/reveal' method='post'>
            <button type='submit'>Reveal My Type</button>
        </form>
    </div>
</body>
</html>""", mimetype='text/html')

@app.route('/reveal', methods=['POST'])
def reveal():
    chosen = random.choice(gamer_types)
    return Response(f"""<!DOCTYPE html>
<html lang='en'>
<head>
    <meta charset='UTF-8'>
    <meta name='viewport' content='width=device-width, initial-scale=1.0'>
    <meta property='og:title' content='You're a {chosen["title"]}!' />
    <meta property='og:description' content='{chosen["desc"]}' />
    <meta property='og:image' content='{chosen["image"]}' />
    <meta name='fc:frame' content='vNext' />
    <meta name='fc:frame:button:1' content='Try Again' />
    <meta name='fc:frame:post_url' content='https://gamer-frame.onrender.com/reveal' />
    <link rel='stylesheet' href='/static/css/style.css'>
    <title>{chosen["title"]}</title>
</head>
<body>
    <div class='container'>
        <h1>You’re a <span>{chosen["title"]}</span>!</h1>
        <p>{chosen["desc"]}</p>
        <img src='{chosen["image"]}' alt='{chosen["title"]}' class='reveal-img'/>
        <form action='/reveal' method='post'>
            <button type='submit'>Try Again</button>
        </form>
    </div>
</body>
</html>""", mimetype='text/html')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
