from BitVector import *
def cryptBreak (ciphertextFile,key_bv):

    # This code has been with reference to the code provided in lecture 2 with respective letters mentioned along the lines

    PassPhrase = "Hopes and dreams of a million years"                          #(C)



    BLOCKSIZE = 16                                                              #(D)
    numbytes = BLOCKSIZE // 8                                                   #(E)



    # Reduce the passphrase to a bit array of size BLOCKSIZE:
    bv_iv = BitVector(bitlist = [0]*BLOCKSIZE)                                  #(F)
    for i in range(0,len(PassPhrase) // numbytes):                              #(G)
        textstr = PassPhrase[i*numbytes:(i+1)*numbytes]                         #(H)
        bv_iv ^= BitVector( textstring = textstr )                              #(I)



    # Create a bitvector from the ciphertext hex string:
    FILEIN = open(ciphertextFile)                                                  #(J)
    encrypted_bv = BitVector( hexstring = FILEIN.read() )                       #(K)




    # Create a bitvector for storing the decrypted plaintext bit array:
    msg_decrypted_bv = BitVector( size = 0 )                                    #(T)



    # Carry out differential XORing of bit blocks and decryption:

    previous_decrypted_block = bv_iv                                            #(U)
    for i in range(0, len(encrypted_bv) // BLOCKSIZE):                          #(V)
        bv = encrypted_bv[i*BLOCKSIZE:(i+1)*BLOCKSIZE]                          #(W)
        temp = bv.deep_copy()                                                   #(X)
        bv ^=  previous_decrypted_block                                         #(Y)
        previous_decrypted_block = temp                                         #(Z)
        bv ^=  key_bv                                                           #(a)
        msg_decrypted_bv += bv                                                  #(b)


    # Extract plaintext from the decrypted bitvector:    
        
    output=msg_decrypted_bv.get_text_from_bitvector()
    return output                   #(c)







































