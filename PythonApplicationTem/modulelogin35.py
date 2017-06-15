import sys    #for sys.argv
import urllib
#import urllib.request
#import urllib.parse
#import modulelogin

url = 'http://kq.digitalearth.cn/v3.0/rz.asp?id=1 '
def login():
    #action = 'login'
    username = 'zhoujg'    
    password = 'zhoujg'
    styleid=3
    ac_id = 6
    type = 1
    data = {
        'username': username,
        'password': password,
        'styleid':styleid
    }
    postdata=urllib.parse.urlencode(data).encode('utf-8')
    try:
        request=urllib.request.Request(url, postdata)
        response=urllib.request.urlopen(request)
        re=response.read()
        #print(re)
        urln='http://kq.digitalearth.cn/v3.0/qiandao.asp'
        requestn=urllib.request.Request(urln)
        requestn.add_header('Referer','http://kq.digitalearth.cn/v3.0/rz.asp?id=3')
        requestn.add_header('User-Agent',"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36")

        
        responsen=request.url(requestn)
        ren=responsen.read()
        print(ren)

        if(response.read().decode('utf-8').find('login_ok')>0):
            print('login_ok')
    except Exception as e:
        print('oops!Please check network!')
        print(e)

def logout():
    logoutdata = {'action': 'logout'}
    postdata=urllib.parse.urlencode(logoutdata).encode('utf-8')
    request=urllib.request.Request(url, postdata)
    response=urllib.request.urlopen(request)
    print(response.read().decode('utf-8')) 

    
if __name__ == '__main__':
    if len(sys.argv) == 1:
        print (modulelogin.renrenBrower("http://www.renren.com/home","�û���","����") )
        login()
    else:
        logout()
