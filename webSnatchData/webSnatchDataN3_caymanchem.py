#!/usr/local/bin/python3.5
#http://www.sigmaaldrich.com/catalog/search?term=109-99-9&interface=CAS%20No.&N=0&mode=match%20partialmax&lang=en&region=US&focus=product
#主要功能是抓取主页面的产品列表
import io,sys,re,imp
import pymssql
import sys
import codecs
from lxml import etree
import urllib.request
from io import StringIO
import json
#import six
import os
import threading

g_url=""
s=""
url_second=''

#写入数据库函数
def InsertToDatabase(url,Value1,Value2,Value3,Value4):
    return;
    try:
        con=pymssql.connect(host='192.168.1.252',user='netdata1',password='@@231abc',database='NetData')
        curA=con.cursor()
        InsertSql="Insert into NetData1(url,Value1,Value2,Value3,Value4) values('"+str(url)+"','"+Value1.replace("'","''")+"','"+Value2.replace("'","''")+"','"+Value3.replace("'","''")+"','"+Value4.replace("'","''")+"')"
        curA.execute(InsertSql)
        con.commit()
        con.close()
    except Exception as ex:
        print( ex)
    pass

#报错文件到同目录
def saveFile(s,name):
    mdir = sys.path[0]+'/'
    file = open(mdir+name,'a',1)
    file.write(str(s.encode('GB18030')))
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

g_title='AAAAA'
g_title_item=0

def get_title():    
    global g_title
    global g_title_item
    re=g_title+str(g_title_item    )
    g_title_item+=1
    return re;
    pass


#获取头部
def getHeader(tree):
    try:
        #
        list = tree.xpath("//div[@id='productHeader']")
        first_Name = list[0].xpath('h1[@id="productHeaderName"]/text()')
        
        colvalue=get_title()
        lists=list[0].xpath("div/div[@class='productHeaderDetail col-md-4 col-xs-12']/em")
        for ll in lists:
           print(ll.text)
           #write to database       
           InsertToDatabase(g_url,colvalue,ll.text,'','')
    except Exception as ex:
        print (ex)

        
    return "";
    pass

#获取价格
def get_Price(tree):
    try:
        #
        list = tree.xpath("//table[@id='productVariantTable']/tbody/tr")        
        for ll in list:
            t1=ll.xpath("td[@class='size col-xs-3 text-center']/text()")
            t2=ll.xpath("td[@class='price col-xs-3 text-right']/text()")
            if(len(t1)>0):
                print(t1, t2)
                #write to database       
                InsertToDatabase(g_url,t1[0],t2[0],'','')
    except Exception as ex:
        print (ex)

    return "";
    pass

#获取 Description
def get_Description(tree):
    try:
        #
        list = tree.xpath("//div[@id='description']")    
        first_Head = list[0].xpath('div[@class="sectionHeading"]/text()')   
        first_SubHeade = list[0].xpath('div[@class="sectionSubHeading"]/text()')   

        colvalue=get_title()
        first_syn = list[0].xpath('ul[@id="synonymList"]/li')   
        for ll in first_syn:            
            if(len(ll.text)>0):
                print(ll.text)
                #write to database  
                InsertToDatabase(g_url,colvalue,ll.text,'','')

        colvalue=get_title()
        first_text = list[0].xpath('p[@class="text-justify"]')   
        if(len(first_text)):
            text = first_text[0].xpath('string(.)')     
            print(text)
            #write to database  
            InsertToDatabase(g_url,colvalue,text,'','')

    except Exception as ex:
        print (ex)

    return "";
    pass

#获取 RELATED PRODUCTS
#https://www.caymanchem.com/solr/cchProduct/select?wt=json&rows=1000&q=catalogNum:(11427%20OR%2011428%20OR%2011429%20OR%2011432%20OR%2011438%20OR%2011444%20OR%2017876%20OR%2020431%20OR%2020432%20OR%2020433)
def get_RELATED_PRODUCTS(tree):
    try:
        #
        list = tree.xpath("//div[@id='relatedProductList']")        
        products=list[0].get('data-relatedproducts').replace('[','(').replace(']',')').replace('\'','').replace(' ','%20').replace(',','%20OR')
        newurl='https://www.caymanchem.com/solr/cchProduct/select?wt=json&rows=1000&q=catalogNum:'+products
        cat=httpRquest(newurl)
                
        hjson = json.loads(cat)
        list = hjson['response']['docs']
     
        colvalue=get_title()
        for ll in list:     
            for k, v in ll.items():
                if(k=='markupName'):
                    print ("%s: %s"%(k, v))          
                    #write to database
                    InsertToDatabase(g_url,colvalue,v,'','')

       

    except Exception as ex:
        print (ex)

    return "";
    pass
#get_TECHNICAL_INFORMATION
def get_TECHNICAL_INFORMATION(tree):
    try:
        #
        list = tree.xpath("//div[@id='technicalInformation']")        
        sectionhead=list[0].xpath('div/text()')

        first_text = list[0].xpath('table/tr') 
        for ll in first_text:            
            tex = ll.xpath('td') 
            
            if(tex):
                print(str(tex[0].text).encode('GB18030'))  
                print(str(tex[1].text).encode('GB18030'))  
                 
                #write to database       
                InsertToDatabase(g_url,tex[0].text,tex[1].text,'','')
    except Exception as ex:
        print (ex)

    return "";
    pass
#查找//div[@id='technicalInformation']
def get_TECHNICAL_INFORMATION_NoTree_Tbody(content):
    try:
        pos1=content.find('technicalInformationTable')
        
        if(pos1>0):
            tem=content[pos1:]
            pos2=tem.find('</table>')
            if(pos2>0):
                temn=tem[:pos2]
                return temn

        return ''
        pass
    except Exception as ex:
        print(ex)
    pass
#get_TECHNICAL_INFORMATION
def get_TECHNICAL_INFORMATION_NoTree_td(tdbody):
    try:        
        pos1=tdbody.find('\">')
        if(pos1>0):
            tex0 = tdbody[pos1+2:]
            aim='</td>'
            pos2=tex0.find(aim)
            if(pos2>0):
                aim=tex0[:pos2]
                return aim
       
        return ''
    except Exception as ex:
        print (ex)

    return "";
    pass
#get_TECHNICAL_INFORMATION
def get_TECHNICAL_INFORMATION_NoTree(content):
    try:
        tbody=get_TECHNICAL_INFORMATION_NoTree_Tbody(content)
        x= tbody.split('<tr',)
        for ii in x:    
            pos1=ii.find('<td')
            if(pos1>0):
                tex0 = ii[pos1:]
                aim='<td'
                pos2=tex0.find(aim,3)
                if(pos2>0):
                    textd1=tex0[:pos2]
                    textd2=tex0[pos2:]
                    name=get_TECHNICAL_INFORMATION_NoTree_td(textd1)
                    value=get_TECHNICAL_INFORMATION_NoTree_td(textd2)
                    print(name.encode('GB18030'))
                    print(value.encode('GB18030'))
                    #write to database       
                    InsertToDatabase(g_url,name,value,'','')
    except Exception as ex:
        print (ex)

    return "";
    pass
#get_SHIPPING_STORAGE
def get_SHIPPING_STORAGE(tree):
    try:
        #
        list = tree.xpath("//div[@id='shippingAndStorage']")        
        sectionhead=list[0].xpath('div/text()')

        first_text = list[0].xpath('table/tr') 
        for ll in first_text:            
            tex = ll.xpath('td') 
            
            if(tex):
                print(str(tex[0].text).encode('GB18030'))  
                print(str(tex[1].text).encode('GB18030'))  
                 
                #write to database       
                InsertToDatabase(g_url,tex[0].text,tex[1].text,'','')
    except Exception as ex:
        print (ex)

    return "";
    pass

#get_REFERENCES_PRODUCT_CITATIONS
def get_REFERENCES_PRODUCT_CITATIONS(tree):
    try:
        #
        list = tree.xpath("//div[@id='references']")        
        sectionhead=list[0].xpath('div[@class="sectionHeading"]/text()')
        sectionsubhead=list[0].xpath('div[@class="sectionSubHeading"]/text()')
        
        #write to database 
        InsertToDatabase(g_url,sectionhead[0],sectionsubhead[0],'','')

        colvalue=get_title()
        first_text = list[0].xpath('p[@class="referenceText"]') 
        for ll in first_text:            
            tex = ll.xpath('string(.)')             
            if(len(tex)>0):
                print(str(tex).encode('GB18030'))                   
                #write to database       
                InsertToDatabase(g_url,colvalue,str(tex),'','')

    except Exception as ex:
        print (ex)

    return "";
    pass

def readfile(path):
    file_object = open(path, mode='r', encoding='UTF-8')
    try:
       all_the_text = file_object.read()
       return all_the_text
    finally:
       file_object.close( )
    return ''
    pass

def hello():
    try:
        content = readfile('E:/x/w/tmp/temp20170613/NeosolanioChemical.html')
        tree=StringIO_ToTree(content)
        if not tree:
            return None
        return tree
    except Exception as ex:
        print(ex)
    pass


def parse_Content(content):
    try:
        tree = StringIO_ToTree(content)
        #tree = hello()
        if not tree:
            return None

        ##第一步 头部
        getHeader(tree)
        
        ##第二步 价格
        get_Price(tree)         

        ##第三步 description
        get_Description(tree)   
       
        #第四步 RELATED PRODUCTS 待续
        get_RELATED_PRODUCTS(tree)         

        #第五步 RELATED PRODUCTS 
        #get_TECHNICAL_INFORMATION(tree)         
        get_TECHNICAL_INFORMATION_NoTree(content)         

        #第六步 SHIPPING & STORAGE
        get_SHIPPING_STORAGE(tree)  

        #第七步 REFERENCES & PRODUCT CITATIONS
        get_REFERENCES_PRODUCT_CITATIONS(tree)  

    except Exception as ex:
        print(ex)
    pass

def OpenFile():
    mdir = sys.path[0]+'/'+'productNum.txt'
    file = open(mdir)
 
    while 1:
        line = file.readline()
        if not line:
            break
        print(line)
        InitEnviroment(line.replace('\n',''))
    pass # do something

def InitEnviroment(urlread):
    
    global g_url   
    global s    
    #saveFile(s,"downloadtem.txt")
  
    #url="https://www.caymanchem.com/product/"+str(i)+"?countryRegionId=US"
    url= urlread+"?countryRegionId=US"
    print(url)
    g_url=url
    s=httpRquest(url)
    pos = s.find('No information is currently')
    if(pos>0):
        print('NO Data!!!!!!!!!!!!!!!!!!!!!!!!!')   
        return     
    parse_Content(s)
    pass

    return ''

if __name__=="__main__":
    print(("main"))
    OpenFile()
    