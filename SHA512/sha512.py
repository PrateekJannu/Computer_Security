import sys
from BitVector import *



def sha512(input,output):
    f=open(input,'r')
    text=f.read()
    f.close()

    #print(text)
    bv=BitVector(textstring=text)

    add_1=bv+BitVector(bitstring='1')

    padd_amount=((1024-128)-(add_1.length()))%1024

    add_1.pad_from_right(padd_amount)

    add_len=add_1+BitVector(intVal=bv.length(),size=128)

    #if(add_len.length()%1024==0):
    #    print('YESSIR')


    K_given = ["428a2f98d728ae22", "7137449123ef65cd", "b5c0fbcfec4d3b2f", "e9b5dba58189dbbc", 
         "3956c25bf348b538", "59f111f1b605d019", "923f82a4af194f9b", "ab1c5ed5da6d8118",
         "d807aa98a3030242", "12835b0145706fbe", "243185be4ee4b28c", "550c7dc3d5ffb4e2",
         "72be5d74f27b896f", "80deb1fe3b1696b1", "9bdc06a725c71235", "c19bf174cf692694",
         "e49b69c19ef14ad2", "efbe4786384f25e3", "0fc19dc68b8cd5b5", "240ca1cc77ac9c65", 
         "2de92c6f592b0275", "4a7484aa6ea6e483", "5cb0a9dcbd41fbd4", "76f988da831153b5",
         "983e5152ee66dfab", "a831c66d2db43210", "b00327c898fb213f", "bf597fc7beef0ee4", 
         "c6e00bf33da88fc2", "d5a79147930aa725", "06ca6351e003826f", "142929670a0e6e70",
         "27b70a8546d22ffc", "2e1b21385c26c926", "4d2c6dfc5ac42aed", "53380d139d95b3df", 
         "650a73548baf63de", "766a0abb3c77b2a8", "81c2c92e47edaee6", "92722c851482353b",
         "a2bfe8a14cf10364", "a81a664bbc423001", "c24b8b70d0f89791", "c76c51a30654be30", 
         "d192e819d6ef5218", "d69906245565a910", "f40e35855771202a", "106aa07032bbd1b8",
         "19a4c116b8d2d0c8", "1e376c085141ab53", "2748774cdf8eeb99", "34b0bcb5e19b48a8", 
         "391c0cb3c5c95a63", "4ed8aa4ae3418acb", "5b9cca4f7763e373", "682e6ff3d6b2b8a3",
         "748f82ee5defb2fc", "78a5636f43172f60", "84c87814a1f0ab72", "8cc702081a6439ec", 
         "90befffa23631e28", "a4506cebde82bde9", "bef9a3f7b2c67915", "c67178f2e372532b",
         "ca273eceea26619c", "d186b8c721c0c207", "eada7dd6cde0eb1e", "f57d4f7fee6ed178", 
         "06f067aa72176fba", "0a637dc5a2c898a6", "113f9804bef90dae", "1b710b35131c471b",
         "28db77f523047d84", "32caab7b40c72493", "3c9ebe0a15c9bebc", "431d67c49c100d4c", 
         "4cc5d4becb3e42b6", "597f299cfc657e2a", "5fcb6fab3ad6faec", "6c44198c4a475817"]
    K_list=[]

    word_gen=[None]*80

    for k_constant in K_given:

        K_list.append(BitVector(hexstring = k_constant))

    prime_1=BitVector(hexstring='6a09e667f3bcc908')

    prime_2=BitVector(hexstring='bb67ae8584caa73b')

    prime_3=BitVector(hexstring='3c6ef372fe94f82b')

    prime_4=BitVector(hexstring='a54ff53a5f1d36f1')

    prime_5=BitVector(hexstring='510e527fade682d1')

    prime_6=BitVector(hexstring='9b05688c2b3e6c1f')

    prime_7=BitVector(hexstring='1f83d9abfb41bd6b')

    prime_8=BitVector(hexstring='5be0cd19137e2179')



    for parse in range(0,len(add_len),1024):



        first=add_len[parse:parse+1024]
        
        for break_list in range(0,1024,64):
            word_gen[int(break_list/64)]=(first[break_list:break_list+64])

        for i in range(16,80):
            new_j1=word_gen[i-2]
            new_j2=word_gen[i-15]

            s_0 = (new_j2.deep_copy() >> 1) ^ (new_j2.deep_copy() >> 8) ^ (new_j2.deep_copy().shift_right(7))

            s_1 = (new_j1.deep_copy() >> 61) ^ (new_j1.deep_copy() >> 19) ^ (new_j1.deep_copy().shift_right(6))

            word_gen[i] = BitVector(intVal=(int(word_gen[i-16]) + int(s_1) + int(word_gen[i-7]) + int(s_0)) & 0xFFFFFFFFFFFFFFFF, size=64)     

        a=prime_1
        b=prime_2
        c=prime_3
        d=prime_4
        e=prime_5
        f=prime_6
        g=prime_7
        h=prime_8

        for i in range((len(word_gen))):
                
                ch = (e & f) ^ ((~e) & g)

                maj = (a & b) ^ (a & c) ^ (b & c)

                sum_a = ((a.deep_copy()) >> 28) ^ ((a.deep_copy()) >> 34) ^ ((a.deep_copy()) >> 39)

                sum_e = ((e.deep_copy()) >> 14) ^ ((e.deep_copy()) >> 18) ^ ((e.deep_copy()) >> 41)

                t1 = BitVector(intVal=(int(h) + int(ch) + int(sum_e) + int(word_gen[i]) + int(K_list[i])) & 0xFFFFFFFFFFFFFFFF, size=64)

                t2 = BitVector(intVal=(int(sum_a) + int(maj)) & 0xFFFFFFFFFFFFFFFF, size=64)

                h = g
                g = f
                f = e

                e = BitVector(intVal=(int(d) + int(t1)) & 0xFFFFFFFFFFFFFFFF, size=64)

                d = c
                c = b
                b = a

                a = BitVector(intVal=(int(t1) + int(t2)) & 0xFFFFFFFFFFFFFFFF, size=64)        

        prime_1 = BitVector( intVal = (int(prime_1) + int(a)) & 0xFFFFFFFFFFFFFFFF, size=64 )

        prime_2 = BitVector( intVal = (int(prime_2) + int(b)) & 0xFFFFFFFFFFFFFFFF, size=64 )

        prime_3 = BitVector( intVal = (int(prime_3) + int(c)) & 0xFFFFFFFFFFFFFFFF, size=64 )

        prime_4 = BitVector( intVal = (int(prime_4) + int(d)) & 0xFFFFFFFFFFFFFFFF, size=64 )

        prime_5 = BitVector( intVal = (int(prime_5) + int(e)) & 0xFFFFFFFFFFFFFFFF, size=64 )

        prime_6 = BitVector( intVal = (int(prime_6) + int(f)) & 0xFFFFFFFFFFFFFFFF, size=64 )

        prime_7 = BitVector( intVal = (int(prime_7) + int(g)) & 0xFFFFFFFFFFFFFFFF, size=64 )

        prime_8 = BitVector( intVal = (int(prime_8) + int(h)) & 0xFFFFFFFFFFFFFFFF, size=64 )

    message_final = prime_1+prime_2+prime_3+prime_4+prime_5+prime_6+prime_7+prime_8
                    

    file_output=message_final.get_bitvector_in_hex()

    f=open(output,"w")
    f.write(file_output)
    f.close()
                    
    
       






    #print('sha-512')


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit('Wrong Command')
    else:
        sha512(sys.argv[1], sys.argv[2])