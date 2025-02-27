from flask import Blueprint, render_template, request, flash, jsonify, request, redirect, url_for
from flask_login import login_required, current_user

from . import db

import io
import base64

import requests  # Add this line to import the requests module
import random

# Blueprint for views
views = Blueprint('views', __name__)
views.secret_key = 'your_secret_key'  # Set a secret key for session management


# Route for the home page
@views.route('/', methods=['GET', 'POST'])
@login_required  # Requires login to access this route
def home():
    return render_template("index.html", user=current_user)

@views.route('/explore')
def explore():
    return render_template('explore.html', user=current_user)

@views.route('/make_payment', methods=['GET', 'POST'])
def make_payment():
    amount = request.form.get('amount')
  
    email = request.form.get('email')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
   
    # Generate a random integer between 1 and 100
    random_number = random.randint(1, 10000)

    str_int = str(random_number)

    print("Random number:", random_number)
    
    # API endpoint for making a payment
    url = "https://api.paychangu.com/payment"
    
    # Payload data to send in the POST request
    payload = {
        "currency": "MWK",
        "customization": {
            "title": "Title of payment",
            "description": "Payment description"
        },
        "amount": amount,
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
        "callback_url": "http://127.0.0.1:5000/explore",
        
        "tx_ref": str_int
    }

    # Headers for the POST request
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": "Bearer sec-live-XQEPaw5LZajQ52sLuzyEdEjsy2gIer3p"
    }

    # Send POST request to the payment API with payload and headers
    response = requests.post(url, json=payload, headers=headers)
   
    # for request in response.json()['data']:
    #     print(request)

    # Print the response text from the API (for debugging purposes)
    print("printing response")
    print(response.text)
    # Parse the response as JSON
    response_data = response.json()

    # Access the fields of the JSON object
    field1 = response_data.get('message')
    field2 = response_data.get('status')
    field3 = response_data.get('data')

    print(field1)
    print(field2)
    if field2 == 'success':
        print("successful transaction : ")
        print("printing data : ")
        print(payload)
        
        # Flash a success message to be displayed on the redirected page
        flash('transaction created succesfully! thank you for shopping with us', category='success')
    if field2 == 'failed':
       # Flash a success message to be displayed on the redirected page
        flash(field1, category='error')
        print("failed transaction : ")
        print(payload)

    # Redirect the user to checkout url
    return redirect(field3['checkout_url'])
    
