
TextEncrypt: encrypt and decrypt the text of a file
======================

### Introduction
TextEncrypt is enable to encrypt and decrypt the text of a file using AES algorithm.


Executable script (2022.01.29)

- AES_encrypt_V3.py
- AES_encrypt_V2.py
- AES_encrypt_add.py

### Preparation
1. `pip install pycryptodome`
2. For AES_encrypt_V2.py and AES_encrypt_add.py
	- `pip install pandas`
3. Create a new file named **privateKeys.txt**, to store a key string of 16 arbitrary characters

### Usage
`python AES_encrypt_V3.py`

	############################################################################
	|                                   加密操作                                |
	############################################################################

	=====欢迎使用文件内容加密、解密工具=======
	工具版本：beta 0.3 (2022.01.29)
	维护人员：WangCR

	!!! 存在密钥文件[ privateKeys.txt ]，将使用指定密钥 !!!

	=========请选择你要使用的模式=============
	加密[0]or解密[1]：0
	=========输入以逗号为分隔符的文件=========
	输入文件名：1.csv
	=========请输入你要处理的变量名===========
	输入变量名（以逗号分隔，0则全部变量）：0
	完成！输出文件名：encrypt_1.csv

	请按任意键继续. . .

	

	############################################################################
	|                                   解密操作                                |
	############################################################################

	=====欢迎使用文件内容加密、解密工具=======
	工具版本：beta 0.3 (2022.01.29)
	维护人员：WangCR

	!!! 存在密钥文件[ privateKeys.txt ]，将使用指定密钥 !!!

	=========请选择你要使用的模式=============
	加密[0]or解密[1]：1
	=========输入以逗号为分隔符的文件=========
	输入文件名：encrypt_1.csv
	=========请输入你要处理的变量名===========
	输入变量名（以逗号分隔，0则全部变量）：0
	完成！输出文件名：decrypt_encrypt_1.csv

	请按任意键继续. . .