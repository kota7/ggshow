#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import os
from tempfile import TemporaryDirectory
import numpy as np
import pandas as pd
from ggshow import ggwrite


class TestGGWrite(unittest.TestCase):
    def test_qplot(self):
        with TemporaryDirectory() as dirname:
            targetfile = os.path.join(dirname, "test.png")
            ggwrite("""
              x <- c(1,2,3)
              y <- c(4,5,6)
              qplot(x, y, geom="line")
            """, targetfile, savesize=(3, 2))
            self.assertTrue(os.path.isfile(targetfile))

    def test_pandas(self):
        x = np.linspace(-20, 20, 500)
        y = np.sin(x)
        y2 = 0.4*np.cos(x)

        df1 = pd.DataFrame({"x":x, "y":y})
        df2 = pd.DataFrame({"x":x, "y":y2})
        with TemporaryDirectory() as dirname:
            targetfile = os.path.join(dirname, "test.png")
            ggwrite("""
              ggplot(a, aes(x, y)) + 
                geom_line(color="blue") +
                geom_line(data=b, linetype="dashed", color="red") +
                theme_bw()
            """, targetfile, savesize=(4, 2), a=df1, b=df2)
            self.assertTrue(os.path.isfile(targetfile))

    # def test_multibyte(self):
    #     with TemporaryDirectory() as dirname:
    #         targetfile = os.path.join(dirname, "test.png")
    #         ggwrite("""
    #           x <- data.frame(x=c(1,2,3), y=c(4,5,6), label=c("あ", "い", "う"))
    #           ggplot(x, aes(x, y, label=label, color=label)) +
    #             geom_text(size=12) +
    #             xlab("エックス") +
    #             ylab("ワイ") +
    #             ggtitle("題名")
    #         """, targetfile, savesize=(3, 2))
    #         self.assertTrue(os.path.isfile(targetfile))
