# coding=utf-8
from app import app, logger
from flask import render_template, request
from w1 import get_invoice_info, CURRENCY
import requests


@app.route('/')
def create_payment_form():
    return render_template('payment_form.html', currencies=CURRENCY)

@app.route('/process', methods=['POST'])
def index():
    data_form = dict(request.form.items())
    
    dict_invoice = get_invoice_info(data_form['amount'], data_form['currency'], data_form['payway'])
    return render_template('direct.html', form=dict_invoice)