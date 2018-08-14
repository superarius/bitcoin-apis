# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from models import DemoAddress
import random
import time
from TXtool import *
from ECbitcoin import *
import requests
import json

# Create your views here.

def home(request):
	return render(request, 'homepage.html')

def prepare_signature(request):
	s_address = str(request.GET.get("sender", None))
	receiver = request.GET.get("receiver", None)
	amount = btc2sat(float(request.GET.get("amount", None)))
	fee = btc2sat(float(request.GET.get("fee", None)))
	tx = quick_unsigned_tx(s_address, receiver, amount, fee)
	if tx==-1:
		raise ValueError
	raw_hashes = prepare_sig(tx, s_address)
	hashes = [i.encode('hex') for i in raw_hashes]
	success = 'success!'
	data = {'hashes': hashes, 'success':success, 'unsigned': tx}
	return JsonResponse(data)

def get_testwallet(request):
	demo_wallet = random.choice(DemoAddress.objects.all())
	data = {'address': demo_wallet.address, 'priv':demo_wallet.privkey, 'pub':demo_wallet.pubkey}
	return JsonResponse(data)

def fund_wallets(request):
	j = 0
	num = 0
	while j < 4:
		try:
			priv, pt = genECkeypair()
			address = convertPub2Addr(convertPt2Pub(pt), testnet=True)
			unsigned = quick_unsigned_tx("mfeVwF1taoNGJpT2ozRpuqpYqp37t42SMy", address, btc2sat(0.25), 3000)
			raw_hashes = prepare_sig(unsigned, "mfeVwF1taoNGJpT2ozRpuqpYqp37t42SMy")
			raw_sigs = [ECsign(int(i.encode('hex'),16), T1) for i in raw_hashes]
			btc_format = [rawSig2ScriptSig(i, TP) for i in raw_sigs]
			tx = apply_sig(unsigned, btc_format)
			r = pushTX(tx, testnet=True)
			if r['status'] == 'success':
				hp = hex(priv)
				hp = hp[2:-1] if hp[-1]=='L' else hp[2:]
				pub = convertPt2Pub(pt)
				a = DemoAddress()
				a.address = address
				a.pubkey = pub
				a.privkey = hp
				a.save()
				num += 1
		except:
			pass
		j += 1
		time.sleep(.33)
	string = "created %d new wallets" %num
	data = {'status': string}
	return JsonResponse(data)

def newmurmur(request):
	idkey = str(request.GET.get("IdentityKey", None))
	j = json.dumps({"IdentityKey": idkey})
	r = requests.post('http://127.0.0.1:8080/newmurmur', data=j)
	return JsonResponse(json.loads(r.text))

def write(request):
	key = str(request.GET.get("key", None))
	name = str(request.GET.get("name", None))
	j = json.dumps({"Name":name, "Content":key})
	r = requests.post('http://127.0.0.1:8080/write', data=j)
	d = {"status":"fail"}
	if r.text == "":
		d = {"status":"success"}
	return JsonResponse(d)

def access(request):
	name = str(request.GET.get("name", None))
	j = json.dumps({"Name":name})
	r = requests.post('http://127.0.0.1:8080/access', data=j)
	return JsonResponse(json.loads(r.text))	