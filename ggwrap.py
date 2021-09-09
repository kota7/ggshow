# -*- coding: utf-8 -*-

import os
import subprocess
from tempfile import TemporaryDirectory
from IPython.display import Image

class config:
    rscript = "Rscript"

def set_rscript(command):
    config.rscript = command
    _find_rscript()

def _find_rscript()-> bool:
    try:
        subprocess.run([config.rscript, "--version"],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except FileNotFoundError as e:
        warnings.warn(str(e))
        return False

# check if the Rscript is a valid command when loading this module
if not _find_rscript():
    print("'{}' is not a valid Rscript command. Please set by set_rscript(<rscript command>)")

def ggwrite(plotcode: str, outfile: str, libs=(),
            width=None, height=None, scale=1, units="in", dpi=300,
            ggsave_opts: dict={}, **dataframes):
    with TemporaryDirectory() as tmpdir:
        libs += ("ggplot2",)
        importcode = ";".join("library({})".format(l) for l in libs)
        readcode = []
        for name, df in dataframes.items():
             filename = os.path.join(tmpdir, "__data_{}.csv".format(name))
             df.to_csv(filename, index=False)
             readcode.append("{} <- read.csv('{}', as.is=TRUE)".format(name, filename))
        readcode = ";".join(readcode)

        if width is None: width = "NA"
        if height is None: height = "NA"
        code = """
        {importcode}
        {readcode}
        ..g <- {{
          {plotcode}
        }}
        ggsave("{outfile}", ..g,
               width={width}, height={height}, scale={scale}, units='{units}', dpi={dpi})
        """.format(importcode=importcode, readcode=readcode, plotcode=plotcode,
                   outfile=outfile, width=width, height=height, scale=scale, units=units, dpi=dpi)
        subprocess.run([config.rscript, "-e", code])


def ggshow(plotcode: str, dispwidth=300, dispheight=None, libs=(),
           width=None, height=None, scale=1, units="in", dpi=300,
           ggsave_opts: dict={}, **dataframes)-> Image:
    with TemporaryDirectory() as tmpdir:
        outfile = os.path.join(tmpdir, "__ggout.png")
        ggwrite(plotcode, outfile, libs=libs,
                width=width, height=height, scale=scale, units=units, dpi=dpi,
                ggsave_opts=ggsave_opts, **dataframes)
        im = Image(filename=outfile, width=dispwidth, height=dispheight)
        return im
