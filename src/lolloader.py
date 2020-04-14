from loader import Loader


class LolLoader(Loader):

    def get_lols(self):
        self.lols = list(filter(lambda x: self.get_lolness(x) > 0, self.lines))
        for lol in self.lols:
            print(lol)
        print(len(self.lols), "lines laughing")
        print(self.nicks)

    def score_lines(self):
        self.scored_lines = []
        for i in range(len(self.lines)):
            upper_bound = min(i + 11, len(self.lines))
            context = self.lines[i+1:upper_bound]
            score = self.get_lol_score(self.lines[i], context)
            self.scored_lines.append((i, score))
        self.scored_lines.sort(key=lambda x: x[1], reverse=True)

        for i in range(10):
            index = self.scored_lines[i][0]
            print(" ".join(self.lines[index]))

    def get_lol_score(self, line, context):
        total_lolness = 0.0
        for i in range(len(context)):
            line_lolness = self.get_lolness(context[i])
            if line_lolness > 0:
                # earlier lols are more likely to be addressed to the line
                total_lolness += line_lolness / (i + 1)
        return total_lolness

    """
    " Returns lolness of line.
    " 0.0 = no lol
    " 1.0 = short lol :D
    " 1.1 -> long lol :---DDDDD
    """
    def get_lolness(self, line):
        word = line[2]
        if len(word) < 1:
            return False
        # case 1: laugh at start of line
        if len(word) > 2 and (word[:2] in [":D", "xD", "XD"] or word[:2] == ":-" and word[len(word) - 1] in ["D", "d"]):
            return 1 + 0.1 * (len(word) - 1)
        # case 2: name of user and laugh at them
        if self.is_address(word) and len(line) > 3 and len(line[3]) > 1 and line[3][:2] == ":D":
            return 1 + 0.1 * (len(line[3]) - 1)
        return 0.0

    def is_address(self, word):
        if len(word) < 3:
            return False
        name = word.replace(":", "")
        if name in self.nicks:
            return True
        return False


LolLoader().score_lines()
