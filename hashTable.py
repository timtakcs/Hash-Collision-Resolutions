import time
import string
import random
from random import shuffle

class Table(object):
    def __init__(self):
        self.maxLength = 256
        self.loadFactor = 0.75
        self.length = 0
        self.table = [None] * self.maxLength

    def hashFunc(self, key, message):
        return self.hash1(key, message) % self.maxLength

    def hash1(self, message, table):
        hashKey = len(message) % 256
        for i in message:
            hashKey = table[hashKey^ord(i)]
        return hashKey

    def len(self):
        return self.length

    def storeItem(self, key, item):
        startTime = time.time()
        self.length += 1
        hash = self.hashFunc(key, item)
        while self.table[hash] is not None:
            if self.table[hash][0] == key:
                print("collision, key already exists")
                # collisions += 1
                self.length -= 1
            hash = self.increment(hash)
        record = (key, item)
        self.table[hash] = record
        endTime = time.time()
        return startTime - endTime

    def search(self, key, message):
        startTime = time.time()
        hash = self.hashFunc(key, message)
        if self.table[hash] is None:
            print("record doesn't exist")
        if self.table[hash][0] != key:
            while self.table[hash][0] != key:
                hash = self.increment(hash)
                if self.table[hash] is None:
                    print("record wasn't added correctly")
        endTime = time.time()
        timeTaken = endTime - startTime
        return hash, timeTaken

    def increment(self, key):
        return (key + 1) % self.maxLength

    def getItem(self, key):
        index = self.search(key)
        return self.table[index][1]
    
    def removeItem(self, key):
        index = self.search(key)
        self.table[index] = None

    def resize(self):
        self.maxLength *= 2
        self.length = 0
        table = self.table
        self.table = [None] * self.maxLength
        for keyItem in table:
            if keyItem is not None:
                self[keyItem[0]] = keyItem[1]

def main():
    items = []

    hashTable = Table()

    dataTable = list(range(0,1024))
    shuffle(dataTable)

    def stringCreator(size=10, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    for i in range(0, 1000):
        stringToAdd = stringCreator()
        items.append(stringToAdd)

    addTime = 0

    for i in range(0, len(items)):
        key = hashTable.hash1(items[i], dataTable)
        time = hashTable.storeItem(key, items[i])
        addTime += time

    print(hashTable.table)
    print(addTime)

if __name__ == "__main__":
    main()
    

