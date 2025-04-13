import os
import json
import random
import hashlib
import requests
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Etherscan API key and leaderboard file
ETHERSCAN_API_KEY = "6K86CA6HRB1CPRNF1D3A56S3P8MVIZQUWQ"
LEADERBOARD_FILE = "leaderboard.json"

# Sample gamer types (images are in /static/images/)
gamer_types = [
    {
        "title": "Casual Clicker",
        "image": "casual_clicker.png",
        "desc": "You enjoy playing simple and fun games, often indulging in casual clickers or idle games."
    },
    {
        "title": "Hardcore Raider",
        "image": "hardcore_raider.png",
        "desc": "You thrive on challenges and love grinding through tough raids in RPGs and MMOs."
    },
    {
        "title": "Strategic Master",
        "image": "strategic_master.png",
        "desc": "You are a thinker, always planning your next move, whether in RTS or strategic board games."
    },
    {
        "title": "Explorer",
        "image": "explorer.png",
        "desc": "You love exploration games, diving into new worlds and discovering all their secrets."
    }
]

def get_wallet_data(wallet_address):
    """Fetch ETH balance, transaction count, and NFT count from Etherscan."""
    base_url = "https://api.etherscan.io/api"
    
    # ETH balance
    eth_url = f"{base_url}?module=account&action=balance&address={wallet_address}&tag=latest&apikey={ETHERSCAN_API_KEY}"
    eth_res = requests.get(eth_url).json()
    eth_balance = int(eth_res.get('result', 0)) / 10**18
    
    # Transaction count
    tx_url = f"{base_url}?module=account&action=txlist&address={wallet_address}&startblock=0&endblock=99999999&sort=asc&apikey={ETHERSCAN_API_KEY}"
    tx_res = requests.get(tx_url).json()
    transaction_count = len(tx_res.get('result', []))
    
    # NFT count via ERC-721 transfers using the tokentx API (each transfer with 'tokenID' considered as an NFT transaction)
    nft_url = f"{base_url}?module=account&action=tokennfttx&address={wallet_address}&startblock=0&endblock=99999999&sort=asc&apikey={ETHERSCAN_API_KEY}"
    nft_res = requests.get(nft_url).json()
    nft_count = 0
    if nft_res.get('status') == '1' and 'result' in nft_res:
        for tx in nft_res['result']:
            # Use .get() to avoid KeyError if 'tokenID' doesn't exist.
            if tx.get('tokenID') is not None:
                nft_count += 1

    return eth_balance, transaction_count, nft_count

def get_gamer_type_from_address(wallet_address):
    """Deterministically choose gamer type based on wallet hash."""
    hash_digest = hashlib.sha256(wallet_address.encode()).hexdigest()
    index = int(hash_digest, 16) % len(gamer_types)
    return gamer_types[index]

def load_leaderboard():
    """Load the leaderboard from the JSON file."""
    if not os.path.exists(LEADERBOARD_FILE):
        return []
    with open(LEADERBOARD_FILE, 'r') as f:
        return json.load(f)

def save_to_leaderboard(wallet, eth, txs, nfts):
    """Update leaderboard with data for a wallet."""
    leaderboard = load_leaderboard()
    # Check if wallet is already in leaderboard; update if exists
    updated = False
    for entry in leaderboard:
        if entry["wallet"] == wallet:
            entry["eth"] = eth
            entry["txs"] = txs
            entry["nfts"] = nfts
            updated = True
            break
    if not updated:
        leaderboard.append({"wallet": wallet, "eth": eth, "txs": txs, "nfts": nfts})
    with open(LEADERBOARD_FILE, 'w') as f:
        json.dump(leaderboard, f, indent=2)

# Homepage route with wallet input form
@app.route('/')
def index():
    wallet_address = request.args.get('wallet', '')
    return render_template('index.html', wallet_address=wallet_address)

# Analysis route: fetch data, save leaderboard, and show result
@app.route('/analyze')
def analyze():
    wallet_address = request.args.get('wallet', '').strip()
    if not wallet_address:
        return redirect(url_for('index'))

    eth, txs, nfts = get_wallet_data(wallet_address)
    if eth is None:
        return render_template('error.html', message="Failed to fetch data for this wallet address.")

    # Save/update leaderboard
    save_to_leaderboard(wallet_address, eth, txs, nfts)

    gamer_type = get_gamer_type_from_address(wallet_address)
    return render_template('result.html',
                           wallet=wallet_address,
                           eth=eth,
                           txs=txs,
                           nfts=nfts,
                           gamer_type=gamer_type)

# Leaderboard route: display top wallets sorted by NFT count
@app.route('/leaderboard')
def leaderboard():
    leaderboard_data = load_leaderboard()
    # Sort by NFT count descending
    sorted_leaderboard = sorted(leaderboard_data, key=lambda x: x.get("nfts", 0), reverse=True)
    return render_template("leaderboard.html", leaderboard=sorted_leaderboard)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
