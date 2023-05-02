import pyupbit

print(pyupbit.get_orderbook(ticker="KRW-BTC"))


# 지정가 매도
print(pyupbit.sell_limit_order("KRW-XRP", 600, 20))

# 지정가 매수
print(pyupbit.buy_limit_order("KRW-XRP", 613, 10))

# 시장가 매수 (리플 10000원치를 시장가에 매수, 수수료가 잔고에 있어야 됨)
print(pyupbit.buy_market_order("KRW-XRP", 10000))

# 시장가 매도 (리플 30개를 시장가에 매도, 수수료를 제외하고 입금됨)
print(pyupbit.sell_market_order("KRW-XRP", 30))


