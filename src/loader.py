from nicks import nicks

import re


class Loader():

    def __init__(self):
        data = []
        self.nicks = list(dict.fromkeys(nicks))

        with open("../data/logs1.txt") as infile:
            data += infile.readlines()
        with open("../data/logs2.txt") as infile:
            data += infile.readlines()
        with open("../data/logs3.txt") as infile:
            data += infile.readlines()

        print("Loaded", len(data), "rows of data")

        self.data = list(map(lambda x: self.split_line(x), data))

        # collect topic changes
        topics = list(filter(lambda x: len(x) > 6 and " ".join(x[3:6]) == "changed the topic", self.data))
        self.topics = list(map(lambda x: " ".join(x[9:]), topics))
        # print(self.topics)

        self.lines = list(map(lambda x: self.format_nicks(x), self.data))

        print(self.lines[456], self.lines[1006345], self.lines[2000000])

        # keep only lines by users (no join messages, etc.)
        self.lines = list(filter(lambda x: len(x[0]) in [9, 10] and self.is_nick(x[2]), self.lines))

        # standardize nicknames
        self.lines = list(map(lambda x: self.standardize_nicks(x), self.lines))

        print("Filtered, left with", len(self.lines), "rows of text")
        print(self.lines[456], self.lines[1006345], self.lines[2000000])

    def split_line(self, line):
        words = []
        for space_split in line.split(" "):
            for tab_split in space_split.split("\t"):
                if len(tab_split) > 0:
                    words.append(tab_split.replace("\n", ""))
        return words

    def format_nicks(self, line):
        if len(line) < 3:
            return line
        new_line = [line[0], line[1]]
        if line[2] == "<":
            nick = re.sub(r"[<>@+]", "", line[3])
            new_line.append(nick)
            new_line += line[4:]
        else:
            nick = re.sub(r"[<>@+]", "", line[2])
            new_line.append(nick)
            new_line += line[3:]
        return new_line

    def standardize_nicks(self, line):
        if len(line) < 5:
            return line
        return [line[0], line[1], self.find_nick(line[2])] + line[3:]

    def is_nick(self, string):
        if len(string) > 1:
            return True
        return False

    def find_nick(self, nick):
        for nickname in nicks:
            if nick in nicks[nickname]:
                return nickname
        return "UNKNOWN"
