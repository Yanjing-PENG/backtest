# -*- encoding: utf-8 -*-

from datetime import datetime, timedelta
import os
import pickle

def getData(thscode,start_time, end_time):
    """
    # get relevant data
    - - - - - - - - - - - - - - - - - - - - - -
    # Inputs:
      thscode      security ID
      start_time   backtest start time, format in "2018-01-01 09:15:00"
      end_time     backtest ent time, format in  "2019-06-30 15:15:00"
    - - - - - - - - - - - - - - - - - - - - - -
    # Outputs:
      data_1m      candlestick data for 1 minute cycle， the data type is DICTIONARY
    """

    if os.path.exists(os.getcwd() + '/data/' + start_time[:10].replace('-','') + '_' + end_time[:10].replace('-','') + '.pkl'):
        f = open(os.getcwd() + '/data/' + start_time[:10].replace('-','') + '_' + end_time[:10].replace('-','') + '.pkl', 'rb')
        data = pickle.load(f)
        f.close()

    else:
        print("The data does not exist")

    return data

if __name__ == '__main__':
    data = getData('IF', '2010-04-16 09:15:00', '2019-07-31 15:15:00')
    print(data)