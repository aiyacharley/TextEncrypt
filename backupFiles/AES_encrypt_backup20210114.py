# -*- coding: utf-8 -*-
import os,sys
import csv,time,re,gzip
import numpy as np
import pandas as pd
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex

def check_type():
    label = input("加密[0]or解密[1]：")
    if label == "0":
        return(label)
    elif label == "1":
        return(label)
    else:
        print("\n请输入正确的处理模式[0:加密,1:解密]")
        label = check_type()
        return(label)
def check_file():
    print("=========请输入你要处理的文件名=========")
    inName = input("输入文件名：")
    if os.path.exists(inName):
        return(inName)
    else:
        print("\n不存在(%s)文件，请输入正确的文件名"%inName)
        inName = check_file()
        return(inName)
def check_var(columns):
    print("=========请输入你要处理的变量名=========")
    TargetV = input("输入变量名（多个变量请以逗号分隔）：")
    TargetVars = re.split(",|，",TargetV)
    if set(columns) > set(TargetVars):
        return(TargetVars)
    else:
        print("\n输入的变量名(%s)有误，请输入正确的变量名"%(set(TargetVars)-set(columns)))
        TargetVars = check_var(columns)
        return(TargetVars)
def check_key():
    #print("\n请确认当前文件夹中存在密钥文件，否在将使用默认密钥！！！")
    if os.path.exists("BIGCS_AESkeys"):
        print("存在密钥文件，将使用指定密钥!!!\n")
        handle = gzip.open("BIGCS_AESkeys","rb")
        next(handle)
        for rec in handle:
            key = str(rec).split("'")[1]
    else:
        print("不存在密钥文件，将使用默认密钥!!!\n")
        key = "0000000000000000"
    return(key)
class AesCrypto():
    def __init__(self,key="0000000000000000"):
        self.mode = AES.MODE_CBC 
        self.key = key
    # 加密函数，text参数的bytes类型必须位16的倍数
    def encrypt(self, text):
        text = text.encode()
        iv = self.key[:16].encode('utf-8')
        key = self.key.encode('utf-8')
        cryptor = AES.new(key, self.mode, iv)
        length = 16
        count = len(text)
        if(count%length != 0):
            add = length-(count%length)
        else:
            add=0
        text = text+("\0".encode()*add)  # 这里的"\0"必须编码成bytes，不然无法和text拼接
        self.ciphertext = cryptor.encrypt(text)
        return(b2a_hex(self.ciphertext).decode('utf-8'))
    # 解密函数
    def decrypt(self, text):
        iv = self.key[:16].encode('utf-8')
        key = self.key.encode('utf-8')
        try:
            text1 = a2b_hex(text.encode('utf-8'))
        except:
            print("Not encrypted content !!! Please encrypting first.")
        cryptor = AES.new(key, self.mode, iv)
        try:
            plain_text = cryptor.decrypt((text1)).decode()
            return(plain_text.rstrip("\0"))
        except Exception as e:
            return(text)
def setAesCrypto(df,colname,Crypto="0"):
    known = df.loc[:,colname].values
    newL = []
    for s in known:
        if Crypto=="0":
            e = pc.encrypt(str(s))
        else:
            e = pc.decrypt(str(s))
        newL.append(e)
    return(newL)
def main():
    for var in TargetVars:
        newL = setAesCrypto(df,var,Crypto=label)
        df.loc[:, var] = newL
    df.to_csv(outFile,index=0,encoding='gbk')
    if label=="0":
        print("文件加密完成！输出文件名：%s"%outFile)
    else:
        print("文件解密完成！输出文件名：%s"%outFile)
    time.sleep(3)
    os.system('pause') #按任意键继续

if __name__ == '__main__':
    global label,inName
    os.chdir(os.path.abspath(os.path.dirname(sys.argv[0])))
    print("=====欢迎使用文件内容加密、解密工具=====")
    print("工具版本：beta 0.1 (2021.01.14)")
    print("维护人员：Wang Chengrui\n")
    key = check_key()
    pc = AesCrypto(key=key) # key的长度必须是16的倍数,key不设置则为默认的16个0
    print("=========请选择你要使用的模式==========")
    label = check_type() # label=="0"为加密，=="1"为解密
    inName = check_file()
    if label=="0":
        outFile = "encrypt_"+inName
    else:
        outFile = "decrypt_"+inName
    df = pd.read_csv(inName,encoding='gbk')
    TargetVars = check_var(df.columns)
    main()