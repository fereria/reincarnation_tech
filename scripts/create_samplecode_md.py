# -*- coding: utf-8 -*-
"""
SampleCode以下にある
"""

import codecs
import sys
import os
import os.path
import importlib
sampleDir = os.getcwd() + "/docs/65_SampleCode"

for root, dirs, files in os.walk(sampleDir):
    for file in files:

        f = os.path.join(root, file)
        d = os.path.dirname(f)

        bn, ext = os.path.splitext(file)

        if ext == ".py":
            sys.path.append(d)
            text = []
            try:
                mod = importlib.import_module(bn)
                if hasattr(mod, 'title'):
                    text += ["---",
                             "title: " + mod.title]
                else:
                    text += ["---",
                             "title: " + file]

                if hasattr(mod, 'tags'):
                    text += ['tags:']
                    for tag in mod.tags:
                        text.append(f"  - {tag}")
            except:
                pass

            if len(text) > 0:
                text += ["---", ""]

            mdFile = os.path.join(d, bn) + ".md"

            text.append('{{include("' + file + '")}}')

            with codecs.open(mdFile, 'w', 'utf-8') as f:
                f.write("\n".join(text))
