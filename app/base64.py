import string

class Base64Converter():
    def __init__(self):
        #constants
        self.alphabet = string.ascii_uppercase + string.ascii_lowercase + \
           string.digits + '-_'
        self.alphaRev = dict((c, i) for (i, c) in enumerate(self.alphabet))
        self.base = len(self.alphabet)
    
    def num_encode(self, num_array):
        output = ''
        for num in num_array:
            if num < 64:
                output += 'A'
            string = []
            while True:
                num, r = divmod(num, self.base)
                string.append(self.alphabet[r])
                if num == 0: break
            output += ''.join(reversed(string))
        return output


    def num_decode(self, string):
        num_array = []
        for (char1, char2) in zip(string[0::2], string[1::2]):
            chars = char1 + char2
            num = 0
            for char in chars:
                num = num * self.base + self.alphaRev[char]
            num_array.append(num)
        return num_array