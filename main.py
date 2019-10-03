# -*- encoding:utf-8 -*-

from getdata import getData
from ema import ema
from signaltrade import signaltrade
from tradestats import tradestats
from plot import plot_net_value

import os
import pandas as pd

# set the display parameters for pandas DataFrame
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

def backtest(test_type='IF', st_time='2010-04-16 09:15:00', en_time='2019-07-31 15:15:00',ema_s=180, ema_l=240):

    # set some basic parameters
    code_type = test_type
    start_time = st_time
    end_time = en_time
    init_capital = 3000
    quantity = 1
    fee_rate = 0.0001

    # do the backtest
    data = getData(code_type, start_time, end_time)
    data_1m_with_ema = ema(data[0], ema_s, ema_l)
    signaltrade_result = signaltrade(data_1m_with_ema, 0.003, quantity, fee_rate)

    # get detailed backtest performance
    stats_detail = {}
    for item in signaltrade_result[1].keys():
        stats_detail[item] = tradestats(signaltrade_result[1][item], init_capital, signaltrade_result[2][item])

    # get overall backtest performance
    code_list = list(signaltrade_result[1].keys())
    orderbook_total = signaltrade_result[1][code_list[0]]
    tradedate_total = signaltrade_result[2][code_list[0]]

    for i in range(1,len(code_list),1):
        orderbook_total = pd.concat([orderbook_total, signaltrade_result[1][code_list[i]]], axis=0)
        tradedate_total.extend(signaltrade_result[2][code_list[i]])

    stats_total = tradestats(orderbook_total, init_capital, tradedate_total)

    # save backtest performance into excel file
    writer = pd.ExcelWriter(os.getcwd() + '/result/' + 'backtest_result_' + start_time[:10].replace('-', '') + '-' + end_time[:10].replace('-', '') + '.xlsx')

    stats = pd.DataFrame(
        columns=['code', 'num_trades', 'percent_win', 'pnl_total', 'total_win', 'total_loss', 'pnl_avg', 'max_win',
                 'max_loss', 'maxdrawdown_ratio', 'max_active_drawdown_ratio', 'daypnl_avg', 'daypnl_std', 'annsharp'])
    for item in stats_detail.keys():
        stats = stats.append(
            {'code': item, 'num_trades': stats_detail[item].iloc[0, 0], 'percent_win': stats_detail[item].iloc[0, 1],
             'pnl_total': stats_detail[item].iloc[0, 2], 'total_win': stats_detail[item].iloc[0, 3], 'total_loss': stats_detail[item].iloc[0, 4],
             'pnl_avg': stats_detail[item].iloc[0, 5], 'max_win': stats_detail[item].iloc[0, 6], 'max_loss': stats_detail[item].iloc[0, 7],
             'maxdrawdown_ratio': stats_detail[item].iloc[0, 9], 'max_active_drawdown_ratio': stats_detail[item].iloc[0, 11],
             'daypnl_avg': stats_detail[item].iloc[0, 12], 'daypnl_std': stats_detail[item].iloc[0, 13], 'annsharp': stats_detail[item].iloc[0, 14]}, ignore_index=True)

    stats = stats.append({'code': 'total', 'num_trades': stats_total.iloc[0, 0], 'percent_win': stats_total.iloc[0, 1],
                          'pnl_total': stats_total.iloc[0, 2], 'total_win': stats_total.iloc[0, 3], 'total_loss': stats_total.iloc[0, 4],
                          'pnl_avg': stats_total.iloc[0, 5], 'max_win': stats_total.iloc[0, 6], 'max_loss': stats_total.iloc[0, 7],
                          'maxdrawdown_ratio': stats_total.iloc[0, 9], 'max_active_drawdown_ratio': stats_total.iloc[0, 11],
                          'daypnl_avg': stats_total.iloc[0, 12], 'daypnl_std': stats_total.iloc[0, 13], 'annsharp': stats_total.iloc[0, 14]}, ignore_index=True)

    stats.to_excel(writer, 'stats', index=False)

    orderbook_total.to_excel(writer, 'orderbook_total', index=False)

    for item in signaltrade_result[1].keys():
        signaltrade_result[1][item].to_excel(writer, item, index=False)

    writer.save()

    # plot the net value figure
    plot_net_value(orderbook_total, start_time[:16], end_time[:16], init_capital)

    # print out the backtest performance
    print('-------------------------------------------------------------------------------')
    print(stats_total)
    print('-------------------------------------------------------------------------------')

if __name__ == '__main__':
    backtest('IF', '2010-04-16 09:15:00', '2019-07-31 15:15:00', 180, 240)