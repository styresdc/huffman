##DCS
##Compresses alpha chars and '\n' to a file, with the ability to decompress later.
import heapq as heapq
import sys
import array
class Huffman:
    freq = []
    tree = []
    prefixes = dict()
    message = ""
    compressedMessage = ""
    decompressedMessage = ""

    ##Init and get our args
    def __init__(self):
        if(len(sys.argv) < 4):
            print("for compressing 'python huffman.py code example.txt huffman.dat'")
            print("for decompressing 'python huffman.py decode example.txt.huff huffman.dat'")
            exit()

        mode = sys.argv[1]
        path = sys.argv[2]
        dat = sys.argv[3]
        if(mode == "code"):
            print("Compressing... " + path)
            self.encode(path, dat)
        if(mode == "decode"):
            print("Decompressing... " + path)
            self.decode(path, dat)

    #for encoding, we read a text file, create a frequency list, generate a tree,
    #generate prefixes, and then write a compressed bitsream to file.
    def encode(self, path, dat):
        self.read(path)
        self.getFreq(dat)
        self.generateTree()
        self.prefixer(self.tree)
        self.enComp()
        self.bitWrite(path)

    #for decoding, we read our bitsream, create our frequency list, generate a tree,
    #setup our prefixes, then map the input.
    def decode(self, path, dat):
        self.bitRead(path)
        self.getFreq(dat)
        self.generateTree()
        self.prefixer(self.tree)
        self.unComp()
        print("Decoded Message: " + self.decompressedMessage)

    #reads an input ascii file
    def read(self, path):
        with open(path, 'r') as f:
            #not going to handle uppercase
            self.message = f.read().lower()
        f.close

    #read in our frequecny list
    def getFreq(self,dat):
        print("Reading Frequencies")
        #open and read file, place into a tuple structure
        with open(dat) as f:
            self.freq = f.readlines()
        self.freq = [x.strip("\n") for x in self.freq]
        for x in range(0, len(self.freq)):
            #tuple of form (frequency, char)
            self.freq[x] = (float(self.freq[x][2:]), self.freq[x][0].lower())
        #add our newline char to the list.
        self.freq.append((0.0370370,'\n'))
        f.close

    #generate a heapq type huffman tree.
    def generateTree(self):
        print("Heap Creation")
        self.tree = self.freq
        #init heap
        heapq.heapify(self.tree)
        #while we dont have a single tree
        while len(self.tree) > 1:
            #set r/l child to the roots on top of the tree, (highest frequency)
            right = heapq.heappop(self.tree)
            left = heapq.heappop(self.tree)
            #parent node = sum of its child values.
            parent = (left[0] + right[0], left, right)
            #add out new tree to the heap
            heapq.heappush(self.tree, parent)
        self.tree = self.tree[0]

    #generate prefixes for characters
    def prefixer(self, hTree, prefix = ''):
        if len(hTree) == 2:
            self.prefixes[hTree[1]] = prefix
        else:
            #recursive call, left node, right node.
            self.prefixer(hTree[1], prefix + '0')
            self.prefixer(hTree[2], prefix + '1')

    #map chars to their prefixes
    def enComp(self):
        print("Preencoded Size = " + str(len(self.message)*8))
        for c in self.message:
            self.compressedMessage += self.prefixes[c]
        print("Encoded Size = " + str(len(self.compressedMessage)))

    def unComp(self):
        current = ""
        #invert our dictionary so we can lookup chars instead of freqs.
        inverse = dict([[v,k] for k,v in self.prefixes.items()])
        #for each byte in our input
        for i in self.message:
            current += i
            #if we have that char
            if current in inverse:
                self.decompressedMessage += inverse[current]
                current = ''

    #write prefixes to bitpacked file.
    def bitWrite(self, path):
        #bitpack
        #have to make bytes 8, add zeros to compensate for shorter strings
        pad = 8-len(self.compressedMessage) % 8
        for x in range(0,pad):
            self.compressedMessage += "0"
        #info character used for decompression
        info = "{0:08b}".format(pad)
        self.compressedMessage = info + self.compressedMessage
        #store data in byte array
        b = bytearray()
        #f/e in compressedMessage convert to byte and store
        for x in range(0, len(self.compressedMessage), 8):
            byte = self.compressedMessage[x:x+8]
            b.append(int(byte,2))
        #write bytes to file
        with open(path+".huff", 'wb') as f:
            f.write(bytes(b))
        f.close()

    #reads an input bitpacked file
    def bitRead(self, path):
        #open file
        with open(path, 'rb') as f:
            #string accumulator
            bit_s = ""
            #read a byte
            byte = f.read(1)
            #while we still have bits in this byte
            while(len(byte) > 0):
                #convert to ascii
                byte = ord(byte)
                bits = bin(byte)[2:].rjust(8, '0')
                #append converted bit
                bit_s += bits
                #read next byte
                byte = f.read(1)
        #check for padding and remove.
        pad = bit_s[:8]
        pad = int(pad, 2)
        bit_s = bit_s[8:]
        self.message = bit_s[:-1*pad]



Huffman()
