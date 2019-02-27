<img src="images/alpaca_logo.jpg" alt="drawing" width="400px" style="display: block; margin-left: auto; margin-right: auto"/>

# Manual Alpaca

This project is meant to manually interact with Alpaca's trading API in order
to more easily debug trading algorithms, and also provide a new way to trade.

## Acknowledgements

The base code for this repository was forked from
[Matt Haines](https://bitbucket.org/snugglepuppy/manual_alpaca/overview>)
on 02/26/2019 because I thought it was a cool project, but I wanted to expand
on the code and possibly add a GUI or Web interface. I would have made this
an actual GitHub fork, but the repo is hosted on BitBucket.

## Setup

### Python API Client 

This repository makes use of the Alpaca API's
[Python client](https://github.com/alpacahq/alpaca-trade-api-python).

#### Conda Environment

To create a portable/sandboxed conda environment for your python packages, run:

```bash
conda env create -f config/environment.yaml
source activate manual_alpaca
```

#### Pip

To install the required python packages with `pip` instead, run:

```bash
pip install -r config/requirements.txt
```

### API Keys

You will need API Keys to use the API, see the
[Alpaca API Documentation](https://docs.alpaca.markets/api-documentation/web-api/)
for help with generating your API keys.

For now, you should put your API keys in `config/config.yaml`. This may change in
the future.

## Usage

Once you've installed everything and setup your API keys, you're all set!
To get started, you can run:

```bash
python3 manual_alpaca.py
```
