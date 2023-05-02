import pyupbit
import time
import datetime

access_key = "RSN3OKMJehVdvjFGaxj6M2L6stZCp5FQlCR8Zxm5"
secret_key = "lgFo0ejmY0ghq01Btz34OIWNNLLkjKaLcDen0m15"
upbit = pyupbit.Upbit(access_key, secret_key)

# 매수 가격 초기화
buy_price = 0

def buy_more_eth():
    krw_balance = upbit.get_balance("KRW")
    if krw_balance < 200000:
        print("KRW balance is too low.")
        return
    eth_price = pyupbit.get_current_price("KRW-ETH")
    eth_amount = 200000 / eth_price
    current_package_name = "Package" + str(current_package_num).zfill(2)
    upbit.buy_limit_order("KRW-ETH", eth_price, eth_amount, current_package_name)
    print(current_package_name, "purchased at", eth_price)
    global buy_price
    buy_price = eth_price

def sell_package(package_name):
    eth_price = pyupbit.get_current_price("KRW-ETH")
    eth_balance = upbit.get_balance("ETH")
    upbit.sell_limit_order("KRW-ETH", eth_price * 1.03, eth_balance, package_name)

# 현재 가지고 있는 패키지 중 가장 높은 번호 찾기
current_package_num = 1
for balance in upbit.get_balances():
    if "Package" in balance["unit_currency"]:
        package_num = int(balance["unit_currency"].split("Package")[1])
        if package_num > current_package_num:
            current_package_num = package_num
print("Current package number:", current_package_num)

# 현재 패키지의 매수가 찾기
for balance in upbit.get_balances():
    if balance["unit_currency"] == "KRW-ETH":
        buy_price = float(balance["avg_buy_price"])
        break
print("Current buy price:", buy_price)

while True:
    try:
        eth_price = pyupbit.get_current_price("KRW-ETH")
        profit_rate = (eth_price / buy_price - 1) * 100
        if profit_rate >= 3 * current_package_num:
            sell_package("Package" + str(current_package_num).zfill(2))
            current_package_num += 1
            buy_more_eth()
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)