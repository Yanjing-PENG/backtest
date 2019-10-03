# -*- encoding: utf-8 -*-

from addorder import addorder
import pandas as pd

def signaltrade(data_1m, loss_ratio, quantity=1, fee_rate=0.0001):
    """
    ## basing on signals and the strategy to do the backtest simulation
    - - - - - - - - - - - - - - - - - - - - - - - - - - -
    ## Inputs:
    #  data_1m        candlesticks data of 1 minute cycle
    #  quantity       security quantity for each trade
    #  fee_rate       commission fee rate
    - - - - - - - - - - - - - - - - - - - - - - - - - - -
    ## Outputs:
    #  data_1m        data with trade signals
    #  orderbook      order history
    """
    # initialize order book and backtest tradedate
    orderbook = {}
    tradedate = {}

    # loops basing on contracts
    for i in data_1m.keys():
        # get the i-th contract's data
        data_1m_i = data_1m[i]

        # get the last trade date
        expire_date = data_1m_i.iloc[-1,0].split(' ')[0]
        clear_time = '14:00'

        # initialize signals
        con_1 = 0
        con_2 = 0
        data_1m_i['order'] = 0

        # initialize the i-th contract's orderbook
        orderbook[i] = pd.DataFrame(columns=['datetime','price','quantity','fee','pnl','type'])

        # get the i-th contract's tradedate
        tradedate[i] = data_1m_i['time'].str.split(' ',expand=True)[0].drop_duplicates(keep='first').tolist()

        # loops basing on time
        for j in data_1m_i.index.tolist()[2:]:

            # get trade signals
            con_1 = (data_1m_i.loc[j-1,'ema_short']<=data_1m_i.loc[j-1,'ema_long'] and data_1m_i.loc[j,'ema_short']>data_1m_i.loc[j,'ema_long'])  # ema_short上穿ema_long
            con_2 = (data_1m_i.loc[j-1,'ema_short']>=data_1m_i.loc[j-1,'ema_long'] and data_1m_i.loc[j,'ema_short']<data_1m_i.loc[j,'ema_long'])  # ema_short下穿ema_long
            c = data_1m_i.loc[j, 'close']
            # excute trades
            if data_1m_i.loc[j,'time'] !=  (expire_date+' '+clear_time):
                if data_1m_i['order'].sum() == 0 and con_1:   # open long position
                    orderbook[i] = addorder(orderbook[i], [data_1m_i.loc[j, 'time'], c, quantity, fee_rate], '开多')
                    data_1m_i.loc[j, 'order'] = 1
                    threshold_price = c*(1-loss_ratio)

                if data_1m_i['order'].sum() == 1 and data_1m_i.loc[j,'close']< threshold_price:   # close long position
                    if con_2:
                        orderbook[i] = addorder(orderbook[i], [data_1m_i.loc[j, 'time'], c, -quantity, fee_rate], '平多')
                        orderbook[i] = addorder(orderbook[i], [data_1m_i.loc[j, 'time'], c, -quantity, fee_rate], '开空')
                        data_1m_i.loc[j, 'order'] = -2
                        threshold_price = c*(1+loss_ratio)
                    else:
                        orderbook[i] = addorder(orderbook[i], [data_1m_i.loc[j, 'time'], c, -quantity, fee_rate], '平多')
                        data_1m_i.loc[j, 'order'] = -1

                if data_1m_i['order'].sum() == 1 and con_2 and data_1m_i.loc[j, 'close'] >= threshold_price:  # keep holding long position
                    threshold_price = threshold_price + (data_1m_i.loc[j, 'close']-threshold_price)*0.5

                if data_1m_i['order'].sum() == 0 and con_2:  # open short position
                    orderbook[i] = addorder(orderbook[i], [data_1m_i.loc[j, 'time'], c, -quantity, fee_rate], '开空')
                    data_1m_i.loc[j, 'order'] = -1
                    threshold_price = c*(1+loss_ratio)

                if data_1m_i['order'].sum() == -1 and data_1m_i.loc[j, 'close'] > threshold_price:  # close short position
                    if con_1:
                        orderbook[i] = addorder(orderbook[i], [data_1m_i.loc[j, 'time'], c, quantity, fee_rate], '平空')
                        orderbook[i] = addorder(orderbook[i], [data_1m_i.loc[j, 'time'], c, quantity, fee_rate], '开多')
                        data_1m_i.loc[j, 'order'] = 2
                        threshold_price = c*(1-loss_ratio)
                    else:
                        orderbook[i] = addorder(orderbook[i], [data_1m_i.loc[j, 'time'], c, quantity, fee_rate], '平空')
                        data_1m_i.loc[j, 'order'] = 1

                if data_1m_i['order'].sum() == -1 and con_1 and data_1m_i.loc[j, 'close'] <= threshold_price:  # keep holding short position
                    threshold_price = threshold_price - (threshold_price-data_1m_i.loc[j, 'close'])*0.5

                else:
                    pass

            else:
                if data_1m_i['order'].sum() == 1:   # close long position on the last trade date
                    orderbook[i] = addorder(orderbook[i], [data_1m_i.loc[j, 'time'], c, -quantity, fee_rate], '最后交易日平多')
                    data_1m_i.loc[j, 'order'] = -1
                    data_1m_i.loc[j, 'ordertype'] = '最后交易日平多'
                    break

                elif data_1m_i['order'].sum() == -1:   # close short position on the last trade date
                    orderbook[i] = addorder(orderbook[i], [data_1m_i.loc[j, 'time'], c, quantity, fee_rate], '最后交易日平空')
                    data_1m_i.loc[j, 'order'] = 1
                    data_1m_i.loc[j, 'ordertype'] = '最后交易日平空'
                    break

                else:
                    break

    return [data_1m, orderbook, tradedate]
