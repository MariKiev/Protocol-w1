# coding=utf-8
import requests
from collections import defaultdict
from hashlib import md5
import binascii
from config import SECRET_KEY, MERCHANT_ID, PAYMENT_RESULT, token

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

def payment_result():
    payment_result = PAYMENT_RESULT
    
    if "WMI_SIGNATURE" not in payment_result:
        return u'RETRY&WMI_DESCRIPTION=Отсутствует параметр WMI_SIGNATURE'

    if "WMI_PAYMENT_NO" not in payment_result:
        return u'RETRY&WMI_DESCRIPTION=Отсутствует параметр WMI_PAYMENT_NO'

    if "WMI_ORDER_STATE" not in payment_result:
        return u'RETRY&WMI_DESCRIPTION=Отсутствует параметр WMI_ORDER_STATE'

    payment_result_signature = payment_result.pop("WMI_SIGNATURE")
    if get_signature(payment_result, SECRET_KEY) != payment_result_signature:
        return 'RETRY&WMI_DESCRIPTION=Invalid sign'

    return 'OK'

def balance():
    headers =  {
        "Authorization": "Bearer %s" % token,
        "Accept": "application/vnd.wallet.openapi.v1+json"
    }
    response = requests.get('https://api.w1.ru/OpenApi/balance', headers=headers)
    return response

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