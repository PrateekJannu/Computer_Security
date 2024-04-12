import sys
from PrimeGenerator import *
from BitVector import *
from solve_pRoot import *


class breakRSA():
    def __init__(self , e) -> None:
        if sys.argv[1]=='-e' or sys.argv[1]=='-d':
            #file1=open(sys.argv[3],'r')
            #file2=open(sys.argv[4],'r')


            self.e = e
            #self.p = int(file1.readline())
            #self.q = int(file2.readline())
            #self.totient=(self.p-1)*(self.q-1)
            #self.n = self.p*self.q
            #e=BitVector(intVal=self.e)
            #totient=BitVector(intVal=self.totient)
#
            #inv_e=e.multiplicative_inverse(totient)
#
            #d=int(inv_e) % int(totient)
#
            #self.d = d
            #print('p=',self.p,'q=',self.q,'d=',self.d)


            #file1.close()
            #file2.close()
        else:
            self.e = e




    def encrypt(self , plaintext:str , ciphertext:str,n:int) -> None:
        self.n=n
        f=open(plaintext,"r")
        text=(f.read())
        text_bv = BitVector(textstring = text)
        f.close() 
        f=open(ciphertext,'w')

        for parse in range(0,len(text_bv),128):      
            if(parse+128>len(text_bv)):
                #print(parse,len(text_bv))
                first=text_bv[parse:len(text_bv)]
                first.pad_from_right(128-len(first))            
            else:
                first=text_bv[parse:parse+128]

            #print(first)
                
            first.pad_from_left(128) 

            #print('Second step should be 256 bits=',len(first))  

            third=(int(first)**self.e)%self.n

            fourth=BitVector(intVal=third,size=256)

            f.write(fourth.get_bitvector_in_hex())

        f.close()


        #print('Encrypt fn')


    def break_rsa(self,enc1:str,enc2:str,enc3:str,n1_n2_n3:str,output:str)->None:
        crypt_strings=[]
        n_123=[]

        f=open(enc1,'r')
        string_read=f.read()
        text_bv1 = BitVector(hexstring = string_read)
        f.close()


        f=open(enc2,'r')
        string_read=f.read()
        text_bv2 = BitVector(hexstring = string_read)
        f.close()


        f=open(enc3,'r')
        string_read=f.read()
        text_bv3 = BitVector(hexstring = string_read)
        f.close()


        f=open(n1_n2_n3,'r')
        n_123=f.readlines()
        f.close()
        
        n_123=[int(n_123[0]),int(n_123[1]),int(n_123[2])]
        #print(n_123)
        n_combined=n_123[0]*n_123[1]*n_123[2]
        #print(n_combined)
    
        CRT_step_two=[0,0,0]
        CRT_step_one=[n_123[1]*n_123[2],n_123[0]*n_123[2],n_123[1]*n_123[0]]
        for i in range(len(CRT_step_one)):
            temp=BitVector(intVal=CRT_step_one[i])
        #for j in range(len(CRT_step_one)): 
            CRT_step_two[i]=int(temp.multiplicative_inverse(BitVector(intVal=n_123[i])))
            #print(CRT_step_two[i])

        f=open(output,"w")
        #print(CRT_step_two)
        for parse in range(0,len(text_bv1),256):      
            if(parse+256>len(text_bv1)):
                #print(parse,len(text_bv))
                first_1=text_bv1[parse:len(text_bv1)]
                first_1.pad_from_right(256-len(first_1))  


                first_2=text_bv2[parse:len(text_bv2)]
                first_2.pad_from_right(256-len(first_2))    

                first_3=text_bv3[parse:len(text_bv3)]
                first_3.pad_from_right(256-len(first_3))         
            else:
                first_1=text_bv1[parse:parse+256]
                first_2=text_bv2[parse:parse+256] 
                first_3=text_bv3[parse:parse+256]  
                CRT_step_three=[int(first_1),int(first_2),int(first_3)]
                M_cubed=0
                for j in range(len(n_123)):
                    #print(M_cubed)
                    M_cubed=M_cubed+(CRT_step_three[j]*int(CRT_step_one[j])*int(CRT_step_two[j]))

                M_cubed=M_cubed % n_combined    

                M_final=solve_pRoot(3,M_cubed)
        

                final_step=BitVector(intVal=M_final,size=128)
                #print(final_step.get_bitvector_in_ascii())
                f.write(final_step.get_bitvector_in_ascii())
        #print('broken')





def generate():
    n_ge=PrimeGenerator(bits=128)
    e_bv=BitVector(intVal=3)
    while True:
        p=n_ge.findPrime()
        q=n_ge.findPrime()
        bv1=BitVector(intVal=p)
        bv2=BitVector(intVal=q)
        bv3=BitVector(intVal=(p-1))
        bv4=BitVector(intVal=(q-1))
        if( bv1!=bv2 and bv1[0]==1 and bv1[1]==1 and bv2[1]==1 and bv2[0]==1 and int(bv3.gcd(e_bv))==1 and int(bv4.gcd(e_bv))==1):
            n=p*q
            #file1=open(p_text,"w")
            #file1.write('%d' % p)
            #file1.close()
            #file2=open(q_text,"w")
            #file2.write('%d' % q)
            #file2.close()
            return p,q,n
            break
        else:
            continue



        #print('done')




if __name__ == "__main__":
    cipher = breakRSA(e=3)
    if sys.argv[1] == "-e":
        pub_keys=[]
        priv_keys=[]
        n_s=[]
        f=open(sys.argv[6],"w")
        for i in range(0,3):
            pub,private,ne=generate()
            pub_keys.append(pub)
            priv_keys.append(private)
            n_s.append(ne)
            cipher.encrypt(plaintext=sys.argv[2], ciphertext=sys.argv[i+3],n=ne)
            #print('\n Public Key=',pub)
            #print('\n Private keys=',private)
            f.write(str(ne)+'\n')
        f.close()
    elif sys.argv[1]== "-c":
        cipher.break_rsa(sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5],sys.argv[6])



#1 python breakRSA.py -g p3.txt q3.txt
#2 python breakRSA.py -g p4.txt q4.txt
#3 python breakRSA.py -g p5.txt q5.txt


# python breakRSA.py -e message.txt enc1.txt enc2.txt enc3.txt n_1_2_3.txt


# python breakRSA.py -c enc1.txt enc2.txt enc3.txt n_1_2_3.txt cracked.txt







