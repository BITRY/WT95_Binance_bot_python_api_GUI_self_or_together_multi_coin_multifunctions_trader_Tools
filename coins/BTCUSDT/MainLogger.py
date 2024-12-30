import time
import sys

from NOW import pnl




#LOGGING   USE DEBUG TO SEE RESPONSE FROM BINANCE    USE WARNING FOR LOG SCRIPT OUTPUTS	

Logfilepath = 'MainLogger.log'


import logging
logging.basicConfig(filename = Logfilepath, format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.WARNING)

formatter = logging.Formatter('%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

def setup_logger(name, log_file, level=logging.INFO):
    """To setup as many loggers as you want"""

    handler = logging.FileHandler(log_file)        
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger



while True:

    logging.warning('                  PNL: '+str(pnl)+'USDT')
    logging.warning('                  ROE: '+str(roe)+'%')
    logging.warning('                                                           SmallHOLDSELLStartCounter: '+str(SmallHOLDSELLStartCounter))       
    logging.warning('SMALLHOLDaddedSELLCounter_Locker_for_ROI_CRASH_COUNT: '+str(SMALLHOLDaddedSELLCounter))   
    logging.warning('                                                          SmallHOLDBUYStartCounter: '+str(SmallHOLDBUYStartCounter))
    logging.warning('SMALLHOLDaddedBUYCounter_Locker_for_ROI_CRASH_COUNT: '+str(SMALLHOLDaddedBUYCounter))
    logging.warning ('                  StopTradesBUYnotSELL: '+str(StopTradesBUYnotSELL))
    logging.warning ('                  StopTradesSELLnotBUY: '+str(StopTradesSELLnotBUY))
    logging.warning('                  SELLLoopSelf_Counter Delay last Trade: '+str(SellLoopSelf_Counter))  		  
    logging.warning('                  ROICrashBlocker_STATE_for_SELL_POSITION: '+str(AfterSELLRoiCrashBlockerSELL))
    logging.warning('                  AfterSELLRoiCrashBlockerSELLCounter: '+str(AfterSELLRoiCrashBlockerSELLCounter))
    logging.warning('                  BUYLoopSelfCounter Delay last Trade: '+str(BUYLoopSelf_Counter)) 
    logging.warning('                  ROICrashBlocker_STATE_for_BUY_POSITION: '+str(AferBUYRoiCrashBlockerBUY))
    logging.warning('                  AferBUYRoiCrashBlockerBUYCounter: '+str(AferBUYRoiCrashBlockerBUYCounter))
    logging.warning('after_takeprofitfromSELL_RoiCrashBlocker: '+str(after_takeprofitfromSELL_RoiCrashBlocker))
    logging.warning('after_takeprofitfromSELL_RoiCrashBlockerCounter: '+str(after_takeprofitfromSELL_RoiCrashBlockerCounter))
    logging.warning('after_takeprofitfromSELL_RoiCrashBlockerCounterLIMIT: '+str(after_takeprofitfromSELL_RoiCrashBlockerCounterLIMIT))
    logging.warning('after_takeprofitfromBUY_RoiCrashBlocker: '+str(after_takeprofitfromBUY_RoiCrashBlocker))
    logging.warning('after_takeprofitfromBUY_RoiCrashBlockerCounter: '+str(after_takeprofitfromBUY_RoiCrashBlockerCounter))
    logging.warning('after_takeprofitfromBUY_RoiCrashBlockerCounterLIMIT: '+str(after_takeprofitfromBUY_RoiCrashBlockerCounterLIMIT)) 
    logging.warning("PNL_STOP_ORDER_REDUCE_SELL_NOPE")
    logging.warning("PNL_STOP_ORDER_REDUCE_BUY_NOPE")	  
    logging.warning('AfterRoiCrash_SELL_BLOCKER_FLAG: '+str(AfterRoiCrash_SELL_BLOCKER_FLAG))
    logging.warning('AfterRoiCrash_SELL_BLOCKER_Counter: '+str(AfterRoiCrash_SELL_BLOCKER_Counter))
    logging.warning('AfterRoiCrash_BUY_BLOCKER_FLAG: '+str(AfterRoiCrash_BUY_BLOCKER_FLAG))
    logging.warning('AfterRoiCrash_BUY_BLOCKER_Counter: '+str(AfterRoiCrash_BUY_BLOCKER_Counter))    	
    logging.warning('SMALLHOLD_muchRoi_SELL_added_Flag: '+str(SMALLHOLD_muchRoi_SELL_added_Flag))
    logging.warning('SMALLHOLD_muchRoi_SELL_added_Counter: '+str(SMALLHOLD_muchRoi_SELL_added_Counter)) 
    logging.warning('SMALLHOLD_muchRoi_SELL_added_Counter_LIMIT: '+str(SMALLHOLD_muchRoi_SELL_added_Counter_LIMIT)) 	
    logging.warning('SMALLHOLD_muchRoi_BUY_added_Flag: '+str(SMALLHOLD_muchRoi_BUY_added_Flag))
    logging.warning('SMALLHOLD_muchRoi_BUY_added_Counter: '+str(SMALLHOLD_muchRoi_BUY_added_Counter)) 
    logging.warning('SMALLHOLD_muchRoi_BUY_added_Counter_LIMIT: '+str(SMALLHOLD_muchRoi_BUY_added_Counter_LIMIT)) 
    logging.warning ('NewSetBUYCount: '+str(NewSetBUYCount))
    logging.warning ('setUPstart: '+str(setUPstart))     
    logging.warning ('NewSetSELLCount: '+str(NewSetSELLCount))   	
    logging.warning ('setDOWNstart: '+str(setDOWNstart))
    logging.warning ('countUP: '+str(countUP))   
    logging.warning ('countDown: '+str(countDown))
    time.sleep(2)
    
  
