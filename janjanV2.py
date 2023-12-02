
# --- Do not remove these libs ---
from freqtrade.strategy import IStrategy
from typing import Dict, List
from functools import reduce
from pandas import DataFrame
from technical.consensus import Consensus
# --------------------------------
import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib

class janjan(IStrategy):
    INTERFACE_VERSION: int = 3
    minimal_roi = {
        "60":  0.01,
        "30":  0.03,
        "20":  0.04,
        "0":  0.05
    }

    stoploss = -0.10
    timeframe = '15m'
    trailing_stop = False
    trailing_stop_positive = 0.01
    trailing_stop_positive_offset = 0.02
    process_only_new_candles = True
    use_exit_signal = True
    exit_profit_only = True
    ignore_roi_if_entry_signal = False
    # startup_candle_count = 400
    
    plot_config = {
        'main_plot': {
            'ema20': {'color': '#958f5e'},
            'ema25': {'color': '5d04e8'},
            'ema30': {'color': '#5e5618'},
            'ema35': {'color': '#ab517d'},
            'ema40': {'color': '#d6ebd7'},
            'ema50': {'color': '#8834ff'},
            'ema100': {'color': '#da54c9'},
            'ema200': {'color': '#d7580e'},
            },
        }
    

    order_types = {
        'entry': 'limit',
        'exit': 'limit',
        'stoploss': 'market',   
        'stoploss_on_exchange': False
    }
    
    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
    
        dataframe['ema20'] = ta.EMA(dataframe, timeperiod=20)
        dataframe['ema25'] = ta.EMA(dataframe, timeperiod=25)
        dataframe['ema30'] = ta.EMA(dataframe, timeperiod=30)
        dataframe['ema35'] = ta.EMA(dataframe, timeperiod=35)
        dataframe['ema40'] = ta.EMA(dataframe, timeperiod=40)
        dataframe['ema50'] = ta.EMA(dataframe, timeperiod=50)
        dataframe['ema100'] = ta.EMA(dataframe, timeperiod=100)
        dataframe['ema200'] = ta.EMA(dataframe, timeperiod=200)
        # ------------------------------------------------------
        dataframe['ratio4050'] = (100 - ((100 / dataframe['ema40']) * dataframe['ema50']))
        dataframe['ratio3540'] = (100 - ((100 / dataframe['ema35']) * dataframe['ema40']))
        dataframe['ratio3035'] = (100 - ((100 / dataframe['ema30']) * dataframe['ema35']))
        dataframe['ratio2530'] = (100 - ((100 / dataframe['ema25']) * dataframe['ema30']))
        dataframe['ratio2025'] = (100 - ((100 / dataframe['ema20']) * dataframe['ema25']))
        dataframe['ratio50100'] = (100 - ((100 / dataframe['ema50']) * dataframe['ema100']))
        # ------------------------------------------------------
        c = Consensus(dataframe)
        c.evaluate_stoch_rsi()
        dataframe['consensus_buy'] = c.score()['buy']
        dataframe['consensus_sell'] = c.score()['sell']
        #dataframe['k']= c.evaluate_stoch_rsi.stoch_rsi_14_fastk
        #dataframe['k']=c.stoch_rsi_fastk
        #dataframe['d']=c.stoch_rsi_fastd
        
        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                (dataframe['close'] > dataframe['ema30'])&
                (dataframe['ema100'] > dataframe['ema200']) &
                (dataframe['ema50'] < dataframe['ema40']) &
                (dataframe['ema40'] < dataframe['ema35']) &
                (dataframe['ema35'] < dataframe['ema30']) &
                (dataframe['ema30'] < dataframe['ema20']) &
                #
                (dataframe['lowest'].shift(1) > dataframe['ema30'].shift(1)) &
                (dataframe['lowest'].shift(2) > dataframe['ema30'].shift(2)) &
                (dataframe['lowest'].shift(3) > dataframe['ema30'].shift(3)) &
                (dataframe['lowest'].shift(4) > dataframe['ema30'].shift(4)) &
                (dataframe['lowest'].shift(5) > dataframe['ema30'].shift(5)) &
                (dataframe['lowest'].shift(6) > dataframe['ema30'].shift(6)) &
                #
                (dataframe['consensus_buy'] > 34) &
                (dataframe['volume'] > 0)
            ),
            'buy'
        ] = 1
        dataframe.loc[
            (
                      (dataframe['lowest'] > dataframe['ema25'])&
                      (dataframe['ema100'] > dataframe['ema200']) &
                      (dataframe['ema50'] < dataframe['ema40']) &
                      (dataframe['ema40'] < dataframe['ema35']) &
                      (dataframe['ema35'] < dataframe['ema30']) &
                      (dataframe['ema30'] < dataframe['ema20']) &
                      (dataframe['volume'] > 0) &

                     (dataframe['consensus_buy'] > 34) &
                     (dataframe['volume'] > 0)   

                      (dataframe['lowest'].shift(1) > dataframe['ema25'].shift(1)) &
                      (dataframe['lowest'].shift(2) > dataframe['ema25'].shift(2)) &
                      (dataframe['lowest'].shift(3) > dataframe['ema25'].shift(3)) &
                      (dataframe['lowest'].shift(4) > dataframe['ema25'].shift(4)) &
                      (dataframe['lowest'].shift(5) > dataframe['ema25'].shift(5)) &
                      (dataframe['lowest'].shift(8) > dataframe['ema25'].shift(8)) &
                      (dataframe['lowest'].shift(10) > dataframe['ema25'].shift(10)) &
                      (dataframe['lowest'].shift(12) > dataframe['ema25'].shift(12)) &
                      (dataframe['lowest'].shift(14) > dataframe['ema25'].shift(14)) &
                      (dataframe['lowest'].shift(16) > dataframe['ema25'].shift(16)) &
                      (dataframe['lowest'] > dataframe['lowest'] .shift(8)) &
                      (dataframe['lowest'] > dataframe['lowest'] .shift(9)) &
                      (dataframe['lowest'] > dataframe['lowest'] .shift(10)) 

            ),
            ['buy', 'buy_tag']] = (1, 'AddedMoreCloseCandle')  
        dataframe.loc[
            (
                      (dataframe['lowest'] > dataframe['ema25'])&
                      (dataframe['ema100'] > dataframe['ema200']) &
                      (dataframe['ema50'] < dataframe['ema40']) &
                      (dataframe['ema40'] < dataframe['ema35']) &
                      (dataframe['ema35'] < dataframe['ema30']) &
                      (dataframe['ema30'] < dataframe['ema20']) &
                      (dataframe['volume'] > 0) &

                     (dataframe['consensus_buy'] > 34) &
                     (dataframe['volume'] > 0)   

                      (dataframe['lowest'] > dataframe['ema30']) &
                      (dataframe['lowest'].shift(1) > dataframe['ema25'].shift(1)) &
                      (dataframe['lowest'].shift(2) > dataframe['ema25'].shift(2)) &
                      (dataframe['lowest'].shift(3) > dataframe['ema25'].shift(3)) &
                      (dataframe['lowest'].shift(4) > dataframe['ema25'].shift(4)) &
                      (dataframe['lowest'].shift(5) > dataframe['ema25'].shift(5)) &
                      (dataframe['lowest'].shift(8) > dataframe['ema25'].shift(8)) &
                      (dataframe['lowest'].shift(10) > dataframe['ema25'].shift(10)) &
                      (dataframe['lowest'].shift(12) > dataframe['ema25'].shift(12)) &
                      (dataframe['lowest'].shift(14) > dataframe['ema25'].shift(14)) &
                      (dataframe['lowest'].shift(16) > dataframe['ema25'].shift(16)) &
                      (dataframe['lowest'] > dataframe['lowest'] .shift(8)) &
                      (dataframe['lowest'] > dataframe['lowest'] .shift(9)) &
                      (dataframe['lowest'] > dataframe['lowest'] .shift(10)) &

                      (100 - ((100 / dataframe['ema35'].shift(1)) * dataframe['ema40'].shift(1))) >= 0.023341792 &
                      (100 - ((100 / dataframe['ema35'].shift(3)) * dataframe['ema40'].shift(3))) >= 0.023341792 &
                      (100 - ((100 / dataframe['ema35'].shift(5)) * dataframe['ema40'].shift(5))) >= 0.023341792 &
                      (100 - ((100 / dataframe['ema35'].shift(7)) * dataframe['ema40'].shift(7))) >= 0.023341792 &
                      (100 - ((100 / dataframe['ema35'].shift(9)) * dataframe['ema40'].shift(9))) >= 0.023341792 &
                      (100 - ((100 / dataframe['ema35'].shift(11)) * dataframe['ema40'].shift(11))) >= 0.023341792 &
                      (100 - ((100 / dataframe['ema35'].shift(14)) * dataframe['ema40'].shift(14))) >= 0.023341792 &  # 100 -200 arasında açıyada belki bakılabilir, oversold <10


                      (100 - ((100 / dataframe['ema40'].shift(1)) * dataframe['ema50'].shift(1))) >= 0.023341792 &
                      (100 - ((100 / dataframe['ema40'].shift(3)) * dataframe['ema50'].shift(3))) >= 0.023341792 &
                      (100 - ((100 / dataframe['ema40'].shift(5)) * dataframe['ema50'].shift(5))) >= 0.023341792 &
                      (100 - ((100 / dataframe['ema40'].shift(7)) * dataframe['ema50'].shift(7))) >= 0.023341792 &
                      (100 - ((100 / dataframe['ema40'].shift(9)) * dataframe['ema50'].shift(9))) >= 0.023341792 &
                      (100 - ((100 / dataframe['ema40'].shift(11)) * dataframe['ema50'].shift(11))) >= 0.023341792 &
                      (100 - ((100 / dataframe['ema40'].shift(14)) * dataframe['ema50'].shift(14))) >= 0.023341792 &


                      (100 - ((100 / dataframe['ema30'].shift(1)) * dataframe['ema35'].shift(1))) >= 0.023341792 &
                      (100 - ((100 / dataframe['ema30'].shift(3)) * dataframe['ema35'].shift(3))) >= 0.023341792 &
                      (100 - ((100 / dataframe['ema30'].shift(5)) * dataframe['ema35'].shift(5))) >= 0.023341792 &
                      (100 - ((100 / dataframe['ema30'].shift(7)) * dataframe['ema35'].shift(7))) >= 0.023341792 &
                      (100 - ((100 / dataframe['ema30'].shift(9)) * dataframe['ema35'].shift(9))) >= 0.023341792 &
                      (100 - ((100 / dataframe['ema30'].shift(11)) * dataframe['ema35'].shift(11))) >= 0.023341792 &
                      (100 - ((100 / dataframe['ema30'].shift(14)) * dataframe['ema35'].shift(14))) >= 0.023341792 &


                      (100 - ((100 / dataframe['ema25'].shift(1)) * dataframe['ema30'].shift(1))) >= 0.023341792 &
                      (100 - ((100 / dataframe['ema25'].shift(3)) * dataframe['ema30'].shift(3))) >= 0.023341792 &
                      (100 - ((100 / dataframe['ema25'].shift(5)) * dataframe['ema30'].shift(5))) >= 0.023341792 &
                      (100 - ((100 / dataframe['ema25'].shift(7)) * dataframe['ema30'].shift(7))) >= 0.023341792 &
                      (100 - ((100 / dataframe['ema25'].shift(9)) * dataframe['ema30'].shift(9))) >= 0.023341792 &
                      (100 - ((100 / dataframe['ema25'].shift(11)) * dataframe['ema30'].shift(11))) >= 0.023341792 &
                      (100 - ((100 / dataframe['ema25'].shift(14)) * dataframe['ema30'].shift(14))) >= 0.023341792 &


                      (100 - ((100 / dataframe['ema20'].shift(1)) * dataframe['ema25'].shift(1))) >= 0.023341792 &
                      (100 - ((100 / dataframe['ema20'].shift(3)) * dataframe['ema25'].shift(3))) >= 0.023341792 &
                      (100 - ((100 / dataframe['ema20'].shift(5)) * dataframe['ema25'].shift(5))) >= 0.023341792 &
                      (100 - ((100 / dataframe['ema20'].shift(7)) * dataframe['ema25'].shift(7))) >= 0.023341792 &
                      (100 - ((100 / dataframe['ema20'].shift(9)) * dataframe['ema25'].shift(9))) >= 0.023341792 &
                      (100 - ((100 / dataframe['ema20'].shift(11)) * dataframe['ema25'].shift(11))) >= 0.023341792 &
                      (100 - ((100 / dataframe['ema20'].shift(14)) * dataframe['ema25'].shift(14))) >= 0.023341792 &


                      (100 - ((100 / dataframe['ema100'].shift(1)) * dataframe['ema200'].shift(1))) >= 0.023341792 &
                      (100 - ((100 / dataframe['ema100'].shift(3)) * dataframe['ema200'].shift(3))) >= 0.023341792 &
                      (100 - ((100 / dataframe['ema100'].shift(5)) * dataframe['ema200'].shift(5))) >= 0.023341792 &
                      (100 - ((100 / dataframe['ema100'].shift(7)) * dataframe['ema200'].shift(7))) >= 0.023341792 &
                      (100 - ((100 / dataframe['ema100'].shift(9)) * dataframe['ema200'].shift(9))) >= 0.023341792 &
                      (100 - ((100 / dataframe['ema100'].shift(11)) * dataframe['ema200'].shift(11))) >= 0.023341792 &
                      (100 - ((100 / dataframe['ema100'].shift(14)) * dataframe['ema200'].shift(14))) >= 0.023341792 

  
            ),
            ['buy', 'buy_tag']] = (1, 'Super Flama')  # https://prnt.sc/tHglaXPDZ42r
    
        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                (dataframe['consensus_sell'] > 88) &
                (dataframe['volume'] > 0)
            ),
            'sell'
        ] = 1
        return dataframe