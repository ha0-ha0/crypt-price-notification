"""
 bitbank から xrp のローソク足を取得（日足）
"""
from datetime import datetime, date, timedelta
import requests
import time
#python_bitbankccのパッケージをインポート
import python_bitbankcc

# public API classのオブジェクトを取得
pub = python_bitbankcc.public()

#今日
now_info = datetime.today()
now = now_info.strftime( "%Y-%m-%d %H:%M" )
#昨日
yesterday_info = now_info - timedelta( days = 1 )
yesterday = yesterday_info.strftime( "%Y%m%d" )

value = pub.get_ticker( 'xrp_jpy' )
"""
    sell: 現在の売り注文の最安値
    buy: 現在の買い注文の最安値
    high: 過去24時間の最高値取引価格
    low: 過去24時間の最安値取引価格
    last: 最新取引価格
    vol: 過去24時間の出来高
"""
last_price = value['last']
data = ['xrp_jpy', last_price, now]

# 前日の9:00のxrpの価格
prev_value = pub.get_candlestick('xrp_jpy',  '1hour', yesterday)
prev_candle = prev_value['candlestick'][0]
prev_price = prev_candle['ohlcv'][0][0]

# 前日比
rate = float(last_price) / float(prev_price) * 100
rate = rate - 100
rate = round(rate,2)

#最新取引価格
print('最新取引価格:' + last_price)
print('前日取引価格:' + prev_price)
print('前日比:' + str(rate) + '%')

#
# 実行するとlineに通知がいくようになる
#
def LineNotify( message ):
    line_notify_token = "LINETOKEN"
    line_notify_api = "https://notify-api.line.me/api/notify"

    payload = {"message":message}
    headers = {"Authorization":"Bearer " + line_notify_token}
    requests.post(line_notify_api, data = payload, headers = headers)

message = '現在価格は:' + last_price + '円、' + '前日価格は:' + prev_price + '円、前日比は' + str(rate) + '%'

LineNotify(message)
