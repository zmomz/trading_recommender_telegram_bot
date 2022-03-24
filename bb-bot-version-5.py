import ta
import ccxt
import pandas as pd
import telegram
import schedule
import time
import datetime


# change the symbol as you wish ex:'BTC/USDT' for bitcoin
symbols =[
            "ETH/USDT"
        ]
# you can change the exchange to Binance by using ccxt.binance()
# BTW no need for Auth or API-keys,, all actions are through public-API
exchange = ccxt.binance(config={
    'enableRateLimit': True
})

# Telegram bot connected by this token is @bbrsibot
telegram_keys = {
    'test':'write your key',
    'live':"Write your key"
}

telegram_token= telegram_keys['test']

# limit of fetched data columns, you choose one of them ... 
# (full_day_limit = 1+ (24h * 60m) / timeframe)

full_day_limit_5_m = 289
full_day_limit_15_m = 97
full_day_limit_1_h = 25

# list of all open chats, started empty
all_chat_ids = []
buy_list = []
sell_list= []

telegram_bot = telegram.Bot(telegram_token)

# fetching all updates from open conversations
updates = telegram_bot.get_updates()

#check open chats
def update_chat_list(updates):
    for update in updates:
        all_chat_ids.append(update.message.from_user.id)


# preparing OHLCV dataframe
def data_processing():
    df = pd.DataFrame()
    for symbol in symbols:
        ohlcv = exchange.fetchOHLCV (symbol, timeframe = '5m', limit = full_day_limit_5_m,)     
        df[f"{symbol}"] = [x[4] for x in ohlcv]
    # print(df)
    return df

def bbdata_processing(df):
    # adding Bollinger Band
    for pair in df.columns:
        indicator_bb = ta.volatility.BollingerBands(close=df[f"{pair}"], window=21)
        df[f'{pair}-HBB'] = indicator_bb.bollinger_hband()
        df[f'{pair}-LBB'] = indicator_bb.bollinger_lband()
        # Adding Relative stringth index
        df[f'{pair}-RSI']=ta.momentum.rsi(df[f"{pair}"],window=21)
        #removing missing data
        # print(coin)
    return df
# bbdata_processing(data_processing())
#Indecator logic
def logic(df):
    status=[]
    for symbol in symbols:

        current_close = df[f'{symbol}'].iloc[-1]        # value of last candle close
        current_HBB = df[f'{symbol}-HBB'].iloc[-1]      # High Bollinger Band
        current_LBB = df[f'{symbol}-LBB'].iloc[-1]      # low Bollinger Band
        current_RSI = df[f'{symbol}-RSI'].iloc[-1]      # Relative Strength Indicator

        # Notification message logic

        # indicator of overbought ..
        if current_close > current_HBB and current_RSI >= 70:

            #checking if we already notified the investor to sell
            if symbol not in sell_list: 

                print(f"\noverbought\n {symbol}\nclose: {current_close}\nHBB: {current_HBB}\nLBB: {current_LBB}\nRSI: {current_RSI}")
                # message for overbought
                status.append(f"🟥  <b>SELL</b> [<b>{symbol}</b>]\n[{datetime.datetime.now().strftime('%H:%M:%S')} AST]\nCurrent status: Overbought.\nPrice: $ {current_close}\nClose is above BBH & RSI above 70 \n\nRecommendation: start selling... \n\nfor Algo-trading bots \ncontact us in:\nhttps://linktr.ee/ABTTrading ")
                
                # recording the notification
                sell_list.append(symbol)

                # removing the previos record of buying if any 
                if symbol in buy_list:
                    buy_list.remove(symbol)

        # indicator of oversold ..
        elif current_close < current_LBB and current_RSI <= 35:

            #checking if we already notified the investor to buy
            if symbol not in buy_list:
                print(f"\noversold\n {symbol}\nclose: {current_close}\nHBB: {current_HBB}\nLBB: {current_LBB}\nRSI: {current_RSI}")
                # message for oversold
                status.append(f"🟩  <b>BUY</b> [<b>{symbol}</b>]\n[{datetime.datetime.now().strftime('%H:%M:%S')} AST]\nPrice: $ {current_close}\nCurrent status: Oversold.\nClose is lower than BBL & RSI is less than 35 \n\nRecommendation: start buying... \n\nfor Algo-trading bots \ncontact us in:\nhttps://linktr.ee/ABTTrading ")  

                # recording the notification
                buy_list.append(symbol)

                # removing the previos record of selling if any
                if symbol in sell_list:
                    sell_list.remove(symbol)

        else:
            print(f"\n\n {symbol}\nclose: {current_close}\nHBB: {current_HBB}\nLBB: {current_LBB}\nRSI: {current_RSI}")
    return status

# sending the message for all open chats
def notify(status, chat_ids):
    if len(chat_ids) > 0:
        if len(status) > 0:
            for id in chat_ids:
                for txt in status:
                    telegram_bot.send_message(text= txt, chat_id=id, parse_mode=telegram.ParseMode.HTML)


# dummy function for checking if the bot is working or not
# def am_still_running(chat_ids):
#     for id in chat_ids:
#         telegram_bot.send_message(text= f"am still running in chat: {id}", chat_id=id)


#schedule job, running all above functions every specified period
def job():
    global updates
    update_chat_list(updates)
    row_data = data_processing()
    bbdata = bbdata_processing(row_data)
    status = logic(bbdata)
    notify(status, list(set(all_chat_ids)))

# main function,runs the schedule job(), you can specify lag period from the while loop
def watcher(chat_ids = list(set(all_chat_ids))):    
    schedule.every(10).seconds.do(job)
    # schedule.every(3).hours.do(am_still_running, chat_ids = chat_ids)
    print('watching BB')
    while True:
        schedule.run_pending()
        time.sleep(5)

watcher()