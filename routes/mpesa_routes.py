from flask import Blueprint, request, jsonify
from utils.mpesa import get_mpesa_token, initiate_stk_push
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

mpesa_routes = Blueprint('mpesa_routes', __name__)

@mpesa_routes.route('/api/mpesa/pay', methods=['POST'])
def pay_with_mpesa():
    data = request.json
    phone = data['phone']
    amount = data['amount']

    # Fetch credentials from environment variables
    consumer_key = os.getenv('CONSUMER_KEY')
    consumer_secret = os.getenv('CONSUMER_SECRET')
    shortcode = os.getenv('SHORTCODE')
    passkey = os.getenv('PASSKEY')
    callback_url = os.getenv('CALLBACK_URL')

    token = get_mpesa_token(consumer_key, consumer_secret)
    result = initiate_stk_push(phone, amount, token, shortcode, passkey, callback_url)

    return jsonify(result), 200

@mpesa_routes.route('/api/mpesa/callback', methods=['POST'])
def mpesa_callback():
    data = request.json
    print("✅ Payment callback received:", data)
    # TODO: Save payment data to the database
    return jsonify({'ResultCode': 0, 'ResultDesc': 'Accepted'})
