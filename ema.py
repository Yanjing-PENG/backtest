# -*- encoding:utf-8 -*-

import pandas as pd
import numpy as np

def ema(data_1m, ema_short, ema_long):
    """
    ## Calculate EMA
    - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    ## Inputs:
    #  data_1m          candlestick data for 1 minute cycle
    #  ema_short        EMA parameter of shorter cycle
    #  ema_long         EMA parameter of longer cycle
    - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    ## Outputs:
    #  data_1m          candlestick data with EMA
    - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    """
    # inspect the parameters
    if not (ema_long>0 and ema_short>0 and ema_long>ema_short):
        raise Exception('ema_long should be larger than ema_short，please reenter')

    # calculate indicators
    for item in data_1m.keys():
        # initialize ema
        data_1m[item]['ema_short'] = 0
        data_1m[item]['ema_long'] = 0
        data_1m[item].iloc[0,3] = data_1m[item].iloc[0,2]
        data_1m[item].iloc[0,4] = data_1m[item].iloc[0,2]

        for i in range(1,len(data_1m[item])):
            data_1m[item].iloc[i,3] = ((ema_short-1)/(ema_short+1))*data_1m[item].iloc[i-1,3] + (2/(ema_short+1))*data_1m[item].iloc[i,2]
            data_1m[item].iloc[i,4] = ((ema_long-1)/(ema_long+1))*data_1m[item].iloc[i-1,4] + (2/(ema_long+1))*data_1m[item].iloc[i,2]

    return data_1m

