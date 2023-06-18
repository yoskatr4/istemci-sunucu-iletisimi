import socket
import subprocess as s

host = '127.0.0.1'
port = 50002

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))

server_socket.listen(1)  # Bağlantıları dinle

conn, addr = server_socket.accept()
print("Connected from: " + str(addr))

while True:
    data = conn.recv(1024).decode()
    print(data)

    result = s.run(data, stdout=s.PIPE, shell=True)
    if result.stdout.decode() != "":
        response_data = result.stdout
    
    elif data.startswith("aç"):
        dosya_adi = data[3:]
        try:
            with open(dosya_adi, 'r') as dosya:
                response_data = dosya.read().encode()
        except FileNotFoundError:
            response_data = "Dosya bulunamadı.".encode()
    elif data.startswith("çalıştır"):
        komut = data[9:]
        try:
            result = s.run(komut, stdout=s.PIPE, stderr=s.PIPE, shell=True)
            if result.returncode == 0:
                response_data = result.stdout
            else:
                response_data = result.stderr
        except Exception as e:
            response_data = str(e).encode() 
    
    else:
        response_data = "Command Error".encode()
    conn.send(response_data)

    if data == "exit":  # Eğer 'exit' mesajı alınırsa döngüden çık
        break

conn.close()
server_socket.close()
