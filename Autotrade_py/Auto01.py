import pyupbit
import pyupbit.websocket_api as wsck


access_key = "xxx"
secret_key = "xxx"
upbit = pyupbit.Upbit(access_key, secret_key)

#스토리 보드
#계좌의 잔고 및 이더리움 현재가 확인

balances = upbit.get_balances()
print(balances)

# # total_krw = float(balances[0]['balance'])
# # eth_balance = float(balances[1]['balance'])
# # krw_per_package = total_krw * 0.05
# eth_price = pyupbit.get_current_price("KRW-ETH")

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



