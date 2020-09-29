class Pairs:
    def __init__(self, list):
        self.list = list
    
    def equals(self, target):
        idx = []
        x1 = 0
        while x1 < len(self.list):
            x2 = 0
            while x2 < len(self.list):
                if x1 != x2 and self.list[x1] + self.list[x2] == target:
                    pair = (str(x1), str(x2))
                    reverse = (str(x2), str(x1))
                    if pair not in idx and reverse not in idx:
                        idx.append(pair)
                x2 += 1
            x1 += 1
        return idx
    
    
list = [10, 20, 10, 40, 50, 60, 70]        
target = int(input("What is your target number? "))
idx = Pairs(list).equals(target)
for pair in idx:
    print("index1=" + pair[0] + ", index2=" + pair[1])