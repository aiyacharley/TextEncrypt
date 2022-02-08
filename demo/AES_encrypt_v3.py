import os
import sys
import re
from glob import glob
# 安装Crypto，pip install pycryptodome
# C:\Users\Administrator\AppData\Local\Programs\Python\Python36\Lib\site-packages
# 找到这个路径，下面有一个文件夹叫做crypto,将c改成C，对就是改成大写就ok了！！！
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
    print("=========输入以逗号为分隔符的文件=========")
    inName = input("输入文件名or带通配符的文件格式：")
    files = glob(inName)
    if len(files) == 0:
        print("不存在(%s)文件，请输入正确的文件名" % inName)
        inName = check_file()
        return(inName)

    filesList = []
    for inF in files:
        if os.path.exists(inF):
            print("存在(%s)文件" % inF)
            filesList.append(inF)
        else:
            print("不存在(%s)文件，请输入正确的文件名" % inF)
            inName = check_file()
            return(inName)
    return(",".join(filesList))


def check_var(columns, inName):
    print("=========(%s)请输入你要处理的变量名===========" % inName)
    TargetV = input("输入变量名（以逗号分隔，0则全部变量，默认为0）：")
    # print(TargetV)
    if str(TargetV) == "0" or TargetV == '':
        TargetVars = list(columns)
    else:
        TargetVars = re.split(",|，", TargetV)
    # print(TargetVars)
    if set(columns) >= set(TargetVars):
        return(TargetVars)
    else:
        print("\n输入的变量名%s有误，请输入正确的变量名" % (set(TargetVars)-set(columns)))
        TargetVars = check_var(columns, inName)
        return(TargetVars)


def check_key():
    # print("\n请确认当前文件夹中存在密钥文件，否在将使用默认密钥！！！")
    if os.path.exists("privateKeys.txt"):
        print("!!! 存在密钥文件[ privateKeys.txt ]，将使用指定密钥 !!!\n")
        try:
            handle = open("privateKeys.txt", "r", encoding="utf-8-sig")
        except:  # noqa: E722
            handle = open("privateKeys.txt", "r", encoding="gbk")
        for rec in handle:
            if rec[0].startswith("#"):
                continue
            else:
                key = str(rec.strip())
    else:
        print("!!! 不存在密钥文件[ privateKeys.txt ]，将使用默认密钥 !!!")
        print("用户可自定义生成密钥文件[ privateKeys.txt ], 长度为16、24、32的任意字符串。\n")
        key = "0000000000000000"
    return(key)


class AesCrypto():
    def __init__(self, key="0000000000000000"):
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
        if(count % length != 0):
            add = length - (count % length)
        else:
            add = 0
        text = text+("\0".encode()*add)  # 这里的"\0"必须编码成bytes，不然无法和text拼接
        self.ciphertext = cryptor.encrypt(text)
        return(b2a_hex(self.ciphertext).decode('utf-8'))

    # 解密函数
    def decrypt(self, text):
        iv = self.key[:16].encode('utf-8')
        key = self.key.encode('utf-8')
        try:
            text1 = a2b_hex(text.encode('utf-8'))
        except:  # noqa: E722
            print("Not encrypted content !!! Please encrypting first.")
        cryptor = AES.new(key, self.mode, iv)
        try:
            plain_text = cryptor.decrypt((text1)).decode()
            return(plain_text.rstrip("\0"))
        except Exception as e:  # noqa: F841
            print("Error privateKeys !!!")
            return(text)


def process(handle, header, label, pc, TargetVarsIndex, outFile):
    out = open(outFile, 'w', encoding='utf-8', newline="")
    out.write(header+'\n')
    for line in handle:
        rec = re.split(",", line.strip())
        newL = []
        for i, s in enumerate(rec):
            if label == "0":
                if i in TargetVarsIndex:
                    newLs = pc.encrypt(s)
                else:
                    newLs = s
            else:
                if i in TargetVarsIndex:
                    newLs = pc.decrypt(s)
                else:
                    newLs = s
            newL.append(newLs)
        out.write(",".join(newL)+'\n')
    out.close()

    print("完成！输出文件名：%s\n" % outFile)
    # os.system('pause')  # 按任意键继续


def TextEncrypt():
    print("=====欢迎使用文件内容加密、解密工具=======")
    print("工具版本：beta 0.3")
    print("维护人员：WangCR\n")
    key = check_key()
    pc = AesCrypto(key=key)  # key的长度必须是16的倍数,key不设置则为默认的16个0
    print("=========请选择你要使用的模式=============")
    label = check_type()  # label=="0"为加密，=="1"为解密
    inNames = check_file()
    for inName in inNames.split(','):
        if label == "0":
            outFile = "encrypt_"+inName
        else:
            outFile = "decrypt_"+inName
        try:
            handle = open(inName, 'rt', encoding='gbk')
            header = next(handle).strip()
        except Exception as e:
            handle = open(inName, 'rt', encoding='utf-8-sig')
            header = next(handle).strip()
            # print(e)

        headerL = re.split(",", header.strip())
        TargetVars = check_var(headerL, inName)
        TargetVarsIndex = [headerL.index(v) for v in TargetVars]

        process(handle, header, label, pc, TargetVarsIndex, outFile)


if __name__ == '__main__':
    # global label,inName
    os.chdir(os.path.abspath(os.path.dirname(sys.argv[0])))
    TextEncrypt()
    