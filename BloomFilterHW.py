from BitHash import BitHash
from BitVector import BitVector



class BloomFilter(object):
    
    #Function that returns the number of bits needed in the Bloom Filter for 
    #given conditions of number of keys, num of hashes, and desired 
    #false posotive rate 
    def __bitsNeeded(self, numKeys, numHashes, maxFalsePositive):
        
        #math to determine proportion of zero bits in the Bit Vector  
        zeroFrac = (1 - (maxFalsePositive**(1/numHashes))) 
        
        #using that value to determine how many bits are needed in the Bloom Filter 
        #to get the wanted results
        numBitsNeeded = numHashes/(1-(zeroFrac**((1/numKeys))))
        
        #turn that value into an integer so that it can be properly 
        #used, and add 1 because integer division disregards remainder 
        return int(numBitsNeeded)+1
    
    
    # Create a Bloom Filter that will store numKeys keys, using 
    # numHashes hash functions, and that will have a false positive 
    # rate of maxFalsePositive.
    def __init__(self, numKeys, numHashes, maxFalsePositive):
        
        #attributes 
        self.__numKeys = numKeys 
        self.__numHashes = numHashes 
        self.__maxFalsePositive = maxFalsePositive
        
        #bit vector size - use the bitsNeeded method to calculate
        #the needed size of the bit vector 
        self.__size = self.__bitsNeeded(numKeys, numHashes, maxFalsePositive)   
        
        #initialize bit vector with the proper amount of bits 
        self.__bitList = BitVector(size = self.__size)
        
        #track of how many bits have been set to 1- updated in insert 
        #used for num bits set and false pos rate 
        self.__setCount = 0 
        
        
        
        
    # insert the specified key into the Bloom Filter.
    # Doesn't return anything, since an insert into 
    # a Bloom Filter always succeeds!
    def insert(self, key):
        
        #for however many times you want to hash 
        for i in range(self.__numHashes): 
            
            #hash they key with the curret hash function
            hashVal = BitHash(s=key, hashFuncNum=i+1) % self.__size
            
            #if there is a 0 at that position 
            #set that pos to 1, add 1 to the count of bits set to 1 
            if self.__bitList[hashVal] ==0: 
                self.__bitList[hashVal] =1 
                self.__setCount += 1 
        
    
    
    # Returns True if key MAY have been inserted into the Bloom filter. 
    # Returns False if key definitely hasn't been inserted into the BF.
    def find(self, key):
        
        #find hashval 
        for i in range(self.__numHashes): 
            hashVal = BitHash(s=key, hashFuncNum=i+1) % self.__size 
            
            #if you reach a 0 at that pos, you know for sure the key 
            #was not inserted 
            if self.__bitList[hashVal] ==0: 
                return False 
        
        #reached here, means likely that the key was inserted 
        return True 
            
        
       
    # Returns the PROJECTED current false positive rate based on the
    # ACTUAL current number of bits actually set in this Bloom Filter. 
    def falsePositiveRate(self):
        
        totalBits =self.__size   
        
        #porporion of bits that are still zero 
        curPhi = (totalBits - self.__setCount) / totalBits 
        
        #get false pos rate with the cur phi value 
        curFPR= (1-curPhi)**(self.__numHashes) 
        
        return curFPR 
       
    # Returns the current number of bits ACTUALLY set in this Bloom Filter
    def numBitsSet(self):
        return self.__setCount      


       

def __main():
    numKeys = 100000
    numHashes = 4
    maxFalse = .05
    
    # create the Bloom Filter
    b= BloomFilter(numKeys, numHashes, maxFalse) 
    
    # read the first numKeys words from the file and insert them 
    # into the Bloom Filter. Close the input file.
    fin = open("wordlist.txt") 
    for i in range(numKeys): 
        
        #read word 
        word = fin.readline()
        
        #add word into bloom filter 
        b.insert(word)
        
    fin.close()
    
    # Print out what the PROJECTED false positive rate should 
    # THEORETICALLY be based on the number of bits that ACTUALLY ended up being set
    # in the Bloom Filter. Use the falsePositiveRate method.    
    pFPR = b.falsePositiveRate() 
    
    print("The projected false positivity rate is " + str(pFPR) + " which is " + str(pFPR*100) + "%")

   
    # Now re-open the file, and re-read the same bunch of the first numKeys 
    # words from the file and count how many are missing from the Bloom Filter, 
    # printing out how many are missing. This should report that 0 words are 
    # missing from the Bloom Filter.
    fin = open("wordlist.txt") 
    
    missingCount = 0 
    
    for i in range(numKeys): 
        word = fin.readline()
        
        #if find method returns false, add 1 to count, this should never happen
        #bc all of these words were already inserted into the bloom filter 
        if not b.find(word): 
            missingCount += 1 
            
    print("There are " + str(missingCount) + " words missing")
        


    # Now read the next numKeys words from the file, none of which 
    # have been inserted into the Bloom Filter, and count how many of the 
    # words can be (falsely) found in the Bloom Filter.
    FalseCount = 0 
    
    for i in range(numKeys): 
        word = fin.readline() 
        
        #if find returns true, meaning that all the values it hashed to were 1
        #even though this particular word was never inserted, add 1 to false count 
        if b.find(word): 
            FalseCount +=1 
            
    fin.close()
    
    # Print out the percentage rate of false positives.
    # THIS NUMBER MUST BE CLOSE TO THE ESTIMATED FALSE POSITIVE RATE ABOVE    
    percent = (FalseCount/numKeys) * 100 
            
    print("The actual false positivity rate is " + str(percent) + "%") 
    
            


    
if __name__ == '__main__':
    __main()       

