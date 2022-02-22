from .models import TradeHistory, Portfolio
import requests


class Trade:
    def __init__(self, user, orderType, type, pair, amount):
        self.user = user
        self.orderType = orderType
        self.portfo = Portfolio.objects.filter(usr=self.user, marketType='spot')
        self.result = None
        self.type = type
        self.pair = pair
        self.amount = float(amount.split(' ')[0])
        self.crp = amount.split(' ')[1]
        self.base = pair.split('-')[0]
        self.qoute = pair.split('-')[1]
        self.pairPrice = 0
        self.equivalent = 0
        self.callf()
        # dict = {'pair':'MANA-USDT', 'type':'buy', 'amount':'20 MANA'}

    def callf(self):
        self.equivalent = self.calc_equivalent(self.base, self.qoute, self.amount)
        if self.type == 'buy':
            if self.crp == self.base:
                state = self.check_available(self.equivalent, self.qoute)
                toSub = price = self.equivalent
                toAdd = self.amount
            else:
                state = self.check_available(self.amount, self.qoute)
                toSub = price = self.amount
                toAdd = self.equivalent
            if state == 0:
                # subtract
                obj = self.portfo.get(cryptoName=self.qoute)
                obj.amount = obj.amount - toSub
                obj.save()
                # add
                try:
                    obj = self.portfo.get(cryptoName=self.base)
                    obj.amount = obj.amount + toAdd
                    obj.save()
                except:
                    newCrypto = Portfolio(usr=self.user, cryptoName=self.base, amount=toAdd, equivalentAmount=None)
                    newCrypto.save()
    #     type = sell
        else:
            if self.crp == self.base:
                state = self.check_available(self.amount, self.base)
                toSub = self.amount
                toAdd = price = self.equivalent
            else:
                state = self.check_available(self.equivalent, self.base)
                toSub = self.equivalent
                toAdd = price = self.amount
            if state == 0:
                # subtract
                obj = self.portfo.get(cryptoName=self.base)
                obj.amount = obj.amount - toSub
                obj.save()
                # add
                try:
                    obj = self.portfo.get(cryptoName=self.qoute)
                    obj.amount = obj.amount + toAdd
                    obj.save()
                except:
                    newCrypto = Portfolio(usr=self.user, cryptoName=self.qoute, amount=toAdd, equivalentAmount=None)
                    newCrypto.save()
        # create history and give results
        if state == 0:
            histAmount =dict()
            for index, item in enumerate(self.portfo.iterator()):
                histAmount[index] = {'cryptoName':item.cryptoName, 'amount':item.amount}
            baseAmount = self.portfo.get(cryptoName=self.base).amount
            quoteAmount = self.portfo.get(cryptoName=self.qoute).amount
            newHistory = TradeHistory(
                usr=self.user,
                type=self.type,
                pair=self.pair,
                histAmount=histAmount,
                amount=str(self.amount)+' '+self.crp,
                price=price,
                complete=True,
                orderType=self.orderType
            )
               
                    
            newHistory.save()
            self.result = {'state': 0, self.base: baseAmount, self.qoute: quoteAmount}
        else:
            self.result = {'state': state}

    def calc_equivalent(self, base, qoute, amount):
        base = base.upper()
        response = requests.get(
            "https://min-api.cryptocompare.com/data/pricemulti?fsyms=" + base + "," + qoute + "&tsyms=USDT,USDT")
        response = response.json()
        basePrice = float(response[base]['USDT'])
        qoutePrice = float(response[qoute]['USDT'])
        pairPrice = basePrice / qoutePrice
        if self.crp == base:
            equivalent = pairPrice * amount
        else:
            equivalent = amount / pairPrice

        return equivalent

    def check_available(self, amount, name):
        try:
            obj = self.portfo.get(cryptoName=name)
            if amount <= obj.amount:
                return 0
            else:
                return 1
        except:
            return 2