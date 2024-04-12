from BitVector import *
import sys
class DES():


# class constructor - when creating a DES object , the
# class ’s constructor is called and the instance variables
# are initialized
# note that the constructor specifies each instance of DES
# be created with a key file (str)
    

    def __init__(self,key):


    # within the constructor , initialize instance variable
    # these could be the s-boxes , permutation boxes , and
    # other variables you think each instance of the DES
    # class would need .
    # encrypt method declaration for students to implement
    # Inputs : message_file (str), outfile (str)
    # Return : void
        


        # Opening file to read key
        file = open(key, "r")
        self.key=key
        key_string=file.read()
        file.close()



        #Key to bit vector
        key_bitvector = BitVector(textstring = key_string)

        #S boxes taken from the Lecture code!
        s_boxes = {i:None for i in range(8)}

        s_boxes[0] = [ [14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7],
                    [0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8],
                    [4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0],
                    [15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13] ]

        s_boxes[1] = [ [15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10],
                    [3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5],
                    [0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15],
                    [13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9] ]

        s_boxes[2] = [ [10,0,9,14,6,3,15,5,1,13,12,7,11,4,2,8],
                    [13,7,0,9,3,4,6,10,2,8,5,14,12,11,15,1],
                    [13,6,4,9,8,15,3,0,11,1,2,12,5,10,14,7],
                    [1,10,13,0,6,9,8,7,4,15,14,3,11,5,2,12] ]

        s_boxes[3] = [ [7,13,14,3,0,6,9,10,1,2,8,5,11,12,4,15],
                    [13,8,11,5,6,15,0,3,4,7,2,12,1,10,14,9],
                    [10,6,9,0,12,11,7,13,15,1,3,14,5,2,8,4],
                    [3,15,0,6,10,1,13,8,9,4,5,11,12,7,2,14] ]

        s_boxes[4] = [ [2,12,4,1,7,10,11,6,8,5,3,15,13,0,14,9],
                    [14,11,2,12,4,7,13,1,5,0,15,10,3,9,8,6],
                    [4,2,1,11,10,13,7,8,15,9,12,5,6,3,0,14],
                    [11,8,12,7,1,14,2,13,6,15,0,9,10,4,5,3] ]  

        s_boxes[5] = [ [12,1,10,15,9,2,6,8,0,13,3,4,14,7,5,11],
                    [10,15,4,2,7,12,9,5,6,1,13,14,0,11,3,8],
                    [9,14,15,5,2,8,12,3,7,0,4,10,1,13,11,6],
                    [4,3,2,12,9,5,15,10,11,14,1,7,6,0,8,13] ]

        s_boxes[6] = [ [4,11,2,14,15,0,8,13,3,12,9,7,5,10,6,1],
                    [13,0,11,7,4,9,1,10,14,3,5,12,2,15,8,6],
                    [1,4,11,13,12,3,7,14,10,15,6,8,0,5,9,2],
                    [6,11,13,8,1,4,10,7,9,5,0,15,14,2,3,12] ]

        s_boxes[7] = [ [13,2,8,4,6,15,11,1,10,9,3,14,5,0,12,7],
                    [1,15,13,8,10,3,7,4,12,5,6,11,0,14,9,2],
                    [7,11,4,1,9,12,14,2,0,6,10,13,15,3,5,8],
                    [2,1,14,7,4,10,8,13,15,12,9,0,3,5,6,11] ]
        
        #Key permutations and shifts for round key gen also taken from the notes

        key_permutation_1 = [56,48,40,32,24,16,8,0,57,49,41,33,25,17,
        9,1,58,50,42,34,26,18,10,2,59,51,43,35,
        62,54,46,38,30,22,14,6,61,53,45,37,29,21,
        13,5,60,52,44,36,28,20,12,4,27,19,11,3]
        
        key_permutation_2 = [13,16,10,23,0,4,2,27,14,5,20,9,22,18,11,
        3,25,7,15,6,26,19,12,1,40,51,30,36,46,
        54,29,39,50,44,32,47,43,48,38,55,33,52,
        45,41,49,35,28,31]

        pbox_permutation=[15, 6, 19 ,20 ,28, 11, 27, 16,
        0, 14, 22, 25, 4, 17, 30, 9,
        1, 7, 23, 13, 31, 26, 2 ,8,
        18 ,12 ,29, 5, 21, 10, 3 ,24]

        
        shifts_for_round_key_gen = [1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1]

        # Just to make sure it is accessible to other instances of the class 
        self.s_boxes=s_boxes
        self.pbox_permutation=pbox_permutation
        
        # following function Taken from lecture notes generate_round_keys.py

        key_bitvector = key_bitvector.permute(key_permutation_1)
        round_keys = []
        key = key_bitvector.deep_copy()
        for round_count in range(16):
            [LKey, RKey] = key.divide_into_two()
            shift = shifts_for_round_key_gen[round_count]
            LKey << shift
            RKey << shift
            key = LKey + RKey
            round_key = key.permute(key_permutation_2)
            round_keys.append(round_key)

         # Just to make sure it is accessible to other instances of the class 

        self.word=round_keys


        # Just a simple if else to implement the respective functions
        # Should it call the functions here or outside in main
        if(sys.argv[1])=='-e':
            
            self.encrypt(message_file=sys.argv[2],outfile=sys.argv[4])
        elif(sys.argv[1])=='-d':
            
            self.decrypt(encrypted_file=sys.argv[2],outfile=sys.argv[4])
        elif(sys.argv[1])=='-i':
           
            self.ppm(message_file=sys.argv[2],outfile=sys.argv[4])
       

    def encrypt (self , message_file , outfile ):
        #String or file
 
        # Get string from file
        file = open(message_file, "r")
        message_string=file.read()
        file.close()
        

        #Setting block size
        Block_size=64

        #This is for keeping the final string
        final = BitVector( size = 0 )

        #Parsing through the message through 8 bytes at a time
        for i in range(0,len(message_string),8):
            
            input_word=BitVector(textstring=message_string[i:i+8])
            
            if(len(input_word)!=64):
                #why pad from left
                input_word.pad_from_right(Block_size-len(input_word))


            [left_e, right_e] = input_word.divide_into_two()
            # Iterating through round keys
            for word in self.word:
                #print("Left and right at start",right_e.get_hex_string_from_bitvector(),left_e.get_hex_string_from_bitvector())

                #1)Expansion step for making right half to 48 bits
                E_step=BitVector(intVal=0,size = 48)
                for j in range(0,len(right_e)//4):                    
                    if j==0:
                        E_step[0]=right_e[-1]
                        E_step[1:6]=right_e[0:5]
                    elif j==7:
                        E_step[47]=right_e[0]
                        E_step[42:47]=right_e[27:32]
                    else:
                        E_step[j*6:(j*6)+6]=right_e[j*4-1:(j*4-1)+6]
                        
                    
                #2)Estep xor with the Round Key
                step_two=E_step^word
           
                # 3)This has also been taken from the lecture code illustrate_des_substitution.py
                #Basically the 8 S boxes 
                output = BitVector (size = 32)
                segments = [step_two[x*6:x*6+6] for x in range(8)]
                for sindex in range(len(segments)):
                    row = 2*segments[sindex][0] + segments[sindex][-1]
                    column = int(segments[sindex][1:-1])
                    output[sindex*4:sindex*4+4] = BitVector(intVal = self.s_boxes[sindex][row][column], size = 4)  
                
                #4)Permutation with P Box
                fourth = output.permute(self.pbox_permutation)


                #5) Finally Xor with left half
                left_e=fourth^left_e 


                
                #6) Invert fot the next step
                temp=right_e
                right_e=left_e
                left_e=temp
                               
                #print(final.get_hex_string_from_bitvector())

            #Just concatinating all ciphertext
            final=final+right_e+left_e

        hex_output=final.get_hex_string_from_bitvector()
        #Null bytes in output
        outputfile = open(outfile, 'w')                                             
        outputfile.write(hex_output)                                                    
        outputfile.close()  
                    
    def ppm(self , message_file , outfile ):
        #String or file
 
        # Get string from file
        with open(message_file, 'rb') as file:
            
            header_lines = [file.readline().decode('utf-8').strip() for _ in range(3)]
            message_string = BitVector(rawbytes=file.read())
            
        file.close()

        #Setting block size
        
        Block_size=64
        
        #This is for keeping the final string
        final = BitVector( size = 0 )

        #Parsing through the message through 8 bytes at a time
        for i in range(0,len(message_string),64):
            if(i+64>len(message_string)):
                input_word=message_string[i:len(message_string)-(i+64)]
                input_word.pad_from_right(Block_size-len(input_word))
            else:
                input_word=message_string[i:i+64]
            
            [left_e, right_e] = input_word.divide_into_two()
            # Iterating through round keys
            for word in self.word:
                #print("Left and right at start",right_e.get_hex_string_from_bitvector(),left_e.get_hex_string_from_bitvector())

                #1)Expansion step for making right half to 48 bits
                E_step=BitVector(intVal=0,size = 48)
                for j in range(0,len(right_e)//4):                    
                    if j==0:
                        E_step[0]=right_e[-1]
                        E_step[1:6]=right_e[0:5]
                    elif j==7:
                        E_step[47]=right_e[0]
                        E_step[42:47]=right_e[27:32]
                    else:
                        E_step[j*6:(j*6)+6]=right_e[j*4-1:(j*4-1)+6]
                        
                    

                #2)Estep xor with the Round Key
                step_two=E_step^word
           


                # 3)This has also been taken from the lecture code illustrate_des_substitution.py
                #Basically the 8 S boxes 
                output = BitVector (size = 32)
                segments = [step_two[x*6:x*6+6] for x in range(8)]
                for sindex in range(len(segments)):
                    row = 2*segments[sindex][0] + segments[sindex][-1]
                    column = int(segments[sindex][1:-1])
                    output[sindex*4:sindex*4+4] = BitVector(intVal = self.s_boxes[sindex][row][column], size = 4)  
                
                #4)Permutation with P Box
                fourth = output.permute(self.pbox_permutation)


                #5) Finally Xor with left half
                left_e=fourth^left_e 
                
                #6) Invert fot the next step
                temp=right_e
                right_e=left_e
                left_e=temp
                     

            #Just concatinating all ciphertext
            final=final+right_e+left_e

        final_file = open(outfile, 'wb')
        for j in header_lines:
            final_file.write(str.encode(j+ '\n'))
        final.write_to_file(final_file)
        final_file.close()
            

    def decrypt (self , encrypted_file , outfile ):

        #Same as the encrypt function, commented the changes

        file = open(encrypted_file, "r")
        message_string=file.read()
        file.close()
        
        Block_size=64
        
        final = BitVector( size = 0 )
        #16 because each hex is 4 bits and 64//4 =16
        for i in range(0,len(message_string),16):
            #Hexstring instead of texstrong
            input_word=BitVector(hexstring=message_string[i:i+16])
            
            if(len(input_word)!=64):
                
                #why pad from left
                input_word.pad_from_right(Block_size-len(input_word))

            
            [left_e, right_e] = input_word.divide_into_two()

            for word in reversed(self.word):
                E_step=BitVector(intVal=0,size = 48)

                for j in range(0,len(right_e)//4):                    
                    if j==0:
                        E_step[0]=right_e[-1]
                        E_step[1:6]=right_e[0:5]
                    elif j==7:
                        E_step[47]=right_e[0]
                        E_step[42:47]=right_e[27:32]
                    else:
                        E_step[j*6:(j*6)+6]=right_e[j*4-1:(j*4-1)+6]
                        
    
                step_two=E_step^word
               
                output = BitVector (size = 32)
                segments = [step_two[x*6:x*6+6] for x in range(8)]
                for sindex in range(len(segments)):
                    row = 2*segments[sindex][0] + segments[sindex][-1]
                    column = int(segments[sindex][1:-1])
                    output[sindex*4:sindex*4+4] = BitVector(intVal = self.s_boxes[sindex][row][column], size = 4)  
                    
                fourth = output.permute(self.pbox_permutation)
                left_e=fourth^left_e         
             
                temp=right_e
                right_e=left_e
                left_e=temp
                
              
            final=final+right_e+left_e

        text_output=final.get_text_from_bitvector()

        outputfile = open(outfile, 'w')                                              
        outputfile.write(text_output)                                                     
        outputfile.close() 
        

if __name__ == '__main__':

    if(len(sys.argv)!=5):
        print("Invalid Number of Arguments")
 
    cipher = DES(key=sys.argv[3])



