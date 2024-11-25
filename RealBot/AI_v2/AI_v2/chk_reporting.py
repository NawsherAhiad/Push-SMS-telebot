import mysql.connector
from datetime import datetime, date
import pandas as pd
import csv
from flask import Flask, Response


def edit(df):
    for i in range(len(df[1])):
        request = df[1].iloc[i].split(",")
        request.pop(1)  # Remove the element at index 1
        request.pop(5)  # Remove the element at index 5

                # Assign the modified list back to the DataFrame
        df.at[i, 1] = ','.join(request)
        df.to_csv('output.csv')
        #print(df) 
        #sql_results = df.to_string()
        #sql_results = df 
    return df

def orient(sql_results):
    text = ""
    for i in sql_results.itertuples():
        masking = i[1]
        request = i[2]
        response = i[3]
        hittime = i[4]
        response_time = i[5]
        msisdn = i[6]
        mno_response_message = i[7]
        text += "<b>MASKING: </b> " + str(masking) +  "\n "  + "<b> MSISDN: </b>" +str(msisdn) +"\n " + "<b> REQUEST TIME: </b>" +str(hittime)+" \n "+ "<b> RESPONSE TIME: </b>" +str(response_time)+"\n "+ "<b> MNO STATUS: </b>" +str(mno_response_message)+"\n\n "  + "<b> REQUEST: </b>" + str(request) +"\n\n " + "<b> RESPONSE: </b>" + str(response)+  " \t"
    return text




def infozilion_logs_report(msisdn, fdate,tdate, masking):
    sql_results = ""
    
    mydb = mysql.connector.connect(
                host="0.0.0.0",
                user="******",
                password="***********",
                database="*******"
    )


    mycursor = mydb.cursor()
    
    sql1 = """
            SELECT  masking, request, response , hittime, response_time, msisdn, mno_response_message 
            FROM infozilion_logs
            WHERE masking = %s AND msisdn = %s AND DATE(hittime) BETWEEN %s AND %s order by hittime DESC LIMIT 15
            """
    sql2 = """
            SELECT  masking, request, response , hittime, response_time, msisdn, mno_response_message  
            FROM infozilion_logs_backup
            WHERE masking = %s AND msisdn = %s AND DATE(hittime) BETWEEN %s AND %s ORDER BY hittime DESC LIMIT 15
        """
    sql3 ="""
            SELECT masking, request, response , hittime, response_time, msisdn , mno_response_message 
            FROM infozilion_logs_backup WHERE masking = %s AND msisdn = %s  AND DATE(hittime) BETWEEN %s AND %s 
            union all
            SELECT masking, request, response , hittime, response_time, msisdn, mno_response_message  
            FROM infozilion_logs WHERE masking = %s AND msisdn = %s AND DATE(hittime) BETWEEN %s AND %s
        """
   ##############################################################
    sql_nomasking1= """
            SELECT  masking, request, response , hittime, response_time, msisdn , mno_response_message 
            FROM infozilion_logs
            WHERE msisdn = %s AND DATE(hittime) BETWEEN %s AND %s order by hittime DESC LIMIT 15
            """
    sql_nomasking2 ="""
            SELECT  masking, request, response , hittime, response_time, msisdn, mno_response_message  
            FROM infozilion_logs_backup
            WHERE msisdn = %s AND DATE(hittime) BETWEEN %s AND %s ORDER BY hittime DESC LIMIT 15
        """
    sql_nomasking3 = """
            SELECT masking, request, response , hittime, response_time, msisdn , mno_response_message 
            FROM infozilion_logs_backup WHERE msisdn = %s  AND DATE(hittime) BETWEEN %s AND %s 
            union all
            SELECT masking, request, response , hittime, response_time, msisdn, mno_response_message
            FROM infozilion_logs WHERE msisdn = %s AND DATE(hittime) BETWEEN %s AND %s
        """
    
    fdate_obj = datetime.strptime(fdate, "%Y-%m-%d")
    tdate_obj = datetime.strptime(tdate, "%Y-%m-%d")
    fdate_obj = fdate_obj.date()
    tdate_obj = tdate_obj.date()
    today_date = datetime.now().date()

    dateflag = 0
    if abs(today_date.day - fdate_obj.day ) <= 2 and abs(today_date.day - tdate_obj.day) <= 2:
        dateflag = 0
        #infozilion_logs
    elif abs(today_date.day - fdate_obj.day ) > 2 and abs(today_date.day - tdate_obj.day) <= 2:
        dateflag = 1
        #print("yes")
        #both infozilion_logs and infozilion_logs_backuo
    else:
        dateflag = 2
        #print("yes2")
        #only infozilion_logs_backup


    flag = 0
    columns=['Masking', 'request', 'response', 'hittime', 'response_time', 'msisdn', 'mno_response_message' ]

    if dateflag == 0:
        if masking != '1': #if masking exist 
            val = (masking, msisdn, fdate, tdate, )
            mycursor.execute(sql1, val)
            sql_results = mycursor.fetchall()
            #print(sql_results)
            mydb.close()

            if len(sql_results)<= 0 :
                flag = 1 # means no result found
                return flag
            
            else:
                #print("Logs infozilion logssssss report1: ")
            
                df = pd.DataFrame(sql_results, columns=['Masking', 'request', 'response', 'hittime', 'response_time', 'msisdn', 'mno_response_message' ])
                # Assuming your SQL result is stored in the variable 'sql_result'
                df = pd.DataFrame.from_records(sql_results)
                #df = df.rename(columns={0: 'Masking', 1: 'request', 2: 'response', 3: 'hittime', 4: 'response_time', 5: 'msisdn'})
                #print(df)
                pd.set_option('display.max_colwidth', None)
                sql_results = edit(df)
                
                sql_results = orient(sql_results)
                
            return sql_results
        else:
            val = (msisdn, fdate, tdate, )
            mycursor.execute(sql_nomasking1, val)
            sql_results = mycursor.fetchall()
            #print(sql_results)
            mydb.close()

            if len(sql_results)<= 0 :
                flag = 1 # means no result found
                return flag
            
            else:
               
            
                df = pd.DataFrame(sql_results, columns=['Masking', 'request', 'response', 'hittime', 'response_time', 'msisdn', 'mno_response_message' ])
                # Assuming your SQL result is stored in the variable 'sql_result'
                df = pd.DataFrame.from_records(sql_results)
                
                pd.set_option('display.max_colwidth', None)
                sql_results = edit(df)
                sql_results = orient(sql_results)
                
            return sql_results

    
    elif dateflag == 1: #backup+live
        if masking != '1': #if masking exist 
            val = (masking, msisdn, fdate, tdate, masking, msisdn, fdate, tdate, )
            
            mycursor.execute(sql3, val)
            sql_results = mycursor.fetchall()
            mydb.close()

            if len(sql_results)<= 0 :
                flag = 1 # means no result found
                return flag
            
            else:
                #print("Logs infozilion logssssss report1: ")
            
                df = pd.DataFrame(sql_results, columns=['Masking', 'request', 'response', 'hittime', 'response_time', 'msisdn', 'mno_response_message' ])
                # Assuming your SQL result is stored in the variable 'sql_result'
                df = pd.DataFrame.from_records(sql_results)
                
                pd.set_option('display.max_colwidth', None)
                #print(df)
                sql_results = edit(df)
                sql_results = orient(sql_results)
                
            return sql_results
        else:
            val = ( msisdn, fdate, tdate, msisdn, fdate, tdate, )
            
            mycursor.execute(sql_nomasking3, val)
            sql_results = mycursor.fetchall()
            mydb.close()

            if len(sql_results)<= 0 :
                flag = 1 # means no result found
                return flag
            
            else:
                #print("Logs infozilion logssssss report1: ")
            
                df = pd.DataFrame(sql_results, columns=['Masking', 'request', 'response', 'hittime', 'response_time', 'msisdn', 'mno_response_message' ])
                # Assuming your SQL result is stored in the variable 'sql_result'
                df = pd.DataFrame.from_records(sql_results)
                #df = df.drop(0, axis=1)
                pd.set_option('display.max_colwidth', None)
                #print(df)
                sql_results = edit(df)
                sql_results = orient(sql_results)
                
            return sql_results

    
    elif dateflag == 2: #backup
        if masking != '1':#if masking exist 
            val = (masking, msisdn, fdate, tdate )
            mycursor.execute(sql2, val)
            sql_results = mycursor.fetchall()
            mydb.close()
            #print(sql_results)
            if len(sql_results)<= 0 :
                flag = 1 # means no result found
                return flag
            
            else:
                #print("Logs infozilion logssssss report1: ")
            
                df = pd.DataFrame(sql_results, columns=['Masking', 'request', 'response', 'hittime', 'response_time', 'msisdn', 'mno_response_message' ])
                # Assuming your SQL result is stored in the variable 'sql_result'
                df = pd.DataFrame.from_records(sql_results)
                pd.set_option('display.max_colwidth', None)    
                sql_results = edit(df)
                sql_results = orient(sql_results)
        
            return sql_results
        else:
            val = (msisdn, fdate, tdate )
            mycursor.execute(sql_nomasking2, val)
            sql_results = mycursor.fetchall()
            mydb.close()
            #print(sql_results)
            if len(sql_results)<= 0 :
                flag = 1 # means no result found
                return flag
            
            else:
                #print("Logs infozilion logssssss report1: ")
            
                df = pd.DataFrame(sql_results, columns=['Masking', 'request', 'response', 'hittime', 'response_time', 'msisdn', 'mno_response_message' ])
                # Assuming your SQL result is stored in the variable 'sql_result'
                df = pd.DataFrame.from_records(sql_results)
                pd.set_option('display.max_colwidth', None)    
                sql_results = edit(df)
                sql_results = orient(sql_results)
            return sql_results

        



        

        
        
    
    
    







    
   
    

    
   
    
    
        
