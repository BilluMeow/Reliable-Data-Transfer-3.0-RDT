
import socket


class sender:

    def __init__(self, port):
        self.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.socket.bind(('127.0.0.1', port))
        self.last_seq = 1
        

    def get_checksum_and_data(self, data, bad=False):
        data = bytearray(data, 'utf-8')
        data_len = len(data)
        checksum = 0
        for b in data:
            checksum = checksum | b

        if bad:
            checksum = 7

        return checksum.to_bytes(1, 'big') + data

    def get_payload(self, data, bad=False):
        return self.last_seq.to_bytes(2, 'big') + self.get_checksum_and_data(data, bad=bad)

    def connect(self, ip, port):
        self.target_addr = (ip, port)

        self.send_wait("Chalo Hoja Start")
        print("Connection established with : " + str(self.target_addr))

    def send(self, msg, bad=False):
        self.send_wait(msg, bad=bad)

    def send_wait(self, data, bad=False):
        data_len = len(data.encode())
        data = self.get_payload(data, bad=bad)
        
        flag = True
        self.socket.settimeout(1)
        i = 0
        while flag and i<5:
            i = i + 1
            self.socket.sendto(data, self.target_addr)
            try:
                ack = self.socket.recv(1024)
                try:
                    if int(ack.decode()) == self.last_seq + data_len:
                        flag = False
                    else:
                        print("Wrong Acked : Resending")
                except:
                    print("Wrong Acked : Resending")
            except:
                print("Time Out : Resending")
                pass
            
        if i>4 and not bad:
            raise Exception("Connection Time out, Client not Responding")
        if not bad:
            self.last_seq = self.last_seq + data_len
            
        self.socket.settimeout(50)

    def close(self):
        self.send("Chal Beta Agla Laga")
        self.socket.close()
        


myrdt = sender(12346)
myrdt.connect('127.0.0.1', 12345)

myrdt.send("Dick", bad=True)


while True:
    msg = input("Enter Message to Send :")
    if msg == "Exit":
        myrdt.close()
        break
    else:
        myrdt.send(msg)
    




