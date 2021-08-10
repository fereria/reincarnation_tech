# -*- coding: utf-8 -*-
"""
SampleCode以下にある
"""

import os
import os.path
sampleDir = os.getcwd() + "/docs/65_SampleCode"

for root, dirs, files in os.walk(sampleDir):
    for file in files:

        f = os.path.join(root, file)
        d = os.path.dirname(f)

        bn, ext = os.path.splitext(file)

        if ext == ".py":
            mdFile = os.path.join(d, bn) + ".md"
            text = ['{{include("' + file + '")}}']
            with open(mdFile, 'w') as f:
                f.write("\n".join(text))
