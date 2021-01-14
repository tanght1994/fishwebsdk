import time
import socket
import struct


def get_strtime(value=0):
    """
    1.获得字符串形式的时间
    2.返字符串形式的时间，如：'2020-10-10 10:10:10'
    3.参数为与当前时间相差的秒数，为正则是返回未来时间，为负则是过去的时间
    4.get_strtime()             返回当前时间
    5.get_strtime(60*60*24)     返回明天的当前时间
    6.get_strtime(-60*60*24)    返回昨天的当前时间
    """
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() + int(value)))


def strtime2timestamp(strtime):
    """
    1.字符串时间转为时间戳
    2.传入'2020-10-10 10:10:10'返回1602295810
    """
    return int(time.mktime(time.strptime(strtime, "%Y-%m-%d %H:%M:%S")))


def timestamp2strtime(timestamp):
    """
    1.时间戳转字符串时间
    2.传入1602295810返回'2020-10-10 10:10:10'
    """
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(timestamp)))


def strip2numip(ip):
    """
    功能：字符串IP转换为数字型IP
    示例：strip2numip('0.0.0.1')返回1
    注意：socket.inet_aton有BUG，这里手动实现这个函数
    """
    try:
        tmp = ip.split('.')
        for i in tmp:
            if int(i) > 255:
                raise Exception(f'strip2numip error, ip is {ip}')
        result = 0
        result += int(tmp[0]) * 16777216
        result += int(tmp[1]) * 65536
        result += int(tmp[2]) * 256
        result += int(tmp[3])
        return result
    except Exception as e:
        raise Exception(f'strip2numip error, ip is {ip}, {str(e)}')


def numip2strip(ip):
    """
    功能：数字型IP转换为字符串IP
    示例：numip2strip(1)返回'0.0.0.1'
    """
    return socket.inet_ntoa(struct.pack("!L", ip))


def fill_ip(ip):
    """
    功能：不足三位，用0补足
    示例：传入'127.0.0.1'返回'127.000.000.001'
    """
    return '.'.join([f'{"0" * (3 - len(i))}{i}' for i in str(ip).split('.')])
