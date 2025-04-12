import os
from flask import Flask, render_template, request
import random
import requests

app = Flask(__name__)

# Sample gamer types
gamer_types = [
    {
        "title": "Casual Clicker",
        "image": "static/images/casual_clicker.png",  # Replace with actual image paths
        "desc": "You enjoy playing simple and fun games, often indulging in casual clickers or idle games."
    },
    {
        "title": "Hardcore Raider",
        "image": "static/images/hardcore_raider.png",  # Replace with actual image paths
        "desc": "You thrive on challenges and love grinding through tough raids in RPGs and MMOs."
    },
    {
        "title": "Strategic Master",
        "image": "static/images/strategic_master.png",  # Replace with actual image paths
        "desc": "You are a thinker, always planning your next move, whether in RTS or strategic board games."
    },
    {
        "title": "Explorer",
        "image": "static/images/explorer.png",  # Replace with actual image paths
        "desc": "You love exploration games, diving into new worlds and discovering all their secrets."
    }
]

# Function to generate random gamer type
def generate_random_gamer_type():
    return random.choice(gamer_types)

# Function to fetch wallet data (balance, NFTs, transactions)
def fetch_wallet_data(wallet_address):
    # API key and endpoint for Etherscan API
    etherscan_api_key = "6K86CA6HRB1CPRNF1D3A56S3P8MVIZQUWQ"
    etherscan_url = f"https://api.etherscan.io/api?module=account&action=balance&address={wallet_address}&tag=latest&apikey={etherscan_api_key}"

    # Fetch ETH balance
    eth_balance_response = requests.get(etherscan_url).json()
    eth_balance = int(eth_balance_response['result']) / 10**18  # Convert wei to eth

    # Fetch number of transactions (ERC-20 or ETH)
    transaction_count_response = requests.get(f"https://api.etherscan.io/api?module=account&action=txlist&address={wallet_address}&startblock=0&endblock=99999999&sort=asc&apikey={etherscan_api_key}").json()
    transaction_count = len(transaction_count_response['result'])

    # Fetch NFTs held (example for ERC-721 tokens, you may need a specific API for NFT collections)
    nft_count_response = requests.get(f"https://api.opensea.io/api/v1/assets?owner={wallet_address}&order_direction=desc&offset=0&limit=1").json()
    nft_count = len(nft_count_response['assets'])

    return eth_balance, transaction_count, nft_count

# Homepage route
@app.route('/')
def index():
    wallet_address = request.args.get('wallet', '')
    return render_template('index.html', wallet_address=wallet_address)

# Analyze route
@app.route('/analyze')
def analyze():
    wallet_address = request.args.get('wallet')
    
    # Fetch wallet data
    eth_balance, transaction_count, nft_count = fetch_wallet_data(wallet_address)
    
    # Generate random gamer type based on wallet activity
    gamer_type = generate_random_gamer_type()
    
    return render_template('result.html', 
                           wallet_address=wallet_address,
                           eth_balance=eth_balance,
                           transaction_count=transaction_count,
                           nft_count=nft_count,
                           gamer_type=gamer_type)

# Ensure the app listens on the correct port and host
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Default to port 5000 if not set by Render
    app.run(host='0.0.0.0', port=port, debug=True)
