#! usr/bin/env python3

import alpaca_trade_api as tradeapi
import os
import sys
from pandas import read_csv
import pandas as pd


def menu_input(argument):
    switcher = {
        "G": get_positions,
        "T": get_ticker,
        "O": order_list_all,
        "OC": order_list_closed,
        "OO": order_list_open,
        "H": help_text,
        "Q": exit_script,
        "I": change_id,
    }
    # Get the function from switcher dictionary
    func = switcher.get(argument, lambda: print("Invalid entry ('H' for help)"))
    # Execute the function
    func()
    return


def change_id():

    global strat

    print("change user id...")
    print("current id prefix: ", strat)
    inp = input("enter new user id prefix for orders (max 10 chars): ")
    if len(inp) > 10:
        print("input too long. returning...")
        return
    if inp != "":
        strat = inp + "_"
    else:
        strat = ""

    print("user id prefix changed to: ", strat)

    return ()


def order_list_all():

    print("get all orders...")

    inp = input("Since (M)idnight or return for all: ").upper()
    order_list = []
    nr = {}

    midnight = now.strftime("%Y-%m-%d")

    if inp == "M":
        print("Orders since midnight...")
        orders = api.list_orders(status="all", after=midnight)
    else:
        orders = api.list_orders(status="all")

    for o in orders:
        nr = {
            "symbol": o.symbol,
            "qty": o.qty,
            "id": o.client_order_id,
            "side": o.side,
            "status": o.status,
        }
        order_list.append(nr)

    print(
        "{:>3} {:<7} {:>7} {:>7} {:>9}  {:>10}".format(
            "#", "symbol", "qty", "side", "status", "client id"
        )
    )

    for i in range(0, len(order_list)):
        print(
            "{:>3} {:<7} {:>7} {:>7} {:>9}  {:>10}".format(
                i,
                order_list[i]["symbol"],
                order_list[i]["qty"],
                order_list[i]["side"],
                order_list[i]["status"],
                order_list[i]["id"],
            )
        )

    return


def order_list_closed():

    print("get all closed orders...")

    inp = input("Since (M)idnight or return for all: ").upper()
    order_list = []
    nr = {}

    midnight = now.strftime("%Y-%m-%d")

    if inp == "M":
        print("Orders since midnight...")
        orders = api.list_orders(status="closed", after=midnight)
    else:
        orders = api.list_orders(status="closed")

    cnt = 0
    for o in orders:
        nr = {
            "symbol": o.symbol,
            "qty": o.qty,
            "id": o.client_order_id,
            "side": o.side,
            "status": o.status,
        }
        order_list.append(nr)

    print(
        "{:>3} {:<7} {:>7} {:>7} {:>9}  {:>10}".format(
            "#", "symbol", "qty", "side", "status", "client id"
        )
    )

    for i in range(0, len(order_list)):
        print(
            "{:>3} {:<7} {:>7} {:>7} {:>9}  {:>10}".format(
                i,
                order_list[i]["symbol"],
                order_list[i]["qty"],
                order_list[i]["side"],
                order_list[i]["status"],
                order_list[i]["id"],
            )
        )

    return


def order_list_open():

    print("get all open orders...")

    inp = input("Since (M)idnight or return for all: ").upper()
    order_list = []
    nr = {}

    midnight = now.strftime("%Y-%m-%d")

    if inp == "M":
        print("Orders since midnight...")
        orders = api.list_orders(status="open", after=midnight)
    else:
        orders = api.list_orders(status="open")

    cnt = 0
    for o in orders:
        nr = {
            "symbol": o.symbol,
            "qty": o.qty,
            "cid": o.client_order_id,
            "side": o.side,
            "status": o.status,
            "id": o.id,
        }
        order_list.append(nr)

    print(
        "{:>3} {:<7} {:>7} {:>7} {:>9}  {:>10}".format(
            "#", "symbol", "qty", "side", "status", "client id"
        )
    )
    for i in range(0, len(order_list)):
        print(
            "{:>3} {:<7} {:>7} {:>7} {:>9}  {:>10}".format(
                i,
                order_list[i]["symbol"],
                order_list[i]["qty"],
                order_list[i]["side"],
                order_list[i]["status"],
                order_list[i]["cid"],
            )
        )

    inp = input("enter order number to cancel, or return to exit: ")
    try:
        inpint = int(inp)
    except Exception as e:
        print("No order number entered. Returning...")
        return
    if inpint > len(order_list) or inpint < 0:
        print("Order number out of range. Returning...")
        return

    print(
        "canceling {} order # {}".format(
            order_list[inpint]["symbol"], order_list[inpint]["id"]
        )
    )
    try:
        api.cancel_order(order_list[inpint]["id"])
    except Exception as e:
        print("error {}\nreturning....".format(e))
        return
    print("cancelation submitted.")
    return


def help_text():

    print("help menu...")

    filepath = root_path + "man_alp_help.txt"
    with open(filepath) as fp:
        line = fp.readline()
        cnt = 1
        while line:
            print("{}: {}".format(cnt, line.strip()))
            line = fp.readline()
            cnt += 1
            if cnt % 22 == 0:
                bif = input("\nhit return...")

    return


def exit_script():

    print("exiting...")
    sys.exit()

    return


def get_ticker():

    type_tif = {"G": "gtc", "D": "day", "O": "opg"}

    order = {}

    print("get ticker...")

    ticker = input("enter ticker: ").upper()

    today_am = now.strftime("%Y-%m-%d") + "T09:30"

    try:
        lquote = api.polygon.last_trade(ticker)
    except Exception as e:
        print("error:\n", e)
        return

    print(
        "symbol: {} last trade price: {} size: {} time: {}".format(
            ticker,
            lquote.price,
            lquote.size,
            lquote.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        )
    )

    inp = input("Buy (M)arket, (L)imit or return: ").upper()

    if inp == "M" or inp == "L":
        if inp == "L":
            lim = input("enter limit price: ")
            tif = input('time in force ("(D)ay" or "(G)tc" only): ').upper()
            order_type = "limit"

        else:
            order_type = "market"
            tif = input("time in force: (G)TC, (D)ay, (O)PG: ").upper()

        if max_pos_size == 0:
            qty = input("quantity to buy (blank to cancel): ")
            if qty == "":
                print("cancel and returning...")
                return
        else:
            qty = input(
                "quantity to buy (or enter for max position of {} shares, 0 to return): ".format(
                    int(max_pos_size / lquote.price)
                )
            )
            if isinstance(qty, int) == False:
                print("Input error detected. Returning...")
                return
            if qty == "0":
                print("Command canceled. Returning...")
                return
            if qty == "":
                print("quantity = ", int(max_pos_size / lquote.price))
                qty = str(int(max_pos_size / lquote.price))

        print(strat + str(pd.Timestamp.utcnow().isoformat()))

        try:
            if inp == "L":
                order = api.submit_order(
                    symbol=ticker,
                    qty=qty,
                    side="buy",
                    type=order_type,
                    time_in_force=type_tif[tif],
                    client_order_id=strat + str(pd.Timestamp.utcnow().isoformat()),
                    limit_price=lim,
                )

            else:
                order = api.submit_order(
                    symbol=ticker,
                    qty=qty,
                    side="buy",
                    type=order_type,
                    client_order_id=strat + str(pd.Timestamp.utcnow().isoformat()),
                    time_in_force=type_tif[tif],
                )
        except Exception as e:
            print("error\n", e)
            return
        print("order status: ")
        print(order)

    else:
        print("No order type. Returning....")
        return

    return


def get_positions():

    type_men = {"M": "market", "L": "limit"}
    type_tif = {"G": "gtc", "D": "day", "O": "opg"}
    limprice = ""

    print("get positions...")
    len = 0
    holdings = {}

    positions = api.list_positions()
    print("{:>3} {:<7} {:>7} {:>10}".format("#", "symbol", "qty", "current_price"))

    for p in positions:
        holdings[len] = {
            "symbol": p.symbol,
            "qty": p.qty,
            "current_price": p.current_price,
        }
        if len in holdings:
            print(
                "{:>3} {:<7} {:>7} {:>10}".format(
                    len,
                    holdings[len]["symbol"],
                    holdings[len]["qty"],
                    holdings[len]["current_price"],
                )
            )
        len += 1
    inpraw = input("position # to sell (enter to return to menu) ")
    try:
        inp = int(inpraw)
    except:
        print("selection error. returning...")
        return

    if inp in holdings:

        selltype = input(
            "selling {}: (M)arket, (L)imit: ".format(holdings[inp]["symbol"])
        ).upper()

        sell_tif = input("time in force: (G)TC, (D)ay, (O)PG: ").upper()

        numsharesraw = input(
            "# of shares to sell (max = {})".format(holdings[inp]["qty"])
        )
        numshares = int(numsharesraw)

        if (numshares > int(holdings[inp]["qty"])) or (numshares == 0):
            print("too many shares...")
            return

        if selltype == "L":
            limprice = input("enter limit price (XXX)X.XX : ")

            try:
                api.submit_order(
                    symbol=holdings[inp]["symbol"],
                    qty=numsharesraw,
                    side="sell",
                    limit_price=limprice,
                    type="limit",
                    client_order_id=strat + str(pd.Timestamp.utcnow().isoformat()),
                    time_in_force=type_tif[sell_tif],
                )

            except Exception as e:
                print("error ", e)

        else:

            try:
                print(
                    "market order {} {} {}".format(
                        holdings[inp]["symbol"], numsharesraw, type_tif[sell_tif]
                    )
                )
                api.submit_order(
                    symbol=holdings[inp]["symbol"],
                    qty=numsharesraw,
                    side="sell",
                    type="market",
                    client_order_id=strat + str(pd.Timestamp.utcnow().isoformat()),
                    time_in_force=type_tif[sell_tif],
                )

            except Exception as e:
                print("error ", e)

    else:

        print("selection not recognized. Returning to menu...")

    return


def live_print():

    print("*" * 48)
    print("LIVE! " * 8)
    print("*" * 48)

    return


# main loop

max_pos_size = 0
root_path = ""


live = input('Live or paper trading? Enter "live" or enter: ')

if live == "live":
    live_print()
    try:
        keys = read_csv("live_keys.csv")

    except Exception as e:
        print("error ", e)
        print("Live keys not found. Exiting...")
        sys.exit()

    os.environ["APCA_API_BASE_URL"] = "https://api.alpaca.markets"
else:
    try:
        keys = read_csv(root_path + "keys.csv")

    except Exception as e:
        print("error ", e)
        print("Paper keys not found. Exiting...")
    os.environ["APCA_API_BASE_URL"] = "https://paper-api.alpaca.markets"


pub_key = keys.at[0, "pub"]
priv_key = keys.at[0, "priv"]

global strat
strat = ""
api = tradeapi.REST(pub_key, priv_key)

clock = api.get_clock()
now = clock.timestamp
today = now.strftime("%Y-%m-%d")

inp = input("Enter max position size if desired (or enter to ignore): ")

try:
    max_pos_size = int(inp)
except Exception as e:
    print("*** No position size detected. ***")

loop = True
while loop == True:
    acct = api.get_account()
    if live == "live":
        live_print()

    print(
        "\naccount value: {}, buying power: {}".format(
            acct.portfolio_value, acct.buying_power
        )
    )
    print("user prefix: ", strat)

    user_selection = input("Enter Selection ('H'for help, 'Q' for quit): ").upper()
    menu_input(user_selection)
