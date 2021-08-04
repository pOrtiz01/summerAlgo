from statsmodels.tsa.arima.model import ARIMA
from datetime import datetime, timedelta
import numpy as np
class FocusedYellowGreenPenguin(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2019,10,4)
        self.SetEndDate(2021,7,15)
        self.SetCash(100000) 
        self.AddEquity("AAL", Resolution.Daily)
        self.AddEquity("DAL", Resolution.Daily)
        self.aal=self.AddEquity("AAL", Resolution.Daily)
        self.dal=self.AddEquity("DAL", Resolution.Daily)
        self.closingDAL=[]
        self.forecast=[]
        self.forecastOne=[]
        self.df_AAL={}
        self.df_DAL={}
        self.differenceDAL=0
        self.differenceAAL=0
        self.Schedule.On(self.DateRules.EveryDay(),self.TimeRules.AfterMarketOpen("AAL",1),self.createSignal)
        
     
    
    def createSignal(self):
        closingAAL=self.History(["AAL"],timedelta(252),Resolution.Daily)
        closingDAL=self.History(["DAL"],timedelta(252),Resolution.Daily)
        #self.closingDAL=self.History(["DAL"],timedelta(252),Resolution.Daily)
        self.closingAAL=closingAAL["close"].to_list()
        self.closingDAL=closingDAL["close"].to_list()
        #self.closingAAL
        self.model_AAL = ARIMA(self.closingAAL, order=(1,2,0))
        self.result_AAL = self.model_AAL.fit()
        self.model_DAL = ARIMA(self.closingDAL, order=(1,2,0))
        self.result_DAL = self.model_DAL.fit()
        self.forecast = [np.nan]*30
        for i in range(1,252, 30):
            self.window = self.closingAAL[i-30:i]
            self.model = ARIMA(self.window, order=(1,1,1))
            self.result = self.model.fit()
            self.forecast.append(self.result.forecast()[0])
           
            
        self.df_AAL['forecast'] = self.forecast
        
        
        self.forecastOne = [np.nan]*30
        for i in range(1,252, 30):
            self.window1 = self.closingDAL[i-30:i]
            self.model1 = ARIMA(self.window1, order=(1,1,1))
            self.result1 = self.model1.fit()
            self.forecastOne.append(self.result1.forecast()[0])
        
        self.df_DAL['forecast1'] = self.forecastOne
        
        self.differenceAAL=self.forecast[-1]-self.closingAAL[-1]
        self.differenceDAL=self.forecastOne[-1]-self.closingDAL[-1]
        
        
    
    def OnData(self, data):
        ''' OnData event is the primary entry point for your algorithm. Each new data point will be pumped in here.
            Arguments:
                data: Slice object keyed by symbol containing the stock data
        '''
     
        if self.differenceAAL>0 and self.differenceDAL<0:
            self.Liquidate("DAL")
            self.Liquidate("AAL")
            self.SetHoldings("AAL",.6)
            self.SetHoldings("DAL",-.4)
                
        elif self.differenceAAL<0 and self.differenceDAL>0:
            self.Liquidate("AAL")
            self.Liquidate("DAL")
            self.SetHoldings("DAL",.4)
            self.SetHoldings("AAL",-.6)
        
        elif self.differenceAAL<0 and self.differenceDAL<0:
            self.Liquidate("AAL")
            self.Liquidate("DAL")
            if self.differenceAAL>self.differenceDAL:
                 self.SetHoldings("AAL",.6)
                 self.SetHoldings("DAL",-.4)
            else:
                self.SetHoldings("DAL",.4)
                self.SetHoldings("AAL",-.6)
        
        elif self.differenceAAL>0 and self.differenceDAL>0:
            self.Liquidate("AAL")
            self.Liquidate("DAL")
            if self.differenceAAL>self.differenceDAL:
                 self.SetHoldings("AAL",.6)
                 self.SetHoldings("DAL",-.4)
            else:
                self.SetHoldings("DAL",.4)
                self.SetHoldings("AAL",-.6)
                
        
            
        
      
   
  
      
