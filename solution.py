from socket import *
import os
import sys
import struct
import time
import select
import binascii


ICMP_ECHO_REQUEST = 8
MAX_HOPS = 30
TIMEOUT = 2
TRIES = 1
# The packet that we shall send to each router along the path is the ICMP echo
# request packet, which is exactly what we had used in the ICMP ping exercise.
# We shall use the same packet that we built in the Ping exercise


def checksum(string):
# In this function we make the checksum of our packet
    csum = 0
    countTo = (len(string) // 2) * 2
    count = 0


    while count < countTo:
        thisVal = (string[count + 1]) * 256 + (string[count])
        csum += thisVal
        csum &= 0xffffffff
        count += 2


    if countTo < len(string):
        csum += (string[len(string) - 1])
        csum &= 0xffffffff


    csum = (csum >> 16) + (csum & 0xffff)
    csum = csum + (csum >> 16)
    answer = ~csum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer


def build_packet():
    #Fill in start
    # In the sendOnePing() method of the ICMP Ping exercise ,firstly the header of our
    # packet to be sent was made, secondly the checksum was appended to the header and
    # then finally the complete packet was sent to the destination.
    tempChecksum = 0
    tempID = os.getpid() & 0xFFFF

    # Make the header in a similar way to the ping exercise.
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, tempChecksum, tempID, 1)
    data = struct.pack("d", time.time())

    # Append checksum to the header.
    tempChecksum = checksum(header + data)
    if sys.platform == 'darwin':
        tempChecksum = socket.htons(tempChecksum) & 0xffff
        #Convert 16-bit integers from host to network byte order.
    else:
        tempChecksum = htons(tempChecksum)

    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, tempChecksum, tempID, 1)
    # Don’t send the packet yet , just return the final packet in this function.
    #Fill in end


    # So the function ending should look like this
    packet = header + data
    return packet


def get_route(hostname):
    timeLeft = TIMEOUT
    tracelist1 = [] #This is your list to use when iterating through each trace
    tracelist2 = [] #This is your list to contain all traces

    for numHops in range(1,MAX_HOPS):
        for tries in range(TRIES):
            nohostaddress = False
            destAddr = gethostbyname(hostname)
            tracelist1 = []
            #Fill in start
            # Make a raw socket named mySocket
            icmp = getprotobyname("icmp")
            mySocket = socket(AF_INET, SOCK_RAW, icmp)
            #Fill in end

            mySocket.setsockopt(IPPROTO_IP, IP_TTL, struct.pack('I', numHops))
            mySocket.settimeout(TIMEOUT)
            try:
                d = build_packet()
                mySocket.sendto(d, (hostname, 0))
                t= time.time()
                startedSelect = time.time()
                whatReady = select.select([mySocket], [], [], timeLeft)
                howLongInSelect = (time.time() - startedSelect)
                if whatReady[0] == []: # Timeout
                    tracelist1.append("* * * Request timed out.")
                    #Fill in start
                    #You should add the list above to your all traces list
                    tracelist2.append(tracelist1)
                    break
                    #continue
                    #Fill in end
                recvPacket, addr = mySocket.recvfrom(1024)
                timeReceived = time.time()
                #print("Num hop is " + str(numHops) + " Time let is " + str(timeLeft) + " hoelonginselect is " + str(howLongInSelect))

                timeLeft = timeLeft - howLongInSelect

                if timeLeft <= 0:
                    #print("Time let inside if" + str(timeLeft))
                    tracelist1.append("* * * Request timed out.")
                    #Fill in start
                    #You should add the list above to your all traces list
                    tracelist2.append(tracelist1)
                    break
                    #Fill in end
                #tracelist2.append(tracelist1)
            except timeout:
                continue


            else:
                #Fill in start
                #Fetch the icmp type from the IP packet
                icmpHeader = recvPacket[20:28]
                request_type, code, checksum, packetID, sequence = struct.unpack("bbHHh", icmpHeader)

                ipHeader = struct.unpack('!BBHHHBBH4s4s', recvPacket[:20])
                ttlive = ipHeader[5]
                hostIP = inet_ntoa(ipHeader[8])
                hostAddress = ""
                length = len(recvPacket) - 20

                #Fill in end
                try: #try to fetch the hostname
                    #Fill in start
                    hostAddress = gethostbyaddr(hostIP)
                    #tracelist1.append(addr[0])
                    #tracelist2.append(tracelist1)
                    #Fill in end
                except herror:   #if the host does not provide a hostname
                    #Fill in start
                    #tracelist1.append("hostname not returnable")
                    nohostaddress = True
                    #tracelist2.append(tracelist1)
                    #Fill in end


                if request_type == 11:
                    bytes = struct.calcsize("d")
                    timeSent = struct.unpack("d", recvPacket[28:28 + bytes])[0]
                    #Fill in start
                    tracelist1.append(numHops)
                    tracelist1.append(str(ttlive) + "ms")
                    tracelist1.append(hostIP)
                    if (not nohostaddress):
                         tracelist1.append(hostAddress[0])
                    else:
                        tracelist1.append("hostname not returnable")
                    #tracelist2.append(tracelist1)addr[0]
                    #print(tracelist2)
                    #print(" %d  %d   %.0fms %s %s " % (numHops, ttlive, (timeReceived - t) * 1000, addr[0], format(hostAddress)))
                    #You should add your responses to your lists here
                    #Fill in end
                elif request_type == 3:
                    bytes = struct.calcsize("d")
                    timeSent = struct.unpack("d", recvPacket[28:28 + bytes])[0]
                    #Fill in start
                    tracelist1.append(numHops)
                    tracelist1.append(str(ttlive) + "ms")
                    tracelist1.append(hostIP)
                    tracelist1.append(hostAddress[0])
                    #tracelist2.append(tracelist1)
                    #print(tracelist2)
                    #print(" %d  %d   %.0fms %s %s " % (numHops, ttlive, (timeReceived - t) * 1000, addr[0], format(hostAddress)))
                    #You should add your responses to your lists here
                    #Fill in end
                elif request_type == 0:
                    bytes = struct.calcsize("d")
                    timeSent = struct.unpack("d", recvPacket[28:28 + bytes])[0]
                    #Fill in start
                    tracelist1.append(numHops)
                    tracelist1.append(str(ttlive) + "ms")
                    tracelist1.append(hostIP)
                    tracelist1.append(hostAddress[0])
                    #tracelist2.append(tracelist1)
                    #print(tracelist2)
                    #print(" %d  %d   %.0fms %s %s " % (numHops, ttlive, (timeReceived - t) * 1000, addr[0], format(hostAddress)))
                    #exit()
                    #You should add your responses to your lists here and return your list if your destination IP is met
                    #Fill in end
                else:
                    #Fill in start
                    #If there is an exception/error to your if statements, you should append that to your list here
                    tracelist2.append(["error"])
                    #print("error")
                    #Fill in end
                break
            finally:
                #print(tracelist2)
                mySocket.close()
        tracelist2.append(tracelist1)
    return tracelist2
get_route("www.google.com")