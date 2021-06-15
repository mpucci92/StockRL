import pandas as pd
import yfinance as yf
import os


def getData(ticker, startDate, endDate):
    df = yf.download(ticker,
                     start=startDate,
                     end=endDate,
                     progress=False)

    return df

def cleanData(dataframe):
    dataframe.reset_index(inplace=True)
    dataframe.drop(['Adj Close'], axis=1, inplace=True)

    return dataframe


def saveData(dataframe, ticker):
    filename = 'GetData.py'
    path = os.path.abspath(filename)
    directory = os.path.dirname(path)
    saveLocation = directory + "\\Data\\"

    # +'\data\'

    dataframe.to_csv(saveLocation + f'{ticker}.csv')


if __name__ == "__main__":
    """
    Input the ticker to download, the start time and the end time for the range to query ticker data upon.
    Return: Dataframe containing ticker data of the selected company of choice.
    """

    ticker = 'TSLA'
    startDate = '2010-01-01'
    endDate = '2021-06-11'

    df = getData(ticker, startDate, endDate)
    df = cleanData(df)
    saveData(df, ticker)