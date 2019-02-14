#coding:utf8 
''''' 
日报 
'''  
import datetime  
import email  
import smtplib  
import os
import sys
from email.mime.text import MIMEText  
from email.mime.multipart import MIMEMultipart  
from email.mime.image import MIMEImage
import gethtml

class MyEmail:  
    def __init__(self):  
        self.user = "用户名"
        self.passwd = "密码"
        self.to_list = []  
        self.cc_list = []  
        self.tag = None  
        self.doc = None
        self.txt= ''
        self.imgs=[]
  
  
    def send(self):  
        ''''' 
        发送邮件 
        '''  
        try:  
            server = smtplib.SMTP_SSL("smtp.exmail.qq.com",port=465)  
            server.login(self.user,self.passwd)  
            server.sendmail("<%s>"%self.user, self.to_list + self.cc_list, self.get_attach())  
            server.close()  
            print "send email successful"  
        except Exception,e:
            print e
            print "send email failed"

    def add_img(self,src,imgid):
        fp = open(src, 'rb')  #打开文件
        msgImage = MIMEImage(fp.read()) #读入 msgImage 中
        fp.close() #关闭文件
        msgImage.add_header('Content-ID', imgid)
        return msgImage

    def get_attach(self):  
        ''''' 
        构造邮件内容 
        '''  
        attach = MIMEMultipart('related')
        #添加邮件内容  
        txt = MIMEText(self.txt,'html','utf-8')
        attach.attach(txt)
        #print txt
        if self.tag is not None:  
            #主题,最上面的一行  
            attach["Subject"] = unicode(self.tag,'utf-8')  
        if self.user is not None:  
            #显示在发件人  
            attach["From"] = unicode("发送人<%s>"%self.user,'utf-8')
        if self.to_list:  
            #收件人列表  
            attach["To"] = ";".join(self.to_list)  
        if self.cc_list:  
            #抄送列表  
            attach["Cc"] = ";".join(self.cc_list)  
        if self.doc:  
            #估计任何文件都可以用base64，比如rar等  
            #文件名汉字用gbk编码代替  
            name = os.path.basename(self.doc).encode("gbk")  
            f = open(self.doc,"rb")  
            doc = MIMEText(f.read(), "base64", "gb2312")  
            doc["Content-Type"] = 'application/octet-stream'  
            doc["Content-Disposition"] = 'attachment; filename="'+name+'"'  
            attach.attach(doc)  
            f.close()
        if self.imgs:
            #加载本地图片
            for img in self.imgs:
                attach.attach(self.add_img(img['img_url'],img['img_tag']))

        attach['Accept-Language']='zh-CN'
        attach['Accept-Charset']='utf-8,ISO-8859-1'
        return attach.as_string() 
  
  
if __name__=="__main__":
    my = MyEmail()  
    #my.user = ""
    #my.passwd = ""
    my.to_list = ["",]
    #my.cc_list = [""]
    my.tag = "邮件模板"
    now_time = datetime.datetime.now()  
    yes_time = now_time + datetime.timedelta(days=-1)  
    yes_time_nyr = yes_time.strftime('%Y-%m-%d')  
    #my.doc =r"C:\Users\Administrator\Desktop\111.html"
    
    #my.imgs=[{'img_url':'report_imgs/a.jpg','img_tag':'apic'},{'img_url':'report_imgs/b.jpg','img_tag':'bpic'}]

    my.txt="""
    <html xmlns='http://www.w3.org/1999/xhtml'>
            <head>
                <meta http-equiv='Content-Type' content='text/html; charset=UTF-8' />
            </head>
            <body >
                <div>


          <table width='100%' >


			<tr><td colspan=4 style='font-size:1.5em;border-top:1px solid black;border-left:1px solid black;border-right:1px solid black;background:rgb(230, 86, 27);color:white;padding-top:5px;padding-bottom:5px;'>【系统推送】KTR任务监控报错</td></tr>
			<tr>
			<td width='20%'><b>ktr文件名</b></td> 
			<td width='30%'>test1.ktr</td>
			<td width='20%'><b>报错时间</b></td>
			<td width='30%'>2018-12-19 17:47:04</td>
			<tr>
			</table>
			<div>

        </body>
        </html>
    """
    my.send()  
