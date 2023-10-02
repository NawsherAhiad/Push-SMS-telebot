from flask import Flask, jsonify, request, make_response
import num_valid
import chk_reporting
from datetime import datetime
import international_report
import phonenumbers


app = Flask(__name__)
result = "test result"
@app.route('/smsai/v1', methods = ['GET', 'POST'])
def home():
    msisdn = request.args.get('msisdn')
    fsmstime = request.args.get('from_date')
    tsmstime = request.args.get('to_date')
    masking = request.args.get('masking')
    msisdn_validity = num_valid.valid_num(msisdn)
    
    if msisdn[0] == '+' and (msisdn[1] and msisdn[2]) =='8' :
        msisdn = msisdn[3:]
    elif (msisdn[0] and msisdn[1]) =='8':
        msisdn = msisdn[2:]
    
    res = True
    f_date = False
    t_date = False
    format = "%Y-%m-%d"
    try:
        f_date = bool(datetime.strptime(fsmstime, format))
        t_date = bool(datetime.strptime(tsmstime, format))
    except ValueError:
        res = False
    if msisdn_validity == True and f_date == True and t_date== True:
        #ismsB = isms_block_msisdn.block_msisdn(msisdn)
        #ismspB = ismsplus_block_msisdn.block_msisdn(msisdn)
        #block = ismsB+ismspB+"\n\n"
        #c_report = chk_reporting.chk_report(msisdn, )
        #block = ismsB+ismspB
        #print(block)


        info = chk_reporting.infozilion_logs_report('88' + msisdn, fsmstime, tsmstime, masking )
        if info == 1:
            info = chk_reporting.infozilion_logs_report(msisdn, fsmstime, tsmstime, masking )
            if info == 1:
                info = chk_reporting.infozilion_logs_report(msisdn[3:], fsmstime, tsmstime, masking )
                if info== 1:
                    info = "No Log found\n"
                    return info
       
        
            
        #old = isms_processing_check.isms_bulklog(msisdn, fsmstime, tsmstime)
        #new = ismsPlus_processing_check.isms_bulklog(msisdn, fsmstime, tsmstime)
        #sms = old+new
        #print(sms)
        #result = block+sms
        #print(result)
        # sms = str(info)
        sms = info 
        result = sms
        #print("backup",result)
        if sms == "SMS Response: \n":
            return "No SMS request found for the msisdn: "+msisdn+" at the mentioned time."
        else:
            return result
    
    elif msisdn_validity == False:
        
        try: 
            #parsed_number = phonenumbers.parse(msisdn, None)
            #is_valid = phonenumbers.is_valid_number(parsed_number)
            is_valid = True
            if is_valid == True:
                info2 = international_report.international_sms(msisdn, fsmstime, tsmstime, masking)
                if info2 == 1:
                    return "NO RESULT FOUND"
                else: 
                    return info2
        except phonenumbers.phonenumberutil.NumberParseException:
            return "INVALID MSISDN"
    
    elif res == False:
            return "Invalid Date"
    else:
        return "Invalid MSISDN"
        
    return jsonify({"hello  ": home()})



if __name__ == '__main__':
  
    app.run(debug = True, host = '0.0.0.0', port = 8080)