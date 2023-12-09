import os

from lxml.builder import unicode


class DFAFilter():
    def __init__(self):
        self.keyword_chains = {}
        self.delimit = '\x00'

    def add(self, keyword):
        if not isinstance(keyword, unicode):
            keyword = keyword.decode('utf-8')
        keyword = keyword.lower()
        chars = keyword.strip()
        if not chars:
            return
        level = self.keyword_chains
        for i in range(len(chars)):
            if chars[i] in level:
                level = level[chars[i]]
            else:
                if not isinstance(level, dict):
                    break
                for j in range(i, len(chars)):
                    level[chars[j]] = {}
                    last_level, last_char = level, chars[j]
                    level = level[chars[j]]
                last_level[last_char] = {self.delimit: 0}
                break
        if i == len(chars) - 1:
            level[self.delimit] = 0

    def parse(self, path):
        with open(path) as f:
            for keyword in f:
                self.add(keyword.strip())

    def filter(self, message, repl="*"):
        if not isinstance(message, unicode):
            message = message.decode('utf-8')
        message = message.lower()
        ret = []
        blur = []
        stepp = ""
        start = 0
        while start < len(message):
            level = self.keyword_chains
            step_ins = 0
            for char in message[start:]:
                if char in level:
                    stepp = stepp + char
                    step_ins += 1
                    if self.delimit not in level[char]:
                        level = level[char]
                    else:
                        blur.append(stepp)
                        stepp = ""
                        ret.append(repl * step_ins)
                        start += step_ins - 1
                        break
                else:
                    stepp = ""
                    ret.append(message[start])
                    break
            else:
                ret.append(message[start])
            start += 1

        # print("".join(ret))
        # print(message)
        if message == "".join(ret):
            return [True, []]
        # ''.join(ret)
        return [False, blur]


gfw = DFAFilter()
basedir = os.path.abspath(os.path.dirname(__file__))
gfw.parse(os.path.join(basedir, "negative-words.txt"))


def local_negative_word_detector(input_sentence):
    input_sentence = input_sentence.replace("hello", "")
    global gfw
    return gfw.filter(input_sentence, "*")


if __name__ == "__main__":
    # gfw = NaiveFilter()
    # gfw = BSFilter()
    gfw = DFAFilter()
    gfw.parse("negative-words.txt")
    import time

    t = time.time()
    print(gfw.filter("sdkjfkldsjfkld 123sask kd haks fuck", "*"))
    print((time.time() - t) * 1000)
