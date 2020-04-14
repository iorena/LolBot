from nicks import nicks

import re


class Loader():

    def __init__(self):
        data = []
        self.nicks = list(dict.fromkeys(nicks))

        with open("../data/2012-12-13_to_2014-02-01") as infile:
            data += infile.readlines()
        with open("../data/2014-04-10_to_2016-06-15") as infile:
            data += infile.readlines()
        with open("../data/2016-08-17_to_2018-02-12") as infile:
            data += infile.readlines()

        print("Loaded", len(data), "rows of data")

        self.data = list(map(lambda x: x.split(" "), data))

        # print(self.data[5])
        # print("".join(self.data[5][3:5]))

        topics = list(filter(lambda x: len(x) > 6 and " ".join(x[3:6]) == "changed the topic", self.data))
        self.topics = list(map(lambda x: " ".join(x[9:]), topics))
        # print(self.topics)

        # keep only lines by users (no join messages, etc.)
        self.lines = list(filter(lambda x: len(x[0]) == 5 and self.is_nick(x[1]), self.data))
        # filter out \n
        self.lines = list(map(lambda x: " ".join(x).replace("\n", "").split(" "), self.lines))

        # standardize nicknames
        self.lines = list(map(lambda x: [x[0], self.find_nick(x[1])] + x[2:], self.lines))

        print("Filtered, left with", len(self.lines), "rows of text")


    def is_nick(self, string):
        if len(string) > 3 and string[0] == "<" and string[len(string) - 1] == ">":
            return True
        return False

    def find_nick(self, nick):
        nick = re.sub(r"[<> @+]", "", nick)
        for nickname in nicks:
            if nick in nicks[nickname]:
                return nickname
        return "UNKNOWN"
