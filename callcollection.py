# -*- coding: utf-8 -*-

import argparse
import csv
import callrecord
from datetime import timedelta

class CallCollection:
    def __init__(self):
        self.calls = list()
    def addcall(self, call):
        self.calls.append(call)
    def calls_list(self):
        return [x for x in self.calls if isinstance(x, callrecord.CallRecord)]
    def sms_list(self):
        return [x for x in self.calls if isinstance(x, callrecord.SMSRecord)]
    def internet_list(self):
        return [x for x in self.calls if isinstance(x, callrecord.InternetRecord)]
    def printstat(self):
        print('Total calls: {0}'.format(len(self.calls)))
        callin  = len([x for x in self.calls_list() if x.direction == 'IN'])
        callout = len([x for x in self.calls_list() if x.direction == 'OUT'])
        smsin   = len([x for x in self.sms_list() if x.direction == 'IN'])
        smsout  = len([x for x in self.sms_list() if x.direction == 'OUT'])
        print('      Calls: {0} (IN {1}, OUT {2})'.format(callin+callout, callin, callout))
        print('        SMS: {0} (IN {1}, OUT {2})'.format(smsin+smsout, smsin, smsout))
        print('   Internet: {0}'.format(len([x for x in self.internet_list()])))
        
        calldurin = sum([int(x.volume.total_seconds()) for x in self.calls_list() if x.direction == 'IN'])
        calldurout = sum([int(x.volume.total_seconds()) for x in self.calls_list() if x.direction == 'OUT'])
        durin, durout = timedelta(seconds=calldurin), timedelta(seconds=calldurout)
        print('Call duration: {0} (IN {1}, OUT {2})'.format(durin+durout, durin, durout))
        print('Internet volume: {0}'.format(sum([x.volume for x in self.internet_list()])))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Great Description To Be Here')
    parser.add_argument('-f', action='store', dest='f', help='File to parse')
    args = parser.parse_args()

    collect = CallCollection()
    
    with open(args.f, 'r') as csvfile:
        filereader = csv.DictReader(csvfile, delimiter='\t')
        for row in filereader:
            #print '+'.join(row)
            if row['Тип вызова'] == 'SMS' or row['Тип вызова'] == 'SMS-премиум' :
                collect.addcall(callrecord.SMSRecord(row['Дата/время вызова'], row['Направление'], row['Регион нахождения'], row['Стоимость']))
            elif row['Тип вызова'] == 'GPRS(Internet) Город' or row['Тип вызова'] == 'GPRS(Internet)':
                collect.addcall(callrecord.InternetRecord(row['Дата/время вызова'], row['Объем'], row['Регион нахождения'], row['Стоимость']))
            else:
                collect.addcall(callrecord.CallRecord(row['Дата/время вызова'], row['Номер, точка доступа'], row['Объем'], row['Направление'], row['Регион нахождения'], row['Тип вызова'], row['Стоимость']))

    collect.printstat()
