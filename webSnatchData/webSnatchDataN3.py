#!/usr/local/bin/python3.5
#http://www.sigmaaldrich.com/catalog/search?term=109-99-9&interface=CAS%20No.&N=0&mode=match%20partialmax&lang=en&region=US&focus=product
#主要功能是抓取主页面的产品列表，打开列表页面取页面中的信息 页面头部 产品属性 描述 价格 customer view等信息 

import io,sys,re,imp
import pymssql
import sys
import codecs
from lxml import etree
import urllib.request
from io import StringIO
import six

url=""
s=""
url_second=''

#写入数据库函数
#def InsertToDatabase(url,Value1,Value2,Value3,Value4):
#    try:
#        con=pymssql.connect(host='192.168.1.252',user='netdata1',password='@@231abc',database='NetData')
#        curA=con.cursor()
#        InsertSql="Insert into NetData1(url,Value1,Value2,Value3,Value4) values('"+str(url)+"','"+Value1.replace("'","''")+"','"+Value2.replace("'","''")+"','"+Value3.replace("'","''")+"','"+Value4.replace("'","''")+"')"
#        curA.execute(InsertSql)
#        con.commit()
#        con.close()
#    except Exception as ex:
#        print( ex
#    pass

#报错文件到同目录
def saveFile(s,name):
    mdir = sys.path[0]+'/'
    file = open(mdir+name,'a',1)
    file.write(s)
    file.close()
    return 1

#通用get请求html
def httpRquest(url):
    try:
        req = urllib.request.urlopen(url)        
        s = req.read()
        html = s.decode('UTF-8','ignore')
        return html;
    except Exception as ex:
        print( ex)
    pass

def InitEnviroment():
    url="http://www.sigmaaldrich.com/catalog/search?term=109-99-9&interface=CAS%20No.&N=0&mode=match%20partialmax&lang=en&region=US&focus=product"
    global s
    s=httpRquest(url)
    return ''

#通用返回html转tree 有错误返回None
def StringIO_ToTree(content):
    try:
        if not content:
            return None
    
        htmlparser = etree.HTMLParser()
        content1 = io.StringIO(content)
        #content1 = six.StringIO(str(content))
        #content1 = io.BytesIO(bytes(content, encoding = "utf8"))
        tree = etree.parse(content1,htmlparser)

        return tree
    except Exception as ex:
        print( ex)
    pass

#获取第二级产品信息 页面头部标题
def getProductRequestInfosecondReult(content,nurl):
    
    tree=StringIO_ToTree(content)
    if not tree:
        return None

    list=tree.xpath("//div/div/div/div/div/ul[@class='clearfix']/li")
    for ll in list:
       first_Name=ll.xpath("p/text()")
       first_Value=ll.xpath("p/span/a/text()")
       if(len(first_Name)>0):
           print( first_Name )
           print( first_Value)

           ####写入数据库 标题
           #InsertToDatabase(url_second,first_Name,first_Value,'','')
       
      

    return "";

    pass
#
def del_n_r(str):
    return str.replace("\r\n"," ")
    pass
#获取第二级产品信息 页面属性
def getProductRequestInfosecondReult_Properties(content):
    try:
        tree=StringIO_ToTree(content)
        if not tree:
            return None

        list=tree.xpath("//div/div/div/div/div/div[@id='productDetailProperties']/table/tbody/tr")
        for ll in list:
           first_Name=ll.xpath("td[@class='lft']/text()")
           listvalue=ll.xpath("td[@class='rgt']/a/text()")
           if(len(listvalue)==0):
                listvalue=ll.xpath("td[@class='rgt']/text()")
           first_value=''
           for text in listvalue:
               if(len(text)>0):
                   first_value += text+','
      
           if(len(first_Name)>0):
               p_Name = re.sub('\xa0',' ',''.join(first_Name))
               p_Value = re.sub(r'\n|\t|,','',''.join(first_value))
               print( p_Name.encode('GB18030'))
               print( p_Value.encode('GB18030'))

               ####写入数据库  property
               #InsertToDatabase(url_second,first_Name,first_Value,'','')
       
        return "";
    except Exception as ex:
        print( ex)
    pass

#获取第二级产品信息 页面属性 描述
def getProductRequestInfosecondReult_productDescription(content):
    try:
        tree=StringIO_ToTree(content)
        if not tree:
            return None

        list=tree.xpath("//div[@id='productDescription']/div[@class='descriptionContent']/h4")
        listp=tree.xpath("//div[@id='productDescription']/div[@class='descriptionContent']/p")
  
        descriptionName=[]
        descriptionvalue=[]
        descriptionPack=''
        first = 'false'
        for llst in listp:        
           listvaluetem = llst.xpath('string(.)')               
           descriptionvalue.append(listvaluetem)

        for ll in list:
           first_Name=ll.xpath("text()")
           descriptionName.append(first_Name)

        descriptionvaluenew=[]
        descriptionvaluenew.append(descriptionvalue[0])
        tem=''
        i=1
        for i in range(1,len(descriptionvalue)-3):
           tem +=descriptionvalue[i]
           i+=1
        size=i
        descriptionvaluenew.append(tem)
        for i in range(size,len(descriptionvalue)):
           descriptionvaluenew.append(descriptionvalue[i])
           i+=1

        if(len(descriptionName)==len(descriptionvaluenew)):
            for i in range(0, len(descriptionName)): 
                name=str(descriptionName[i]).replace('\\n',"").replace('\\t',"")                
                print((''.join(name))                )
                print((descriptionvaluenew[i].encode('GB18030'))) 
                ####写入数据库  property
                #InsertToDatabase(url_second,descriptionName[i],descriptionvaluenew[i],'','')
       
        return "";
    except Exception as ex:
        print( ex)
    pass

#获取第二级产品信息 页面属性 safetyInfo
def getProductRequestInfosecondReult_SafetyInfo(content):    
    try:    
        tree=StringIO_ToTree(content)
        if not tree:
            return None

        list=tree.xpath("//div[@id='productDetailSafety']/div[@class='safetyBox']/div[@class='safetyRow']")
    
        for llst in list: 
           listteml = llst.xpath("div[@class='safetyLeft']/text()") 
           listtemr = ''
           listtemr = llst.xpath("div[@class='safetyRight']/text()")    
           print(  str(listteml).replace('\\n','') )
           print( str(listtemr).replace('\\n',''))

           if(len(listtemr)==0):
               listtemr = llst.xpath("div[@class='safetyRight']/a/text()")  

           if(len(listtemr)>0):
               name=str(listtemr).replace('\\n','')
               print( str(listtemr).replace('\\n',''))
               ####写入数据库  property
               #InsertToDatabase(url_second,listteml,listtemr,'','')        
        return "";
    except Exception as ex:
        print( ex)
    pass

#获取第二级产品信息
def getProductRequestInfosecond(s):
    
    nurl="http://www.sigmaaldrich.com"+s+"?lang=en&region=US"    
    global url_second
    url_second=nurl
    productinfore=httpRquest(nurl) 
     
    #获取第二级  property
    getProductRequestInfosecondReult_Properties(productinfore)    

    #获取第二级  Description
    getProductRequestInfosecondReult_productDescription(productinfore)
    
    #获取第二级  SafetyInfo
    getProductRequestInfosecondReult_SafetyInfo(productinfore)

    return "";

#post 获取价格信息 特殊处理请求方式
def post_url_data2(url,header,data):
    try:
        html = None
        response = unirest.post(url,headers=header, params=data)
        #print( response.code        # The HTTP status code
        #print( response.headers     # The HTTP headers
        html= response.body         # The parsed response
        return html
    except Exception as ex:
        print( ex)
    pass

def httpRquest_old(url):
    try:
        req = urllib.request.Request(url)
        f = urllib.request.urlopen(req)
        s = f.read()
        s = s.decode('UTF-8','ignore')
        return s;
    except Exception as ex:
        print(ex)

#获取第二级  price 结果解析展示，写入数据库
def parse_List_price(content,pn,cat):
    
    tree=StringIO_ToTree(content)
    if not tree:
        return None

    list=tree.xpath("//tr")
    for ll in list:
       
       sku=ll.xpath("td[@class='sku']/p/text()")
       if(len(sku)>0):
           result="{'sku':'"+"".join(sku)+"',"
           price=ll.xpath("td[@class='price']/p/text()")
           if(len(price)>0):
               print( ''.join(sku))
               print( ''.join(price))
               ####写入数据库  价格
               #InsertToDatabase(url_second,sku,price,'','')

    pass


#获取第二级  price 
def run_one_by_one_price(url,pn,cat):
    try:        
        index_url = "http://www.sigmaaldrich.com/catalog/PricingAvailability.do?productNumber="+pn+"&brandKey="+cat+"&divId=pricingContainerMessage"

        header = {"Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
                  "Host":"www.sigmaaldrich.com",
                  "Pragma":"no-cache",
                   "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:36.0) Gecko/20100101 Firefox/36.0",
                   "X-Requested-With":"XMLHttpRequest",
                   "cookie":"JSESSIONID=B39B7B6464174A9F9591E43808AF317A.stltcat03; TLTUID=ADD4638A09D91009091CAB1C2EA6F5D4; GUID=b79af922-3ecf-4c3b-917b-bf4ea0994994|NULL|1426506067726; __unam=40e1073-1472b322e5b-1e6ef7e1-25; country=USA; SialLocaleDef=CountryCode~US|WebLang~-1|; SessionPersistence=CLICKSTREAMCLOUD%3A%3DvisitorId%3Danonymous%7CPROFILEDATA%3A%3Davatar%3D%2Fetc%2Fdesigns%2Fdefault%2Fimages%2Fcollab%2Favatar.png%2CisLoggedIn%3Dtrue%2CisLoggedIn_xss%3Dtrue%2CauthorizableId%3Danonymous%2CauthorizableId_xss%3Danonymous%2CformattedName%3D%2CformattedName_xss%3D%7CSURFERINFO%3A%3Dbrowser%3DUnresolved%2COS%3DWindows%2Cresolution%3D1366x768%2Ckeywords%3D%7C; _ga=GA1.2.1674815859.1405179022; __ar_v4=7LVJN6BSTJF53GX2R4GID7%3A20150315%3A20%7CJ7B5WUY6URABXKGK2JGKIC%3A20150315%3A20%7CQ4SKPJ6JAFAM3L6QZME5SD%3A20150315%3A20; TLTSID=B626435ACC9810CC000DD72A766B60AB;"
                  }
        #data="loadFor=PRD_RS"        
        #params = urllib.parse.urlencode({'loadFor': 'PRD_RS', 'productNumber': 'TX0277', 'brandKey': 'MM', 'divId': 'pricingContainerMessage'}).encode(encoding='UTF8')

        param = urllib.parse.urlencode({'loadFor':'PRD_RS'}).encode(encoding='UTF8')

        req = urllib.request.Request(index_url, param, header)
        response = urllib.request.urlopen(req)
        html = response.read()        

        list=parse_List_price(html.decode('UTF-8','ignore'),pn,cat)
    except Exception as ex:
        print( ex)
    pass

#获取第二级  Customer 结果解析展示，写入数据库
def parse_List_Customers(content,pn,cat):
    try:
        tree=StringIO_ToTree(content)
        if not tree:
            return None

        list=tree.xpath('//div[@class="product-recommend__product-container"]')

        for ll in list:       
           first_Name=ll.xpath('p[@class="product-recommend__product-name"]/a/text()')
           first_Num=ll.xpath('p[@class="product-recommend__product-number"]/text()')
           first_Key=ll.xpath('p[@class="product-recommend__product-key"]/text()')
           ####写入数据库  customer
           #InsertToDatabase(url_second,first_Name,first_Num,first_Key,'')
    except Exception as ex:
        print( ex)
    pass

#获取第二级  Customer review html
def run_one_by_one_customers(url,pn,cat):
    try:
        index_customer_url = "http://cloud-analytics.sial.com/?get=recBlock&type=caRecBlock&guid=5df11486-9e57-46b0-8ba2-d27372a12a85&country=USA&product="+pn+"&brand="+cat+"&memberId=Unknown"
        html=httpRquest(index_customer_url)
        list=parse_List_Customers(html,pn,cat)
    except Exception as ex:
        print( ex)

    pass

#获取第二级产品信息-价格信息 javascript:openPAOnSR_RS('401757','SIAL','padiv11_401757SIAL','pabtn11_401757SIAL','
def getProduct_Request_Second_Html_price_customer(s):
    pos=s.find('(')
    tem = s[pos+1:]
    pos=tem.find(')')
    tem = tem[:pos].replace('\'','')
    rearry=tem.split(',')
    #根据第一级页面的产品 参数请求价格 和 customerview的 html
    run_one_by_one_price('',rearry[0],rearry[1])
    run_one_by_one_customers('',rearry[0],rearry[1])

    return "";

def parse_List(content):
    try:
        tree=StringIO_ToTree(content)
        if not tree:
            return None

        #第一步取得第二级页面的 url中间路径参数
        #list=tree.xpath("//div/div/div/div/div/div/ul/li[@class='productNumberValue']/a/@href")
        #for ll in list:
        #   getProductRequestInfosecond(ll)
        #第二步获取第二级页面价格、customer review所需参数
        listPrice=tree.xpath("//div/div/div/div/div/div/ul/li[@class='priceValue']/div/a/@onclick")
        for ll in listPrice:
           getProduct_Request_Second_Html_price_customer(ll)          

    except Exception as ex:
        print(ex)
    pass


if __name__=="__main__":
    print(("main"))
    InitEnviroment()
    list=parse_List(s)