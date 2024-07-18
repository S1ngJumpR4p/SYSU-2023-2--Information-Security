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

def PC_minus_1_process(key):
    '''
    Input:
        key: 64位有效密钥01比特字符串
    Output:
        result: 密钥置换PC-1后56位01比特字符串
    '''
    result = ""
    for i in PC_minnus_1:
        result += key[i-1]
    return result

def leftShift(key, num):
    """
    Input:
        key: PC-1置换后的28位01比特字符串
        num: 左移的位数
    Output:
        result: 左移num位的结果
    """
    result = key[num: 28] + key[0:num]
    return result

def PC_minus_2_process(key):
    '''
    Input:
        key : 56位移位后密钥01比特字符串
    Output:        
        result : 密钥置换PC-2后48比特序列字符串
    '''
    result = ""
    for i in PC_minnus_2:
        result += key[i-1]
    result

def generateKey(key):
    """
    Input:
        key: 56位移位后密钥01比特字符串
    Output    
        result: PC-2置换后48位序列字符串
    """
    result = []
    Key = PC_minus_1_process(key)   # PC-1置换
    left, right = Key[0:28], Key[28:]
    for i in range(len(LEFT_LOOR_SHIFT)):
        Left = leftShift(left, LEFT_LOOR_SHIFT[i])
        Right = leftShift(right, LEFT_LOOR_SHIFT[i])
        Key_i = PC_minus_2_process(Left + Right)   # PC-2置换
        result.append(Key_i)
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

def XOR(bits, key):
    '''
    Input:
        bits: 48位01字符串 / 32位01比特字符串 F函数输出
        key: 48位01密钥序列 / 32位01比特字符串 Li
    Output    
        result: bits与ki异或运算得到的48bit01 / 32bit01 
    '''    
    result = ""
    for i in range(len(bits)):
        if bits[i] == key[i]:
            result += "0"
        else:
            result += "1"
    return result

def S(bits, id):
    """
    Input:
        bits: 6位01比特字符串
        id: S盒编号
    Output:
        result: S盒运算后的4位01比特字符串
    """
    row = int(bits[0]+bits[-1], 2)  # 将首尾两位组合起来，再转成十进制
    col = int(bits[1:-1], 2)    # 取中间4位组合起来，再转成十进制
    result = bin(S[id-1][row*16+col])[2:]   # 获取S盒对应位置的元素
    L = len(result)
    for i in range(4-L):  # 补0
        result = "0" + result   
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
