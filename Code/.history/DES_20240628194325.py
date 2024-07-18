from Tables import *

def readFile(inputname):
    """
    Input:
        inputname: 打开文件名
    Output: 
        message: 读取文件中字符串
    """
    try:
        f = open(inputname, "r", encoding="utf-8")   # 使用utf-8编码读取文件
        message = f.read()  # 读取文件内容
        f.close()   
        return message
    except:
        print("Failed to open file!")

def writeFile(outputname, message):
    '''
    Input:
        outputname: 写入文件名
        message ：字符串
    '''
    try:
        f = open(outputname, "w", encoding="utf-8")   # 使用utf-8编码写入文件
        f.write(message)  # 写入文件
        f.close()
    except:
        print("Failed to write file!")

def str2bit(message):
    """
    Input:
        message: 字符串
    Output:
        bits: 字符串对应的二进制字符串
    """
    bits = ""
    for i in message:
        Asc2i = bin(ord(i))[2:]   # 使用bin将十进制数转二进制返回去掉0b的01字符串
        for _ in range(8-len(Asc2i)): # 可能需要补齐至8位
            Asc2i = "0" + Asc2i
        bits += Asc2i
    return bits

def key2bit(key):
    """
    Input:
        key: 密钥字符串
    Output:
        key_bits: 密钥对应的64位二进制字符串
    """
    key_bits = str2bit(key)
    if len(key_bits) < 64:
        for _ in range(64-len(key_bits)):   # 可能需要补齐至64位
            key_bits = "0" + key_bits
    return key_bits

def key2bit_and_check(key):
    """
    Input:
        key: 密钥字符串
    Output:
        key_bits: 密钥对应的64位二进制字符串(采用偶校验)
    """
    key_bits = ""
    for i in key:
        one_count = 0
        Asc2i = bin(ord(i))[2:] # 使用bin将十进制数转二进制返回去掉0b的01字符串
        for j in Asc2i:
            one_count += int(j) # 计算1的个数
        if one_count % 2 == 1:
            Asc2i += "1"
        else:
            Asc2i += "0"
        for _ in range(7-len(Asc2i)):   # 补齐至7位,第8位作为奇偶效验位
            Asc2i = "0" + Asc2i
        key_bits += Asc2i
    if len(key_bits) > 64:
        return key_bits[0:64]
    else:
        for _ in range(64-len(key_bits)):   # 可能需要补齐至64位
            key_bits += "0"
        return key_bits

def divide(bits, num):
    """
    Input:
        bits: 输入的二进制字符串
        num: 分割的位数即要将bits按照num位进行分组
    Output:
        divided_bits: 分割后的二进制字符串(列表)
    """
    divided_num = len(bits) // num
    divided_bits = []
    for i in range(divided_num):
        divided_bits.append(bits[i*num:(i+1)*num])
    if len(bits) % num != 0:
        divided_bits.append(bits[divided_num*num:])
        for i in range(num - len(divided_bits[divided_num])):
            divided_bits[divided_num] += "0"    # 补0
    return divided_bits

def IP_process(bits):
    """
    Input:
        bits: 64位的01比特字符串
    Output:
        IP_bits: 初始置换后的64位01比特序列
    """
    IP_bits = ""
    for i in IP:
        IP_bits += bits[i-1]
    return IP_bits