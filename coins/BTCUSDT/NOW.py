#
# Copyright [2024-2030] [TraRyTrade]
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.
#/

#Sry didnt celan it becasue i dont use it anymore WT95 is old stuff for me thats why i release in the www...make PR  we clean build please will add it then ...

from binance.client import Client
import config
import time
import sys
import subprocess
from WinTradeDB_FUNCTIONS import *
import sqlite3
import os
from tradehistory import *
from Request import *
import tradehistory
import Request
from varmove import *
from datetime import datetime, timedelta
import importlib.util
import re

#Set fo sellstop buystop


#USER SETTINGS




TakeAllModus = 0  # Set 1 to activate the Take All Profit Modus ( TakeProfitFromBUY2 + TakeProfitFromSELL2 )

STOPLIMIT = - 125					#  StopLossLimit in USDT -0.5	HAVE TO BE NEGATIVE






#LOGGING   USE DEBUG TO SEE RESPONSE FROM BINANCE    USE WARNING FOR LOG SCRIPT OUTPUTS	
import logging


LOG_FILE_SIZE_MB_HODL_INFO = 250
LOG_FILE_SIZE_MB_HODL_TRADES = 35
LOG_FILE_SIZE_MB_HODL_Calculation = 35
LOG_FILE_EXPIRATION_DAYS = 7

log_file_path = 'HODL_INFO.log'
trades_log_file_path = 'HODL_TRADES.log'
calculation_log_file_path = 'HODL_Calculation.log'
restartlog = 'restartlog.txt'
logging.basicConfig(filename = log_file_path, format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.WARNING)


formatter = logging.Formatter('%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

def setup_logger(name, log_file, level=logging.INFO):
    """To setup as many loggers as you want"""
    handler = logging.FileHandler(log_file)        
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

 # first file logger
Tradeslog = setup_logger('first_logger', 'HODL_TRADES.log')   # USE WITH    Tradeslog.warning('This is just info message')

 # second file logger
Calculation = setup_logger('second_logger', 'HODL_Calculation.log')
Calculation.warning('Calcualtion logger Restarted')

# Calculate the expiration date
expiration_date = datetime.now() - timedelta(days=LOG_FILE_EXPIRATION_DAYS)


#BINANCE-PYTHON API HOODLER SCRIPT CREATED By M.Ry

client = Client(config.api_key, config.api_secret)
logging.warning("logged in")



countDown = 0                               # must set to 0
countUP = 0                                   # must set to 0
setDOWNstartInitial = setDOWNstart  
setUPstart = setDOWNstart                            
setUPstartInitial =  setUPstart 
countDownLIMIT = 2                   # 5  x Loop and  x Loop Over setDOWNstart, then release sell Order when all good
countUPLIMIT = 2 						     # 5  x Loop and x Loop setUPstart, then release buy Order when all good

ROICloseLevelInitialEVER = ROICloseLevelInitial

StopTradesInitial = StopTrades

TakeProfitFromBUYInitial = TakeProfitFromBUY			
TakeProfitFromSELL = TakeProfitFromBUY
TakeProfitFromSELLInitial = TakeProfitFromSELL			
TakeProfitFromSELL2 = TakeProfitFromBUY2


SellLoopSelf_CounterLIMIT = 1        # 20 32 30 15 Delay next SELL for x Loop
BUYLoopSelf_CounterLIMIT = 1         # 20 32 30 Delay next BUY for x Loop






SmallHOLDSELLStartCounterLIMIT_Initial = 1 
SmallHOLDSELLStartCounterLIMIT = SmallHOLDSELLStartCounterLIMIT_Initial    # 9 18 15 5 Loop before START SmallHOLDSELL add 1x

SmallHOLDBUYStartCounterLIMIT_Initial = 1
SmallHOLDBUYStartCounterLIMIT = SmallHOLDBUYStartCounterLIMIT_Initial   # 9 18 15 5 Loop before START SmallHOLDBUY add 1x





SELLTradeThisLoop = 0
BUYTradeThisLoop = 0
DontSELL = 0
DontBUY = 0


SELLTradesCounter = 0
BUYTradesCounter = 0



SellLoopSelf_Counter = 0
BUYLoopSelf_Counter = 0
SmallHOLDSELLStartCounter = 0
SmallHOLDBUYStartCounter = 0





TakeProfitSELLCounter = 0
TakeProfitBUYCounter = 0



modifedsell = 0
modifedbuy = 0

SELL_TakeProfit_COUNTER_lastest = 0
BUY_TakeProfit_COUNTER_lastest = 0
SELL_Loop_COUNTER_lastest = 0
BUY_Loop_COUNTER_lastest = 0


PosSizetest = 0
lockedthatBUY = 0
lockedthatSELL = 0

BLOCKER = 0

closeSizeSELL = 0
closeSizeBUY = 0

SELLGrower1 = 0
SELLGrower2 = 0
SELLGrower3 = 0
SELLGrower4 = 0
SELLGrower5 = 0
BUYGrower1 = 0
BUYGrower2 = 0
BUYGrower3 = 0
BUYGrower4 = 0
BUYGrower5 = 0

closeSizeSELLRoiUnderLevel = 0
closeSizeBUYRoiUnderLevel = 0
lastest_PosSizetest = 0
setManaulTrades = 0


StartUp = 0


SaverSELL_1 = 0
SaverSELL_2 = 0
SaverSELL_3 = 0
SaverSELL_4 = 0
SaverSELL_5 = 0
SaverSELL_6 = 0
SaverBUY_1 = 0
SaverBUY_2 = 0
SaverBUY_3 = 0
SaverBUY_4 = 0
SaverBUY_5 = 0
SaverBUY_6 = 0

SELLOrderActive = 0
BUYOrderActive = 0

setflipfloproi = 0
setflopfromBuytosell1 = 0
setflopfromSelltobuy1 = 0


TakedSell = 0
TakedBuy = 0
WinAmount = 0

setwait1 = 0
stoppp1 = 0
stoppp2 = 0
stoppp3 = 0

quantity = 0  
quantity2 = 0

reducetradeTrue = 0
optimazetradeTrue = 0

min_trade_qty = 0
mintradeWaitAsk = 0
GROWER_SELL_TakeProfit_COUNTER_lastest = 0 
GROWER_BUY_TakeProfit_COUNTER_lastest = 0

average_price = 0
mark_price = 0
Locked1 = 0
Locked2 = 0


PosFastClose = 0

PNL = 0
pnl = 0



roe=0

check = 0


PositionSizeSaved = 0

multiadddiffspread = 0

setmanualTrades = 0

HRoeInitBefore = 0

timeframe2 = 0

TradeAmountBefore = 0
ROICloseLevelInitialBefore = 0
GrowCount = 0
StartGrowDiffInit = 100
StartGrowDiff = StartGrowDiffInit
StartGrowDiffAddInit = 100
StartGrowDiffAdd = StartGrowDiffAddInit
EnableGrowerBUY=0
EnableGrowerBUYLastestŜtate= 0
EnableGrowerSELL=0
EnableGrowerSELLLastestŜtate= 0
EnableBUYLastestŜtate = 0
EnableBUY = 0    
EnableSELLLastestŜtate = 0
EnableSELL = 0     
ROISwicherInvertLastestŜtate = 0 
ROISwicherInvert = 0      
TakeProfitLastestŜtate = 0
TakeProfit = 0
SmallHoldMUCHROILastestŜtate = 0
SmallHoldMUCHROI = 0
onlyGoToMinLastestŜtate = 0
onlyGoToMin = 0
smallholdsmallroiEnable = 0
setStopMarketHardSwich = 0
setStopMarketHardSwichLastestŜtate = 0
cleanLogsforCoinLastestŜtate = 0
cleanLogsforCoin = 0

def load_instructions():
    # Load the instructions from instrct.py
    spec = importlib.util.spec_from_file_location("instrct", "./instrct.py")
    instrct = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(instrct)
    
    # Extract the variables from instrct.py
    changeside = getattr(instrct, "changeside", False)
    nextamount = getattr(instrct, "nextamount", None)
    timeframe = getattr(instrct, "timeframe", False)
    max_switches = getattr(instrct, "max_switches", None)
    RoiCloseAdd = getattr(instrct, "RoiCloseAdd", False)
    spreadAdd = getattr(instrct, "spreadAdd", None)
    HRoeInit = getattr(instrct, "HRoeInit", None)
    HRoeDiff = getattr(instrct, "HRoeDiff", None)
    HRoeAddDiff = getattr(instrct, "HRoeAddDiff", None)
    TriggerPoint = getattr(instrct, "TriggerPoint", None)




    
    return changeside, nextamount, timeframe, max_switches, RoiCloseAdd, spreadAdd, HRoeInit, HRoeDiff, HRoeAddDiff, TriggerPoint


def Load_OptionsTrueFalse():
    # Load the instructions from optionsstate.py
    spec = importlib.util.spec_from_file_location("optionsstate", "./optionsstate.py")
    optionsstate = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(optionsstate)
    

    option1 = getattr(optionsstate, "option1", None)
    option2 = getattr(optionsstate, "option2", None)
    option3 = getattr(optionsstate, "option3", None)
    option4 = getattr(optionsstate, "option4", None)
    option5 = getattr(optionsstate, "option5", None)
    option6 = getattr(optionsstate, "option6", None)
    option7 = getattr(optionsstate, "option7", None)
    option8 = getattr(optionsstate, "option8", None)
    option9 = getattr(optionsstate, "option9", None)
    option10 = getattr(optionsstate, "option10", None)
    option11 = getattr(optionsstate, "option11", None)



    
    return option1, option2, option3, option4, option5, option6, option7, option8, option9, option10, option11

def save_opt11_false():
    # Read the contents of optionsstate.py
    with open("./optionsstate.py", "r") as file:
        lines = file.readlines()
    
    # Find the line with option11 and set it to False
    for i, line in enumerate(lines):
        if line.strip().startswith("option11 ="):
            lines[i] = "option11 = False\n"
            break
    
    # Write the modified contents back to optionsstate.py
    with open("./optionsstate.py", "w") as file:
        file.writelines(lines)


def reducetrade(symbol,TradeAmount):
    try:
        client.futures_create_order(
            symbol=symbol,
            type='MARKET',
            side='SELL',
            quantity=TradeAmount
        )
    except Exception as e:
        error_message = str(e)
        if 'APIError(code=-2019)' in error_message:
            Tradeslog.warning('Margin is insufficient. Waiting for 25 seconds...')
            time.sleep(5)
            reducetradeTrue = 0
        else:
            Tradeslog.warning(f'reducetrade111 API error: {error_message}')
        reducetradeTrue = 0
	   	

def optimazetrade(symbol,TradeAmount):
    try:
        client.futures_create_order(
            symbol=symbol,
            type='MARKET',
            side='BUY',
            quantity=TradeAmount
        )
    except Exception as e:
        error_message = str(e)
        if 'APIError(code=-2019)' in error_message:
            Tradeslog.warning('Margin is insufficient. Waiting for 25 seconds...')
            time.sleep(5)
            optimazetradeTrue = 0
        else:
            Tradeslog.warning(f'optimazetrade222 API error: {error_message}')
        optimazetradeTrue = 0




def reducetrade_reduceOnly(symbol,TradeAmount):
    if TradeAmount > 0:
        try:
            client.futures_create_order(
                symbol=symbol,
                type='MARKET',
                side='SELL',
                quantity=TradeAmount,
                reduceOnly=True
            )
        except Exception as e:
            error_message = str(e)
            if 'APIError(code=-2019)' in error_message:
                Tradeslog.warning('Margin is insufficient. Waiting for 25 seconds...')
                time.sleep(5)
            else:
                Tradeslog.warning(f'reducetrade333 API error: {error_message}')

def optimazetrade_reduceOnly(symbol,TradeAmount):
    if TradeAmount > 0:
        try:
            client.futures_create_order(
                symbol=symbol,
                type='MARKET',
                side='BUY',
                quantity=TradeAmount,
                reduceOnly=True
            )
        except Exception as e:
            error_message = str(e)
            if 'APIError(code=-2019)' in error_message:
                Tradeslog.warning('Margin is insufficient. Waiting for 25 seconds...')
                time.sleep(5)
            else:
                Tradeslog.warning(f'optimazetrade444 API error: {error_message}')


def get_mark_and_average_price(symbol):
    try:
        mark_price_info = client.futures_mark_price(symbol=symbol)
        
        mark_price = float(mark_price_info['markPrice'])
        average_price = mark_price
        
        return mark_price, average_price
    
    except Exception as e:
        Tradeslog.warning(f'Error retrieving mark and average price: {str(e)}')
        return None, None





def get_minimum_quantity(symbol, order_type):
    try:
    
        mark_price, average_price = get_mark_and_average_price(symbol)
        
        exchange_info = client.futures_exchange_info()

        symbol_info = next((s for s in exchange_info['symbols'] if s['symbol'] == symbol), None)

        if symbol_info is None:
            Tradeslog.warning(f"Symbol {symbol} not found in trading rules")
            return None

        filters = symbol_info['filters']
        min_trade_qty = None

        # Find the relevant filters
        price_filter = next(filter(lambda f: f['filterType'] == 'PRICE_FILTER', filters), None)

        lot_size_filter = next(filter(lambda f: f['filterType'] == 'LOT_SIZE', filters), None)

        min_notional_filter = next(filter(lambda f: f['filterType'] == 'MIN_NOTIONAL', filters), None)

        leftopen = float(lot_size_filter['stepSize'])        

        if order_type == 'MARKET':
            if min_notional_filter and average_price:
                min_trade_qty = max(float(lot_size_filter['stepSize']),
                                   float(min_notional_filter['notional']) / average_price)
                min_trade_qty = ( min_trade_qty * 135 ) / 100   
                print('Rounded1 '    +str(min_trade_qty ) +    '           min_trade_qty = ' +str(min_trade_qty ))
        elif order_type == 'LIMIT':
            if price and min_notional_filter:
                min_trade_qty = max(float(lot_size_filter['stepSize']),
                                   float(min_notional_filter['notional']) / price)




        if min_trade_qty is not None:
            return min_trade_qty, leftopen
            
              
        Tradeslog.warning(f"Minimum TradeAmount not found for symbol {symbol}")
        return None


                

              
        Tradeslog.warning(f"Minimum TradeAmount not found for symbol {symbol}")
        return None
        
        

            
            
             
    except Exception as e:
        Tradeslog.warning(f'Error retrieving minimum TradeAmount: {str(e)}')
        return None


buystop_set = 0
sellstop_set = 0

def setbuystop():
    trading_script = "stop.py"
    current_dir = os.path.dirname(os.path.abspath(__file__))
    stop = os.path.join(current_dir, "stop.py")
    subprocess.run(["python3.8", stop, "buystop"])
    buystop_set = 1

def setsellstop():
    trading_script = "stop.py"
    current_dir = os.path.dirname(os.path.abspath(__file__))
    stop = os.path.join(current_dir, "stop.py")
    subprocess.run(["python3.8", stop, "sellstop"])
    sellstop_set = 1



def setbuystopdel():
    trading_script = "delstop.py"
    current_dir = os.path.dirname(os.path.abspath(__file__))
    stop = os.path.join(current_dir, "delstop.py")
    subprocess.run(["python3.8", stop, "buystop"])
    buystop_set = 0

def setsellstopdel():
    trading_script = "delstop.py"
    current_dir = os.path.dirname(os.path.abspath(__file__))
    stop = os.path.join(current_dir, "delstop.py")
    subprocess.run(["python3.8", stop, "sellstop"])
    sellstop_set = 0





TradeAmount = TradeAmount
symbol = Coin


check = 0
PositionSizeLastest = 0

# Initialize variables for tracking the last switch event timestamp and the next monitoring time
last_switch_timestamp = None
next_monitoring_time = datetime.now() 
next_monitoring_time2 = datetime.now() 
next_monitoring_time3 = datetime.now() 
WaitHadEvents =0





TradeAmountOld=0
HRoeSell = -500
HRoeBuy = -500
ROICloseLevelOld=0
HRoeInit= -500
HRoeInitLive = HRoeInit
Switchy = 0
punshd = 0

while True:


    # Read the variables from varmove.py
    with open('varmove.py', 'r') as file:
        code = file.read()

    # Execute the code to update the current variables
    exec(code)



    TradeAmount = TradeAmount
    symbol = Coin




    PosCalDiff = (TradeAmount) / 2  # Don't Change it!!
    PositionLimitBUY = round((TradeX * TradeAmount), 3)  # 0.054 HAVE TO BE POSITIVE and same LIMIT as SELL  
    PositionLimitSELL = round(-(TradeX * TradeAmount), 3)  # -0.054 HAVE TO BE NEGATIVE and same LIMIT as BUY 
    PositionLimitBUY2 = round((1000000 * TradeAmount), 3)  # 0.054 HAVE TO BE POSITIVE and same LIMIT as SELL  
    PositionLimitSELL2 = round(-(1000000 * TradeAmount), 3)  # -0.054 HAVE TO BE NEGATIVE and same LIMIT as BUY 

    logging.warning('HODLScript Started or Restart by USER from HERE!!!!!!!\n!!!!!!!!\n!!!!!!!!\n!!!!!!!!\n!!!!!!!!\n!!!!!!!!\n!!!!!!!!\n!!!!!!!!\ '+str(TradeAmount))
    logging.warning('CalculatedPosCalDiff '+str(PosCalDiff))
    logging.warning('TradeAmount'+str(TradeAmount))
    logging.warning('PositionLimitBUY '+str(PositionLimitBUY))
    logging.warning('PositionLimitSELL '+str(PositionLimitSELL))
    logging.warning('PositionLimitBUY2 '+str(PositionLimitBUY2))
    logging.warning('PositionLimitSELL2 '+str(PositionLimitSELL2))



    # LOAD OPTIONS FROM FILE


    EnableGrowerBUYLastestŜtate =  EnableGrowerBUY      
    EnableGrowerSELLLastestŜtate =  EnableGrowerSELL     
    EnableBUYLastestŜtate =  EnableBUY     
    EnableSELLLastestŜtate =  EnableSELL     
    ROISwicherInvertLastestŜtate =  ROISwicherInvert
    TakeProfitLastestŜtate =  TakeProfit
    SmallHoldMUCHROILastestŜtate =  SmallHoldMUCHROI
    onlyGoToMinLastestŜtate =  onlyGoToMin
    smallholdsmallroiEnableLastestŜtate =  smallholdsmallroiEnable
    setStopMarketHardSwichLastestŜtate =  setStopMarketHardSwich
    cleanLogsforCoinLastestŜtate =  cleanLogsforCoin

    # Load instructions from updated variables
    changeside, nextamount, timeframe, max_switches, RoiCloseAdd, spreadAdd, HRoeInit, HRoeDiff, HRoeAddDiff, TriggerPoint = load_instructions()

    # Load options from updated variables
    option1, option2, option3, option4, option5, option6, option7, option8, option9, option10, option11 = Load_OptionsTrueFalse()


    if option1 == True: 
        EnableGrowerBUY = 1

    else:
        EnableGrowerBUY = 0


    if EnableGrowerBUYLastestŜtate > EnableGrowerBUY :
            Tradeslog.warning("EnableGrowerBUY==0")   
    if EnableGrowerBUYLastestŜtate < EnableGrowerBUY:
            Tradeslog.warning("EnableGrowerBUY==1")   


    if option2 == True: 
        EnableGrowerSELL = 1

    else:
        EnableGrowerSELL = 0


    if EnableGrowerSELLLastestŜtate > EnableGrowerSELL :
            Tradeslog.warning("EnableGrowerSELL==0")   
    if EnableGrowerSELLLastestŜtate < EnableGrowerSELL:
            Tradeslog.warning("EnableGrowerSELL==1")   

    if option3 == True: 
        EnableBUY = 1

    else:
        EnableBUY = 0


    if EnableBUYLastestŜtate > EnableBUY :
            Tradeslog.warning("EnableBUY==0")   
    if EnableBUYLastestŜtate < EnableBUY:
            Tradeslog.warning("EnableBUY==1")   



    if option4 == True: 
        EnableSELL = 1

    else:
        EnableSELL = 0


    if EnableSELLLastestŜtate > EnableSELL :
            Tradeslog.warning("EnableSELL==0")   
    if EnableSELLLastestŜtate < EnableSELL:
            Tradeslog.warning("EnableSELL==1")   


    if option5 == True: 
        ROISwicherInvert = 1
        onlyGoToMin = 0

    else:
        ROISwicherInvert = 0


    if ROISwicherInvertLastestŜtate > ROISwicherInvert :
            Tradeslog.warning("ROISwicherInvert==0")   
    if ROISwicherInvertLastestŜtate < ROISwicherInvert:
            Tradeslog.warning("ROISwicherInvert==1")   
  
        

    if option6== True: 
        TakeProfit = 1

    else:
        TakeProfit = 0


    if TakeProfitLastestŜtate > TakeProfit :
            Tradeslog.warning("TakeProfit==0")   
    if TakeProfitLastestŜtate < TakeProfit:
            Tradeslog.warning("TakeProfit==1")   


    if option7== True: 
        SmallHoldMUCHROI = 1

    else:
        SmallHoldMUCHROI = 0


    if SmallHoldMUCHROILastestŜtate > SmallHoldMUCHROI :
            Tradeslog.warning("SmallHoldMUCHROI==0")   
    if SmallHoldMUCHROILastestŜtate < SmallHoldMUCHROI:
            Tradeslog.warning("SmallHoldMUCHROI==1")   
  
        
    if option8 == True and ROISwicherInvert == 1: 
        Tradeslog.warning("For ussage of onlyGoToMin you have to disable ROISwicherInvert!!  ")  

    if option8== True and ROISwicherInvert == 0: 
        onlyGoToMin = 1

    else:
        onlyGoToMin = 0


    if onlyGoToMinLastestŜtate > onlyGoToMin :
            Tradeslog.warning("onlyGoToMin==0")   
    if onlyGoToMinLastestŜtate < onlyGoToMin:
            Tradeslog.warning("onlyGoToMin==1")   
  
        




    if option9== True:
        smallholdsmallroiEnable = 1

    else:
        smallholdsmallroiEnable = 0


    if smallholdsmallroiEnableLastestŜtate > smallholdsmallroiEnable :
            Tradeslog.warning("smallholdsmallroiEnable==0")   
    if smallholdsmallroiEnableLastestŜtate < smallholdsmallroiEnable:
            Tradeslog.warning("smallholdsmallroiEnable==1")   
 

    if option10 == True:
        setStopMarketHardSwich = 1

    else:
        setStopMarketHardSwich = 0


    if setStopMarketHardSwichLastestŜtate > setStopMarketHardSwich :
            Tradeslog.warning("setStopMarketHardSwich==0")   
            if BUYOrderActive == 1 and setStopMarketHardSwich == 0:
                setbuystopdel()
                buystop_set = 0
                sellstop_set = 0       
        
            if SELLOrderActive == 1 and setStopMarketHardSwich == 0:
                setsellstopdel()
                sellstop_set = 0
                buystop_set = 0   



    if setStopMarketHardSwichLastestŜtate < setStopMarketHardSwich:
            Tradeslog.warning("setStopMarketHardSwich==1")   
            if BUYOrderActive == 1 and setStopMarketHardSwich == 1:
                setbuystop()
                buystop_set = 1
                sellstop_set = 0       
        
            if SELLOrderActive == 1 and setStopMarketHardSwich == 1:
                setsellstop()
                sellstop_set = 1
                buystop_set = 0   


    if option11 == True:
        cleanLogsforCoin = 1

    else:
        cleanLogsforCoinHardSwich = 0


    if cleanLogsforCoinLastestŜtate > cleanLogsforCoin :
            Tradeslog.warning("cleanLogsforCoin==0")   


    if cleanLogsforCoinLastestŜtate < cleanLogsforCoin:
            Tradeslog.warning("cleanLogsforCoin==1")   
            try:
                if cleanLogsforCoin ==1 and os.path.exists(log_file_path):
                    os.remove(log_file_path)            
            except OSError:
                pass
        
            try:
                if cleanLogsforCoin ==1 and os.path.exists(trades_log_file_path):
                    os.remove(trades_log_file_path)
            except OSError:
                pass
        
            try:
                if cleanLogsforCoin ==1 and os.path.exists(calculation_log_file_path):
                    os.remove(calculation_log_file_path)
            except OSError:
                pass
        
            try:
                if cleanLogsforCoin ==1 and os.path.exists(restartlog):
                    os.remove(restartlog)
            except OSError:
                pass
            cleanLogsforCoin = 0
            save_opt11_false ()


  




    
    
    if StartUp == 1 and HRoeInit > HRoeInitBefore or HRoeInit < HRoeInitBefore:
        weight = (roe) 
        HRoeInitBefore= HRoeInit
        HRoeInitLive = HRoeInit
        HRoeBuy = weight
        HRoeSell = weight





    
    if StartUp == 1 and TradeAmountBefore > TradeAmount or TradeAmountBefore < TradeAmount:
        TradeAmountOld = TradeAmount
        
        
    if StartUp == 1 and  ROICloseLevelInitialBefore > ROICloseLevelInitial or ROICloseLevelInitialBefore < ROICloseLevelInitial:
        ROICloseLevelInitialEVER = ROICloseLevelInitial






    log_file = "HODL_TRADES.log"
    switch_count_buy = 0
    switch_count_sell = 0
    total_switch_count = 0
    current_time = datetime.now()
    start_time = current_time - timedelta(seconds=timeframe)
    pattern_matched = False  # Flag to indicate if the pattern matched any lines

    try:
        with open(log_file, 'r') as file:
            for line in file:
                # Match for BUY orders...
                match_buy = re.search(r'(\d+-\w+-\d+ \d+:\d+:\d+) - BUY\s+ORDER\s+swich\s+Order\s+weight=([-\d.]+)', line)
                if StartUp == 0:
                    next_monitoring_time = current_time + timedelta(seconds=timeframe) 
                    WaitHadEvents =1
                    
                if match_buy and WaitHadEvents == 0:
                    pattern_matched = True  # Set the flag to True if pattern matches any line
                    timestamp_str = match_buy.group(1)
                    timestamp = datetime.strptime(timestamp_str, '%d-%b-%y %H:%M:%S')
                    weight = float(match_buy.group(2))

                    # Check if the timestamp is within the specified timeframe
                    if timestamp >= start_time and timestamp <= current_time:
                        switch_count_buy += 1
                        total_switch_count += 1
                        #Tradeslog.warning(f"Buy switch detected: Weight: {weight}")
                        last_switch_timestamp = timestamp  # Update the last switch event timestamp

                # Match for SELL orders...
                match_sell = re.search(r'(\d+-\w+-\d+ \d+:\d+:\d+) - SELL\s+ORDER\s+swich\s+Order\s+weight=([-\d.]+)', line)
                if match_sell and WaitHadEvents ==0:
                    pattern_matched = True  # Set the flag to True if pattern matches any line
                    timestamp_str = match_sell.group(1)
                    timestamp = datetime.strptime(timestamp_str, '%d-%b-%y %H:%M:%S')
                    weight = float(match_sell.group(2))

                    # Check if the timestamp is within the specified timeframe
                    if timestamp >= start_time and timestamp <= current_time:
                        switch_count_sell += 1
                        total_switch_count += 1
                        #Tradeslog.warning(f"Sell switch detected: Weight: {weight}")
                        last_switch_timestamp = timestamp  # Update the last switch event timestamp


        
 
        timeframe2=2*timeframe
        timeframe3=3*timeframe
        

        if total_switch_count >= max_switches and WaitHadEvents == 0 and last_switch_timestamp is not None and Switchy==0 :
            switch_count_buy = 0
            switch_count_sell = 0
            total_switch_count = 0
            TradeAmountOld = TradeAmount
            ROICloseLevelInitialEVER = ROICloseLevelInitial
            next_monitoring_time2 = last_switch_timestamp + timedelta(seconds=timeframe2)  
            next_monitoring_time3  = last_switch_timestamp + timedelta(seconds=timeframe3)                 
            TradeAmount = min_trade_qty
            next_monitoring_time = last_switch_timestamp + timedelta(seconds=timeframe)              
            WaitHadEvents =1
            Switchy=1


            if ROICloseLevel > -150: 
                ROICloseLevelInitial = ROICloseLevelInitial - RoiCloseAdd
                ROICloseLevel = ROICloseLevelInitial
                Tradeslog.warning(f"Lots of switches detected. new temp RoiCloseLevel for that run is  {ROICloseLevel}")  # Debug print
            if spread1 < 175: 
                spread1Initial = spread1Initial + spreadAdd
                spread1 = spread1Initial 
                Tradeslog.warning(f"Lots of switches detected. new temp spread1 for that run is  {spread1}")  # Debug print   




        if current_time < next_monitoring_time:
            if punshd == 0:
                Tradeslog.warning(f"{Coin}___Waiting until {next_monitoring_time} before continuing...")
                punshd = 1


                    
        if current_time > next_monitoring_time:
            WaitHadEvents=0          
            punshd = 0




        if StartUp == 1 and current_time > next_monitoring_time2 and ROICloseLevelInitialEVER  > ROICloseLevelInitial + 3 and Switchy==1 : 
            ROICloseLevelInitial =  ROICloseLevelInitial +3



        if StartUp == 1 and current_time > next_monitoring_time3 and TradeAmountOld  > TradeAmount + min_trade_qty and Switchy==1 : 
        
            TradeAmount = TradeAmount + min_trade_qty   
            Tradeslog.warning(f"next_monitoring_time3 reached, setback TradeAmount to original TradeAmountOld= {TradeAmountOld}, TradeAmount= {TradeAmount} ")  
            
            if TradeAmount > 1 or TradeAmount == 1:
                TradeAmount = round(TradeAmount)
            elif TradeAmount < 1 and not TradeAmount < 0.1:
                TradeAmount = round(TradeAmount, 1)
            elif TradeAmount < 0.1 and not TradeAmount < 0.01:
                TradeAmount = round(TradeAmount, 2)
            else:
                TradeAmount = round(TradeAmount, 3)             


        if StartUp == 1 and current_time > next_monitoring_time3 and TradeAmountOld  == TradeAmount + min_trade_qty  and Switchy==1:
            Switchy= 0


        if StartUp == 1 and current_time > next_monitoring_time3 and TradeAmountOld  < TradeAmount + min_trade_qty  and Switchy==1:
            Switchy= 0



    except FileNotFoundError:
        print("Log file not found.")




























    time.sleep(0.1)  # Delay for 2 seconds before the next iteration





# Read the variables from varmove.py
    with open('mintrade.py', 'r') as file:
        code = file.read()

    # Execute the code to update the current variables
    exec(code)

    time.sleep(0.2)  # Delay for 2 seconds before the next iteration


# Read the variables from lastprice.py
    with open('lastprice.py', 'r') as file:
        code = file.read()

    # Execute the code to update the current variables
    exec(code)

    time.sleep(0.1)  # Delay for 2 seconds before the next iteration    

    
    order_type= "MARKET"

    if StartUp == 0:
        HRoeInitLive = HRoeInit
        HRoeSell = -500
        HRoeBuy = -500
        TriggerPoint = -500
        HRoeInitBefore= HRoeInit
        ROICloseLevelInitialEVER = ROICloseLevelInitial

        min_trade_qty, leftopen = get_minimum_quantity(symbol, order_type)
        mark_price, average_price = get_mark_and_average_price(symbol)
        Tradeslog.warning('average_price: '+str(average_price))
        Tradeslog.warning('mark_price: '+str(mark_price))       
        Tradeslog.warning('PosFastClose: '+str(PosFastClose))        
        if min_trade_qty > 1 or min_trade_qty == 1:
            min_trade_qty = round(min_trade_qty)
        elif min_trade_qty < 1 and not min_trade_qty < 0.1:
            min_trade_qty = round(min_trade_qty, 1)
        elif min_trade_qty < 0.1 and not min_trade_qty < 0.01:
            min_trade_qty = round(min_trade_qty, 2)
        else:
            min_trade_qty = round(min_trade_qty, 3)             

                    

        # Read the content of instrct.py
        with open('instrct.py', 'r') as file:
            lines = file.readlines()

        # Find the line containing 'TriggerPoint' variable and modify its value
        for i, line in enumerate(lines):
            if 'TriggerPoint=' in line:
                lines[i] = 'TriggerPoint=-500\n'  # Modify the value to 0
                break

        # Write the modified content back to instrct.py
        with open('instrct.py', 'w') as file:
            file.writelines(lines)

	
    if setwait1 == 1:
        time.sleep(45)
        setwait1 == 0	

    


    max_retries = 8
    delay = 5

# GET PositionSize
    for _ in range(max_retries):
        try:
            OpenOrders = client.futures_coin_account_balance(symbol=symbol)
            time.sleep(0.2)
            account = client.futures_account()
            break  # If the API call is successful, break out of the loop
        except Exception as e:
            print("An error occurred while fetching account information:", str(e))
            time.sleep(delay)
            pass

    else:
        print("Max retries exceeded. Failed to fetch account information.")
        continue

    PositionSize = 0
    
    for b2 in account['positions']:
        if b2['symbol'] == symbol:
            PositionSize = float(b2['positionAmt'])
    logging.warning('                  Pos_Size: ' + str(PositionSize))
    time.sleep(0.1)

    if PositionSize < 0 and SELLOrderActive == 0:
        ROICloseLevel = ROICloseLevelInitial
        TakeProfitFromSELL = TakeProfitFromSELLInitial
        TakeProfitFromBUY = TakeProfitFromBUYInitial
        spread1 = spread1Initial
        SELLOrderActive = 1
        BUYOrderActive = 0
        PositionSizeSaved = PositionSize
        buystop_set = 0
        check = 0
        PositionSizeLastest = abs(PositionSize)
        HRoeSell = -500
        HRoeBuy = -500
        HRoeInitLive = HRoeInit
        TriggerPoint = -500
        GrowCount = 0
        StartGrowDiff = StartGrowDiffInit
        StartGrowDiffAdd = StartGrowDiffAddInit

    if PositionSize > 0 and BUYOrderActive == 0:
        ROICloseLevel = ROICloseLevelInitial
        TakeProfitFromSELL = TakeProfitFromSELLInitial
        TakeProfitFromBUY = TakeProfitFromBUYInitial
        spread1 = spread1Initial
        BUYOrderActive = 1
        SELLOrderActive = 0
        PositionSizeSaved = PositionSize
        sellstop_set = 0
        check = 0
        PositionSizeLastest = abs(PositionSize)
        HRoeSell = -500
        HRoeBuy = -500
        HRoeInitLive = HRoeInit
        TriggerPoint = -500
        GrowCount = 0
        StartGrowDiff = StartGrowDiffInit
        StartGrowDiffAdd = StartGrowDiffAddInit

    logging.warning('BUYOrderActive: ' + str(BUYOrderActive))
    logging.warning('SELLOrderActive: ' + str(SELLOrderActive))

    if PositionSize == 0:
        time.sleep(45)




   #  Between the get position set also the STOPMARKET
        

    if BUYOrderActive == 1 and setStopMarketHardSwich == 1 and buystop_set == 0:
        setbuystop()
        buystop_set = 1
        sellstop_set = 0
 

    if SELLOrderActive == 1 and setStopMarketHardSwich == 1 and sellstop_set == 0:
        setsellstop()
        sellstop_set = 1
        buystop_set = 0


    if  BUYOrderActive == 1 and PositionSize > PositionSizeSaved and setStopMarketHardSwich == 1 and lokedTakeP_BUY == 0:
        setbuystop()
        buystop_set = 1
        sellstop_set = 0
        Tradeslog.warning ('BUYOrderActive buystop_set='+str(buystop_set)) 


    if  SELLOrderActive == 1 and PositionSize < PositionSizeSaved and setStopMarketHardSwich == 1 and lokedTakeP_SELL == 0:
        setsellstop()
        sellstop_set = 1
        buystop_set = 0
        Tradeslog.warning ('SELLOrderActive and sellstop_set='+str(sellstop_set)) 


    if StartUp == 1:
        check = check + 1
                    
    if BUYOrderActive == 1 and PositionSize - PositionSizeSaved > (5 * TradeAmount) :
        ROICloseLevel = ROICloseLevelInitial
        spread1 = spread1Initial
        check=0
        PositionSizeSaved = PositionSize  
        setmanualTrades= 1
        Tradeslog.warning("BACK TO INITIAL MANAUL BUY OR SELL")  
 

    if SELLOrderActive == 1 and  abs(PositionSize) - abs(PositionSizeSaved) > (5 * TradeAmount) :
        ROICloseLevel = ROICloseLevelInitial
        spread1 = spread1Initial
        check=0
        PositionSizeSaved = PositionSize 
        setmanualTrades= 1
        Tradeslog.warning("BACK TO INITIAL MANAUL BUY OR SELL")        


          
    if check==5:
        check=0       
                
    if PositionSize > 0 or PositionSize < 0:
        for _ in range(max_retries):
            try:
                balance = client.futures_account_balance(symbol=symbol)
                time.sleep(0.2)
                account = client.futures_account(symbol=symbol)
                break  # If the API call is successful, break out of the loop
            except Exception as e:
                print("An error occurred while fetching account information:", str(e))
                time.sleep(delay)
                pass

        else:
            print("Max retries exceeded. Failed to fetch account information.")
            continue

        usdtbalance = 0

        for b1 in account['positions']:
            if b1['symbol'] == symbol:
                initialmargin = float(b1['initialMargin'])
                unrealizedprofit = float(b1['unrealizedProfit'])
                pnl = unrealizedprofit
                if unrealizedprofit is not None and initialmargin is not None:
                    roe = unrealizedprofit / initialmargin * 100
        logging.warning('                  ROE: ' + str(roe) + '%')
        logging.warning('                  PNL: ' + str(pnl) + ' USDT')
        time.sleep(0.1)
        PNL = (pnl) 
        weight = roe
    
    
    if PNL == 0:
        PNL = 0.00001


# Get minTrade and round to a always usable amount
    if PositionSize > 0 and StartUp == 1 or PositionSize < 0 and StartUp == 1:
        mintradeWaitAsk = mintradeWaitAsk + 1
           
  
      
    if mintradeWaitAsk == 30:
        min_trade_qty, leftopen = get_minimum_quantity(symbol, order_type)
        min_trade_qty = min_trade_qty * 120 / 100   
        mark_price, average_price = get_mark_and_average_price(symbol)
        mintradeWaitAsk = 0
        if min_trade_qty > 1 or min_trade_qty == 1:
            min_trade_qty = round(min_trade_qty)
        elif min_trade_qty < 1 and not min_trade_qty < 0.1:
            min_trade_qty = round(min_trade_qty, 1)
        elif min_trade_qty < 0.1 and not min_trade_qty < 0.01:
            min_trade_qty = round(min_trade_qty, 2)
        else:
            min_trade_qty = round(min_trade_qty, 3)     
            
                    
    if min_trade_qty is not None:
        if TradeAmount < min_trade_qty:
            TradeAmount = min_trade_qty

    

    if PositionSize > 0 or PositionSize < 0:
        # Write the variable values to varmove.py
        with open('lastprice.py', 'w') as file:
            file.write(f"average_price = {average_price!r}\n")
            file.write(f"mark_price = {mark_price!r}\n")
            file.write(f"PNL = {pnl!r}\n")



    if min_trade_qty is not None:
        # Write the variable values to varmove.py
        with open('mintrade.py', 'w') as file:
            file.write(f"min_trade_qty = {min_trade_qty!r}\n")





# Highest ROE Catcher Start wehn ROE Close get over locked1 (buy) or lcoked2 from sell

    weight = (roe) 
    Trigger1 = 0
    Trigger2 = 0
 
    if Locked1 == 1 :
        HRoeBuy = -500
        HRoeSell  = -500
        HRoeInitLive = HRoeInit
        TriggerPoint = -500
           



    if Locked2 == 1 :
        HRoeSell = -500
        HRoeBuy = -500       
        HRoeInitLive = HRoeInit
        TriggerPoint = -500


       

    if PositionSize > 0  and  weight > HRoeInitLive and HRoeBuy > HRoeInitLive and HRoeBuy < weight and weight > 100   :   
    
        HRoeBuy = round(HRoeBuy)        
        Tradeslog.warning('HRoeBuy: '+str(HRoeBuy))  
        Trigger1= round(HRoeBuy - (ROICloseLevel))
        Tradeslog.warning('Trigger1: '+str(Trigger1))  
        Trigger2=  (Trigger1/HRoeDiff)
        Tradeslog.warning('Trigger2: '+str(Trigger2))  
        TriggerPoint= round(HRoeBuy - Trigger2)        
        if TriggerPoint < 100:
            TriggerPoint = - 500
        Tradeslog.warning('TriggerPoint: '+str(TriggerPoint))      
        Tradeslog.warning('HRoeBuy TriggerPoint  activated TriggerPoint: '+str(TriggerPoint))          
       # Write the content of instrct.py
        with open('instrct.py', 'r') as file:
            lines = file.readlines()

        # Find the line containing 'TriggerPoint' variable and modify its value
        for i, line in enumerate(lines):
            if 'TriggerPoint=' in line:
                lines[i] = 'TriggerPoint = ' + str(TriggerPoint) + '\n'  # Modify the value to YourDesiredValue
                break

        # Write the modified content back to instrct.py
        with open('instrct.py', 'w') as file:
            file.writelines(lines)


        


    if PositionSize > 0 and HRoeBuy < weight and  StartUp == 1:
        HRoeBuy = weight 




    if PositionSize > 0  and weight < TriggerPoint and weight > 100:
        ROICloseLevelOld = ROICloseLevel
        ROICloseLevel= round(((TriggerPoint-(ROICloseLevel))/HRoeAddDiff) +   (ROICloseLevel) )
        Tradeslog.warning('HRoeBuy  activated ROICloseLevelOld: '+str(ROICloseLevelOld)+'ROICloseLevel: '+str(ROICloseLevel))  
        HRoeInitLive =HRoeInit + 100
        HRoeBuy = - 500
        TriggerPoint = -500

            
            




    if PositionSize < 0  and  weight > HRoeInitLive and HRoeSell > HRoeInitLive and HRoeSell < weight and weight > 100  :
        HRoeSell = round(HRoeSell)
        
        Tradeslog.warning('HRoeSell: '+str(HRoeSell))  
        Trigger1= round(HRoeSell - (ROICloseLevel))
        Tradeslog.warning('Trigger1: '+str(Trigger1))  
        Trigger2=  (Trigger1/HRoeDiff)
        Tradeslog.warning('Trigger2: '+str(Trigger2))  
        TriggerPoint= round(HRoeSell - Trigger2)      
        if TriggerPoint < 100:
            TriggerPoint = - 500  
        Tradeslog.warning('TriggerPoint: '+str(TriggerPoint))      
        Tradeslog.warning('HRoeSell TriggerPoint  activated TriggerPoint: '+str(TriggerPoint))  
       # Write the content of instrct.py
        with open('instrct.py', 'r') as file:
            lines = file.readlines()

        # Find the line containing 'TriggerPoint' variable and modify its value
        for i, line in enumerate(lines):
            if 'TriggerPoint=' in line:
                lines[i] = 'TriggerPoint = ' + str(TriggerPoint) + '\n'  # Modify the value to YourDesiredValue
                break

        # Write the modified content back to instrct.py
        with open('instrct.py', 'w') as file:
            file.writelines(lines)




    if PositionSize < 0 and HRoeSell < weight and  StartUp == 1 :
        HRoeSell = weight 



    if PositionSize < 0  and weight < TriggerPoint and weight > 100:
        ROICloseLevelOld = ROICloseLevel
        ROICloseLevel= round(((TriggerPoint-(ROICloseLevel))/HRoeAddDiff) +   (ROICloseLevel) )
        Tradeslog.warning('HRoeSell  activated ROICloseLevelOld: '+str(ROICloseLevelOld)+'ROICloseLevel: '+str(ROICloseLevel))          
        HRoeInitLive =HRoeInit + 100
        HRoeSell = -500
        TriggerPoint = -500




   # Write the content of instrct.py
    with open('instrct.py', 'r') as file:
        lines = file.readlines()

    # Find the line containing 'TriggerPoint' variable and modify its value
    for i, line in enumerate(lines):
        if 'TriggerPoint=' in line:
            lines[i] = 'TriggerPoint = ' + str(TriggerPoint) + '\n'  # Modify the value to YourDesiredValue
            break

    # Write the modified content back to instrct.py
    with open('instrct.py', 'w') as file:
        file.writelines(lines)
            
            

     
        
# CALC POS CLOSE SIZE

    PosFastClose = abs(PositionSize) - min_trade_qty
    PosFastClose = round(PosFastClose, 5)
    time.sleep(0.1)

    if PosFastClose < min_trade_qty:
        PosFastClose = 0
        time.sleep(0.1)



    if StartUp == 0:
        Tradeslog.warning('PosFastClose: '+str(PosFastClose))  



# CALC POS CLOSE SIZE min for dont roi swich mode 

    PosFastCloseMin = abs(PositionSize) -  leftopen
    time.sleep(0.1)

    if PosFastCloseMin < 0 or PosFastCloseMin == None :
        PosFastCloseMin = 0
        time.sleep(0.1)



    if StartUp == 0:
        Tradeslog.warning('PosFastClose: '+str(PosFastClose))  
        Tradeslog.warning('PosFastCloseMin: '+str(PosFastCloseMin))  


    weight = roe
    calcspread1 = weight - ROICloseLevel



    while calcspread1 - spread1 > 2 and StartUp == 1:
        print("FastCalcNewROE")

        addedtakenextround = 0

        if calcspread1 > spread1:
            spezcalc = calcspread1 - spread1
        if spezcalc > 2:
            spezcalc = 2

        if spezcalc < 0:
            spezcalc = 0

        if ROICloseLevel < 0 and calcspread1 - spread1 > 2 and StartUp == 1 and not PositionSize == 0:
            ROICloseLevel += spezcalc
            spread1 += 2.25
            addedtakenextround = 1


        if ROICloseLevel == 0 and calcspread1 - spread1 > 2 and StartUp == 1 and not PositionSize == 0:
            ROICloseLevel += spezcalc
            spread1 += 2.45
            addedtakenextround = 1


        if ROICloseLevel > 0 and calcspread1 - spread1 > 2 and StartUp == 1 and not PositionSize == 0:
            ROICloseLevel += spezcalc
            spread1 += 2.65
            addedtakenextround = 1


        print("calcspread1:",calcspread1)
        print("spread1:", spread1)
        print("ROICloseLevel:", ROICloseLevel)
        time.sleep(0.05)

 

# Read the variables from varmove.py
    with open('mintrade.py', 'r') as file:
        code = file.read()

    # Execute the code to update the current variables
    exec(code)

    time.sleep(0.1)  # Delay for 2 seconds before the next iteration
    
    

        
    if PositionSize < 0 and tradehistory.movehistory_SELL_TakeProfit_COUNTER == 1:
        SELL_TakeProfit_COUNTER_lastest = tradehistory.movehistory_SELL_TakeProfit_COUNTER 

    if PositionSize < 0 and tradehistory.movehistory_SELL_TakeProfit_COUNTER == 0:
        SELL_TakeProfit_COUNTER_lastest = 0     



    

    if PositionSize > 0 and tradehistory.movehistory_BUY_TakeProfit_COUNTER == 1:
       BUY_TakeProfit_COUNTER_lastest = tradehistory.movehistory_BUY_TakeProfit_COUNTER 

    if PositionSize > 0 and tradehistory.movehistory_BUY_TakeProfit_COUNTER == 0:
       BUY_TakeProfit_COUNTER_lastest = 0 
              

     #SELL    
   
    if PositionSize < 0 and SELL_TakeProfit_COUNTER_lastest == 1 and modifedsell == 0 and setManaulTrades == 0:
        SELL_TakeProfit_COUNTER_lastest = SELL_TakeProfit_COUNTER_lastest + 1
        TakeProfitFromSELL = TakeProfitFromSELL + 15
        modifedsell = 1

    if PositionSize < 0 and SELL_TakeProfit_COUNTER_lastest == 3 and  modifedsell == 1:
        SELL_TakeProfit_COUNTER_lastest = SELL_TakeProfit_COUNTER_lastest + 1      
        TakeProfitFromSELL = TakeProfitFromSELL + 25
        modifedsell = 2


    if PositionSize < 0 and SELL_TakeProfit_COUNTER_lastest == 6 and  modifedsell == 2:
        SELL_TakeProfit_COUNTER_lastest = SELL_TakeProfit_COUNTER_lastest + 1
        TakeProfitFromSELL = TakeProfitFromSELL + 35
        modifedsell = 3

    if PositionSize < 0 and SELL_TakeProfit_COUNTER_lastest == 9 and  modifedsell == 3:
        SELL_TakeProfit_COUNTER_lastest = SELL_TakeProfit_COUNTER_lastest + 1
        TakeProfitFromSELL = TakeProfitFromSELL + 45
        modifedsell = 4

    if PositionSize < 0 and SELL_TakeProfit_COUNTER_lastest == 12 and  modifedsell == 4:
        SELL_TakeProfit_COUNTER_lastest = SELL_TakeProfit_COUNTER_lastest + 1
        TakeProfitFromSELL = TakeProfitFromSELL + 55
        ROICloseLevel = ROICloseLevel + 15
        modifedsell = 5

    if PositionSize < 0 and SELL_TakeProfit_COUNTER_lastest == 15 and  modifedsell == 5:
        SELL_TakeProfit_COUNTER_lastest = SELL_TakeProfit_COUNTER_lastest + 1
        TakeProfitFromSELL = TakeProfitFromSELL + 55
        ROICloseLevel = ROICloseLevel + 20
        modifedsell = 6

    if PositionSize < 0 and SELL_TakeProfit_COUNTER_lastest == 20 and  modifedsell == 6:
        SELL_TakeProfit_COUNTER_lastest = SELL_TakeProfit_COUNTER_lastest + 1
        TakeProfitFromSELL = TakeProfitFromSELL + 55
        ROICloseLevel = ROICloseLevel + 25
        modifedsell = 7

    if PositionSize < 0 and SELL_TakeProfit_COUNTER_lastest == 25 and  modifedsell == 7:
        SELL_TakeProfit_COUNTER_lastest = SELL_TakeProfit_COUNTER_lastest + 1
        TakeProfitFromSELL = TakeProfitFromSELL + 55    
        
        
        
        
    if PositionSize < 0 and SELL_TakeProfit_COUNTER_lastest < tradehistory.movehistory_SELL_TakeProfit_COUNTER :
        SELL_TakeProfit_COUNTER_lastest = SELL_TakeProfit_COUNTER_lastest + 1
        TakeProfitFromSELL = TakeProfitFromSELL + 16


    if tradehistory.movehistory_SELL_Order_ROI_Switcher_COUNTER > 0 :
        modifedsell = 0

    logging.warning('StopTrades_Valve_ Modification_SELL_ON_START: '+str(StopTrades))
    logging.warning('Takeprofit_Valve_ Modification_SELL_ON_START: '+str(TakeProfitFromSELL))  
    logging.warning('ROICloseLevel_Valve_ Modification_SELL_ON_START: '+str(ROICloseLevel))  




 
    if PositionSize < 0 and tradehistory.movehistory_SELL_Loop_COUNTER == 1 and lockedthatSELL == 0:
        SELL_Loop_COUNTER_lastest = tradehistory.movehistory_SELL_Loop_COUNTER
        lockedthatSELL= 1

    if PositionSize < 0 and tradehistory.movehistory_SELL_Order_ROI_Switcher_COUNTER > 0:
        SELL_Loop_COUNTER_lastest = 0 
        lockedthatSELL= 0


    if PositionSize < 0 and SELL_Loop_COUNTER_lastest < tradehistory.movehistory_SELL_Loop_COUNTER:
        SELL_Loop_COUNTER_lastest = SELL_Loop_COUNTER_lastest + 1

      

   
    #BUY
    

       
   
    
    if PositionSize > 0 and BUY_TakeProfit_COUNTER_lastest == 1 and modifedbuy == 0 and setManaulTrades == 0:
        BUY_TakeProfit_COUNTER_lastest = BUY_TakeProfit_COUNTER_lastest + 1
        TakeProfitFromBUY = TakeProfitFromBUY + 15
        modifedbuy = 1 

    if PositionSize > 0 and BUY_TakeProfit_COUNTER_lastest == 3 and modifedbuy == 1:
        BUY_TakeProfit_COUNTER_lastest = BUY_TakeProfit_COUNTER_lastest + 1
        TakeProfitFromBUY = TakeProfitFromBUY + 25
        modifedbuy = 2   

    if PositionSize > 0 and BUY_TakeProfit_COUNTER_lastest == 6 and modifedbuy == 2:
        BUY_TakeProfit_COUNTER_lastest = BUY_TakeProfit_COUNTER_lastest + 1
        TakeProfitFromBUY = TakeProfitFromBUY + 25
        modifedbuy = 3   

    if PositionSize > 0 and BUY_TakeProfit_COUNTER_lastest == 9 and modifedbuy == 3:
        BUY_TakeProfit_COUNTER_lastest = BUY_TakeProfit_COUNTER_lastest + 1
        TakeProfitFromBUY = TakeProfitFromBUY + 45
        modifedbuy = 4   
                
    if PositionSize > 0 and  BUY_TakeProfit_COUNTER_lastest == 12 and modifedbuy == 4:
        BUY_TakeProfit_COUNTER_lastest = BUY_TakeProfit_COUNTER_lastest + 1
        TakeProfitFromBUY = TakeProfitFromBUY + 55
        ROICloseLevel = ROICloseLevel + 15
        modifedbuy = 5

    if PositionSize > 0 and  BUY_TakeProfit_COUNTER_lastest == 15 and modifedbuy == 5:
        BUY_TakeProfit_COUNTER_lastest = BUY_TakeProfit_COUNTER_lastest + 1
        TakeProfitFromBUY = TakeProfitFromBUY + 55
        ROICloseLevel = ROICloseLevel + 20
        modifedbuy = 6
 
    if PositionSize > 0 and  BUY_TakeProfit_COUNTER_lastest == 20 and modifedbuy == 6:
        BUY_TakeProfit_COUNTER_lastest = BUY_TakeProfit_COUNTER_lastest + 1
        TakeProfitFromBUY = TakeProfitFromBUY + 55
        ROICloseLevel = ROICloseLevel + 25
        modifedbuy = 7

    if PositionSize > 0 and  BUY_TakeProfit_COUNTER_lastest == 25 and modifedbuy == 7:
        BUY_TakeProfit_COUNTER_lastest = BUY_TakeProfit_COUNTER_lastest + 1
        TakeProfitFromBUY = TakeProfitFromBUY + 55
        
              
              

    if PositionSize > 0 and BUY_TakeProfit_COUNTER_lastest < tradehistory.movehistory_BUY_TakeProfit_COUNTER :
        BUY_TakeProfit_COUNTER_lastest = BUY_TakeProfit_COUNTER_lastest + 1
        TakeProfitFromBUY = TakeProfitFromBUY + 16

                        
    if  tradehistory.movehistory_BUY_Order_ROI_Switcher_COUNTER > 0 :
        modifedbuy = 0

    logging.warning('StopTrades_Valve_ Modification_BUY_ON_START: '+str(StopTrades))
    logging.warning('Takeprofit_Valve_ Modification_BUY_ON_START: '+str(TakeProfitFromBUY))  
    logging.warning('ROICloseLevel_Valve_ Modification_BUY_ON_START: '+str(ROICloseLevel))  
        
        


    if PositionSize > 0 and tradehistory.movehistory_BUY_Loop_COUNTER == 1 and lockedthatBUY == 0:
        BUY_Loop_COUNTER_lastest = tradehistory.movehistory_BUY_Loop_COUNTER
        lockedthatBUY = 1


    if PositionSize > 0 and tradehistory.movehistory_BUY_Loop_COUNTER == 0 and tradehistory.movehistory_BUY_TakeProfit_COUNTER  == 0:
        BUY_Loop_COUNTER_lastest = 0
        lockedthatBUY = 0


    if PositionSize > 0 and BUY_Loop_COUNTER_lastest < tradehistory.movehistory_BUY_Loop_COUNTER:
        BUY_Loop_COUNTER_lastest = BUY_Loop_COUNTER_lastest + 1
            









#CHECK HOW MANY TIME SELL TRADES OPEN Trade AMOUNT * X  



    if PositionSize > 0 and PositionSize < TradeAmount:
        PosSizetest = 0
        logging.warning('PosSizetest: '+str(PosSizetest))  
        logging.warning('PosSizetest: '+str(PosSizetest))  
        logging.warning('PosSizetest: '+str(PosSizetest))  
        logging.warning('PosSizetest: '+str(PosSizetest))  

    if PositionSize > 0 and PositionSize >=  TradeAmount:
        PosSizetest = ( PositionSize  ) / ( round(TradeAmount ,5)) 
        logging.warning('PosSizetest: '+str(PosSizetest))  
        logging.warning('PosSizetest: '+str(PosSizetest))  
        logging.warning('PosSizetest: '+str(PosSizetest))  
        logging.warning('PosSizetest: '+str(PosSizetest))  
        
        

    if PositionSize < 0 and abs(PositionSize) < TradeAmount:
        PosSizetest = 0
        logging.warning('PosSizetest: '+str(PosSizetest))  
        logging.warning('PosSizetest: '+str(PosSizetest))  
        logging.warning('PosSizetest: '+str(PosSizetest))  
        logging.warning('PosSizetest: '+str(PosSizetest))  

    if PositionSize < 0 and abs(PositionSize)  >=  TradeAmount:
        PosSizetest = abs(PositionSize) / ( round(TradeAmount ,5)) 
        logging.warning('PosSizetest: '+str(PosSizetest))  
        logging.warning('PosSizetest: '+str(PosSizetest))  
        logging.warning('PosSizetest: '+str(PosSizetest))  
        logging.warning('PosSizetest: '+str(PosSizetest))  


    if StartUp == 0 :      
        TakeProfitFromBUY = TakeProfitFromBUYInitial
        TakeProfitFromSELL = TakeProfitFromSELLInitial
        ROICloseLevel = ROICloseLevelInitial
        spread1 = spread1Initial
        
        
    if PositionSize > 0 and  BUYOrderActive  == 1 and SELLOrderActive == 0 and weight > TakeProfitFromBUY + 22  and StartUp == 0 :      
        TakeProfitFromBUY = round(weight + 3)
        StartUp = 1
        logging.warning('StartUp: '+str(StartUp))  

    if PositionSize < 0 and  SELLOrderActive == 1 and BUYOrderActive  == 0 and weight > TakeProfitFromSELL + 22  and StartUp == 0 :     
        TakeProfitFromSELL = round(weight + 3)
        StartUp = 1
        logging.warning('StartUp: '+str(StartUp))  
        

    StartUp = 1





    
#MRY1
#SMALLHOLD BUY SELL MOVE to x1 Trades when LOW Profit  
    weight = (roe)

    if abs(PositionSize) < min_trade_qty and  PositionSize < 0 and weight > setDOWNstart:     
        SmallHOLDSELLStartCounter = SmallHOLDSELLStartCounter + 1 
        logging.warning('SmallHOLDSELLStartCounter: '+str(SmallHOLDSELLStartCounter)) 
    if abs(PositionSize) > min_trade_qty :    
        SmallHOLDSELLStartCounter = 0        
          
        
    if abs(PositionSize) < min_trade_qty and PositionSize > 0  and weight > setDOWNstart:       
        SmallHOLDBUYStartCounter = SmallHOLDBUYStartCounter + 1
        logging.warning('SmallHOLDBUYStartCounter: '+str(SmallHOLDBUYStartCounter))        
    if abs(PositionSize) > min_trade_qty :
        SmallHOLDBUYStartCounter = 0           
           	 	


    #SELLPOSITION     
    if smallholdsmallroiEnable== 1 and abs(PositionSize) < min_trade_qty and PositionSize < 0 and  SmallHOLDSELLStartCounter == SmallHOLDSELLStartCounterLIMIT:
        reducetradeTrue = 1
        reducetrade(symbol,min_trade_qty)
        
    if reducetradeTrue == 1:
        reducetradeTrue = 0
        TakeProfitBUYCounter = 0
        countDown = 0      
        SmallHOLDSELLStartCounter = 0  
        ROICloseLevel = ROICloseLevelInitial
        TakeProfitFromSELL = TakeProfitFromSELLInitial
        TakeProfitFromBUY = TakeProfitFromBUYInitial
        spread1 = spread1Initial
        Tradeslog.warning("ADD 1x to SMALLHOLDPositionSELL")
        SetPrg(1)          




        
        
      

        
    #BUYPOSITION 
    if  smallholdsmallroiEnable== 1 and abs(PositionSize) < min_trade_qty and PositionSize > 0 and SmallHOLDBUYStartCounter == SmallHOLDBUYStartCounterLIMIT:
        optimazetradeTrue = 1
        optimazetrade(symbol,min_trade_qty)
        
    if optimazetradeTrue == 1:
        optimazetradeTrue = 0
        TakeProfitSELLCounter = 0
        countUP = 0   
        SmallHOLDBUYStartCounter = 0
        ROICloseLevel = ROICloseLevelInitial
        TakeProfitFromSELL = TakeProfitFromSELLInitial
        TakeProfitFromBUY = TakeProfitFromBUYInitial
        spread1 = spread1Initial 
        Tradeslog.warning("ADD 1x to SMALLHOLDadded")
        SetPrg(11)          



    

 
     
     
                        	          

#MRY3        
#STOP TRADES	    
    weight = (roe)




    if PositionSize <0 and PositionSize  < PositionLimitSELL :
    	logging.warning ("PositionLimitSELL_OVER LIMIT!!!!!!")
    	
    if PositionSize <0 and PositionSize == PositionLimitSELL :
    	logging.warning ("PositionLimitSELL_Reached")




    if PositionSize > 0 and PositionSize > PositionLimitBUY :
    	logging.warning ("PositionLimitBUY_OVER LIMIT!!!!!!")
    	
    if PositionSize > 0 and PositionSize == PositionLimitBUY :
    	logging.warning ("PositionLimitBUY_Reached")    	
    	  
   


    	
    	
    	    	    	 	
#MRY4 
#SELL LOOP	    
    weight = (roe)
    if EnableSELL == 1 and  weight < StopTrades and countDown == countDownLIMIT and PositionSize < 0 and PositionSize > PositionLimitSELL and SellLoopSelf_Counter == 0 :   
        reducetradeTrue = 1
        Tradeslog.warning("Try to SELL LOOP SELL 1x") 
        reducetrade(symbol,TradeAmount)


            
    if reducetradeTrue == 1:
        sellstop_set = 0
        SetPrg(3)
        reducetradeTrue = 0
        TakeProfitBUYCounter = 0
        SELLTradesCounter = SELLTradesCounter + 1
        countDown = 0
        SELLTradeThisLoop = 1
        SellLoopSelf_Counter = SellLoopSelf_Counter + 1
        Tradeslog.warning("SELL LOOP SELL 1x Done ;-)") 
                
                                        
    elif	PositionLimitSELL == PositionSize:
    	logging.warning ("PositionLimitReachedSELL")
    else:
    	logging.warning("NOTHING_SELL_LOOP")
    	SELLTradeThisLoop = 0    	
       
    if SellLoopSelf_Counter > 0:
        SellLoopSelf_Counter = SellLoopSelf_Counter + 1
        logging.warning('SELLLoopSelf_Counter Delay last Trade: '+str(SellLoopSelf_Counter))        
        
    if SellLoopSelf_Counter == SellLoopSelf_CounterLIMIT: #Solid mit 15
        SellLoopSelf_Counter = 0



    logging.warning('SELLLoopSelf_Counter Delay last Trade: '+str(SellLoopSelf_Counter))  		  
    	
    #SELL LOOP GROWER 
        
#    if PositionSize < 0 and tradehistory.movehistory_SELL_TakeProfit_COUNTER == 1:
#        GROWER_SELL_TakeProfit_COUNTER_lastest = GROWER_SELL_TakeProfit_COUNTER_lastest + 1
#
#    if PositionSize < 0 and not tradehistory.movehistory_SELL_TakeProfit_COUNTER == 1 and not tradehistory.movehistory_SELL_TakeProfit_COUNTER == 0  and GROWER_SELL_TakeProfit_COUNTER_lastest < tradehistory.movehistory_SELL_TakeProfit_COUNTER:
#        GROWER_SELL_TakeProfit_COUNTER_lastest = GROWER_SELL_TakeProfit_COUNTER_lastest + 1
#
#    if PositionSize < 0 and tradehistory.movehistory_SELL_TakeProfit_COUNTER == 0:
#        GROWER_SELL_TakeProfit_COUNTER_lastest = 0             
#        
#    if PositionSize < 0 and GROWER_SELL_TakeProfit_COUNTER_lastest == 8 and PositionSize > PositionLimitSELL2 :
#        GROWER_SELL_TakeProfit_COUNTER_lastest = 0 
#        reducetrade(symbol,TradeAmount)
#        reducetrade(symbol,TradeAmount)
#        SELLTradesCounter = SELLTradesCounter + 2
#        countUP = 0
#        Tradeslog.warning("SELL GROWER SELL 2x")               


    

    
    if EnableGrowerSELL == 1 and StartUp == 1 and PositionSize < 0 and  ROICloseLevel > 15 and  weight - ROICloseLevel > StartGrowDiff  and PositionSize > PositionLimitSELL2 :
        GROWER_SELL_TakeProfit_COUNTER_lastest = 0 
        reducetrade(symbol,TradeAmount)
        SELLTradesCounter = SELLTradesCounter + 1
        countUP = 0
        ROICloseLevel = ROICloseLevelInitial
        spread1 = spread1Initial
        GrowCount= GrowCount + 1
        StartGrowDiff = StartGrowDiff + ( round(StartGrowDiffAdd  +  (20 *  GrowCount)  ) )
        Tradeslog.warning("SELL GROWER SELL 1x")  
        Tradeslog.warning('SELL GROWER SELL 1x: NEW StartGrowDiff is =  '+str(StartGrowDiff))    
        Tradeslog.warning('SELL GROWER SELL 1x: GrowCount is =  '+str(GrowCount))  
    
    
    
    
    
    







	
#MRY5    	
#BUY LOOP

    weight = (roe)
    if  EnableBUY == 1 and weight < StopTrades and countUP == countUPLIMIT and PositionSize > 0 and PositionSize < PositionLimitBUY and BUYLoopSelf_Counter == 0 :
        optimazetradeTrue == 1
        Tradeslog.warning("Try to BUY LOOP BUY 1x") 
        optimazetrade(symbol,TradeAmount)





    if optimazetradeTrue == 1:
        buystop_set = 0
        SetPrg(4)
        optimazetradeTrue = 0
        TakeProfitSELLCounter = 0
        BUYTradesCounter = BUYTradesCounter + 1
        countUP = 0
        BUYTradeThisLoop = 1  
        BUYLoopSelf_Counter = BUYLoopSelf_Counter +1
        Tradeslog.warning("BUY LOOP BUY 1x Done ;-)") 
 
    elif	PositionLimitBUY == PositionSize:
    	logging.warning ("PositionLimitReachedBUY")
    else:
    	logging.warning("NOTHING_BUY_LOOP")
    	BUYTradeThisLoop = 0
        
    if BUYLoopSelf_Counter > 0:
        BUYLoopSelf_Counter = BUYLoopSelf_Counter + 1
        logging.warning('BUYLoopSelfCounter Delay last Trade: '+str(BUYLoopSelf_Counter))      

    if BUYLoopSelf_Counter == BUYLoopSelf_CounterLIMIT:  #Solid mit 15
        BUYLoopSelf_Counter = 0


        
    logging.warning('BUYLoopSelfCounter Delay last Trade: '+str(BUYLoopSelf_Counter)) 


     
    #BUY LOOP GROWER 
    
#    if PositionSize > 0 and tradehistory.movehistory_BUY_TakeProfit_COUNTER == 1:
#        GROWER_BUY_TakeProfit_COUNTER_lastest = GROWER_BUY_TakeProfit_COUNTER_lastest +1 

#    if PositionSize > 0 and not tradehistory.movehistory_BUY_TakeProfit_COUNTER == 1 and not tradehistory.movehistory_BUY_TakeProfit_COUNTER == 0  and GROWER_BUY_TakeProfit_COUNTER_lastest < tradehistory.movehistory_BUY_TakeProfit_COUNTER :
#        GROWER_BUY_TakeProfit_COUNTER_lastest = GROWER_BUY_TakeProfit_COUNTER_lastest +1 

#    if PositionSize > 0 and tradehistory.movehistory_BUY_TakeProfit_COUNTER == 0:
#        GROWER_BUY_TakeProfit_COUNTER_lastest = 0             
        
#    if PositionSize > 0 and GROWER_BUY_TakeProfit_COUNTER_lastest == 8 and PositionSize < PositionLimitBUY2 :
#        GROWER_BUY_TakeProfit_COUNTER_lastest = 0
#        optimazetrade(symbol,TradeAmount)
#        optimazetrade(symbol,TradeAmount)
#        BUYTradesCounter = BUYTradesCounter + 2
#        countUP = 0
#        Tradeslog.warning("BUY GROWER BUY 2x")          
        
    
    
      
    

    
    if EnableGrowerBUY == 1 and StartUp == 1 and PositionSize > 0 and  ROICloseLevel > 15 and  weight - ROICloseLevel > StartGrowDiff  and PositionSize < PositionLimitBUY2 :
        GROWER_BUY_TakeProfit_COUNTER_lastest = 0 
        optimazetrade(symbol,TradeAmount)  
        BUYTradesCounter = BUYTradesCounter + 1
        countUP = 0
        ROICloseLevel = ROICloseLevelInitial
        spread1 = spread1Initial
        GrowCount= GrowCount + 1
        StartGrowDiff = StartGrowDiff + ( round(StartGrowDiffAdd  +  (20 *  GrowCount)  ) )
        Tradeslog.warning("BUY GROWER BUY 1x")  
        Tradeslog.warning('BUY GROWER BUY 1x: NEW StartGrowDiff is =  '+str(StartGrowDiff))    
        Tradeslog.warning('BUY GROWER BUY 1x: GrowCount is =  '+str(GrowCount))  
        
    




        


    weight = (roe)

    setHroiCloseSELL =0  
    setHroiCloseBUY =0  
 
   
    #SELL TRADES STOP ROI UNDER LEVEL
    if changeside == 1 and PositionSize < 0 and Locked1 == 0:
        if min_trade_qty > 1 or min_trade_qty == 1:
            min_trade_qty = round(min_trade_qty)
        elif min_trade_qty < 1 and not min_trade_qty < 0.1:
            min_trade_qty = round(min_trade_qty, 1)
        elif min_trade_qty < 0.1 and not min_trade_qty < 0.01:
            min_trade_qty = round(min_trade_qty, 2)
        else:
            min_trade_qty = round(min_trade_qty, 3)             
        print('Rounded3'    +str(min_trade_qty ) +    '           min_trade_qty = ' +str(min_trade_qty )) 
        
        TradeAmount=nextamount
        Tradeslog.warning('Changseide TradeAmount='+str(TradeAmount))      

        min_trade_qty = round(min_trade_qty + min_trade_qty, 3)
        optimazetrade_reduceOnly(symbol,PosFastClose)
        optimazetrade(symbol,min_trade_qty)
        SetPrg(5)
        Locked1 = 1
        
        # Read the content of instrct.py
        with open('instrct.py', 'r') as file:
            lines = file.readlines()
        # Find the line containing 'changeside' variable and modify its value
        for i, line in enumerate(lines):
            if 'changeside=' in line:
                lines[i] = 'changeside=0\n'  # Modify the value to 0
                break
        # Write the modified content back to instrct.py
        with open('instrct.py', 'w') as file:
            file.writelines(lines)

        ROICloseLevel = ROICloseLevelInitial
        TakeProfitFromSELL = TakeProfitFromSELLInitial
        TakeProfitFromBUY = TakeProfitFromBUYInitial
        spread1 = spread1Initial
        
        Tradeslog.warning('SELL ORDER swich Order PosFastAmount='+str(PosFastClose))        
        Tradeslog.warning('SELL ORDER swich Order min_trade_qty='+str(min_trade_qty))             
        Tradeslog.warning('SELL ORDER swich Order PNL='+str(PNL))     
        Tradeslog.warning('SELL ORDER swich Order weight='+str(weight))    


  
        
#FOR BUY ORDER ROI UNDER LEVEL swicth to SELL Order
      
      
    #BUY TRADES STOP ROI UNDER LEVEL
    

    
    if changeside == 1 and PositionSize > 0 and Locked2 == 0:
        if min_trade_qty > 1 or min_trade_qty == 1:
            min_trade_qty = round(min_trade_qty)
        elif min_trade_qty < 1 and not min_trade_qty < 0.1:
            min_trade_qty = round(min_trade_qty, 1)
        elif min_trade_qty < 0.1 and not min_trade_qty < 0.01:
            min_trade_qty = round(min_trade_qty, 2)
        else:
            min_trade_qty = round(min_trade_qty, 3)             
        print('Rounded3'    +str(min_trade_qty ) +    '           min_trade_qty = ' +str(min_trade_qty )) 

        TradeAmount=nextamount
        Tradeslog.warning('Changseide TradeAmount='+str(TradeAmount))         

        min_trade_qty = round(min_trade_qty + min_trade_qty, 3)    
        reducetrade_reduceOnly(symbol,PosFastClose)
        reducetrade(symbol,min_trade_qty)
        SetPrg(6)
        Locked2 = 1 

        # Read the content of instrct.py
        with open('instrct.py', 'r') as file:
            lines = file.readlines()

        # Find the line containing 'changeside' variable and modify its value
        for i, line in enumerate(lines):
            if 'changeside=' in line:
                lines[i] = 'changeside=0\n'  # Modify the value to 0
                break

        # Write the modified content back to instrct.py
        with open('instrct.py', 'w') as file:
            file.writelines(lines)


        ROICloseLevel = ROICloseLevelInitial
        TakeProfitFromSELL = TakeProfitFromSELLInitial
        TakeProfitFromBUY = TakeProfitFromBUYInitial
        spread1 = spread1Initial            
            
            
        Tradeslog.warning('BUY ORDER swich Order PosFastAmount='+str(PosFastClose))        
        Tradeslog.warning('BUY ORDER swich Order min_trade_qty='+str(min_trade_qty))             
        Tradeslog.warning('BUY ORDER swich Order PNL='+str(PNL))     
        Tradeslog.warning('BUY ORDER swich Order weight='+str(weight))      




   




    	    
    	   
#MRY6
#FOR SELL ORDER ROI UNDER LEVEL swicth to BUY Order
    weight = (roe)
    Locked1 = 0
    Locked2 = 0
    setHroiCloseSELL =0  
    setHroiCloseBUY =0  
 
   
    #SELL TRADES STOP ROI UNDER LEVEL
    if ROISwicherInvert == 1 and weight < ROICloseLevel and PositionSize < 0 and Locked1 == 0:
        if min_trade_qty > 1 or min_trade_qty == 1:
            min_trade_qty = round(min_trade_qty)
        elif min_trade_qty < 1 and not min_trade_qty < 0.1:
            min_trade_qty = round(min_trade_qty, 1)
        elif min_trade_qty < 0.1 and not min_trade_qty < 0.01:
            min_trade_qty = round(min_trade_qty, 2)
        else:
            min_trade_qty = round(min_trade_qty, 3)        

        if Switchy ==0 :            
            TradeAmount=nextamount
            Tradeslog.warning('Changseide TradeAmount='+str(TradeAmount))         
                
      
        min_trade_qty = round(min_trade_qty + min_trade_qty, 3)
        optimazetrade_reduceOnly(symbol,PosFastClose)
        optimazetrade(symbol,min_trade_qty)
        SetPrg(5)
        Locked1 = 1        
        ROICloseLevel = ROICloseLevelInitial
        TakeProfitFromSELL = TakeProfitFromSELLInitial
        TakeProfitFromBUY = TakeProfitFromBUYInitial
        spread1 = spread1Initial


        Tradeslog.warning('SELL ORDER swich Order PosFastAmount='+str(PosFastClose))        
        Tradeslog.warning('SELL ORDER swich Order min_trade_qty='+str(min_trade_qty))             
        Tradeslog.warning('SELL ORDER swich Order PNL='+str(PNL))     
        Tradeslog.warning('SELL ORDER swich Order weight='+str(weight))      
        print('Rounded3'    +str(min_trade_qty ) +    '           min_trade_qty = ' +str(min_trade_qty )) 




#FOR BUY ORDER ROI UNDER LEVEL swicth to SELL Order
      
      
    #BUY TRADES STOP ROI UNDER LEVEL
    

    
    if ROISwicherInvert == 1 and weight < ROICloseLevel and PositionSize > 0 and Locked2 == 0:
        if min_trade_qty > 1 or min_trade_qty == 1:
            min_trade_qty = round(min_trade_qty)
        elif min_trade_qty < 1 and not min_trade_qty < 0.1:
            min_trade_qty = round(min_trade_qty, 1)
        elif min_trade_qty < 0.1 and not min_trade_qty < 0.01:
            min_trade_qty = round(min_trade_qty, 2)
        else:
            min_trade_qty = round(min_trade_qty, 3)        

        if Switchy ==0 :            
            TradeAmount=nextamount
            Tradeslog.warning('Changseide TradeAmount='+str(TradeAmount))         
    
               
        min_trade_qty = round(min_trade_qty + min_trade_qty, 3)    
        reducetrade_reduceOnly(symbol,PosFastClose)
        reducetrade(symbol,min_trade_qty)
        SetPrg(6)
        Locked2 = 1                 
        ROICloseLevel = ROICloseLevelInitial
        TakeProfitFromSELL = TakeProfitFromSELLInitial
        TakeProfitFromBUY = TakeProfitFromBUYInitial
        spread1 = spread1Initial
        
        
        
        
        Tradeslog.warning('BUY ORDER swich Order PosFastAmount='+str(PosFastClose))        
        Tradeslog.warning('BUY ORDER swich Order min_trade_qty='+str(min_trade_qty))             
        Tradeslog.warning('BUY ORDER swich Order PNL='+str(PNL))     
        Tradeslog.warning('BUY ORDER swich Order weight='+str(weight))
        print('Rounded3'    +str(min_trade_qty ) +    '           min_trade_qty = ' +str(min_trade_qty )) 




#MRY6
#FOR SELL ORDER ROI UNDER LEVEL swicth to BUY Order onlyGoToMin  onlyGoToMin  onlyGoToMin
    weight = (roe)
    Locked1 = 0
    Locked2 = 0
    setHroiCloseSELL =0  
    setHroiCloseBUY =0  
 
   
    #SELL TRADES STOP ROI UNDER LEVEL
    if onlyGoToMin == 1 and ROISwicherInvert == 0 and weight < ROICloseLevel and PositionSize < 0 and abs(PositionSize) > (2 * leftopen) and Locked1 == 0:
        if Switchy ==0 :            
            TradeAmount=nextamount
            Tradeslog.warning('Changseide TradeAmount='+str(TradeAmount))         
        optimazetrade_reduceOnly(symbol,PosFastCloseMin)
        SetPrg(5)
        Locked1 = 1        
        ROICloseLevel = ROICloseLevelInitial
        TakeProfitFromSELL = TakeProfitFromSELLInitial
        TakeProfitFromBUY = TakeProfitFromBUYInitial
        spread1 = spread1Initial


        Tradeslog.warning('SELL ORDER reduce, red. Amount was='+str(PosFastCloseMin))        
        Tradeslog.warning('SELL ORDER swich Order min_trade_qty='+str(min_trade_qty))             
        Tradeslog.warning('SELL ORDER swich Order PNL='+str(PNL))     
        Tradeslog.warning('SELL ORDER swich Order weight='+str(weight))      





#FOR BUY ORDER ROI UNDER LEVEL swicth to SELL Order  onlyGoToMin  onlyGoToMin  onlyGoToMin
      
      
    #BUY TRADES STOP ROI UNDER LEVEL
    

    
    if onlyGoToMin == 1 and ROISwicherInvert == 0 and weight < ROICloseLevel and PositionSize > 0 and abs(PositionSize) > (2 * leftopen) and Locked2 == 0:
        if Switchy ==0 :            
            TradeAmount=nextamount
            Tradeslog.warning('Changseide TradeAmount='+str(TradeAmount))            
               

        reducetrade_reduceOnly(symbol,PosFastCloseMin)
        SetPrg(6)
        Locked2 = 1                 
        ROICloseLevel = ROICloseLevelInitial
        TakeProfitFromSELL = TakeProfitFromSELLInitial
        TakeProfitFromBUY = TakeProfitFromBUYInitial
        spread1 = spread1Initial
        
        
        
        
        Tradeslog.warning('BUY ORDER reduce, red. Amount was='+str(PosFastCloseMin))        
        Tradeslog.warning('BUY ORDER swich Order min_trade_qty='+str(min_trade_qty))             
        Tradeslog.warning('BUY ORDER swich Order PNL='+str(PNL))     
        Tradeslog.warning('BUY ORDER swich Order weight='+str(weight))



              

  


#MRY10
#TAKE PROFIT from SELL ORDER    	
    weight = (roe)
    lokedTakeP_SELL = 0    
   

    if PositionSize < 0 :
       closeSizeSELL   = round( PosSizetest * 8 ) /  100
       closeSizeSELL = round( closeSizeSELL )
    if closeSizeSELL < 1:
         closeSizeSELL = 1   
    logging.warning('TAKE-Profit-closeSizeSELL: '+str(closeSizeSELL))
    
    
    if PositionSize < 0 :
       closeSizeSELLRoiUnderLevel    = PosSizetest
       closeSizeSELLRoiUnderLevel  = round(closeSizeSELLRoiUnderLevel) + 2
       logging.warning('closeSizeSELLRoiUnderLevel : '+str(closeSizeSELLRoiUnderLevel))




    if TakeProfit ==1 and PositionSize < 0 and weight - TakeProfitFromSELL > 30:
        TakeProfitFromSELL = round( TakeProfitFromSELL + ( (weight - TakeProfitFromSELL) / 3 ) )
        ROICloseLevel = ROICloseLevel + 3
        time.sleep(2) 
        Tradeslog.warning("Changed TakeProfitFromSELL because of big Waves")    
  
    
    if TakeProfit ==1 and  weight > TakeProfitFromSELL  and  PosSizetest > 2 and PositionSize < 0 and lokedTakeP_SELL == 0:
        Tradeslog.warning('TAKE PROFIT from SELL ORDER: '+str(closeSizeSELL))
        for _ in range(closeSizeSELL):
             optimazetrade(symbol,TradeAmount)
             reducetrade(symbol,TradeAmount)              
             WinAmount = WinAmount + ( pnl / PosSizetest )  *  (closeSizeBUY) 
        SetPrg(7)          
        BUYTradesCounter = BUYTradesCounter + 1
        TakeProfitSELLCounter = TakeProfitSELLCounter + 1
        lokedTakeP_SELL = 1
      


    #Take-Half Part TakeProfitFromSELL2/2

    TakeHalfSize = round( closeSizeSELLRoiUnderLevel / 2 )
    TakeAllSize = round(  closeSizeSELLRoiUnderLevel + 1 )

    if TakeProfit ==1 and weight > TakeProfitFromSELL2 and PositionSize < 0 and lokedTakeP_SELL == 0 and TakeAllModus == 0 and TakedSell == 0:
        for _ in range(TakeHalfSize):
             optimazetrade(symbol,TradeAmount)
             ROICloseLevel = ROICloseLevelInitial
             spread1 = spread1Initial
             TakeProfitFromSELL = TakeProfitFromSELLInitial
             TakeProfitFromBUY = TakeProfitFromBUYInitial
             Tradeslog.warning('TakeHalfSize from SELL ORDER: '+str(TakeHalfSize)) 
             Tradeslog.warning('Lowered ROICloseLevel (TakeHalfSizeSELL): '+str(ROICloseLevel)) 
        SetPrg(7)        
        lokedTakeP_SELL = 1
        TakedSell = 1


    if weight > (TakeProfitFromSELL2 * 3) :
        TakedSell = 0    


    if TakeProfit ==1 and weight > (TakeProfitFromSELL2 * 2) and PositionSize < 0 and lokedTakeP_SELL == 0 and TakeAllModus == 0 and TakedSell == 0:
        for _ in range(TakeHalfSize):
             optimazetrade(symbol,TradeAmount)
             ROICloseLevel = ROICloseLevelInitial
             spread1 = spread1Initial
             TakeProfitFromSELL = TakeProfitFromSELLInitial
             TakeProfitFromBUY = TakeProfitFromBUYInitial
             Tradeslog.warning('TakeHalfSize from SELL ORDER: '+str(TakeHalfSize)) 
             Tradeslog.warning('Lowered ROICloseLevel (TakeHalfSizeSELL): '+str(ROICloseLevel)) 
        SetPrg(7)        
        lokedTakeP_SELL = 1
        TakedSell = 1
        
        
    #Takeall Part TakeProfitFromSELL +1
    
    if TakeProfit ==1 and weight > TakeProfitFromSELL2 and PositionSize < 0 and lokedTakeP_SELL == 0 and TakeAllModus == 1 and TakedSell == 0:
        for _ in range(TakeAllSize + 1):
             optimazetrade(symbol,TradeAmount)
             Tradeslog.warning('TakeAll from SELL ORDER: '+str(TakeAllSize)) 
        SetPrg(7)          
        lokedTakeP_SELL = 1
        TakedSell = 1
    


    
    if TakedSell == 1 and PositionSize > 0:
        TakedSell = 0              

       


          
#MRY11
#TAKE PROFIT from BUY ORDER
    	
    weight = (roe)
    lokedTakeP_BUY = 0
    
    if PositionSize > 0 :
        closeSizeBUY  = round( PosSizetest * 8 ) / 100
        closeSizeBUY = round( closeSizeBUY )
    if closeSizeBUY < 1:
         closeSizeBUY = 1    
    logging.warning('TAKE-Profit-closeSizeBUY: '+str(closeSizeBUY))
    
    

    if PositionSize > 0 :
        closeSizeBUYRoiUnderLevel  = PosSizetest 
        closeSizeBUYRoiUnderLevel  = round(closeSizeBUYRoiUnderLevel) + 2
        logging.warning('closeSizeBUYRoiUnderLevel : '+str(closeSizeBUYRoiUnderLevel))


    if TakeProfit ==1 and PositionSize > 0 and weight - TakeProfitFromBUY > 25:
        TakeProfitFromBUY = round( TakeProfitFromBUY + ( (weight - TakeProfitFromBUY) / 3 ) )
        ROICloseLevel = ROICloseLevel + 3    
        time.sleep(2)
        Tradeslog.warning("Changed TakeProfitFromBUY because of big Waves")  
            
    if TakeProfit ==1 and weight > TakeProfitFromBUY  and  PosSizetest > 2 and PositionSize > 0 and lokedTakeP_BUY  == 0 :
        Tradeslog.warning('TAKE PROFIT from BUY ORDER: '+str(closeSizeBUY))      
        for _ in range(closeSizeBUY):
             reducetrade(symbol,TradeAmount)
             optimazetrade(symbol,TradeAmount)                
             WinAmount = WinAmount + ( pnl / PosSizetest )  *  (closeSizeBUY) 
        SELLTradesCounter = SELLTradesCounter + 1
        TakeProfitBUYCounter = TakeProfitBUYCounter + 1
        SetPrg(8)
        lokedTakeP_BUY = 1






    #Take-Half Part TakeProfitFromBUY2/2

    TakeHalfSize = round( closeSizeBUYRoiUnderLevel / 2 ) 
    TakeAllSize = round(  closeSizeBUYRoiUnderLevel + 1 )

    if TakeProfit ==1 and weight > TakeProfitFromBUY2 and PositionSize > 0 and TakeAllModus == 0 and lokedTakeP_BUY == 0 and TakedBuy == 0:
        for _ in range(TakeHalfSize):
             reducetrade(symbol,TradeAmount)
             ROICloseLevel = ROICloseLevelInitial
             spread1 = spread1Initial
             TakeProfitFromSELL = TakeProfitFromSELLInitial
             TakeProfitFromBUY = TakeProfitFromBUYInitial
             Tradeslog.warning('TakeHalfSize from BUY ORDER: '+str(TakeHalfSize)) 
             Tradeslog.warning('Lowered ROICloseLevel (TakeHalfSizeBUY): '+str(ROICloseLevel)) 
        SetPrg(7)          
        lokedTakeP_BUY = 1
        TakedBuy = 1
        
    if weight > (TakeProfitFromBUY2*3):
        TakedBuy = 0    

    if TakeProfit ==1 and weight > (TakeProfitFromBUY2 * 2) and PositionSize > 0 and TakeAllModus == 0 and lokedTakeP_BUY == 0 and TakedBuy == 0:
        for _ in range(TakeHalfSize):
             reducetrade(symbol,TradeAmount)
             ROICloseLevel = ROICloseLevelInitial
             spread1 = spread1Initial
             TakeProfitFromSELL = TakeProfitFromSELLInitial
             TakeProfitFromBUY = TakeProfitFromBUYInitial
             Tradeslog.warning('TakeHalfSize from BUY ORDER: '+str(TakeHalfSize)) 
             Tradeslog.warning('Lowered ROICloseLevel (TakeHalfSizeBUY): '+str(ROICloseLevel)) 
        SetPrg(7)          
        lokedTakeP_BUY = 1
        TakedBuy = 1    

           
        
        
    #Takeall Part TakeProfitFromBUY +1
    
    if TakeProfit ==1 and weight > TakeProfitFromBUY2 and PositionSize > 0 and  TakeAllModus == 1 and lokedTakeP_BUY == 0 and TakedBuy == 0:
        for _ in range(TakeAllSize + 1):
             reducetrade(symbol,TradeAmount)
             Tradeslog.warning('TakeAll from BUY ORDER: '+str(TakeHalfSize)) 
        SetPrg(7)          
        lokedTakeP_BUY = 1
        TakedBuy = 1

    if TakedBuy == 1 and PositionSize < 0:
        TakedBuy = 0    
        
        


#MRY12
#PNL STOP_ORDER_REDUCE
	
    if (PNL) == 0:
        pnl=0.001     
    PNL = pnl  
    
    #SELL_STOP_ORDER_REDUCE_PnL_LEVEL_REACHED
    if PNL < STOPLIMIT and PositionSize < 0 and PositionSize < PosCalDiff :
        optimazetrade(symbol,TradeAmount)
        optimazetrade(symbol,TradeAmount)
        SetPrg(9)
        TakeProfitSELLCounter = 0
        BUYTradesCounter = BUYTradesCounter + 2
        ROICloseLevel = ROICloseLevelInitial
        spread1 = spread1Initial
        Tradeslog.warning('PNL_STOP_ORDER_REDUCE_SELL PNL was: '+str(pnl)+'USDT')    	
    else:
        logging.warning("PNL_STOP_ORDER_REDUCE_SELL_NOPE")
    		
    #BUY_STOP_ORDER_REDUCE_PnL_LEVEL_REACHED
    if PNL < STOPLIMIT and PositionSize > 0 and PositionSize > PosCalDiff :
        reducetrade(symbol,TradeAmount)
        reducetrade(symbol,TradeAmount)
        SetPrg(9)
        TakeProfitBUYCounter = 0
        SELLTradesCounter = SELLTradesCounter + 2
        ROICloseLevel = ROICloseLevelInitial
        spread1 = spread1Initial
        Tradeslog.warning('PNL STOP_ORDER_REDUCE BUY PNL was: '+str(pnl)+'USDT')
    else:
        logging.warning("PNL_STOP_ORDER_REDUCE_BUY_NOPE")	
 

  	

    	  

   

#MRY15
#SMALLHOLDING POSITION with much ROI and restart Trading
 
    
 
 #SELLSide 
 

    SmallmROEaddSELL = 0
          
    if SmallHoldMUCHROI ==1 and PosSizetest < TradeX and PositionSize < 0 and PositionSize > PositionLimitSELL and weight > PosNotFilledXAddLevel: 
        reducetrade(symbol,TradeAmount)
        ROICloseLevel = ROICloseLevelInitial
        TakeProfitFromSELL = TakeProfitFromSELLInitial
        TakeProfitFromBUY = TakeProfitFromBUYInitial
        spread1 = spread1Initial
        SetPrg(11)
        TakeProfitBUYCounter = 0
        countDown = 0
        SmallmROEaddSELL = 1
        Tradeslog.warning("SMALLHOLDING_SELL POSITION with much ROI add 1x") 
        time.sleep(0.11)


     
 #BUYSide   
 
    SmallmROEaddBUY = 0	
      
    if SmallHoldMUCHROI ==1 and PosSizetest < TradeX and PositionSize > 0 and PositionSize < PositionLimitBUY and weight > PosNotFilledXAddLevel:		
        optimazetrade(symbol,TradeAmount)
        ROICloseLevel = ROICloseLevelInitial
        TakeProfitFromSELL = TakeProfitFromSELLInitial
        TakeProfitFromBUY = TakeProfitFromBUYInitial
        spread1 = spread1Initial
        SetPrg(11)
        TakeProfitSELLCounter = 0
        countUP = 0
        SmallmROEaddBUY = 1
        Tradeslog.warning("SMALLHOLDING_BUY POSITION with much ROI add 1x")
        time.sleep(0.11)



#CHECK HOW MANY TIME SELL TRADES OPEN Trade AMOUNT * X  



    if PositionSize > 0 and PositionSize < TradeAmount:
        PosSizetest = 0
        logging.warning('PosSizetest: '+str(PosSizetest))  
        logging.warning('PosSizetest: '+str(PosSizetest))  
        logging.warning('PosSizetest: '+str(PosSizetest))  
        logging.warning('PosSizetest: '+str(PosSizetest))  

    if PositionSize > 0 and PositionSize >=  TradeAmount:
        PosSizetest = ( PositionSize  ) / ( round(TradeAmount ,5)) 
        logging.warning('PosSizetest: '+str(PosSizetest))  
        logging.warning('PosSizetest: '+str(PosSizetest))  
        logging.warning('PosSizetest: '+str(PosSizetest))  
        logging.warning('PosSizetest: '+str(PosSizetest))  
        
        

    if PositionSize < 0 and abs(PositionSize) < TradeAmount:
        PosSizetest = 0
        logging.warning('PosSizetest: '+str(PosSizetest))  
        logging.warning('PosSizetest: '+str(PosSizetest))  
        logging.warning('PosSizetest: '+str(PosSizetest))  
        logging.warning('PosSizetest: '+str(PosSizetest))  

    if PositionSize < 0 and abs(PositionSize)  >=  TradeAmount:
        PosSizetest = abs(PositionSize) / ( round(TradeAmount ,5)) 
        logging.warning('PosSizetest: '+str(PosSizetest))  
        logging.warning('PosSizetest: '+str(PosSizetest))  
        logging.warning('PosSizetest: '+str(PosSizetest))  
        logging.warning('PosSizetest: '+str(PosSizetest))  


       

		


     	
#ROI COUNTER  	
    weight = (roe) 
     

    #BUY ROI COUNTER
    if weight > setUPstart and PositionSize > 0:
        logging.warning("counterUP+1")
        countUP = countUP + 1
   
 
    #SELL ROI COUNTER 
    if weight > setDOWNstart and PositionSize < 0 :
        logging.warning("counterDown+1")
        countDown = countDown + 1


    if countUP == countUPLIMIT :
        logging.warning("countDown ZAEHLER-RESET")
        countDown = 0
 
    if countDown == countDownLIMIT :
        logging.warning("countUP ZAEHLER-RESET")
        countUP = 0

    if countUP > countUPLIMIT:
        countUP = 0  
        
    if countDown > countDownLIMIT:
        countDown = 0

    logging.warning ('countUP: '+str(countUP))   
    logging.warning ('countDown: '+str(countDown))
      
      
      
    TradeAmountBefore = TradeAmount      
    ROICloseLevelInitialBefore = ROICloseLevelInitial      
    HRoeInitBefore = HRoeInit 



    # Write the variable values to varmove.py
    with open('varmove.py', 'w') as file:
        file.write(f"Coin = {Coin!r}\n")
        file.write(f"TradeAmount = {TradeAmount}\n")
        file.write(f"TradeX = {TradeX}\n")
        file.write(f"setDOWNstart = {setDOWNstart}\n")
        file.write(f"StopTrades = {StopTrades}\n")
        file.write(f"TakeProfitFromBUY = {TakeProfitFromBUY}\n")
        file.write(f"TakeProfitFromBUYInitial = {TakeProfitFromBUYInitial}\n")        
        file.write(f"TakeProfitFromBUY2 = {TakeProfitFromBUY2}\n")
        file.write(f"TakeProfitFromSELL = {TakeProfitFromSELL}\n")
        file.write(f"TakeProfitFromSELLInitial = {TakeProfitFromSELLInitial}\n")        
        file.write(f"ROICloseLevel = {ROICloseLevel}\n")
        file.write(f"ROICloseLevelInitial = {ROICloseLevelInitial}\n")
        file.write(f"spread1 = {spread1}\n")
        file.write(f"spread1Initial = {spread1Initial}\n")
        file.write(f"PosNotFilledXAddLevel = {PosNotFilledXAddLevel}\n")
        file.write(f"GrowCount = {GrowCount}\n")
        file.write(f"StartGrowDiff = {StartGrowDiff}\n")
        file.write(f"StartGrowDiffInit =  {StartGrowDiffInit}\n")
        file.write(f"StartGrowDiffAdd = {StartGrowDiffAdd}\n")
        file.write(f"StartGrowDiffAddInit = {StartGrowDiffAddInit}\n")





    # Continue with other tasks or operations
    
    # Add a delay or sleep to control the loop execution speed
    time.sleep(0.15)  # Delay for 2 seconds before the next iteration        

    # Write the variable values to tradehistory2.py
    with open('tradehistory2.py', 'w') as file:
        file.write(f"BUY_TakeProfit_COUNTER = {tradehistory.movehistory_BUY_TakeProfit_COUNTER!r}\n")
        file.write(f"SELL_TakeProfit_COUNTER = {tradehistory.movehistory_SELL_TakeProfit_COUNTER}\n")
        file.write(f"BUY_Order_ROI_Switcher_COUNTER = {tradehistory.movehistory_BUY_Order_ROI_Switcher_COUNTER}\n")
        file.write(f"SELL_Order_ROI_Switcher_COUNTER = {tradehistory.movehistory_SELL_Order_ROI_Switcher_COUNTER}\n")


    # Continue with other tasks or operations
    
    # Add a delay or sleep to control the loop execution speed
    time.sleep(0.15)  # Delay for 2 seconds before the next iteration                
      


    PositionSizeSaved = PositionSize

      
      
      
    setflag1984 = 0

    if  PosSizetest   > TradeX:
        setflag1984= 1
    if  PosSizetest   == TradeX:
        setflag1984= 1
    if PosSizetest  < TradeX:
        setflag1984= 0
    logging.warning('setflag1984: '+str(setflag1984))  
    
    
    stoppp1 = 0
    stoppp2 = 0
    stoppp2 = 0
    if weight > StopTrades + 2:
        stoppp1 = 1
    else:
        stoppp1 = 0    

    if weight < setDOWNstart:
        stoppp2 = 1
    else:
        stoppp2 = 0    
    if stoppp1 == 1 or stoppp2 == 1:
        stoppp3 = 1
    else:
        stoppp3 = 0       

  
    if setflag1984 == 0 and stoppp3 == 1 and weight - ROICloseLevel  > 1:  
        time.sleep(1.0)
        logging.warning ("SLEEP 2 over 1 ")    
    if setflag1984 == 0 and stoppp3 == 1 and weight - ROICloseLevel  > 2:  
        time.sleep(1.0)
        logging.warning ("SLEEP 2 over 1 ")    
    if setflag1984 == 0 and stoppp3 == 1 and weight - ROICloseLevel  > 10:  
        time.sleep(1.0)
        logging.warning ("SLEEP 2 over 1 ")    
    if setflag1984 == 0 and stoppp3 == 1 and weight - ROICloseLevel  > 15:  
        time.sleep(1.0)
        logging.warning ("SLEEP 2 over 1 ")    
    if setflag1984 == 0 and stoppp3 == 1 and weight - ROICloseLevel  > 30:  
        time.sleep(2.0)
        logging.warning ("SLEEP 2 over 1 ")    
    if setflag1984 == 0 and stoppp3 == 1 and weight - ROICloseLevel  > 45:  
        time.sleep(2.0)
        logging.warning ("SLEEP 2 over 1 ")    
    if setflag1984 == 0 and stoppp3 == 1 and weight - ROICloseLevel  > 55:  
        time.sleep(1.0)
        logging.warning ("SLEEP 2 over 1 ")    
    if setflag1984 == 0 and stoppp3 == 1 and weight - ROICloseLevel  > 75:  
        time.sleep(1.0)
        logging.warning ("SLEEP 2 over 1 ")   
    if setflag1984 == 0 and stoppp3 == 1 and weight - ROICloseLevel  > 125:  
        time.sleep(4.0)
        logging.warning ("SLEEP 2 over 1 ")   
    if setflag1984 == 0 and stoppp3 == 1 and weight - ROICloseLevel  > 165:  
        time.sleep(5.0)
        logging.warning ("SLEEP 2 over 1 ")   
    if setflag1984 == 0 and stoppp3 == 1 and weight - ROICloseLevel  > 250:  
        time.sleep(10.0)
        logging.warning ("SLEEP 2 over 1 ")   



    if setflag1984 == 1 and weight - ROICloseLevel  > 1:  
        time.sleep(1.0)
        logging.warning ("SLEEP 2 over 1 ")    
    if setflag1984 == 1 and weight - ROICloseLevel  > 2:  
        time.sleep(1.0)
        logging.warning ("SLEEP 2 over 1 ")    
    if setflag1984 == 1 and weight - ROICloseLevel  > 10:  
        time.sleep(1.0)
        logging.warning ("SLEEP 2 over 1 ")    
    if setflag1984 == 1 and weight - ROICloseLevel  > 15:  
        time.sleep(1.0)
        logging.warning ("SLEEP 2 over 1 ")    
    if setflag1984 == 1 and weight - ROICloseLevel  > 30:  
        time.sleep(2.0)
        logging.warning ("SLEEP 2 over 1 ")    
    if setflag1984 == 1 and weight - ROICloseLevel  > 45:  
        time.sleep(2.0)
        logging.warning ("SLEEP 2 over 1 ")    
    if setflag1984 == 1 and weight - ROICloseLevel  > 55:  
        time.sleep(1.0)
        logging.warning ("SLEEP 2 over 1 ")    
    if setflag1984 == 1 and weight - ROICloseLevel  > 75:  
        time.sleep(1.0)
        logging.warning ("SLEEP 2 over 1 ")   
    if setflag1984 == 1 and weight - ROICloseLevel  > 125:  
        time.sleep(4.0)
        logging.warning ("SLEEP 2 over 1 ")   
    if setflag1984 == 1 and weight - ROICloseLevel  > 165:  
        time.sleep(5.0)
        logging.warning ("SLEEP 2 over 1 ")   
    if setflag1984 == 1 and weight - ROICloseLevel  > 250:  
        time.sleep(10.0)
        logging.warning ("SLEEP 2 over 1 ")   



    # Delete log files if they exceed size limit
    try:
        if os.path.exists(log_file_path) and os.path.getsize(log_file_path) > LOG_FILE_SIZE_MB_HODL_INFO * 1024 * 1024:
            os.remove(log_file_path)
    except OSError:
        pass

    try:
        if os.path.exists(trades_log_file_path) and os.path.getsize(trades_log_file_path) > LOG_FILE_SIZE_MB_HODL_TRADES * 1024 * 1024:
            os.remove(trades_log_file_path)
    except OSError:
        pass

    try:
        if os.path.exists(calculation_log_file_path) and os.path.getsize(calculation_log_file_path) > LOG_FILE_SIZE_MB_HODL_Calculation * 1024 * 1024:
            os.remove(calculation_log_file_path)
    except OSError:
        pass

    try:
        if os.path.exists(restartlog) and os.path.getsize(restartlog) > LOG_FILE_SIZE_MB_HODL_Calculation * 1024 * 1024:
            os.remove(restartlog)
    except OSError:
        pass




    try:
        if os.path.exists(log_file_path) and os.path.getmtime(log_file_path) < expiration_date.timestamp():
            os.remove(log_file_path)
    except OSError:
        pass

    try:
        if os.path.exists(trades_log_file_path) and os.path.getmtime(trades_log_file_path) < expiration_date.timestamp():
            os.remove(trades_log_file_path)
    except OSError:
        pass

    try:
        if os.path.exists(calculation_log_file_path) and os.path.getmtime(calculation_log_file_path) < expiration_date.timestamp():
            os.remove(calculation_log_file_path)
    except OSError:
        pass















    
