import os
import sys
import yaml
import alpaca_trade_api as tradeapi

def authenticate(auth_path='', mode='paper'):
	'''
	Alpaca Trade API Authentication                               
	-----------------------------------------------------------------
	Authenticating access to the API can be done in two ways.

	1. Save your "Key ID" (public key) and "Secret Key" (private key)
	   in a config file, such as [config/secrets.yaml]

	2. Save your public and private keys as environment variables.
	   On UNIX, run the following commands in the terminal:
	     >> export APCA_API_KEY_ID: key ID
	     >> export APCA_API_SECRET_KEY: secret key
	'''

	if mode == 'paper':
		os.environ['APCA_API_BASE_URL'] = 'https://paper-api.alpaca.markets'
	elif mode == 'live':
		os.environ['APCA_API_BASE_URL'] = 'https://api.alpaca.markets'
	else:
		print('[mode] must either "paper" or "live".')
		sys.exit(1)

	# Saving keys in config file - example: [config/secrets.json]
	if auth_path:
		with open(auth_path, 'r') as auth_file:
			auth = yaml.load(auth_file)

		try:
			keys = auth[mode]
			api = tradeapi.REST(keys['public_key'], keys['private_key'])
			api.get_account()
		except KeyError:
			print("[{}] must have 'public_key' and 'private_key' fields set for " \
			      "the [{}] field.".format(auth_path, mode))
			sys.exit(1)
		except alpaca_trade_api.rest.APIError:
			print('Authentication failed.')
			print(authenticate.__doc__)
			sys.exit(2)


	# Saving keys as environment variables
	else:
		try:
			assert os.environ.get('APCA_API_KEY_ID') is not None
			assert os.environ.get('APCA_API_SECRET_KEY') is not None
		except AssertionError:
			print('Authentication failed.')
			print('Make sure APCA_API_KEY_ID / APCA_API_SECRET_KEY are set!')
			sys.exit(1)

		try:
			# This will check the environment variables under the hood
			api = tradeapi.REST()
			api.get_account()
		except alpaca_trade_api.rest.APIError:
			print('Authentication failed.')
			print(authenticate.__doc__)
			sys.exit(2)

	print('Authentication successful!')
	return api

if __name__ == '__main__':
	api = authenticate()
	# api = authenticate(auth_path='config/secrets.yaml')
	account = api.get_account()
	print(account)
