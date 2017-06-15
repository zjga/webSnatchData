#!/usr/local/bin/python3.5
import urllib.request,io,os,sys


def httpRquest(url):
    req = urllib.request.Request(url)
    f = urllib.request.urlopen(req)
    s = f.read()
    s = s.decode('UTF-8','ignore')
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



#获取第二级产品信息
def getProductRequestInfosecond(s):
    ret = isDigit(s)
    nurl="http://www.sigmaaldrich.com"+s+"?lang=en&region=US"    

    productinfore=httpRquest(nurl) 
    saveFile(productinfore,'downloadcontent.txt')
    resultarr = []
    arr = productinfore.split('<td') 


    return "";


def saveFile(s,name):
    mdir = sys.path[0]+'/'
    file = open(mdir+name,'a',1,'UTF-8')
    file.write(s)
    file.close()
    return 1

#saveFile(s,'downloadcontent.txt')
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

if __name__=="__main__":
    print("main")
    foo()