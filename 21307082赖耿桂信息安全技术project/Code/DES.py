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

def bit2str(bits):
    """
    Input:
        bits: 01比特字符串
    Output:
        message: 二进制字符串对应的字符串
    """
    message = ""
    for i in range(len(bits)//8):
        message += chr(int(bits[i*8:(i+1)*8],2))
    return message

def key2bit(key):
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
    # print("length of bits:")
    # print(len(bits))
    # print("group nunmber:")
    # print(divided_num)
    result = []
    for i in range(divided_num):
        result.append(list(bits[i*num:(i+1)*num]))
    if len(bits) % num != 0:
        result.append(list(bits[divided_num*num:]))
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
    for i in IP_table:
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
    for i in PC_minnus_1_table:
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
    for i in PC_minnus_2_table:
        result += key[i-1]
    return result

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
    for i in range(len(LEFT_LOOR_SHIFT_table)):
        Left = leftShift(left, LEFT_LOOR_SHIFT_table[i])
        Right = leftShift(right, LEFT_LOOR_SHIFT_table[i])
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
    for i in E_table:
        result += bits[i-1]
    return result

def XOR(bits, key):
    '''
    Input:
        bits: 48位01字符串 / 32位01比特字符串 F函数输出
        key: 48位01密钥序列 / 32位01比特字符串 Li
    Output    
        result: bits与ki异或运算得到的48位01比特字符串 / 32位01比特字符串 
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
    col = int(bits[1:5], 2)    # 取中间4位组合起来，再转成十进制
    result = bin(S_table[id-1][row*16+col])[2:]   # 获取S盒对应位置的元素
    L = len(result)
    for i in range(4-L):  # 补0
        result = "0" + result   
    return result

def S_box(bits):
    """
    Input:
        bits: 48位01比特字符串
    Output:
        result: S盒置换后的32位01比特字符串
    """
    result = ""
    for i in range(8):
        result += S(bits[i*6:(i+1)*6], i+1)
    return result

def P_box(bits):
    """
    Input:
        bits: 32位01比特字符串
    Output:
        result: P盒置换后的32位01比特字符串
    """
    result = ""
    for i in P_table:
        result += bits[i-1]
    return result

def F(bits, key_i):
    """
    Input:
        bits: 32位01比特字符串
        key_i: 48位的第i轮01比特字符串
    Output:
        result: F函数输出(32位01比特字符串)
    """
    XOR_result = XOR(Expand(bits), key_i)
    result = P_box(S_box(XOR_result))
    return result

def IP_inv_process(bits):
    """
    Input:
        bits: 经过16轮迭代的64位01字符串
    Output:
        result: 逆初始置换得到64位密文01字符串
    """
    result = ""
    for i in IP_inv_table:
        result += bits[i-1]
    return result

def Encrypt(bits, key):
    """
    Input:
        bits: 64位01比特字符串
        key: 64位01比特字符串
    Output:
        result: 使用DES加密后的64位01比特字符串
    """
    IP_bits = IP_process(bits)  # 初次置换
    left, right = IP_bits[0:32], IP_bits[32:]
    key_list = generateKey(key)
    for i in range(16):
        next_left = right
        right = XOR(left, F(right, key_list[i]))
        left = next_left
    F_result = right + left
    result = IP_inv_process(F_result)
    return result

def Decrypt(bits, key):
    """
    Input:
        bits: 分组后的64位01比特加密字符串
        key: 64位01比特密钥
    Output:
        result: 解密后的64位的01比特字符串
    """
    IP_bits = IP_process(bits)
    left, right = IP_bits[0:32], IP_bits[32:]
    key_list = generateKey(key)
    for i in range(16):
        next_left = right
        right = XOR(left, F(right, key_list[15-i]))
        left = next_left
    F_result = right + left
    result = IP_inv_process(F_result)
    return result

def DES_Encrypt(message, key):
    """
    Input:
        message: 明文字符串
        key: 密钥字符串
    Output:
        result: 加密后01比特字符串
    """
    bits = str2bit(message)
    key_bits = key2bit(key)
    divided_bits = divide(bits, 64)
    result = ""
    for i in divided_bits:
        result += Encrypt(i, key_bits)
    return result

def DES_Decrypt(message, key):
    """
    Input:
        message: 密文字符串
        key: 密钥字符串
    Output:
        result: 解密后01比特字符串
    """
    bits = str2bit(message)
    key_bits = key2bit(key)
    divided_bits = divide(bits, 64)
    result = ""
    for i in divided_bits:
        result += Decrypt(i, key_bits)
    return result

def main():
    choice = input("Please enter the number:\n1. Encrypt\n2. Decrypt\n3. Exit\n")    # 输入对应功能的编号

    while choice != "1" and choice != "2" and choice != "3":
        print("Invalid input! Please enter again:")
        choice = input()

    if choice == "1":   # DES加密
        input_file_name = input("Please enter the name of the file in plain text that you want to encrypt:")
        message = readFile(input_file_name) # 读入文件
        message = message.replace(" ","")
        print("Plaintext before encryption: " + message)
        key = input("Please enter the key:")    # 输入密钥
        encrypt_result = DES_Encrypt(message, key)  # 使用DES加密
        print("Encrypted 0/1 bits: " + encrypt_result)
        output_file_name = input_file_name[:-4] + "_encrypted.txt"
        result = bit2str(encrypt_result)
        print("Encrypted plaintext: " + result)
        writeFile(output_file_name, result) # 写入加密后的结果
    
    elif choice == "2": # DES解密
        input_file_name = input("Please enter the name of the file in cipher text that you want to decrypt:")
        message = readFile(input_file_name)
        key = input("Please enter the key:")    # 输入密钥
        print("Ciphertext: " + message)
        decrypt_result = DES_Decrypt(message, key)  # 使用DES解密
        print("Decrypted 0/1 bits: " + decrypt_result)
        result = bit2str(decrypt_result)
        print("Decrypted plaintext: " + result)
    
    else:
        print("Exit!")

if __name__ == "__main__":
    main()