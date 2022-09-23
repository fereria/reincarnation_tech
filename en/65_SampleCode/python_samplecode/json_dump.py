# --------------------------------------------------------- #
tags = ['Python', 'Json', 'Python基本']
# --------------------------------------------------------- #

import json


class SampleVal:

    def __init__(self):

        self.val = 10
        self.foo = "var"


class Encode(json.JSONEncoder):

    def default(self, o):

        print(o)

        return json.JSONEncoder.default(self, o)


a = SampleVal()

js = json.dumps(a, cls=Encode)

js.
