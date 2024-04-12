#A skeleton file for your AES.py has been provided below.
import sys
from BitVector import *


AES_modulus = BitVector(bitstring='100011011')
subBytesTable = [99, 124, 119, 123, 242, 107, 111, 197, 48, 1, 103, 43, 254, 215, 171, 118, 
                202, 130, 201, 125, 250, 89, 71, 240, 173, 212, 162, 175, 156, 164, 114, 192, 
                183, 253, 147, 38, 54, 63, 247, 204, 52, 165, 229, 241, 113, 216, 49, 21, 
                4, 199, 35, 195, 24, 150, 5, 154, 7, 18, 128, 226, 235, 39, 178, 117, 
                9, 131, 44, 26, 27, 110, 90, 160, 82, 59, 214, 179, 41, 227, 47, 132, 
                83, 209, 0, 237, 32, 252, 177, 91, 106, 203, 190, 57, 74, 76, 88, 207, 
                208, 239, 170, 251, 67, 77, 51, 133, 69, 249, 2, 127, 80, 60, 159, 168, 
                81, 163, 64, 143, 146, 157, 56, 245, 188, 182, 218, 33, 16, 255, 243, 210, 
                205, 12, 19, 236, 95, 151, 68, 23, 196, 167, 126, 61, 100, 93, 25, 115, 
                96, 129, 79, 220, 34, 42, 144, 136, 70, 238, 184, 20, 222, 94, 11, 219, 
                224, 50, 58, 10, 73, 6, 36, 92, 194, 211, 172, 98, 145, 149, 228, 121, 
                231, 200, 55, 109, 141, 213, 78, 169, 108, 86, 244, 234, 101, 122, 174, 8, 
                186, 120, 37, 46, 28, 166, 180, 198, 232, 221, 116, 31, 75, 189, 139, 138, 
                112, 62, 181, 102, 72, 3, 246, 14, 97, 53, 87, 185, 134, 193, 29, 158, 
                225, 248, 152, 17, 105, 217, 142, 148, 155, 30, 135, 233, 206, 85, 40, 223, 
                140, 161, 137, 13, 191, 230, 66, 104, 65, 153, 45, 15, 176, 84, 187, 22]
invSubBytesTable = [] # SBox for decryption

class AES():
# class constructor - when creating an AES object , the
# class ’s constructor is executed and instance variables
# are initialized




    def __init__(self , keyfile:str) -> None:
    # encrypt - method performs AES encryption on the plaintext and writes the ciphertext to disk
    # Inputs: plaintext (str) - filename containing plaintext
    # ciphertext (str) - filename containing ciphertext
    # Return: void
        
        # Documnetation of Bitvector
        AES_modulus = BitVector(bitstring='100011011')


        bv  =  BitVector(filename = keyfile)
        key_bv =  bv.read_bits_from_file(256)
        bv.close_file_object()
        #print(key_bv)
        self.key_bv=key_bv
        byte_sub_table = gen_subbytes_table()
        # We need 60 keywords (each keyword consists of 32 bits) in the key schedule for
        # 256 bit AES. The 256-bit AES uses the first four keywords to xor the input
        # block with. Subsequently, each of the 14 rounds uses 4 keywords from the key
        # schedule. We will store all 60 keywords in the following list:
        key_words = [None for s in range(60)]
        self.key_words=key_words
        round_constant = BitVector(intVal = 0x01, size=8)
     
        #Computer and Network Security by Avi Kak Lecture 8
        for s in range(8):
            key_words[s] = key_bv[s*32 : s*32 + 32]
        for s in range(8,60):
            if s%8 == 0:
                kwd, round_constant = gee(key_words[s-1], round_constant, byte_sub_table)
                key_words[s] = key_words[s-8] ^ kwd
            elif (s - (s//8)*8) < 4:
                key_words[s] = key_words[s-8] ^ key_words[s-1]
            elif (s - (s//8)*8) == 4:
                key_words[s] = BitVector(size = 0)
                for t in range(0,4):
                    key_words[s] += BitVector(intVal =byte_sub_table[key_words[s-1][8*t:8*t+8].intValue()], size = 8)
                key_words[s] ^= key_words[s-8]
            elif ((s - (s//8)*8) > 4) and ((s - (s//8)*8) < 8):
                key_words[s] = key_words[s-8] ^ key_words[s-1]
            else:
                sys.exit("error in key scheduling algo for s = %d" % s)


        #return key_words
        #print(len(key_words))

        #print('Init')
        

    


    def encrypt(self , plaintext:str , ciphertext:str) -> None:
    # decrypt - method performs AES decryption on the ciphertext and writes the recovered plaintext to disk
    # Inputs: ciphertext (str) - filename containing ciphertext
    # decrypted (str) - filename containing recovered plaintext
    # Return: void
       
        #print ("SBox for Encryption:")
        #print (subBytesTable)

        

        f=open(plaintext,"r")
        text=(f.read())
        text_bv = BitVector(textstring = text)
        f.close()

        cipher_final_text=BitVector(size=0)



        for parse in range(0,len(text_bv),128):
            if(parse+128>len(text_bv)):
                #print(parse,len(text_bv))
                first=text_bv[parse:len(text_bv)]
                first.pad_from_right(128-len(first))            
            else:
                first=text_bv[parse:parse+128]
            #print(len(first))
            #print("First round",first.get_bitvector_in_hex())
                

            s_array=step_one(first)
            s_array=step_two_two(s_array,self.key_words,0)
            #for s in range(0,4):
            #    for t in range(0,4):
            #        print("Second Round Done",s_array.get_bitvector_in_hex())




            for key_perms in range(1,int((len(self.key_words)-4)/4)):


                s_array=step_three_three(s_array)
                #for s in range(0,4):
                #    for t in range(0,4):
                #        print("Third Round Done",s_array.get_bitvector_in_hex())

                s_array=step_four_four(s_array)
                #for s in range(0,4):
                #    for t in range(0,4):
                #        print("Fourth Round Done",s_array.get_bitvector_in_hex())

                s_array=step_five(s_array)
                #for s in range(0,4):
                #    for t in range(0,4):
                #        print("Fifth Round Done",s_array.get_bitvector_in_hex())



                s_array=step_two_two(s_array,self.key_words,key_perms)
                #for s in range(0,4):
                #    for t in range(0,4):
                #        print("Sixth which is add again Round Done",s_array.get_bitvector_in_hex())


            s_array=step_three_three(s_array)
            #for s in range(0,4):
            #    for t in range(0,4):
            #        print("Last Sub bytes",s_array.get_bitvector_in_hex())

            s_array=step_four_four(s_array)
            #for s in range(0,4):
            #    for t in range(0,4):
            #        print("Last Shift rows",s_array.get_bitvector_in_hex())

            s_array=step_two_two(s_array,self.key_words,14)  
            #for s in range(0,4):
            #    for t in range(0,4):
            #        print("Last XOR",s_array.get_bitvector_in_hex())


            cipher_final_text=step_six_six(cipher_final_text,s_array)


            #print(cipher_final_text.get_hex_string_from_bitvector())
        cipher_final_text=cipher_final_text.get_hex_string_from_bitvector()


        f=open(ciphertext,"w")

        f.write(cipher_final_text)

        f.close()



    def encrypt_ppm(self,plaintext):
    # decrypt - method performs AES decryption on the ciphertext and writes the recovered plaintext to disk
    # Inputs: ciphertext (str) - filename containing ciphertext
    # decrypted (str) - filename containing recovered plaintext
    # Return: void
       
        #print ("SBox for Encryption:")
        #print (subBytesTable)

        text_bv = plaintext
       

        cipher_final_text=BitVector(size=0)

      

        for parse in range(0,len(text_bv),128):
            if(parse+128>len(text_bv)):
                #print(parse,len(text_bv))
                first=text_bv[parse:len(text_bv)]
                first.pad_from_right(128-len(first))            
            else:
                first=text_bv[parse:parse+128]
            #print(len(first))
            #print("First round",first.get_bitvector_in_hex())
                

            s_array=step_one(first)
            s_array=step_two_two(s_array,self.key_words,0)
            #for s in range(0,4):
            #    for t in range(0,4):
            #        print("Second Round Done",s_array.get_bitvector_in_hex())




            for key_perms in range(1,int((len(self.key_words)-4)/4)):


                s_array=step_three_three(s_array)
                #for s in range(0,4):
                #    for t in range(0,4):
                #        print("Third Round Done",s_array.get_bitvector_in_hex())

                s_array=step_four_four(s_array)
                #for s in range(0,4):
                #    for t in range(0,4):
                #        print("Fourth Round Done",s_array.get_bitvector_in_hex())

                s_array=step_five(s_array)
                #for s in range(0,4):
                #    for t in range(0,4):
                #        print("Fifth Round Done",s_array.get_bitvector_in_hex())



                s_array=step_two_two(s_array,self.key_words,key_perms)
                #for s in range(0,4):
                #    for t in range(0,4):
                #        print("Sixth which is add again Round Done",s_array.get_bitvector_in_hex())


            s_array=step_three_three(s_array)
            #for s in range(0,4):
            #    for t in range(0,4):
            #        print("Last Sub bytes",s_array.get_bitvector_in_hex())

            s_array=step_four_four(s_array)
            #for s in range(0,4):
            #    for t in range(0,4):
            #        print("Last Shift rows",s_array.get_bitvector_in_hex())

            s_array=step_two_two(s_array,self.key_words,14)  
            #for s in range(0,4):
            #    for t in range(0,4):
            #        print("Last XOR",s_array.get_bitvector_in_hex())


            cipher_final_text=step_six_six(cipher_final_text,s_array)


            #print(cipher_final_text.get_hex_string_from_bitvector())
        return cipher_final_text

        


  
        


        
      
        

    def decrypt(self , ciphertext:str , decrypted:str) -> None:
       
        #print ("\nSBox for Decryption:")
        #print (invSubBytesTable)


        f=open(ciphertext,"r")
        text=(f.read())
        text_bv = BitVector(hexstring = text)
        f.close()

        #print(text_bv)
        plain_final_text=BitVector(size=0)



        for parse in range(0,len(text_bv),128):
            if(parse+128>len(text_bv)):
                #print(parse,len(text_bv))
                first=text_bv[parse:len(text_bv)]
                first.pad_from_right(128-len(first))            
            else:
                first=text_bv[parse:parse+128]
            #print(len(first))
            #print("First round",first.get_bitvector_in_hex())
                

            s_array=step_one(first)
            s_array=step_two_two(s_array,self.key_words,14)
            #for s in range(0,4):
            #    for t in range(0,4):
            #        print("Second Round Done",s_array.get_bitvector_in_hex())




            for key_perms in range(int((len(self.key_words)-4)/4)-1,0,-1):

                s_array=inv_step_four_four(s_array)
                #for s in range(0,4):
                #    for t in range(0,4):
                #        print("Fourth Round Done",s_array.get_bitvector_in_hex())


                s_array=inv_step_three_three(s_array)
                #for s in range(0,4):
                #    for t in range(0,4):
                #        print("Third Round Done",s_array.get_bitvector_in_hex())

                s_array=step_two_two(s_array,self.key_words,key_perms)
                #for s in range(0,4):
                #    for t in range(0,4):
                #        print("Sixth which is add again Round Done",s_array.get_bitvector_in_hex())

                s_array=inv_step_five(s_array)
                #for s in range(0,4):
                #    for t in range(0,4):
                #        print("Fifth Round Done",s_array.get_bitvector_in_hex())



            s_array=inv_step_four_four(s_array)
            #for s in range(0,4):
            #    for t in range(0,4):
            #        print("Last Shift rows",s_array.get_bitvector_in_hex())


            s_array=inv_step_three_three(s_array)
            #for s in range(0,4):
            #    for t in range(0,4):
            #        print("Last Sub bytes",s_array.get_bitvector_in_hex())



            s_array=step_two_two(s_array,self.key_words,0)  
            #for s in range(0,4):
            #    for t in range(0,4):
            #        print("Last XOR",s_array.get_bitvector_in_hex())


            plain_final_text=step_six_six(plain_final_text,s_array)



            #print(cipher_final_text.get_hex_string_from_bitvector())
        plain_text=''
        #plain_text=plain_final_text.get_text_from_bitvector()
        plain_text=plain_final_text.get_bitvector_in_ascii()
        #print(plain_text)


        f=open(decrypted,"w")

        f.write(plain_text)

        f.close()





        #print('Decrypt')
        
        
        
        
        
    def ctr_aes_image(self , iv , image_file , enc_image):
       
        
        with open(image_file, 'rb') as file:
            header_lines = [file.readline().decode('utf-8').strip() for _ in range(3)]
            message_string = BitVector(rawbytes=file.read())
        file.close()        
        Block_size=128
        
        
        
        final_file = open(enc_image, 'wb')
        for j in header_lines:
            final_file.write(str.encode(j+ '\n'))     
        
        
        
        
        
        #print(len(message_string))
        for parse in range(0,len(message_string),128):
            #print(parse)
            if(parse+128>len(message_string)):
                #print(parse,len(text_bv))
                first=message_string[parse:len(message_string)]
                first.pad_from_right(128-len(first)) 
            else:
                first=message_string[parse:parse+128] 
                   
            second=self.encrypt_ppm(iv)
            third=second^first
            
            
            
            
            #final_file.write(third)
            third.write_to_file(final_file)
            next_int=int(iv)+1
            iv=BitVector(intVal=next_int,size=128)
              
        final_file.close()
        
        
    def x931(self , v0 , dt , totalNum , outfile):
        
        f=open(outfile,"w")
        
        
        Date_Time=self.encrypt_ppm(dt)
        v1=v0^Date_Time
        first_number=self.encrypt_ppm(v1)
        v1=Date_Time^first_number
        v1=self.encrypt_ppm(v1)
        f.write(str(int(first_number))+'\n')
        
        for j in range(1,totalNum):
            v1=v1^Date_Time
            first_number=self.encrypt_ppm(v1)
            v1=Date_Time^first_number
            v1=self.encrypt_ppm(v1)
            f.write(str(int(first_number))+'\n')
        
        f.close()
        
        #print('x931')

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        



def step_one(first):
    
    step_one = [[first[(x*8)+(y*32):(x+1)*8+(y*32)] for y in range(0,4)] for x in range(0,4)]
    #print("STEP ONE")
    
    #for s in range(0,4):
    #    for t in range(0,4):
    #        print(step_one[t][s].get_bitvector_in_hex())
    #
    return step_one

def step_two_two(step_one,key_words,iter):
    step_two=[[0 for s in range(0,4)] for t in range(0,4)]

    for s in range(0,4):
        for t in range(0,4):
            round_key=key_words[s+(iter*4)][t*8:(t*8)+8]
            step_two[t][s] = step_one[t][s] ^ round_key  

   
    #print("STEP TWO")
    #for s in range(0,4):
    #    for t in range(0,4):
    #        print(step_two[t][s].get_bitvector_in_hex())
            
    return step_two


def step_three_three(step_two):
    step_three=[[0 for s in range(0,4)] for t in range(0,4)]

    for s in range(0,4):
        for t in range(0,4):
            position = int(step_two[s][t])
            step_three[s][t] = BitVector(intVal=subBytesTable[position],size=8)
    #for s in range(0,4):
    #    for t in range(0,4):
    #        print(step_three[t][s].get_bitvector_in_hex())
    
    return step_three

def inv_step_three_three(step_two):
    step_three=[[0 for s in range(0,4)] for t in range(0,4)]

    for s in range(0,4):
        for t in range(0,4):
            position = int(step_two[s][t])
            step_three[s][t] = BitVector(intVal=invSubBytesTable[position],size=8)
    #for s in range(0,4):
    #    for t in range(0,4):
    #        print(step_three[t][s].get_bitvector_in_hex())
    
    return step_three



def step_four_four(step_three):
    step_four=[[0 for s in range(0,4)] for t in range(0,4)]
    for s in range(0,4):
        for t in range(0,4):
            #print("s,t=",s,t)
            new=t+s
            if new>=4:
                new=new%4
            step_four[s][t]=step_three[s][new]

    #for s in range(0,4):
    #    for t in range(0,4):
    #        print(step_four[t][s].get_bitvector_in_hex())
    return step_four



def inv_step_four_four(step_three):
    step_four=[[0 for s in range(0,4)] for t in range(0,4)]
    for s in range(0,4):
        for t in range(0,4):
            #print("s,t=",s,t)
            new=t-s
            if new<0:
                new=new%4
            step_four[s][t]=step_three[s][new]

    #for s in range(0,4):
    #    for t in range(0,4):
    #        print(step_four[t][s].get_bitvector_in_hex())
    return step_four


def step_five(step_four):
    step_five=[[BitVector(size=8) for s in range(0,4)] for t in range(0,4)]
    Shift_Columns=[['00000010','00000011','00000001','00000001'],['00000001','00000010','00000011','00000001'],['00000001','00000001','00000010','00000011'],['00000011','00000001','00000001','00000010']]
    for s in range(len(Shift_Columns)):
        for t in range(len(step_four[0])):
            for k in range(len(step_four)):
                a=BitVector(bitstring=Shift_Columns[s][k])
                step_five[s][t] ^= a.gf_multiply_modular(step_four[k][t], AES_modulus,8)
                        
    #print("STEP FIVE")            
    #for s in range(0,4):
    #    for t in range(0,4):
    #        print(step_five[t][s].get_bitvector_in_hex())
    
    return step_five
def inv_step_five(step_four):
    step_five=[[BitVector(size=8) for s in range(0,4)] for t in range(0,4)]
    Shift_Columns=[['00001110','00001011','00001101','00001001'],['00001001','00001110','00001011','00001101'],['00001101','00001001','00001110','00001011'],['00001011','00001101','00001001','00001110']]
    for s in range(len(Shift_Columns)):
        for t in range(len(step_four[0])):
            for k in range(len(step_four)):
                a=BitVector(bitstring=Shift_Columns[s][k])
                step_five[s][t] ^= a.gf_multiply_modular(step_four[k][t], AES_modulus,8)
                        
    #print("STEP FIVE")            
    #for s in range(0,4):
    #    for t in range(0,4):
    #        print(step_five[t][s].get_bitvector_in_hex())
    
    return step_five
def step_six_six(step_seven,step_five):
    for s in range(0,4):
        for t in range(0,4):
            step_seven=step_seven+step_five[t][s]
    return step_seven



def gen_subbytes_table():
    AES_modulus = BitVector(bitstring='100011011')
    subBytesTable = []
    c = BitVector(bitstring='01100011')
    for s in range(0, 256):
        a = BitVector(intVal = s, size=8).gf_MI(AES_modulus, 8) if s != 0 else BitVector(intVal=0)
        a1,a2,a3,a4 = [a.deep_copy() for x in range(0,4)]
        a ^= (a1 >> 4) ^ (a2 >> 5) ^ (a3 >> 6) ^ (a4 >> 7) ^ c
        subBytesTable.append(int(a))
    return subBytesTable



   




def gee(keyword, round_constant, byte_sub_table):
    '''
        48
        Computer and Network Security by Avi Kak Lecture 8
        This is the g() function you see in Figure 4 of Lecture 8.
    '''
    AES_modulus = BitVector(bitstring='100011011')
    rotated_word = keyword.deep_copy()
    rotated_word << 8
    newword = BitVector(size = 0)
    for s in range(0,4):
        newword += BitVector(intVal = byte_sub_table[rotated_word[8*s:8*s+8].intValue()], size = 8)
    newword[:8] ^= round_constant
    round_constant = round_constant.gf_multiply_modular(BitVector(intVal = 0x02), AES_modulus, 8)
    return newword, round_constant


def genTables():
    c = BitVector(bitstring='01100011')
    d = BitVector(bitstring='00000101')
    for s in range(0, 256):
        # For the encryption SBox
        a = BitVector(intVal = s, size=8).gf_MI(AES_modulus, 8) if s != 0 else BitVector(intVal=0)
        # For bit scrambling for the encryption SBox entries:
        a1,a2,a3,a4 = [a.deep_copy() for x in range(0,4)]
        a ^= (a1 >> 4) ^ (a2 >> 5) ^ (a3 >> 6) ^ (a4 >> 7) ^ c
        subBytesTable.append(int(a))
        # For the decryption Sbox:
        b = BitVector(intVal = s, size=8)
        # For bit scrambling for the decryption SBox entries:
        b1,b2,b3 = [b.deep_copy() for x in range(3)]
        b = (b1 >> 2) ^ (b2 >> 5) ^ (b3 >> 7) ^ d
        check = b.gf_MI(AES_modulus, 8)
        b = check if isinstance(check, BitVector) else 0
        invSubBytesTable.append(int(b))




if __name__ == "__main__":
    cipher = AES(keyfile = sys.argv[3])
    #print(sys.argv)
    if sys.argv[1] == "-e":
        cipher.encrypt(plaintext=sys.argv[2], ciphertext=sys.argv[4])
    elif sys.argv[1] == "-d":
        cipher.decrypt(ciphertext=sys.argv[2], decrypted=sys.argv[4])
        
    elif sys.argv[1] == "-i":
        cipher.ctr_aes_image(iv= BitVector(textstring="counter-mode-ctr"),image_file=sys.argv[2],enc_image=sys.argv[4])
    else:
        cipher.x931(v0=BitVector(textstring="counter-mode-ctr"), dt=BitVector(intVal=501 ,size=128), totalNum=int(sys.argv[2]), outfile=sys.argv[4])