# -*- coding = utf-8 -*-
# @Time:  5:01 下午
# @Author : tt
# @File: percentage_change.py
# @Software: PyCharm

import backtrader

class percentage_change(backtrader.Strategy):


    def __log(self, txt, dt=None):

        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        self.data_close = self.datas[0].close
        self.data_open = self.datas[0].open
        self.order = None
        self.bar_executed = None
        self.reward = 0
        self.total_reward = 0
        self.count = 0
        self.wincount = 0
        self.order = None

    def next(self):

        if self.order:
            return
        # 如果沒有倉位
        if not self.position:
            x = 0.02  # %Change 參數-（0.2% - 20% ）

            # 1。當昨日股價 跌幅超過 X%
            if (self.data_close[-1]+(self.data_close[-1] * x)) < (self.data_open[-1]) :
                print("Difference：LastClose",self.data_close[0],"<LastOpen",self.data_open[-1])
                self.count += 1  # 交易總次數
            # 2。買入在今日開盤價
                self.__log('BUY ' + ', Price: ' + str(self.data_open[0]))
                self.buy(price=self.data_open[0])
            # 3。賣出在今日收盤價
                self.__log('SELL ' + ', Price: ' + str(self.data_close[0]))
                self.sell()
            # 4。計算獲利
                self.reward = self.data_close[0]-self.data_open[0]
            # 5。計算獲勝次數
                if self.reward > 0:
                    self.wincount += 1
                    print("Win：", self.reward)

                if self.reward < 0:
                    print("Lose:", self.reward)
            # 6。計算在每次交易買一股情況下總獲益
                self.total_reward += self.reward

                # 假設：10000本金、每次買一股的回報率
                print("Total_reward:",(self.total_reward / 10000) *100,"%")
                print("Count",self.count,"-------WinCount",self.wincount)


def main():
   # 1.資金
   startcash = 10000
  
   # 2. 股票/虛擬貨幣的歷史數據
   data = backtrader.feeds.YahooFinanceCSVData(dataname = './Data/ETH-USD.csv')
  
   # 3. 初始化你的AI
   cerebro = backtrader.Cerebro()
  
   # 4. 加入歷史數據
   cerebro.adddata(data)
  
   # 5. 加入寫好的交易策略
   cerebro.addstrategy(percentage_change)

   # 6. 加入準備好的資金
   cerebro.broker.setcash(startcash)
  
   # 7.交易量
   cerebro.addsizer(backtrader.sizers.FixedSize, stake=1)
  
   # 8. 開始交易
   cerebro.run()

if __name__ == '__main__':
   main()


