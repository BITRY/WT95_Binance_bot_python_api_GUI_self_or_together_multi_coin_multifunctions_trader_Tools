import sys

movehistory_SMALLHOLD_Low = int()
movehistory_BackToPositionLimit = 0
movehistory_SELL_Loop = 0
movehistory_BUY_Loop = 0
movehistory_SELL_Order_ROI_Switcher = 0
movehistory_BUY_Order_ROI_Switcher = 0
movehistory_SELL_TakeProfit = 0	
movehistory_BUY_TakeProfit = 0
movehistory_PNL_Stop = 0
movehistory_ROI_Crash = 0
movehistory_SMALLHOLD_Hight = 0

movehistory_SMALLHOLD_Low_COUNTER = int()
movehistory_BackToPositionLimit_COUNTER = 0
movehistory_SELL_Loop_COUNTER =  0
movehistory_BUY_Loop_COUNTER = 0
movehistory_SELL_Order_ROI_Switcher_COUNTER = 0
movehistory_BUY_Order_ROI_Switcher_COUNTER = 0
movehistory_SELL_TakeProfit_COUNTER = 0
movehistory_BUY_TakeProfit_COUNTER = 0
movehistory_PNL_Stop_COUNTER = 0
movehistory_ROI_Crash_COUNTER = 0
movehistory_SMALLHOLD_Hight_COUNTER = 0   

from varmove import Coin

def movehistory():
    #
    global movehistory_SMALLHOLD_Low, movehistory_BackToPositionLimit, movehistory_SELL_Loop, movehistory_BUY_Loop, movehistory_SELL_Order_ROI_Switcher, movehistory_BUY_Order_ROI_Switcher, movehistory_SELL_TakeProfit, movehistory_BUY_TakeProfit, movehistory_PNL_Stop, movehistory_ROI_Crash, movehistory_SMALLHOLD_Hight, movehistory_SMALLHOLD_Low_COUNTER, movehistory_BackToPositionLimit_COUNTER, movehistory_SELL_Loop_COUNTER, movehistory_BUY_Loop_COUNTER, movehistory_SELL_Order_ROI_Switcher_COUNTER, movehistory_BUY_Order_ROI_Switcher_COUNTER, movehistory_SELL_TakeProfit_COUNTER, movehistory_BUY_TakeProfit_COUNTER, movehistory_PNL_Stop_COUNTER, movehistory_ROI_Crash_COUNTER, movehistory_SMALLHOLD_Hight_COUNTER 

    from varmove import Coin
    
    
    
    
    if movehistory_SMALLHOLD_Low == 1:
        movehistory_SMALLHOLD_Low = 0
        movehistory_BackToPositionLimit = 0
        movehistory_SELL_Loop = 0
        movehistory_BUY_Loop = 0
        movehistory_SELL_Order_ROI_Switcher = 0 
        movehistory_BUY_Order_ROI_Switcher = 0
        movehistory_SELL_TakeProfit = 0
        movehistory_BUY_TakeProfit = 0
        movehistory_PNL_Stop = 0
        movehistory_ROI_Crash = 0
        movehistory_SMALLHOLD_Hight = 0
        
        #Functions Stay Counter or delet State of others
        movehistory_SMALLHOLD_Low_COUNTER = movehistory_SMALLHOLD_Low_COUNTER + 1
        movehistory_BackToPositionLimit_COUNTER = 0
        movehistory_SELL_Loop_COUNTER = 0
        movehistory_BUY_Loop_COUNTER = 0
        movehistory_SELL_Order_ROI_Switcher_COUNTER = 0 
        movehistory_BUY_Order_ROI_Switcher_COUNTER = 0
        movehistory_SELL_TakeProfit_COUNTER = 0
        movehistory_BUY_TakeProfit_COUNTER = 0
        movehistory_PNL_Stop_COUNTER = 0
        movehistory_ROI_Crash_COUNTER = 0
        movehistory_SMALLHOLD_Hight_COUNTER = 0

    #
    if movehistory_BackToPositionLimit == 1:
        movehistory_SMALLHOLD_Low = 0
        movehistory_BackToPositionLimit = 0
        movehistory_SELL_Loop = 0
        movehistory_BUY_Loop = 0
        movehistory_SELL_Order_ROI_Switcher = 0 
        movehistory_BUY_Order_ROI_Switcher = 0
        movehistory_SELL_TakeProfit = 0
        movehistory_BUY_TakeProfit = 0
        movehistory_PNL_Stop = 0
        movehistory_ROI_Crash = 0
        movehistory_SMALLHOLD_Hight = 0
        
        #Functions Stay Counter or delet State of others
        movehistory_SMALLHOLD_Low_COUNTER = 0
        movehistory_BackToPositionLimit_COUNTER = movehistory_BackToPositionLimit_COUNTER + 1
        movehistory_SELL_Loop_COUNTER = 0
        movehistory_BUY_Loop_COUNTER = 0
        movehistory_SELL_Order_ROI_Switcher_COUNTER = 0 
        movehistory_BUY_Order_ROI_Switcher_COUNTER = 0
        movehistory_SELL_TakeProfit_COUNTER = 0
        movehistory_BUY_TakeProfit_COUNTER = 0
        movehistory_PNL_Stop_COUNTER = 0
        movehistory_ROI_Crash_COUNTER = 0
        movehistory_SMALLHOLD_Hight_COUNTER = 0

    #
    if movehistory_SELL_Loop == 1:
        movehistory_SMALLHOLD_Low = 0
        movehistory_BackToPositionLimit = 0
        movehistory_SELL_Loop = 0
        movehistory_BUY_Loop = 0
        movehistory_SELL_Order_ROI_Switcher = 0 
        movehistory_BUY_Order_ROI_Switcher = 0
        movehistory_SELL_TakeProfit = 0
        movehistory_BUY_TakeProfit = 0
        movehistory_PNL_Stop = 0
        movehistory_ROI_Crash = 0
        movehistory_SMALLHOLD_Hight = 0
        
        #Functions Stay Counter or delet State of others
        movehistory_SMALLHOLD_Low_COUNTER = 0
        movehistory_BackToPositionLimit_COUNTER = 0
        movehistory_SELL_Loop_COUNTER = movehistory_SELL_Loop_COUNTER + 1
        movehistory_BUY_Loop_COUNTER = 0
        movehistory_SELL_Order_ROI_Switcher_COUNTER = 0 
        movehistory_BUY_Order_ROI_Switcher_COUNTER = 0
        movehistory_SELL_TakeProfit_COUNTER = 0
        movehistory_BUY_TakeProfit_COUNTER = 0
        movehistory_PNL_Stop_COUNTER = 0
        movehistory_ROI_Crash_COUNTER = 0
        movehistory_SMALLHOLD_Hight_COUNTER = 0

    #
    if movehistory_BUY_Loop == 1:
        movehistory_SMALLHOLD_Low = 0
        movehistory_BackToPositionLimit = 0
        movehistory_SELL_Loop = 0
        movehistory_BUY_Loop = 0
        movehistory_SELL_Order_ROI_Switcher = 0 
        movehistory_BUY_Order_ROI_Switcher = 0
        movehistory_SELL_TakeProfit = 0
        movehistory_BUY_TakeProfit = 0
        movehistory_PNL_Stop = 0
        movehistory_ROI_Crash = 0
        movehistory_SMALLHOLD_Hight = 0
        
        #Functions Stay Counter or delet State of others
        movehistory_SMALLHOLD_Low_COUNTER = 0
        movehistory_BackToPositionLimit_COUNTER = 0
        movehistory_SELL_Loop_COUNTER =  0
        movehistory_BUY_Loop_COUNTER = movehistory_BUY_Loop_COUNTER +1
        movehistory_SELL_Order_ROI_Switcher_COUNTER = 0 
        movehistory_BUY_Order_ROI_Switcher_COUNTER = 0
        movehistory_SELL_TakeProfit_COUNTER = 0
        movehistory_BUY_TakeProfit_COUNTER = 0
        movehistory_PNL_Stop_COUNTER = 0
        movehistory_ROI_Crash_COUNTER = 0
        movehistory_SMALLHOLD_Hight_COUNTER = 0

    #
    if movehistory_SELL_Order_ROI_Switcher == 1:
        movehistory_SMALLHOLD_Low = 0
        movehistory_BackToPositionLimit = 0
        movehistory_SELL_Loop = 0
        movehistory_BUY_Loop = 0
        movehistory_SELL_Order_ROI_Switcher = 0 
        movehistory_BUY_Order_ROI_Switcher = 0
        movehistory_SELL_TakeProfit = 0
        movehistory_BUY_TakeProfit = 0
        movehistory_PNL_Stop = 0
        movehistory_ROI_Crash = 0
        movehistory_SMALLHOLD_Hight = 0
        
        #Functions Stay Counter or delet State of others
        movehistory_SMALLHOLD_Low_COUNTER = 0
        movehistory_BackToPositionLimit_COUNTER = 0
        movehistory_SELL_Loop_COUNTER =  0
        movehistory_BUY_Loop_COUNTER = 0
        movehistory_SELL_Order_ROI_Switcher_COUNTER = movehistory_SELL_Order_ROI_Switcher_COUNTER + 1 
        movehistory_BUY_Order_ROI_Switcher_COUNTER = 0
        movehistory_SELL_TakeProfit_COUNTER = 0
        movehistory_BUY_TakeProfit_COUNTER = 0
        movehistory_PNL_Stop_COUNTER = 0
        movehistory_ROI_Crash_COUNTER = 0
        movehistory_SMALLHOLD_Hight_COUNTER = 0

    #
    if movehistory_BUY_Order_ROI_Switcher == 1:
        movehistory_SMALLHOLD_Low = 0
        movehistory_BackToPositionLimit = 0
        movehistory_SELL_Loop = 0
        movehistory_BUY_Loop = 0
        movehistory_SELL_Order_ROI_Switcher = 0 
        movehistory_BUY_Order_ROI_Switcher = 0
        movehistory_SELL_TakeProfit = 0
        movehistory_BUY_TakeProfit = 0
        movehistory_PNL_Stop = 0
        movehistory_ROI_Crash = 0
        movehistory_SMALLHOLD_Hight = 0
        
        #Functions Stay Counter or delet State of others
        movehistory_SMALLHOLD_Low_COUNTER = 0
        movehistory_BackToPositionLimit_COUNTER = 0
        movehistory_SELL_Loop_COUNTER =  0
        movehistory_BUY_Loop_COUNTER = 0
        movehistory_SELL_Order_ROI_Switcher_COUNTER = 0
        movehistory_BUY_Order_ROI_Switcher_COUNTER = movehistory_BUY_Order_ROI_Switcher_COUNTER + 1
        movehistory_SELL_TakeProfit_COUNTER = 0
        movehistory_BUY_TakeProfit_COUNTER = 0
        movehistory_PNL_Stop_COUNTER = 0
        movehistory_ROI_Crash_COUNTER = 0
        movehistory_SMALLHOLD_Hight_COUNTER = 0

    #
    if movehistory_SELL_TakeProfit == 1:
        movehistory_SMALLHOLD_Low = 0
        movehistory_BackToPositionLimit = 0
        movehistory_SELL_Loop = 0
        movehistory_BUY_Loop = 0
        movehistory_SELL_Order_ROI_Switcher = 0 
        movehistory_BUY_Order_ROI_Switcher = 0
        movehistory_SELL_TakeProfit = 0
        movehistory_BUY_TakeProfit = 0
        movehistory_PNL_Stop = 0
        movehistory_ROI_Crash = 0
        movehistory_SMALLHOLD_Hight = 0
        
        #Functions Stay Counter or delet State of others
        movehistory_SMALLHOLD_Low_COUNTER = 0
        movehistory_BackToPositionLimit_COUNTER = 0
        movehistory_SELL_Loop_COUNTER =  0
        movehistory_BUY_Loop_COUNTER = 0
        movehistory_SELL_Order_ROI_Switcher_COUNTER = 0
        movehistory_BUY_Order_ROI_Switcher_COUNTER = 0
        movehistory_SELL_TakeProfit_COUNTER = movehistory_SELL_TakeProfit_COUNTER + 1
        movehistory_BUY_TakeProfit_COUNTER = 0
        movehistory_PNL_Stop_COUNTER = 0
        movehistory_ROI_Crash_COUNTER = 0
        movehistory_SMALLHOLD_Hight_COUNTER = 0

    #
    if movehistory_BUY_TakeProfit == 1:
        movehistory_SMALLHOLD_Low = 0
        movehistory_BackToPositionLimit = 0
        movehistory_SELL_Loop = 0
        movehistory_BUY_Loop = 0
        movehistory_SELL_Order_ROI_Switcher = 0 
        movehistory_BUY_Order_ROI_Switcher = 0
        movehistory_SELL_TakeProfit = 0
        movehistory_BUY_TakeProfit = 0
        movehistory_PNL_Stop = 0
        movehistory_ROI_Crash = 0
        movehistory_SMALLHOLD_Hight = 0
        
        #Functions Stay Counter or delet State of others
        movehistory_SMALLHOLD_Low_COUNTER = 0
        movehistory_BackToPositionLimit_COUNTER = 0
        movehistory_SELL_Loop_COUNTER =  0
        movehistory_BUY_Loop_COUNTER = 0
        movehistory_SELL_Order_ROI_Switcher_COUNTER = 0
        movehistory_BUY_Order_ROI_Switcher_COUNTER = 0
        movehistory_SELL_TakeProfit_COUNTER = 0
        movehistory_BUY_TakeProfit_COUNTER = movehistory_BUY_TakeProfit_COUNTER + 1
        movehistory_PNL_Stop_COUNTER = 0
        movehistory_ROI_Crash_COUNTER = 0
        movehistory_SMALLHOLD_Hight_COUNTER = 0
        
    #
    if movehistory_PNL_Stop == 1:
        movehistory_SMALLHOLD_Low = 0
        movehistory_BackToPositionLimit = 0
        movehistory_SELL_Loop = 0
        movehistory_BUY_Loop = 0
        movehistory_SELL_Order_ROI_Switcher = 0 
        movehistory_BUY_Order_ROI_Switcher = 0
        movehistory_SELL_TakeProfit = 0
        movehistory_BUY_TakeProfit = 0
        movehistory_PNL_Stop = 0
        movehistory_ROI_Crash = 0
        movehistory_SMALLHOLD_Hight = 0
        
        #Functions Stay Counter or delet State of others
        movehistory_SMALLHOLD_Low_COUNTER = 0
        movehistory_BackToPositionLimit_COUNTER = 0
        movehistory_SELL_Loop_COUNTER =  0
        movehistory_BUY_Loop_COUNTER = 0
        movehistory_SELL_Order_ROI_Switcher_COUNTER = 0
        movehistory_BUY_Order_ROI_Switcher_COUNTER = 0
        movehistory_SELL_TakeProfit_COUNTER = 0
        movehistory_BUY_TakeProfit_COUNTER = 0
        movehistory_PNL_Stop_COUNTER = movehistory_PNL_Stop_COUNTER + 1
        movehistory_ROI_Crash_COUNTER = 0
        movehistory_SMALLHOLD_Hight_COUNTER = 0

    #
    if movehistory_ROI_Crash == 1:
        movehistory_SMALLHOLD_Low = 0
        movehistory_BackToPositionLimit = 0
        movehistory_SELL_Loop = 0
        movehistory_BUY_Loop = 0
        movehistory_SELL_Order_ROI_Switcher = 0 
        movehistory_BUY_Order_ROI_Switcher = 0
        movehistory_SELL_TakeProfit = 0
        movehistory_BUY_TakeProfit = 0
        movehistory_PNL_Stop =0
        movehistory_ROI_Crash = 0
        movehistory_SMALLHOLD_Hight = 0
        
        #Functions Stay Counter or delet State of others
        movehistory_SMALLHOLD_Low_COUNTER = 0
        movehistory_BackToPositionLimit_COUNTER = 0
        movehistory_SELL_Loop_COUNTER =  0
        movehistory_BUY_Loop_COUNTER = 0
        movehistory_SELL_Order_ROI_Switcher_COUNTER = 0
        movehistory_BUY_Order_ROI_Switcher_COUNTER = 0
        movehistory_SELL_TakeProfit_COUNTER = 0
        movehistory_BUY_TakeProfit_COUNTER = 0
        movehistory_PNL_Stop_COUNTER = 0
        movehistory_ROI_Crash_COUNTER = movehistory_ROI_Crash_COUNTER + 1
        movehistory_SMALLHOLD_Hight_COUNTER = 0

    #
    if movehistory_SMALLHOLD_Hight == 1:
        movehistory_SMALLHOLD_Low = 0
        movehistory_BackToPositionLimit = 0
        movehistory_SELL_Loop = 0
        movehistory_BUY_Loop = 0
        movehistory_SELL_Order_ROI_Switcher = 0 
        movehistory_BUY_Order_ROI_Switcher = 0
        movehistory_SELL_TakeProfit = 0
        movehistory_BUY_TakeProfit = 0
        movehistory_PNL_Stop =0
        movehistory_ROI_Crash = 0
        movehistory_SMALLHOLD_Hight = 0
        
        #Functions Stay Counter or delet State of others
        movehistory_SMALLHOLD_Low_COUNTER = 0
        movehistory_BackToPositionLimit_COUNTER = 0
        movehistory_SELL_Loop_COUNTER =  0
        movehistory_BUY_Loop_COUNTER = 0
        movehistory_SELL_Order_ROI_Switcher_COUNTER = 0
        movehistory_BUY_Order_ROI_Switcher_COUNTER = 0
        movehistory_SELL_TakeProfit_COUNTER = 0
        movehistory_BUY_TakeProfit_COUNTER = 0
        movehistory_PNL_Stop_COUNTER = 0
        movehistory_ROI_Crash_COUNTER = 0
        movehistory_SMALLHOLD_Hight_COUNTER = movehistory_SMALLHOLD_Hight_COUNTER + 1







    




    


