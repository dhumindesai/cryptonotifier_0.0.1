from __future__ import division
import pandas as pd

#Grab top 10 tickers
def get_top_n_tickers(n):
    top_n_df = pd.read_json("https://api.coinmarketcap.com/v1/ticker/?limit="+str(n))
    return top_n_df.id.tolist()

#Calculate the % change in price from previous interval
def get_percentage_change(previous, latest):
    if(previous == -1):
        return 0
    else:
        return round ((latest - previous)*100/previous , 3)

#Calculate rank change
def get_rank_change(old_rank, new_rank):
    change = old_rank - new_rank
    if change >= 0 : return "+" + str(change)
    if old_rank == 0: return 0
    else: return str(change)

#make html response for email
def get_html_response( crypto_data_list ):

    response = """
    <head>
      <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
      <title>html title</title>
      <style type="text/css" media="screen">
        table{
            background-color: gray;
            empty-cells:hide;
        }
        td.cell{
            background-color: white;
        }
      </style>
    </head>"""

    response += """
    <body>
      <h3> Significant Price actions in the last hour: </h3>
      <h4>Updated at {crypto_data_list[0][7]}</h4>
      <table style="border: gray 1px solid;">
      <tbody>
        <tr>
            <td class="cell">Ticker</td>
            <td class="cell">Coin</td>
            <td class="cell">Price % change</td>
            <td class="cell">Current Price</td>
            <td class="cell">Vol. % change</td>
            <td class="cell">Rank change</td>
        </tr>
        """.format(crypto_data_list =crypto_data_list)

    for coin in crypto_data_list:
        response +=  """
        <tr>
            <td class="cell">{coin[0]}</td>
            <td class="cell">{coin[1]}</td>
            <td class="cell">{coin[2]}</td>
            <td class="cell">{coin[3]}</td>
            <td class="cell">{coin[4]}</td>
            <td class="cell">{coin[6]}({coin[5]})</td>
        </tr>
                    """\
            .format(coin = coin)

    response += """
        </tbody>
      </table>
    </body>
                """

    return response

if __name__ == "__main__":
    #print get_html_response([("ticker","ticker", "ticker", "ticker", "ticker", "ticker", "ticker"),("ticker","ticker", "ticker", "ticker", "ticker", "ticker", "ticker")])
    #print get_percentage_change(11299.4, 11290.9)
    print get_html_response([["CRTM","corethum",93.923, 0.034114, 1.237,"+15", 333,"2018-01-29 14:00:09"]])