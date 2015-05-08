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
    def calls_in_list(self):
        return [x for x in self.calls_list() if x.direction == 'IN']
    def calls_out_list(self):
        return [x for x in self.calls_list() if x.direction == 'OUT']
    def sms_list(self):
        return [x for x in self.calls if isinstance(x, callrecord.SMSRecord)]
    def sms_in_list(self):
        return [x for x in self.sms_list() if x.direction == 'IN']
    def sms_out_list(self):
        return [x for x in self.sms_list() if x.direction == 'OUT']
    def internet_list(self):
        return [x for x in self.calls if isinstance(x, callrecord.InternetRecord)]
    def printstat(self):
        print('='*40)
        print('Total calls: {0}'.format(len(self.calls)))
        callin  = len(self.calls_in_list())
        callout = len(self.calls_out_list())
        smsin   = len(self.sms_in_list())
        smsout  = len(self.sms_out_list())
        print('      Calls: {0} (IN {1}, OUT {2})'.format(callin+callout, callin, callout))
        print('        SMS: {0} (IN {1}, OUT {2})'.format(smsin+smsout, smsin, smsout))
        print('   Internet: {0}'.format(len(self.internet_list())))
        print('-'*40)
        
        calldurin = sum([int(x.volume.total_seconds()) for x in self.calls_in_list()])
        calldurout = sum([int(x.volume.total_seconds()) for x in self.calls_out_list()])
        mindurin = min([int(x.volume.total_seconds()) for x in self.calls_in_list()])
        mindurout = min([int(x.volume.total_seconds()) for x in self.calls_out_list()])
        avgdurin = int(calldurin / float(callin))
        avgdurout = int(calldurout / float(callout))
        maxdurin = max([int(x.volume.total_seconds()) for x in self.calls_in_list()])
        maxdurout = max([int(x.volume.total_seconds()) for x in self.calls_out_list()])
        durin, durout = timedelta(seconds=calldurin), timedelta(seconds=calldurout)
        print('Call duration: {0} (IN {1}, OUT {2})'.format(durin+durout, durin, durout))
        print('Call IN  min/avg/max: {0}/{1}/{2}'.format(timedelta(seconds=mindurin), timedelta(seconds=avgdurin), timedelta(seconds=maxdurin)))
        for x in set([q.type for q in self.calls_in_list()]):
            cnt = len([a for a in self.calls_in_list() if a.type == x])
            dur = sum([int(a.volume.total_seconds()) for a in self.calls_in_list() if a.type == x])
            print('{0:8} {1:>4}: {2:>2} itm on {3}s'.format(' ', x, cnt, timedelta(seconds=dur)))
        print('Call OUT min/avg/max: {0}/{1}/{2}'.format(timedelta(seconds=mindurout), timedelta(seconds=avgdurout), timedelta(seconds=maxdurout)))
        for x in set([q.type for q in self.calls_out_list()]):
            cnt = len([a for a in self.calls_out_list() if a.type == x])
            dur = sum([int(a.volume.total_seconds()) for a in self.calls_out_list() if a.type == x])
            print('{0:8} {1:>4}: {2:>2} itm on {3}s'.format(' ', x, cnt, timedelta(seconds=dur)))
        print('-'*40)
        print('Internet volume: {0}KB'.format(sum([x.volume for x in self.internet_list()])))
        print('='*40)

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
