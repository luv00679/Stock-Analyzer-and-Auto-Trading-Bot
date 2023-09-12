# libraries:
import requests as rq
import yfinance as yf
import pandas as pd
import numpy as np
import io
from SmartApi import SmartConnect
import pyotp

# Main function
def main():
    """
    Calls all the function.
    """
    buy(strategy(get_stocks()))

# Function to find compound interest after 10 years
def rate(A,P):
    """
    Calculates the compund interest rate.
    Parameters:
    A (float): Final amount after 10 years.
    B (float): Principle amount.

    Returns:
    (float): The rate of compounf interest.
    """
    return (pow(A/P,1/10)-1)*100

def get_stocks():
    """
    Function gets the list of all the stocks in nifty 500.
    It then retrive the closing price of all those stocks in 10 years.
    It returns this data in the form of dataframe to be further analysed.

    Returns:
    DataFrame: Containing data about 10yrs of closing price of all nifty 500 stocks
    """
    #url gives a json response containing list of nifty 500 stocks
    url = "https://archives.nseindia.com/content/indices/ind_nifty500list.csv"
    response = rq.get(url)
    df = pd.read_csv(io.StringIO(response.text))
    stock_data = pd.DataFrame()
    close_series_list = []
    #loop collects and stores the data in pandas data frame "stock_data"
    for symbol in df["Symbol"]:
        stock_prices = yf.Ticker(symbol + ".NS").history(period="10y")
        close_prices = stock_prices['Close']
        close_series_list.append(close_prices)
        stock_data = pd.concat(close_series_list, axis=1, keys=df["Symbol"])
    return stock_data

def strategy(n):
    """
    This function analyses and finds the best stock from the data frame.
    First it checks for stocks that have given 13 or above returns in 10 yrs.
    Second it finds the percentage difference between the mean of price in 10yrs and current price
    Third it sorts the data frame with percentage difference and returns the stock with the highest difference.
    Parameter:
    n (pandas dataframe): Data Frame containing data of nifty 500 stocks

    Output:
    string (str): The name of stock
    float (float): The price of the stock

    Return:
    string (str): The name of the stock to buy
    """
    # f will contain the names of stocks
    f=[]
    for j in n.columns:
        f.append(j)
    df=pd.DataFrame()
    # k have the list of mean values of the stocks in 10yrs
    k=n.mean()
    for i in range(len(n.columns)):
        g=n[f[i]][len(n.index)-1] # latest price of a stock
        a=float(k[i])   # mean of a stock
        comp=rate(g,n[f[i]][0])     # finding the compound rate of the sotck
        pcnt_diff=((g-a)/a)*100     # Price difference of the stock b/w mean and current

        if comp>13:
            if g>a and g<a*(1.25) and pcnt_diff>5:
                data={
                    "name":f[i],
                    "rate":comp,
                    "Mean of 10yrs":a,
                    "Current Value":g,
                    "percentage_diff":pcnt_diff
                }
                df=df._append(data,ignore_index=True)
    df=df.sort_values("percentage_diff",ascending=False,ignore_index=True)
    print(df)
    print(df["name"][0],df["Current Value"][0])
    return df["name"][0]


def buy(n):
    '''
    This function buys the stock. User has to enter the API key, ClientID, PIN and how much quantity they want to buy
    PARAMETERS:
    n (str): Name of the stock

    INPUT:
    API key: API key of there smart api account
    Cliend ID: ID of there angel one account
    PIN: PIN of there angel one account
    Quantity: How much quantity they want to buy of the stock

    OUTPUT:
    Order Id.....      /
    Error
    '''
    api_key = input("api-key: ")
    clientId = input("Client-id: ")
    pwd = input("PIN: ")
    quantity=input("Quantity:")
    smartApi = SmartConnect(api_key)
    token = "XEHNL63BNPNQU2C6VYMZKBL3R4"
    totp=pyotp.TOTP(token).now()
    correlation_id = "abc123"

    # login api call

    data = smartApi.generateSession(clientId, pwd, totp)
    # print(data)
    authToken = data['data']['jwtToken']
    refreshToken = data['data']['refreshToken']

    # fetch the feedtoken
    feedToken = smartApi.getfeedToken()

    # fetch User Profile
    res = smartApi.getProfile(refreshToken)
    smartApi.generateToken(refreshToken)
    res=res['data']['exchanges']
    data=rq.get("https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json")
    df=pd.read_json(data.text)
    a=df.loc[df['symbol']==n]
    trading_symbol=a['symbol'].item()
    exchange=a['exch_seg'].item()
    token=a['token'].item()

    # parameters of the order
    try:
        orderparams = {
            "variety": "NORMAL",
            "tradingsymbol": trading_symbol,
            "symboltoken": token,
            "transactiontype": "BUY",
            "exchange": exchange,
            "ordertype": "MARKET",
            "producttype": "DELIVERY",
            "duration": "DAY",
            "squareoff": '0',
            "stoploss": '0',
            "quantity": quantity
            }
        orderId=smartApi.placeOrder(orderparams)
        print("The order id is: {}".format(orderId))
    except Exception as e:
        print("Order placement failed: {}".format(e))


if __name__ == "__main__":
    main()