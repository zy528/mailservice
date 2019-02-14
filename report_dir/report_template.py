#coding:utf8 
''''' 
邮件模板 
'''
import datetime as d
import os
import sys

default_encoding='utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)


BASE_DIR= os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

REPORT_IMG_DIR=BASE_DIR+'/report_imgs/'
REPORT_SIG_DIR=BASE_DIR+'/report_templates/'
REPORT_FILE_DIR=BASE_DIR+'/report_files/'

sys.path.append(BASE_DIR)
sys.path.append(REPORT_SIG_DIR)

from report_signature import config
from mail_service import MyEmail
from report_data_model import ReportData
  
if __name__=="__main__":
    #print config.REPORT_SIG
    #邮件页面
    rd=ReportData()
    report_data=rd.get_ktr_errors()

    errors = ['trans_views_online_source_quality','trans_views_LaunchCnt_detail','trans_crm_saler_mtd']

    to_user = [""]
    table_info=''
    if len(report_data)>0:
        for data in report_data:
            table_info += '<tr><td>'+data[0] +"</td><td>"+data[1] +"</td><td>"+data[2] +"</td><td>"+data[3] +"</td><tr>"
            if data[3] in errors:
                to_user = [""]

    #print table_info,to_user
    ##邮件配置
    my = MyEmail()
    my.to_list=to_user
    sendtime=d.datetime.now()
    my.tag = "["+sendtime.strftime('%Y-%m-%d')+"]"+"KTR任务监控报错"
    my.imgs=[{'img_url':REPORT_IMG_DIR+'page_width.png','img_tag':'pgwd'}]

    #邮件html
    my.txt="""
        <html xmlns='http://www.w3.org/1999/xhtml'>
            <head>
                <meta http-equiv='Content-Type' content='text/html; charset=UTF-8' />
                <style>
                    .footer{
                        width:100%;
                        text-align:left;
                    }
                    .context{
                        width:100%;
                    }
                    .hr_middle{
                        width:40%;
                        margin:0;
                    }

                    .context table td{
                        height:29px;
                    }

                </style>
            </head>
            <body style='padding:0;margin:0;'>
                <div class='context' style='text-align:center;'>
                    
                    
                    <table border='1' cellpadding='0' cellspacing='0' width='100%' style='text-align:center;'>
					<tr><td colspan=4 style='font-size:1.5em;border-top:1px solid black;border-left:1px solid black;border-right:1px solid black;background:rgb(230, 86, 27);color:white;padding-top:5px;padding-bottom:5px;'>【系统推送】KTR任务监控报错</td></tr>
					<tr>
					<td width='20%'><b>报错时间</b></td>
					<td width='20%'><b>服务器名称</b></td>
					<td width='30%'><b>任务文件名</b></td>
					<td width='30%'><b>ktr文件名</b></td>
                        """+table_info+\
                    """
                    <tr><td colspan=4><img src="cid:pgwd" height="30px"></td></tr>
                    </table>
                    <br>
                </div>
    """+config.REPORT_SIG+"""
            </body>
        </html>
    """
    #判断发送条件
    my.send()
