#!/usr/local/bin/python3.5
import urllib.request,io,os,sys
import database
from bs4 import BeautifulSoup

def httpRquest(url):
    req = urllib.request.Request(url)
    f = urllib.request.urlopen(req)
    s = f.read()
    #s = s.decode('UTF-8','ignore')
    s = s.decode('gbk','ignore')
   
    return s;

url="http://www.sigmaaldrich.com/catalog/search?term=109-99-9&interface=CAS%20No.&N=0&mode=match%20partialmax&lang=en&region=US&focus=product"
s=httpRquest(url)

#获取产品信息 第一级产品编号
def getProductRequestInfo_one(s):
    tpos=s.find('\">');   
    st=s[tpos+2:] 
    tpos2=st.find('</a>')
    rsts=st[:tpos2]
      
    return rsts.strip();

#获取产品信息 第一级产品编号url
def getProductRequestInfo_one_url(s):
    aim='<a href='
    tpos=s.find(aim);   
    st=s[tpos+len(aim)+1:] 
    tpos2=st.find('\">')
    rsts=st[:tpos2]
      
    return rsts.strip();

#获取第一级产品信息
def getProductRequestInfo(s):
    arr = s.split('<div class="row clearfix">')
    resultarr = []
    resultarrurl = []
    for item in arr:    
        tpos=item.find('<a href="/catalog/product/');
        if(tpos>0):
            restr=getProductRequestInfo_one(item[tpos:])   
            restrn=getProductRequestInfo_one_url(item[tpos:])   
            resultarr.append(restr)
            resultarrurl.append(restrn)
    return resultarrurl;

def isDigit(my_str): 
    try: 
        int(my_str) 
    except ValueError: 
        return False 
    return True 

#获取第二级产品信息
def getProductRequestInfosecond_page_value(str,url):    
    aim1='</ul>'
    pos = str.find(aim1) 
    tem = str[:pos+5]
    tem=tem.replace("&nbsp;","")

    saveFile(tem,'downloadcontent2.txt')
    bs_obj = BeautifulSoup(tem)  
    #a_list = bs_obj.findAll('li',attrs={'jxbh':True}) 
    a_list = bs_obj.findAll('p') 
    for a in a_list: 
        tret=a.get_text()
        print (tret)
        database.UpdateDatabaseEmail(url,tret,'','','')
        #arr = tret.split(" ") 
        #if(len(arr)>1):
        #    database.UpdateDatabaseEmail(url,arr[0],arr[1],'','')

    return tem;
#获取第二级产品信息
def getProductRequestInfosecond_page(url,productinfore):    
    aim1='<ul class="clearfix">'
    pos = productinfore.find(aim1) 
    aimvalue=''
    if(pos>0):
        temstr=productinfore[pos:]
        aimvalue=getProductRequestInfosecond_page_value(temstr,url)

    

    return "";

#获取第二级产品信息
def getProductRequestInfosecond(s):
    
    nurl="http://www.sigmaaldrich.com"+s+"?lang=en&region=US"    

    productinfore=httpRquest(nurl)     

    #saveFile(productinfore,'downloadcontent.txt')
    getProductRequestInfosecond_page(nurl,productinfore)


    return "";


def saveFile(s,name):
    mdir = sys.path[0]+'/'
    file = open(mdir+name,'a',1,'UTF-8')
    file.write(s)
    file.close()
    return 1

saveFile(s,'downloadcontent.txt')
resultarr = getProductRequestInfo(s)


for item in resultarr:    
    tpos=getProductRequestInfosecond(item);
        



def findChineseEnglishName(s,strchinenes,aimtwo):
    pos = s.find(strchinenes)
    sright = s[pos + 1:]
    straim = '</td>'
    strre = sright.find(straim,len(strchinenes))
    sleft = sright[:strre]
    postwo = sleft.find(aimtwo)
    aimre = sleft[len(aimtwo) + postwo:]
    return aimre.replace("\n", "").replace(" ", "");

strchinenes = '<td width="60" style="font-weight: 900;color: #EA5D5A;">中文名</td>'
aimtwo = '<td colspan="3">'
aimre=findChineseEnglishName(s,strchinenes,aimtwo)
print('(1)')
print('中文名字：'+aimre)

strchinenes = '<td style="font-weight: 900;color: #EA5D5A;">英文名</td>'
aimre=findChineseEnglishName(s,strchinenes,aimtwo)
print('英文名字：'+aimre)

strchinenes = '<td style="font-weight: 900;color: #EA5D5A;">CAS号</td>'
aimtwo='<td width="250">'
aimre=findChineseEnglishName(s,strchinenes,aimtwo)
print('CAS号：'+aimre)

strchinenes = '<td width="60" style="font-weight: 900;color: #EA5D5A;">MDL</td>'
aimtwo='<td>'
aimre=findChineseEnglishName(s,strchinenes,aimtwo)
print('MDL：'+aimre)

strchinenes = '<td style="font-weight: 900;color: #EA5D5A;">分子式</td>'
aimre=findChineseEnglishName(s,strchinenes,aimtwo)
print('分子式：'+aimre)

strchinenes = '<td style="font-weight: 900;color: #EA5D5A;">分子量</td>'
aimre=findChineseEnglishName(s,strchinenes,aimtwo)
print('分子量：'+aimre)

def findChineseEnglishNamehref(s,strchinenes,aimtwo):
    pos = s.find(strchinenes)
    sright = s[pos + 1:]
    straim = '</td>'
    strre = sright.find(straim,len(strchinenes))
    sleft = sright[:strre]
    postwo = sleft.find(aimtwo)
    aimre = sleft[len(aimtwo) + postwo:]
    return aimre.replace("\n", "").replace(" ", "").replace("</a>", "");
print('(2)')
strchinenes = '<td >编号：<a href="/product/proInfo?bpm_no=A01W420061">'
aimtwo='\">'
aimre=findChineseEnglishNamehref(s,strchinenes,aimtwo)
print('编号：'+aimre)

print('(3)')
strchinenes = '<td >规格及纯度：'
aimtwo='\t\t\t'
aimre=findChineseEnglishName(s,strchinenes,aimtwo)
print('规格及纯度：'+aimre)

print('(4)')
strchinenes = '<td >品牌：'
aimtwo='\t\t\t'
aimre=findChineseEnglishName(s,strchinenes,aimtwo)
print('品牌：'+aimre)

print('(5)')
def doProductInfo(s):
    pos = s.find('<th >货号</th>')
    sright = s[pos + 1:]
    pos = sright.find('<td style="color:#999696;font-weight: 900;">')
    sleft=sright[:pos]
    pos = sleft.find('<tr >')
    sright=sleft[pos:]
    return sright

#处理二级产品
for item in resultarr:    
    nurl="http://www.energy-chemical.com.cn/product"+item
    productinfore=doProductInfo(httpRquest(nurl))  
    resultarr = []
    arr = productinfore.split('<td') 
    for item in arr:    
        tpos=item.find('</td>');
        if(tpos>=0):
            itemnew=item[1:tpos]
            tposi=itemnew.find('<font')
            tposinum=itemnew.find('style="color')
            if(tposi>=0):
                itemthird=itemnew[tposi:]
                arrthird = itemthird.split('<font') 
                for itemthir in arrthird:    
                    thirdpos=itemthir.find('</font>')
                    if(thirdpos>=0):
                        itemthirtext=itemthir[:thirdpos]
                        fourpos=itemthirtext.find('\">')
                        if(fourpos>=0):
                            itemfourtext=itemthirtext[fourpos+2:]
                            resultarr.append(itemfourtext)
            elif (tposinum>=0):
                tposinum=itemnew.find('\">')
                if(tposinum>=0):
                    itemcount=itemnew[tposinum+2:]
                    resultarr.append(itemcount.replace('\n',''))
            else:
                resultarr.append(itemnew)
                
    strlen = len(resultarr)
    if(strlen>5):
        print("货号："+resultarr[0])
        print("包装："+resultarr[1])
        print("上海库存："+resultarr[2])
        print("北京库存："+resultarr[3])
        print("目录价："+resultarr[4])
        print("活动价："+resultarr[5])
    elif (strlen==5):
        print("货号："+resultarr[0])
        print("包装："+resultarr[1])
        print("上海库存："+resultarr[2])
        print("北京库存："+resultarr[2])
        print("目录价："+resultarr[3])
        print("活动价："+resultarr[4])
    print()

