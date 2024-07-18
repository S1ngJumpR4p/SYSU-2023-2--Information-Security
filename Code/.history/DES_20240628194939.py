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
        result: 字符串对应的二进制字符串
    """
    result = ""
    for i in message:
        Asc2i = bin(ord(i))[2:]   # 使用bin将十进制数转二进制返回去掉0b的01字符串
        for _ in range(8-len(Asc2i)): # 可能需要补齐至8位
            Asc2i = "0" + Asc2i
        result += Asc2i
    return result

def key2bit(key):
    """
    Input:
        key: 密钥字符串
    Output:
        result: 密钥对应的64位二进制字符串
    """
    result = str2bit(key)
    if len(result) < 64:
        for _ in range(64-len(result)):   # 可能需要补齐至64位
            result = "0" + result
    return result

def key2bit_and_check(key):
    """
    Input:
        key: 密钥字符串
    Output:
        result: 密钥对应的64位二进制字符串(采用偶校验)
    """
    result = ""
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
        result += Asc2i
    if len(result) > 64:
        return result[0:64]
    else:
        for _ in range(64-len(result)):   # 可能需要补齐至64位
            result += "0"
        return result

def divide(bits, num):
    """
    Input:
        bits: 输入的二进制字符串
        num: 分割的位数即要将bits按照num位进行分组
    Output:
        result: 分割后的二进制字符串(列表)
    """
    divided_num = len(bits) // num
    result = []
    for i in range(divided_num):
        result.append(bits[i*num:(i+1)*num])
    if len(bits) % num != 0:
        result.append(bits[divided_num*num:])
        for i in range(num - len(result[divided_num])):
            result[divided_num] += "0"    # 补0
    return result

def IP_process(bits):
    """
    Input:
        bits: 64位的01比特字符串
    Output:
        result: 初始置换后的64位01比特序列
    """
    result = ""
    for i in IP:
        result += bits[i-1]
    return result

def IP_inv_process(bits):
    """
    Input:
        bits: 经过16轮迭代的64位01字符串
    Output:
        result: 逆初始置换得到64位密文01字符串
    """
    result = ""
    for i in IP_inv:
        result += bits[i-1]
    return result

def Expand(bits):
    """
    Input:
        bits: 32位01序列字符串
    Output:
        result: 扩展置换E后的48位01字符串
    """
    result = ""
    for i in E:
        result += bits[i-1]
    return result

