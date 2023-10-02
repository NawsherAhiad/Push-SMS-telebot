import mysql.connector
from datetime import datetime, date
import pandas as pd
import csv
from flask import Flask, Response

def orient(sql_results):
    text = ""
    for i in sql_results:
        sender_id = i[0]
        MSISDN = i[1]
        REFERENCE = i[2]
        requesttime = i[3]
        status = i[4]
        text += "<b>SENDER ID: </b> " + str(sender_id) +  "\n "  + "<b>MSISDN: </b>" + str(MSISDN) +"\n " + "<b>REFERENCE: </b>" + str(REFERENCE)+" \n "+ "<b>REQUEST TIME: </b>" +str(requesttime) +"\n "+ "<b>STATUS: </b>" + str(status) +"\n\n "  +  " \t"
    return text

def international_sms( msisdn, fdate, tdate, masking):
    
    result ="<b>INTERNATIONAL SMS: </b>\n\n"
    print(result)
    mydb = mysql.connector.connect(
                host="192.168.81.17",
                user="smsai",
                password="SmsAI12k!@%32",
                database="routesms"
    )

    mycursor = mydb.cursor()
    
    sql1 = """
            SELECT masking , msisdn, fullreply, sendingtime , replystatus
            FROM smslog WHERE msisdn = %s AND  
            DATE(sendingtime) BETWEEN %s AND %s ORDER BY sendingtime DESC limit 15
            """
    val = (msisdn, fdate, tdate, )
    mycursor.execute(sql1, val)
    sql_results = mycursor.fetchall()
    if len(sql_results)<= 0 :
        flag = 1 # means no result found
        return flag
    else :
        sql_results= orient(sql_results)
        #print(sql_results)
        mydb.close()

        result += sql_results
        return result

