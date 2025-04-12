import json
import os
import hashlib
import requests
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

ETHERSCAN_API_KEY = "6K86CA6HRB1CPRNF1D3A56S3P8MVIZQUWQ"
LEADERBOARD_FILE = "leaderboard.json"

gamer_types = [
    {
        "title": "Casual Clicker",
        "image": "casual_clicker.png",
        "desc": "You enjoy simple and relaxing games. No pressure, just good vibes!"
    },
    {
        "title": "Hardcore Raider",
        "image": "hardcore_raider.png",
        "desc": "You seek thrills and glory. Only the strongest survive your game list."
    },
    {
        "title": "Strategic Master",
        "image": "strategic_master.png",
        "desc": "Chess of the digital age — you outthink, outplay, and dominate."
    },
    {
        "title": "Explorer",
        "image": "explorer.png",
        "desc": "From pixel caves to distant galaxies, you're always discovering new realms."
    }
]

def get_wallet_data(address):
    try:
        bal_url = f"https://api.etherscan.io/api?module=account&action=balance&address={address}&tag=latest&apikey={ETHERSCAN_API_KEY}"
        eth_balance = int(requests.get(bal_url).json()['result']) / 1e18

        tx_url = f"https://api.etherscan.io/api?module=account&action=txlist&address={address}&startblock=0&endblock=99999999&sort=asc&apikey={ETHERSCAN_API_KEY}"
        txs = len(requests.get(tx_url).json()['result'])

        nft_url = f"https://api.etherscan.io/api?module=account&action=tokennfttx&address={address}&startblock=0&endblock=99999999&sort=asc&apikey={ETHERSCAN_API_KEY}"
        nfts = len(requests.get(nft_url).json()['result'])

        return eth_balance, txs, nfts
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None, None, None

def get_gamer_type_from_address(address):
    hash_digest = hashlib.sha256(address.encode()).hexdigest()
    index = int(hash_digest, 16) % len(gamer_types)
    return gamer_types[index]

def load_leaderboard():
    if not os.path.exists(LEADERBOARD_FILE):
        return []
    with open(LEADERBOARD_FILE, 'r') as file:
        return json.load(file)

def save_to_leaderboard(wallet, eth, txs, nfts):
    data = load_leaderboard()
    # Check if wallet already exists
    updated = False
    for entry in data:
        if entry['wallet'] == wallet:
            entry['eth'] = eth
            entry['txs'] = txs
            entry['nfts'] = nfts
            updated = True
            break
    if not updated:
        data.append({"wallet": wallet, "eth": eth, "txs": txs, "nfts": nfts})
    with open(LEADERBOARD_FILE, 'w') as file:
        json.dump(data, file, indent=2)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze')
def analyze():
    wallet = request.args.get('wallet')
    if not wallet:
        return redirect(url_for('index'))

    eth, txs, nfts = get_wallet_data(wallet)
    if eth is None:
        return render_template("error.html")

    save_to_leaderboard(wallet, eth, txs, nfts)

    gamer_type = get_gamer_type_from_address(wallet)
    return render_template("result.html",
                           wallet=wallet,
                           eth=eth,
                           txs=txs,
                           nfts=nfts,
                           gamer_type=gamer_type)

@app.route('/leaderboard')
def leaderboard():
    data = load_leaderboard()
    sorted_data = sorted(data, key=lambda x: x['nfts'], reverse=True)
    return render_template("leaderboard.html", leaderboard=sorted_data)

if __name__ == '__main__':
    app.run(debug=True)
