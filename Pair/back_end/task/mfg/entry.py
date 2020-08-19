from db.models import Basket, Entry

def calc_cost(stock, pos, amt):
    fee = amt * (0.00015 if pos == '+' else 0.001)
    fee = fee - fee % 10

    tax = amt * (0.0025  if pos == '-' else 0)
    tax = tax - tax % 10
    tax = 0 if stock.aimed == 'ETF' else tax

    cost = fee + tax
    return cost

def calc_yield(entry, L_exit_uv, S_exit_uv):
    if 0 in (L_exit_uv, S_exit_uv):
        return 0

    L_buy_amt  = entry.Long.entry_amt
    L_sell_amt = entry.Long.entry_qty  * L_exit_uv
    S_buy_amt  = entry.Short.entry_amt
    S_sell_amt = entry.Short.entry_qty * S_exit_uv

    yield1 = (L_sell_amt / L_buy_amt - 1) * 100
    yield2 = (S_sell_amt / S_buy_amt - 1) * 100

    return yield1 - yield2

