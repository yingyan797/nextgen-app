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

    def parse_pct(self):
        word = self.read_word()
        if word is None:
            return None
        res = ""
        pct = False
        for c in word:
            if c == '%':
                pct = True
                break
            res += c
        if not pct:
            return ""
        print(res)
        return res
    
    def crop_info(self):
        pct_ranges = []
        rg = np.zeros(4)
        i = 0
        while True:
            pct = self.parse_pct()
            if pct is None:
                break
            if pct == "":
                continue
            if i == 4:
                pct_ranges.append(rg)
                rg = np.zeros(4)
                i = 0
            rg[i] = float(pct)/100
            i += 1
        if i == 4:
            pct_ranges.append(rg)
        return pct_ranges
    
# pa = Parser("? heio 12%, kk 45 29% 5% 4.3% 90 7.55% is ok")
# print(pa.crop_info())



    
    
