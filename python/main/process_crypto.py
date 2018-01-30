"""
[u'24h_volume_usd', u'available_supply', u'id', u'last_updated',
       u'market_cap_usd', u'max_supply', u'name', u'percent_change_1h',
       u'percent_change_24h', u'percent_change_7d', u'price_btc', u'price_usd',
       u'rank', u'symbol', u'total_supply']
"""

import  pandas as pd
import time
import sys, traceback


from utils import *
from email_sender import *

#check if price %change is more than 10% and send email
def get_crypto_data(cryto_df,interval, old_price,old_vol, old_rank):

    new_price = cryto_df.price_usd
    ticker = cryto_df.symbol
    name = cryto_df.id
    #updated_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(cryto_df.last_updated))
    updated_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    new_vol = cryto_df["24h_volume_usd"]
    new_rank = cryto_df["rank"]

    # Logic for Percentage change decider
    perc_change_n_mins = get_percentage_change(old_price, new_price)
    vol_per_change = get_percentage_change(old_vol, new_vol)
    rank_change = get_rank_change(old_rank, new_rank)

    return (ticker, name, perc_change_n_mins, new_price, vol_per_change, rank_change, new_rank,updated_time)


# New method for notyfying all cryptos

def process_all_cryptos(args):
    prev_per_change_dict = {}
    prev_vol = {}
    prev_rank = {}

    while True:

        crypto_data_list = []
        try:

            cryto_df = pd.read_json("https://api.coinmarketcap.com/v1/ticker/?limit="+str(args.top))

            print("Data fetched at: " + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))

            for idx, row in cryto_df.iterrows():

                # initializaton for all tickers
                if row.id not in prev_per_change_dict: prev_per_change_dict[row.id] = -1
                if row.id not in prev_vol: prev_vol[row.id] = -1
                if row.id not in prev_rank: prev_rank[row.id] = 0

                # check if the price % change is more than 10%
                price_change = get_percentage_change(prev_per_change_dict[row.id], row.price_usd)
                # print(price_change)
                if (price_change >= 5):
                    print("detected: "+ str(price_change))
                    crypto_data_list.append(
                        get_crypto_data(row, args.interval, prev_per_change_dict[row.id],\
                                        prev_vol[row.id], prev_rank[row.id]))

                prev_per_change_dict[row.id] = row.price_usd
                prev_vol[row.id] = row["24h_volume_usd"]
                prev_rank[row.id] = row["rank"]


            # Send an email
            if crypto_data_list:
                sorted_by_price = sorted(crypto_data_list, key=lambda tup: tup[2], reverse=True)
                email_response = get_html_response(sorted_by_price)
                recipients = get_recipients()
                sender = "ddcryptonotification@gmail.com"
                subject = "DDCryptoAlert"
                send_email(sender, recipients, subject, email_response)
                print (str (len(sorted_by_price)) + "changes sent")

        except:
            print "Exception in user code:"
            print '-' * 60
            traceback.print_exc(file=sys.stdout)
            print '-' * 60

        time.sleep(args.interval * 60)









