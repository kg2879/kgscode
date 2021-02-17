
from socket import *

def smtp_client(port=1025, mailserver='127.0.0.1'):
    msg = "\r\n My message kg2879"
    endmsg = "\r\n.\r\n"

    # Choose a mail server (e.g. Google mail server) if you want to verify the script beyond GradeScope

    # Create socket called clientSocket and establish a TCP connection with mailserver and port

    # Fill in start
    mailserverAndPort = (mailserver, port)
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect(mailserverAndPort)
    # Fill in end

    recv = clientSocket.recv(1024).decode()
    #print(recv)
    #if recv[:3] != '220':
        #print('220 reply not received from server Test1.')

    # Send HELO command and print server response.
    heloCommand = 'HELO Alice\r\n'
    clientSocket.send(heloCommand.encode())
    recv1 = clientSocket.recv(1024).decode()
    #print(recv1)
    #if recv1[:3] != '250':
        #print('250 reply not received from server Test2.')

    # Send MAIL FROM command and print server response.
    # Fill in start
    fromMail = "MAIL FROM: <kg2879@nyu.edu> \r\n"
    clientSocket.send(fromMail.encode())
    recv2 = clientSocket.recv(1024).decode()
    #print("MAIL FROM : " + recv2)
    #if recv2[:3] != '250':
        #print('250 reply not received from server Test3.')
    # Fill in end

    # Send RCPT TO command and print server response.
    # Fill in start
    toMail = "RCPT TO: <kg2879@nyu.edu> \r\n"
    clientSocket.send(toMail.encode())
    recv3 = clientSocket.recv(1024).decode()
    #print("RCPT TO : " + recv3)
    #if recv3[:3] != '250':
        #print('250 reply not received from server Test4.')
    # Fill in end

    # Send DATA command and print server response.
    # Fill in start
    dataCmd = "DATA\r\n"
    clientSocket.send(dataCmd.encode())
    recv4 = clientSocket.recv(1024).decode()
    #print("After DATA command: " + recv4)
    #if recv4[:3] != '354':
        #print('354 reply not received from server Test5.')
    # Fill in end

    # Send message data.
    # Fill in start
    subject = "Subject: SMTP Mail Programming Lab 3 \r\n\r\n"
    clientSocket.send(subject.encode())
    clientSocket.send(msg.encode())
    # Fill in end

    # Message ends with a single period.
    # Fill in start
    clientSocket.send(endmsg.encode())
    recv5 = clientSocket.recv(1024).decode()
    #print("Response after sending message body:" + recv5)
    #if recv5[:3] != '250':
        #print('250 reply not received from server Test6.')
    # Fill in end

    # Send QUIT command and get server response.
    # Fill in start
    quitMail = "QUIT\r\n"
    clientSocket.send(quitMail.encode())
    recv6 = clientSocket.recv(1024).decode()
    #print(recv6)
    clientSocket.close()
    # Fill in end


if __name__ == '__main__':
    smtp_client(1025, '127.0.0.1')