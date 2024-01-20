import numpy as np
class Parser:
    def __init__(self, answer):
        self.answer = answer+" "
        self.progress = 0
        self.separators = " ,:;?!\n\r"

    def read_word(self):
        word = ""
        end = False
        while not end:
            if self.progress >= len(self.answer):
                return None
            c = self.answer[self.progress]
            if c not in self.separators:
                word += c
            elif word:
                end = True
            self.progress += 1
        return word

    def parse_pct(self, word):
        if word is None:
            return None
        res = ""
        pct = False
        for c in word:
            if c == '%':
                pct = True
                break
            elif c.isdigit():
                res += c
        if not pct:
            return ""
        return res
    
    def crop_info(self):
        grammar = ["width", "pct", "pct", "height", "pct", "pct"]
        nums = self.grammar_nums(grammar)
        rgs = []
        for i in range(0, len(nums), 4):
            rg = [nums[j] for j in range(i, i+4)]
            rgs.append(rg)
        return rgs
    
    def grammar_nums(self, grammar):
        i = 0
        res = []
        while True:
            word = self.read_word()
            if word is None:
                break
            proceed = False
            if grammar[i] == "num":
                num = True
                for c in word:
                    if not c.isdigit() and c != '.':
                        num = False
                        break
                if num:
                    res.append(float(word))
                    proceed = True
                    
            elif grammar[i] == "pct":
                pct = self.parse_pct(word)
                if pct:
                    res.append(float(pct)/100)
                    proceed = True
            elif word.lower() == grammar[i].lower():
                proceed = True
            if proceed:
                if i == len(grammar)-1:
                    i = 0
                else:
                    i += 1
        return res
    
# pa = Parser("1. Wyoming: Number 3. South Dakota: Number 3")
# print(pa.grammar_nums(["Number", "num"]))




    
    
