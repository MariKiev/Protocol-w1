# coding=utf-8
from app import app, logger
from flask import render_template, request
from w1 import get_invoice_info, CURRENCY, payment_result
import requests
import pprint


@app.route('/')
def create_payment_form():
    return render_template('payment_form.html', currencies=CURRENCY)

@app.route('/process', methods=['POST'])
def index():
    data_form = dict(request.form.items())
    
    dict_invoice = get_invoice_info(data_form['amount'], data_form['currency'], data_form['payway'])
    return render_template('direct.html', form=dict_invoice)

@app.route('/callback', methods=['GET','POST'])
def callback():
    result_status = payment_result()
    return 'WMI_RESULT= %s' % result_status