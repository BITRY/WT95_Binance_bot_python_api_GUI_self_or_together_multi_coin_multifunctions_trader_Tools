import sqlite3
import sys
import time
from WinTradeDB_FUNCTIONS import *
from tradehistory import *
import WinTradeDB_FUNCTIONS
import tradehistory
from varmove import Coin

def SetPrg(setPrgm):
    import WinTradeDB_FUNCTIONS
    import tradehistory
    from varmove import Coin

 
    id = 1
    
    UpdateLastTradeMove(setPrgm, id)

    ReadLastTradeMove() 
    State = WinTradeDB_FUNCTIONS.lasttradestat
    print(State)
    if State == 1:
        tradehistory.movehistory_SMALLHOLD_Low = 1
    if State == 2:  
        tradehistory.movehistory_BackToPositionLimit = 1
    if State == 3:  
        tradehistory.movehistory_SELL_Loop = 1 
    if State == 4:  
        tradehistory.movehistory_BUY_Loop = 1 
    if State == 5:  
        tradehistory.movehistory_SELL_Order_ROI_Switcher = 1 
    if State == 6:  
        tradehistory.movehistory_BUY_Order_ROI_Switcher = 1 
    if State == 7:  
        tradehistory.movehistory_SELL_TakeProfit = 1
    if State == 8:  
        tradehistory.movehistory_BUY_TakeProfit = 1 
    if State == 9:  
        tradehistory.movehistory_PNL_Stop = 1 
    if State == 10:  
        tradehistory.movehistory_ROI_Crash = 1 
    if State == 11:  
        tradehistory.movehistory_SMALLHOLD_Hight = 1     
    movehistory()
    
    UpdateLastTradeMove(0, id)



    print('TradeState Change on: '+str(Coin))
    
    print('tradehistory.movehistory_SMALLHOLD_Low: '+str(tradehistory.movehistory_SMALLHOLD_Low))
    print('tradehistory.movehistory_SMALLHOLD_Low_COUNTER: '+str(tradehistory.movehistory_SMALLHOLD_Low_COUNTER))

    print('tradehistory.movehistory_BackToPositionLimit: '+str(tradehistory.movehistory_BackToPositionLimit))
    print('tradehistory.movehistory_BackToPositionLimit_COUNTER: '+str(tradehistory.movehistory_BackToPositionLimit_COUNTER))  

    print('tradehistory.movehistory_SELL_Loop: '+str(tradehistory.movehistory_SELL_Loop))
    print('tradehistory.movehistory_SELL_Loop_COUNTER: '+str(tradehistory.movehistory_SELL_Loop_COUNTER))  

    print('tradehistory.movehistory_BUY_Loop: '+str(tradehistory.movehistory_BUY_Loop))
    print('tradehistory.movehistory_BUY_Loop_COUNTER: '+str(tradehistory.movehistory_BUY_Loop_COUNTER))  

    print('tradehistory.movehistory_SELL_Order_ROI_Switcher: '+str(tradehistory.movehistory_SELL_Order_ROI_Switcher))
    print('tradehistory.movehistory_SELL_Order_ROI_Switcher_COUNTER: '+str(tradehistory.movehistory_SELL_Order_ROI_Switcher_COUNTER))  
    
    print('tradehistory.movehistory_BUY_Order_ROI_Switcher: '+str(tradehistory.movehistory_BUY_Order_ROI_Switcher))
    print('tradehistory.movehistory_BUY_Order_ROI_Switcher_COUNTER: '+str(tradehistory.movehistory_BUY_Order_ROI_Switcher_COUNTER))  

    print('tradehistory.movehistory_SELL_TakeProfit: '+str(tradehistory.movehistory_SELL_TakeProfit))
    print('tradehistory.movehistory_SELL_TakeProfit_COUNTER: '+str(tradehistory.movehistory_SELL_TakeProfit_COUNTER))

    print('tradehistory.movehistory_BUY_TakeProfit: '+str(tradehistory.movehistory_BUY_TakeProfit))
    print('tradehistory.movehistory_BUY_TakeProfit_COUNTER: '+str(tradehistory.movehistory_BUY_TakeProfit_COUNTER)) 

    print('tradehistory.movehistory_PNL_Stop: '+str(tradehistory.movehistory_PNL_Stop))
    print('tradehistory.movehistory_PNL_Stop_COUNTER: '+str(tradehistory.movehistory_PNL_Stop_COUNTER))

    print('tradehistory.movehistory_ROI_Crash: '+str(tradehistory.movehistory_ROI_Crash))
    print('tradehistory.movehistory_ROI_Crash_COUNTER: '+str(tradehistory.movehistory_ROI_Crash_COUNTER))

    print('tradehistory.movehistory_SMALLHOLD_Hight: '+str(tradehistory.movehistory_SMALLHOLD_Hight))
    print('tradehistory.movehistory_SMALLHOLD_Hight_COUNTER: '+str(tradehistory.movehistory_SMALLHOLD_Hight_COUNTER))    		
    

    
    
    
   
        
