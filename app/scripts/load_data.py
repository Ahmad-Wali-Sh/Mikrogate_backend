from core.models import Task, Troubleshoot, Installation, ChangeLocation, OnlineSupport, LinkDetails, CheckList
import csv

import datetime


def run():
    with open('core/Table1.csv') as file:
        reader = csv.reader(file)
        next(reader)  # Advance past the header
        LinkDetails.objects.all().delete()
        CheckList.objects.all().delete()
        Installation.objects.all().delete()
        Troubleshoot.objects.all().delete()
        ChangeLocation.objects.all().delete()
        OnlineSupport.objects.all().delete()
        Task.objects.all().delete()
        

        # for row in reader:
        #     print(row)

        #     contract_date = row[1]
        #     activation = row[2]
        #     valid = row[3]
        #     old_format = '%m/%d/%Y %H:%M:%S'
        #     new_format = '%Y-%m-%d %H:%M:%S'

        #     new_contract_date = datetime.datetime.strptime(contract_date, old_format).strftime(new_format)
        #     if activation is not "":
        #         new_activation = datetime.datetime.strptime(activation, old_format).strftime(new_format)
        #     else:
        #         new_activation = new_contract_date
        #     new_valid = datetime.datetime.strptime(valid, old_format).strftime(new_format)
        #     # print(new_datetime_str)
        #     #'18-05-2016 15:37:36'

        #     contract = Contract(referral='',
        #                     contract_type='Individual',
        #                     contract_no=row[0],
        #                     contract_id=row[5],
        #                     Contract_date=new_contract_date,
        #                     activation_date=new_activation,
        #                     valid_upto=new_valid,
        #                     organization=row[4],
        #                     poc_name=row[6],
        #                     poc_number=row[7],
        #                     poc_email=row[9],
        #                     address=row[10],
        #                     packages=row[11],
        #                     package_price=row[12],
        #                     router=row[18],
        #                     antenna=row[13],
        #                     rou_amnt=row[19],
        #                     ann_cond=row[14],
        #                     ann_dec=row[15],
        #                     ann_amnt=row[17],
        #                     ann_lease_amnt=row[16],
        #                     other_service=row[22],
        #                     other_price=row[23],
        #                     other_dec='',
        #                     other_pay_method='',
        #                     service_charge=row[21],
        #                     other_charges=row[24],
        #                     lease_deposit=row[20],
        #                     grand_total=row[25],
        #                     curren=row[26]
        #                 )
        #     contract.save()