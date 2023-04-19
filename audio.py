import pyaudio
import wave

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
RECORD_SECONDS = 2
WAVE_OUTPUT_FILENAME = "Oldboy.wav"

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("请指令......")

frames = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("接收完毕")

stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()

import base64
import urllib
import requests
import json

API_KEY = "KhILGSNrKso5Hlgrf3uvAFIg"
SECRET_KEY = "iZChK3I4IsoPw5GbHze3txlwqh3COC3q"

def main():
        
    url = "https://vop.baidu.com/server_api"
    
    # speech 可以通过 get_file_content_as_base64("C:\fakepath\Oldboy.wav",False) 方法获取
    a=get_file_content_as_base64("D:\\Uesr\\gegui\\Desktable\\录音\\Oldboy.wav",False)

    payload = json.dumps({
        "format": "pcm",
        "rate": 16000,
        "channel": 1,
        "cuid": "123",
        "token": get_access_token(),
        "speech":a,
        "len": 63532
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    response = requests.request("POST",url, headers=headers, data=payload)
    b=response.text.split(",",5)[3]
    global c
    c=b.split(":",2)[1]
    c=c.split("\"",3)[1]
    return c

def get_file_content_as_base64(path, urlencoded=False):
    """
    获取文件base64编码
    :param path: 文件路径
    :param urlencoded: 是否对结果进行urlencoded 
    :return: base64编码信息
    """
    with open(path, "rb") as f:
        content = base64.b64encode(f.read()).decode("utf8")
        if urlencoded:
            content = urllib.parse.quote_plus(content)
    return content

def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))

if __name__ == '__main__':
    main()

from modbus_tk import modbus_rtu
import serial
import modbus_tk.defines as cst
def ConnectRelay(PORT):
    """ 
    此函数为连接串口继电器模块，为初始函数，必须先调用 
    :param PORT: USB-串口端口，需要手动填写，须在计算机中手动查看对应端口 
    :return: >0 连接成功，<0 连接超时
    20  """ 
    try: 
    # c2s03 设备默认波特率 9600、偶校验、停止位 1         
        master = modbus_rtu.RtuMaster(serial.Serial(port=PORT, baudrate=9600, bytesize=8, parity='E', stopbits=1)) 
        master.set_timeout(5.0) 
        master.set_verbose(True) 
        # 读输入寄存器 
        # c2s03 设备默认 slave=2, 起始地址=0, 输入寄存器个数 2 
        master.execute(2, cst.READ_INPUT_REGISTERS, 0, 2) 
        # 读保持寄存器 
        # c2s03 设备默认 slave=2, 起始地址=0, 保持寄存器个数 1 
        master.execute(2, cst.READ_HOLDING_REGISTERS, 0, 1) # 这里可以修改需要读取的功能码 
        #  没有报错，返回 1 
        response_code = 1 
    except Exception as exc: 
        print(str(exc)) 
        # 报错，返回<0 并输出错误 
        response_code = -1 
        master = None 
    return response_code, master
""" 
 此函数为控制继电器开合函数，如果 ACTION=ON 则闭合，如果如果 ACTION=OFF 则断开。 
 :param master: 485 主机对象，由 ConnectRelay 产生 
 :param ACTION: ON 继电器闭合，开启风扇；OFF 继电器断开，关闭风扇。 
 :return: >0 操作成功，<0 操作失败
 """ 
def Switch(master, ACTION): 
    try: 
        if "on" in ACTION.lower():
            # 写单个线圈，状态常量为 0xFF00，请求线圈接通 
            # c2s03 设备默认 slave=2, 线圈地址=0, 请求线圈接通即 output_value 不等于 0
            master.execute(2, cst.WRITE_SINGLE_COIL, 0, output_value=1) 
        else: 
            # 写单个线圈，状态常量为 0x0000，请求线圈断开 
            # c2s03 设备默认 slave=2, 线圈地址=0, 请求线圈断开即 output_value 等于 0 
            master.execute(2, cst.WRITE_SINGLE_COIL, 0, output_value=0) 
            # 没有报错，返回 1 
            response_code = 1 
    except Exception as exc: 
        print(str(exc)) 
        # 报错，返回<0 并输出错误 
        response_code = -1 
        return response_code

a=ConnectRelay("COM3")

print("识别结果：")
print(c)
if c=="打开。":
    Switch(a[1],"ON")
elif c=="关闭。":
    Switch(a[1],"OFF")
else:
    print("请重新命令！")

     