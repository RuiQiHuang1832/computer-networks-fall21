import random


class CDMA:

    def __init__(self):
        self.encoded = []

    def codesMethod(self, num_users, len_code):
        codes = []
        firstCode = self.createCode(len_code)
        codes.append(firstCode)
        for x in range(num_users):
            if x == num_users: break
            while True:
                tmp_code = self.createCode(len_code)
                orthogonal = self.is_orthogonal(tmp_code, codes)
                if not orthogonal:
                    break
            codes.append(tmp_code)
        return codes

    def encode(self, data, code):
        for bitData in data:
            for bitcode in code:
                result = self.XOR(bitData, bitcode)
                self.encoded.append(result)
        return self.encoded

    def encodeAll(self, encodedData):
        frequency = []
        for data in encodedData:
            data = self.toVolts(data)
            for x in len(data) - 1:
                frequency[x] += data[x]
        return frequency

    def decode(self, frequency, code):
        data = []
        code = self.toVolts(code)
        len_code = len(code)
        codeIndex = 0
        for volt in frequency:
            if codeIndex == len_code:
                codeIndex = 0
            result = volt * code[codeIndex]
            data.append(result)
        return data

    def XOR(self, b1, b2):
        if (b1 == 0 and b2 == 0) or (b1 == 1 and b2 == 1):
            return 0
        return 1

    def toVolts(self, bit):
        if bit == 0:
            return 1
        else:
            return -1

    def createCode(self, len_code):
        arr = []
        randomNum = random.randint(0, 1)
        for x in range(len_code):
            if x == len_code: break
            arr.append(randomNum)
        return arr

    def is_orthogonal(self, tmp_code, codes):
        sum = 0
        for i in range(1, 2):
            if sum == 0:
                return False
        return True
