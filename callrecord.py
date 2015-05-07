# -*- coding: utf-8 -*-

from datetime import datetime
from datetime import timedelta

class Record:
    def __init__(self, calldate, number, direction, region, type, realprice):
        self.calldate = datetime.strptime(calldate, '%d.%m.%y %H:%M:%S')
        self.number = number
        self.direction = {'Входящий': 'IN', 'Исходящий': 'OUT', 'Передача данных':'DAT', 'Переадресация на номер 9273590000':'RDR'}[direction]
        self.region = {'Республика Башкортостан':'RB', '':'-'}[region]
        self.type = {'SMS':'SMS', 'SMS-премиум':'SMS', 'Внутрисетевой вызов':'INTRN', 'Вызов':'CALL', 'Междугородний/международный':'EXT', 'Междугородний/международный (Россия, Москва)':'EXT', 'Голосовая почта':'MAIL', 'GPRS(Internet) Город':'GPRS', 'Местный (Россия, Уфа)':'BASH', 'Вызов ОАО МегаФон':'MEGA'}[type]
        self.realprice = realprice
    def __str__(self):
        return '{0} {1:3} {2:2}'.format(self.calldate.strftime('%Y.%m.%d %H:%M:%S'), self.direction, self.region)

class CallRecord(Record):
    def __init__(self, calldate, number, volume, direction, region, type, realprice):
        Record.__init__(self, calldate, number, direction, region, type, realprice)
        try:
            [h, m, s] = [int(x) for x in volume.split(':')]
            self.volume = timedelta(hours=h, minutes=m, seconds=s)
        except:
            print('Error Call volume!!! ' + volume)
            self.volume = volume
    def __str__(self):
        return Record.__str__(self) + ' {0}'.format(int(self.volume.total_seconds()))

class InternetRecord(Record):
    def __init__(self, calldate, volume, region, realprice):
        Record.__init__(self, calldate, 'internet', 'Передача данных', region, 'GPRS(Internet) Город', realprice)
        self.volume = int(volume)
    def __str__(self):
        return Record.__str__(self) + ' {0}'.format(int(self.volume))

class SMSRecord(Record):
    def __init__(self, calldate, direction, region, realprice):
        Record.__init__(self, calldate, '900', direction, region, 'SMS', realprice)
        self.volume = 1
    def __str__(self):
        return Record.__str__(self) + ' {0}'.format(int(self.volume))




if __name__ == '__main__':
    print('test module...')
    rec1 = CallRecord('01.03.15 13:03:29', '79276371573', '00:00:33', 'Исходящий', 'Республика Башкортостан', 'Внутрисетевой вызов', 0.95)
    rec2 = CallRecord('01.03.15 18:24:29', '79276371573', '00:01:09', 'Входящий', 'Республика Башкортостан', 'Вызов', 0.00)
    rec3 = InternetRecord('01.03.15 04:59:35', 250, 'Республика Башкортостан', 0.00)
    rec4 = SMSRecord('01.03.15 08:32:41', 'Входящий', 'Республика Башкортостан', 0.00)

    print(rec1.calldate, rec1.direction, rec1.volume)
    print(rec1)
    print(rec2)
    print(rec3)
    print(rec4)

    print(isinstance(rec4, CallRecord))
    print(isinstance(rec4, SMSRecord))
    print(type(rec4) == CallRecord)
    print(type(rec4) == SMSRecord)
    print(type(rec4))
