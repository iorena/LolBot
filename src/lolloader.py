from loader import Loader


class LolLoader(Loader):

    def get_lols(self):
        self.lols = list(filter(lambda x: self.is_lol(x), self.lines))
        for lol in self.lols:
            print(lol)
        print(len(self.lols), "lines laughing")

    def is_lol(self, line):
        word = line[2]
        if len(word) < 1:
            return False
        # case 1: laugh at start of line
        if len(word) > 2 and word[:2] in [] ":D":
            return True
        # case 2: name of user and laugh at them
        if self.is_address(word) and len(line[3]) > 1 and line[3][:2] == ":D":
            return True
        return False

    def is_address(self, word):
        if len(word) < 3:
            return False
        name = word.replace(":", "")
        if name in self.nicks:
            return True
        return False


LolLoader().get_lols()
