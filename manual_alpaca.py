import yaml
import alpaca_trade_api as tradeapi


def authenticate(auth_path='config/secrets.json'):
	with open(auth_path, 'r') as auth_file:
		auth = yaml.load(auth_file)

	api = tradeapi.REST(auth.public_key, auth.private_key)
	return api

if __name__ == '__main__':
	api = authenticate()
	account = api.get_account()
