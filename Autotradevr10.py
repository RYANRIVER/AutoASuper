import time
import pyupbit

# API KEY 입력
access_key = "RSN3OKMJehVdvjFGaxj6M2L6stZCp5FQlCR8Zxm5"
secret_key = "lgFo0ejmY0ghq01Btz34OIWNNLLkjKaLcDen0m15"

# 로그인
upbit = pyupbit.Upbit(access_key, secret_key)
print("autotrade start")

# 패키지별 매수 금액 설정
balances = upbit.get_balances()
total_krw = float(balances[0]['balance'])
eth_balance = float(balances[1]['balance'])
krw_per_package = total_krw * 0.05
eth_price = pyupbit.get_current_price("KRW-ETH")
initial_price = eth_price
print("Total KRW Balance:", total_krw)
print("ETH Balance:", eth_balance)
print("KRW per Package:", krw_per_package)

packages = {}
for i in range(1, 21):
    package_name = "Package{:02d}".format(i)
    packages[package_name] = {"bought": False, "sold": False, "bought_price": 0, "bought_time": None}
    print("Initialized Package:", package_name)

while True:
    try:
        eth_price = pyupbit.get_current_price("KRW-ETH")
        for i in range(1, 21):
            package_name = "Package{:02d}".format(i)
            package = packages[package_name]
            if not package["bought"]:
                if krw_per_package > 5000:
                    upbit.buy_market_order("KRW-ETH", krw_per_package)
                    bought_eth_balance = upbit.get_balance("KRW-ETH")
                    if bought_eth_balance > 0:
                        package["bought"] = True
                        package["bought_price"] = eth_price
                        package["bought_time"] = time.time()
                        krw_per_package = krw_per_package * 0.99 / 19
                        print("Package Bought:", package_name, "Bought Price:", package["bought_price"], "KRW Balance per Package:", krw_per_package)
            else:
                if not package["sold"]:
                    if eth_price >= package["bought_price"] * 1.03:
                        upbit.sell_market_order("KRW-ETH", upbit.get_balance("KRW-ETH"))
                        package["sold"] = True
                        print("Package Sold:", package_name, "Sold Price:", eth_price, "Profit:", (eth_price / package["bought_price"] - 1) * 100)
                    elif eth_price <= package["bought_price"] * 0.99:
                        if time.time() - package["bought_time"] >= 60:
                            krw_per_package = krw_per_package * 1.01
                            upbit.buy_market_order("KRW-ETH", krw_per_package)
                            package["bought_price"] = eth_price
                            package["bought_time"] = time.time()
                            print("Package Re-Bought:", package_name, "Bought Price:", package["bought_price"], "KRW Balance per Package:", krw_per_package)

        # 이더리움 잔고가 0일 경우, 패키지들 초기화
        eth_balance = upbit.get_balance("KRW-ETH")
        if eth_balance == 0:
            print("ETH Balance is 0, Resetting Packages...")
            for i in range(1, 21):
                package_name = "Package{:02d}".format(i)
                packages[package_name]["bought"] = False
                packages[package_name]["sold"] = False
                packages[package_name]["bought_price"] = 0
                packages[package_name]["bought_time"] = None

            krw_per_package = total_krw * 0.05
            initial_price = pyupbit.get_current_price("KRW-ETH")
            print("Total KRW Balance:", total_krw)
            print("ETH Balance:", eth_balance)
            print("KRW per Package:", krw_per_package)
            time.sleep(1)
    except Exception as e:
            print(e)
            time.sleep(1)