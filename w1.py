# coding=utf-8
import requests
from collections import defaultdict
from hashlib import md5
import binascii
from config import SECRET_KEY, MERCHANT_ID

PAY_TYPES = {
    u'Оплатить OKPay': 'Okpay',
    u'Оплатить WalletOne': 'WalletOne'
}

method = 'post'
url = 'https://wl.walletone.com/checkout/checkout/Index'

CURRENCY = {
    840: "USD",
    978: "EUR",
    980: "UAH",
    643: 'RUB'
}

def get_invoice_info(ammount, currency_id, payway):

    dict_invoice = {
        'action': url,
        'method': method,
        'params': {
            'WMI_MERCHANT_ID': MERCHANT_ID,
            'WMI_PAYMENT_AMOUNT': ammount,
            'WMI_CURRENCY_ID': currency_id,
            'WMI_PTENABLED': PAY_TYPES[payway] + CURRENCY[int(currency_id)]
        }
    }

    dict_invoice['params']['WMI_SIGNATURE'] = get_signature(dict_invoice['params'], SECRET_KEY)

    return dict_invoice

def get_signature(params, secret_key):
    """
    Base64(Byte(MD5(Windows1251(Sort(Params) + SecretKey))))
    params - list of tuples [('WMI_CURRENCY_ID', 643), ('WMI_PAYMENT_AMOUNT', 10)]
    """
    icase_key = lambda s: unicode(s).lower()

    lists_by_keys = defaultdict(list)
    for key, value in params.iteritems():
        lists_by_keys[key].append(value)

    str_buff = ''
    for key in sorted(lists_by_keys, key=icase_key):
        for value in sorted(lists_by_keys[key], key=icase_key):
            str_buff += unicode(value).encode('1251')
    str_buff += secret_key
    md5_string = md5(str_buff).digest()

    return binascii.b2a_base64(md5_string)[:-1]