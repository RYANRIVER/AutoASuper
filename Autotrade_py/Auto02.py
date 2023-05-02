import pyupbit
import pyupbit.websocket_api as wsck

access_key = "XXX"
secret_key = "XXX"
upbit = pyupbit.Upbit(access_key, secret_key)

def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

# orderbook = pyupbit.get_orderbook("KRW-ETH")

# ask_price = orderbook[0]['orderbook_units'][0]['ask_price']   # 가장 낮은 매도 호가
# ask_vol = orderbook[0]['orderbook_units'][0]['ask_size']      # 가장 낮은 매도 호가 수량
# bid_price = orderbook[0]['orderbook_units'][0]['bid_price']   # 가장 높은 매수 호가
# bid_volume = orderbook[0]['orderbook_units'][0]['bid_size']   # 가장 높은 매수 호가 수량

Initial_price = 0.0
last_price = 0.0
buy_no = 0.0
sell_no = 0.0
unitAmount = round(get_balance("KRW")/30,-4)
profit_ratio = 1.022
sell_uuid = []

if __name__ == "__main__":
        wm = wsck.WebSocketManager("ticker", ["KRW-ETH", ])
        while True:
            try :
                data = wm.get()
                print(data['trade_price'])
                if get_balance("ETH") == 0 :
                    if get_balance("KRW") > unitAmount :
                        buyResult = upbit.buy_market_order("KRW-ETH", unitAmount*10)
                        # wait until the order is fully executed
                        while True:
                            order_info = upbit.get_order(buyResult["uuid"])
                            if order_info["state"] == "done":
                                for trade in order_info["trades"]:
                                    trade_price = float(trade["price"])
                                    trade_qty = float(trade["volume"])
                                    print(f"Price: {trade_price}, Qty: {trade_qty}")
                                Initial_price = trade_price
                                last_price = trade_price
                                buy_no = buy_no + 1
                            break
                        sellResult = upbit.sell_limit_order("KRW-ETH", round(trade_price*profit_ratio,-3),trade_qty)
                        order_info = upbit.get_order(sellResult["uuid"])
                        sell_uuid.append(order_info["uuid"])
                        print("매도대기건수:", len(sell_uuid))
                        print("0이면 이상 무, 아니면 이상함 :",buy_no - sell_no - len(sell_uuid))
                        print("원화잔고 :", get_balance("KRW"), ", 이더리움 잔고 :", get_balance("ETH"))
                    else :
                        print ("잔고가 부족합니다")
                elif get_balance("ETH") > 0 and data['trade_price'] < Initial_price * (1 - float(len(sell_uuid))/100) :
                    if get_balance("KRW") > unitAmount : 
                        buyResult = upbit.buy_market_order("KRW-ETH", unitAmount)
                        # wait until the order is fully executed
                        while True:
                            order_info = upbit.get_order(buyResult["uuid"])
                            if order_info["state"] == "done":
                                for trade in order_info["trades"]:
                                    trade_price = float(trade["price"])
                                    trade_qty = float(trade["volume"])
                                    print(f"Price: {trade_price}, Qty: {trade_qty}")
                                last_eth_price = trade_price
                                buy_no = buy_no + 1
                            break
                        sellResult = upbit.sell_limit_order("KRW-ETH", round(trade_price*profit_ratio,-3),trade_qty)
                        order_info = upbit.get_order(sellResult["uuid"])
                        sell_uuid.append(order_info["uuid"])
                        print("매도대기건수:", len(sell_uuid))
                        print("0이면 이상 무, 아니면 이상함 :",buy_no - sell_no - len(sell_uuid))
                        print("원화잔고 :", get_balance("KRW"), ", 이더리움 잔고 :", get_balance("ETH"))
                    else :
                        print("잔고가 부족합니다.")
                else :
                    if len(sell_uuid) > 0:
                        order_info = upbit.get_order(sell_uuid[len(sell_uuid)-1])
                        if order_info["state"] == "done":
                            print(order_info)
                            sell_no = sell_no + 1
                            del sell_uuid[len(sell_uuid)-1]
                            print(order_info)
                            print("0이면 이상 무, 아니면 이상함 :",{buy_no}-{sell_no}-{len(sell_uuid)})
                            print("원화잔고 :", get_balance("KRW"), ", 이더리움 잔고 :", get_balance("ETH"))
            except Exception as e:
                print (e)
                wm.terminate()






