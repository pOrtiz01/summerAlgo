from statsmodels.tsa.arima.model import ARIMA
from datetime import datetime, timedelta
import numpy as np
class FocusedYellowGreenPenguin(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2015,1,1)
        self.SetEndDate(2021,7,15)
        self.SetCash(100000) 
        self.AddEquity("AAL", Resolution.Daily)
        self.AddEquity("DAL", Resolution.Daily)
        self.aal=self.AddEquity("AAL", Resolution.Daily)
        self.dal=self.AddEquity("DAL", Resolution.Daily)
        self.closingAAL=[]
        self.closingDAL=[]
        self.forecast=[]
        self.forecast1=[]
        self.differenceDAL=0
        self.differenceAAL=0
        self.Schedule.On(self.DateRules.EveryDay(),self.TimeRules.AfterMarketOpen("AAL",1),self.createSignal)
    
    def createSignal(self):
        closingAAL=self.History("AAL",timedelta(10),Resolution.Daily)
        self.closingDAL=self.History("DAL",252,Resolution.Daily)
        self.closingAAL=closingAAL["close"].to_list()
        #self.Log(self.closingAAL)
        #self.Log(self.closingDAL)
        self.model_AAL = ARIMA(self.closingAAL, order=(1,2,0))
        self.result_AAL = self.model_AAL.fit()
        self.model_DAL = ARIMA(self.closingDAL, order=(1,2,0))
        self.result_DAL = self.model_DAL.fit()
        self.forecast = [np.nan]*30
        for i in range(30, 252):
            self.window = self.closingAAL[i-30:i]
            self.model = ARIMA(self.indow, order=(1,1,1))
            self.result = self.model.fit()
            self.forecast.append(self.result.forecast()[0])
           
            
        self.df_AAL['forecast'] = self.forecast
        
        
        self.forecast1 = [np.nan]*30
        for i in range(30, 252):
            self.window1 = self.closingDAL[i-30:i]
            self.model1 = ARIMA(self.window1, order=(1,1,1))
            self.result1 = self.model1.fit()
            self.forecast1.append(self.result1.forecast()[0])
        
        self.df_DAL['forecast1'] = self.forecast1
        self.differenceAAL=self.forecast[252]-self.closingAAL[252]
        self.differenceDAL=self.forecast1[252]-self.closingDAL[252]
        
        
    
    def OnData(self, data):
        ''' OnData event is the primary entry point for your algorithm. Each new data point will be pumped in here.
            Arguments:
                data: Slice object keyed by symbol containing the stock data
        '''
      
      
   
