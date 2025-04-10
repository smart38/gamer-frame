from flask import Flask, request, Response
import random

app = Flask(__name__)

gamer_types = [
    {
        "title": "FPS Freak",
        "desc": "Loves fast reflexes, shooters, and explosions.",
        "image": "https://yourdomain.com/images/fps.jpg"
    },
    {
        "title": "MMO Grinder",
        "desc": "Strategic, loyal, and always leveling up.",
        "image": "https://yourdomain.com/images/mmo.jpg"
    },
    # ... add more
]

@app.route('/', methods=['GET'])
def index():
    return Response(f'''
    <meta property="og:title" content="What Kind of Gamer Are You?" />
    <meta property="og:description" content="Click to reveal your gamer type!" />
    <meta property="og:image" content="https://yourdomain.com/images/cover.jpg" />
    <meta name="fc:frame" content="vNext" />
    <meta name="fc:frame:button:1" content="Reveal My Type" />
    <meta name="fc:frame:post_url" content="https://yourdomain.com/reveal" />
    ''', mimetype='text/html')

@app.route('/reveal', methods=['POST'])
def reveal():
    chosen = random.choice(gamer_types)
    return Response(f'''
    <meta property="og:title" content="You're a {chosen['title']}!" />
    <meta property="og:description" content="{chosen['desc']}" />
    <meta property="og:image" content="{chosen['image']}" />
    <meta name="fc:frame" content="vNext" />
    <meta name="fc:frame:button:1" content="Try Again" />
    <meta name="fc:frame:post_url" content="https://yourdomain.com/reveal" />
    ''', mimetype='text/html')

if __name__ == '__main__':
   import os
port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)
