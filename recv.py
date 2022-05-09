import socket


class receiver:

    def __init__(self, port):
        self.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.socket.settimeout(50)
        self.socket.bind(('127.0.0.1', port))
        self.last_seq = 1

    def recv_msg(self):
        i = 0
        flag = True
        while flag and i<5:
            msg, addr = self.socket.recvfrom(1024)
            if self.check_msg(msg) and addr == self.target_addr:
                 self.last_seq = self.last_seq + len(msg[3:])
                 print("Message Received: ", end="")
                 flag = False
            else:
                print("Curropt Message Received : Asking for resend")
                   
            self.socket.sendto(str(self.last_seq).encode(), addr)
            i = i + 1
            
        if flag:
            return ""

        if msg[3:].decode('utf-8') == "Chal Beta Agla Laga":
            self.close()
            raise Exception("Connection Closed From the Sender")

        return msg[3:].decode('utf-8')
            

    def check_msg(self, data):
        check = 0
        for byte in data[3:]:
            check = check | byte
        if check == data[2]:
            return True
        return False
            

    def recv(self):
        return self.recv_msg()

    def listen(self):
        msg, addr = self.socket.recvfrom(1024)
        if self.check_msg(msg):
             self.last_seq = self.last_seq + len(msg[3:])
             self.target_addr = addr
             print("Connection Established With : " + str(addr))
        self.socket.sendto(str(self.last_seq).encode(), addr)

    def close(self):
        self.socket.close()
        
    



shit = receiver(12345)
shit.listen()

while True:
    print(shit.recv())


