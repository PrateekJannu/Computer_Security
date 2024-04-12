import sys
from PrimeGenerator import *
from BitVector import *




class RSA():
    def __init__(self , e) -> None:
        if sys.argv[1]=='-e' or sys.argv[1]=='-d':
            file1=open(sys.argv[3],'r')
            file2=open(sys.argv[4],'r')

            self.e = e
            self.p = int(file1.readline())
            self.q = int(file2.readline())
            self.totient=(self.p-1)*(self.q-1)
            self.n = self.p*self.q
            e=BitVector(intVal=self.e)
            totient=BitVector(intVal=self.totient)

            inv_e=e.multiplicative_inverse(totient)

            d=int(inv_e) % int(totient)

            self.d = d
            #print('p=',self.p,'q=',self.q,'d=',self.d)


            file1.close()
            file2.close()
        else:
            self.e = e



    def encrypt(self , plaintext:str , ciphertext:str) -> None:
       
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

    def generate(self,p_text,q_text):

        n_ge=PrimeGenerator(bits=128)
        e_bv=BitVector(intVal=self.e)
        while True:
            p=n_ge.findPrime()
            q=n_ge.findPrime()
            bv1=BitVector(intVal=p)
            bv2=BitVector(intVal=q)
            bv3=BitVector(intVal=(p-1))
            bv4=BitVector(intVal=(q-1))
            if( bv1!=bv2 and bv1[0]==1 and bv1[1]==1 and bv2[1]==1 and bv2[0]==1 and int(bv3.gcd(e_bv))==1 and int(bv4.gcd(e_bv))==1):
                file1=open(p_text,"w")
                file1.write('%d' % p)
                file1.close()
                file2=open(q_text,"w")
                file2.write('%d' % q)
                file2.close()
                break
            else:
                continue




        #print('done')




    def decrypt(self , ciphertext:str , recovered_plaintext:str)->None:
       
        f=open(ciphertext,"r")
        text=(f.read())
        text_bv = BitVector(hexstring = text)
        f.close() 
        f=open(recovered_plaintext,'w')
        X_of_p=self.q*(int(BitVector(intVal=self.q).multiplicative_inverse(BitVector(intVal=self.p))))
        X_of_q=self.p*(int(BitVector(intVal=self.p).multiplicative_inverse(BitVector(intVal=self.q))))

        for parse in range(0,len(text_bv),256):      
            if(parse+256>len(text_bv)):
                #print(parse,len(text_bv))
                first=text_bv[parse:len(text_bv)]
                first.pad_from_right(256-len(first))            
            else:
                first=text_bv[parse:parse+256]
            #print('Second step should be 256 bits=',len(first),self.d,self.n)  
            second=int(first)
            V_of_p=pow(second,self.d,self.p)
            #print('V_of_p=',V_of_p)
            V_of_q=pow(second,self.d,self.q)
            #print('V_of_q=',V_of_q)
            third=((V_of_p*X_of_p)+(V_of_q*X_of_q))%self.n
            #print('third=',third)
            fourth=BitVector(intVal=third,size=128)
            #print(fourth.get_bitvector_in_ascii())
            
            f.write(fourth.get_bitvector_in_ascii())

        f.close()


        #print('Decrypt Fn')



if __name__ == "__main__":
    cipher = RSA(e=65537)
    if sys.argv[1] == "-e":
        #print(sys.argv)
        cipher.encrypt(plaintext=sys.argv[2], ciphertext=sys.argv[5])
    elif sys.argv[1] == "-d":
        #print(sys.argv)
        cipher.decrypt(ciphertext=sys.argv[2],recovered_plaintext=sys.argv[5])
    elif sys.argv[1]=="-g":
        cipher.generate(sys.argv[2],sys.argv[3])


"""

1 python rsa.py -g p2.txt q2.txt


2 python rsa.py -e message.txt p.txt q.txt encrypted.txt
2.1 python rsa.py -e message.txt p2.txt q2.txt encrypted2.txt


3 python rsa.py -d encrypted.txt p.txt q.txt decrypted.txt
3.1 python rsa.py -d encrypted2.txt p2.txt q2.txt decrypted2.txt

"""