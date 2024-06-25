# webhook.py
from flask import Blueprint, request, jsonify, current_app
import stripe
from .db import get_db

bp = Blueprint('webhook', __name__, url_prefix='/webhook')

@bp.route('/stripe', methods=['POST'])
def stripe_webhook():
    payload = request.get_data(as_text=True)
    sig_header = request.headers.get('Stripe-Signature')
    endpoint_secret = current_app.config['STRIPE_WEBHOOK_SECRET']

    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return jsonify(success=False), 400
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return jsonify(success=False), 400

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        # Fulfill the purchase
        user_id = session['metadata']['user_id']
        db = get_db()
        db.execute(
            "UPDATE Users SET is_paid = 1 WHERE id = ?", (user_id,)
        )
        db.commit()

    return jsonify(success=True)
