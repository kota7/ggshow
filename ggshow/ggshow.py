# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import warnings
from tempfile import TemporaryDirectory
from pathlib import Path

try:
    # This try..except avoids errors on an environment with no ipython
    # ggwrite function will still be available
    from IPython.display import Image, SVG, display_png, display_jpeg, display_svg
except ImportError as e:
    print("'ggshow' function is disabled. Please import ipython to use it", file=sys.stderr)
    Image = None  # this line only exist to avoid the error due to the return type hint of ggshow

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

def ggwrite(plotcode: str, outfile: str, libs: tuple=(),
            savesize: tuple=None, width: float=None, height: float=None,
            scale: float=1, units: str="in", dpi: int=300,
            rscriptpath: str=None, message_encoding: str="utf-8", **data):
    """
    Write a ggplot2 graph to a file

    args:
        plotcode         :   R script to make a plot.
        outfile          :   The graph is saved to this filepath
        libs             :   A Sequence libraries to use inside the R script
        savesize         :   Graph size (width, height) to save
        width            :   Another way to specify savesize[0]
        height           :   Another way to specify savesize[1]
        scale            :   ggsave option scale
        units            :   ggsave option units
        dpi              :   ggsave option gpi
        rscriptpath      :   If given, used as the path to the Rscript command
        message_encoding :   Character encoding of the subprocess outputs
        **data           :   pandas data frames with names used inside the R script

    Returns:
        None
    """
    with TemporaryDirectory() as tmpdir:
        libs = tuple(libs)
        libs += ("ggplot2",)
        importcode = ";".join("library({})".format(l) for l in libs)
        readcode = []
        for name, df in data.items():
             filename = os.path.join(tmpdir, "__data_{}.csv".format(name))
             filename = Path(filename).as_posix()  # normalize the path string on windowns
             df.to_csv(filename, index=False, encoding="utf8")
             readcode.append("{} <- read.csv('{}', as.is=TRUE, fileEncoding='utf8')".format(name, filename))
        readcode = ";".join(readcode)

        if savesize is None: savesize = None, None
        if width is None: width = savesize[0]
        if height is None: height = savesize[1]
        if width is None: width = "NA"
        if height is None: height = "NA"
        outfile = Path(outfile).as_posix()  # normalize the path string on windowns
        if rscriptpath is None:
            rscriptpath = config.rscript

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
        #code = ascii(code)[1:-1]  # escape multibyte characters in the code [1:-1] to remove the quotes
        with TemporaryDirectory() as tmpdir:
            codefile = os.path.join(tmpdir, "__ggcode.R")
            with open(codefile, "w", encoding="utf-8") as f:
                f.write(code)
            p = subprocess.run([rscriptpath, codefile], stdout=subprocess.PIPE, stderr=subprocess.PIPE)        
        if p.returncode != 0:
            warnmessage = ("Some error occurred while running the R code. The graph may not have been created."
                           "\nStdout:\n\n{}\nStderr:\n\n{}\nR code (auto-generated):\n{}").format(
                           p.stdout.decode(), p.stderr.decode(), code)
            warnings.warn(warnmessage, RuntimeWarning)                
        else:
            print(p.stderr.decode(message_encoding, errors="replace"), file=sys.stderr, end="")
            print(p.stdout.decode(message_encoding, errors="replace"), file=sys.stdout, end="")


def ggshow(plotcode: str, dispwidth: float=300, dispheight: float=None, libs: tuple=(), imageformat: str="png", display: bool=True,
           savesize: tuple=None, width: float=None, height: float=None, scale: float=1, units: str="in", dpi: int=300,
           rscriptpath: str=None, message_encoding: str="utf-8", **data)-> Image:
    """
    Draw a ggplot2 graph

    args:
        plotcode         :   R script to make a plot.
        libs             :   A Sequence libraries to use inside the R script
        imageformat      :   Imagefile format. One of ("png", "jpeg", "jpg", "svg"); default: "png"
        display          :   Display image on the notebook
        savesize         :   Graph size (width, height) to save
        width            :   Another way to specify savesize[0]
        height           :   Another way to specify savesize[1]
        scale            :   ggsave option scale
        units            :   ggsave option units
        dpi              :   ggsave option gpi
        rscriptpath      :   If given, used as the path to the Rscript executable file
        message_encoding :   Character encoding of the subprocess outputs
        **data      :   pandas data frames with names used inside the R script

    Returns:
        IPython.core.Image
    """
    assert imageformat in ("png", "jpeg", "jpg", "svg"), "imageformat must be one of 'png', 'jpeg', 'jpg' and 'svg'"
    with TemporaryDirectory() as tmpdir:
        outfile = os.path.join(tmpdir, "__ggout." + imageformat)
        ggwrite(plotcode, outfile, libs=libs,
                savesize=savesize, width=width, height=height, scale=scale, units=units, dpi=dpi,
                rscriptpath=rscriptpath, message_encoding=message_encoding, **data)
        if not os.path.isfile(outfile):
            raise RuntimeError("Graph file not found. Perhaps Rscript failed to produce the graph")
        
        if imageformat in ("png", "jpeg", "jpg"):
            im = Image(filename=outfile, width=dispwidth, height=dispheight)
            if display:
                func = display_png if imageformat=="png" else display_jpeg
                func(im)
        elif imageformat == "svg":
            im = SVG(filename=outfile)
            if display:
                display_svg(im)
        return im


try:
    # We enclose this whole section by try...except
    # so that the module can be imported on an environment with no ipython
    from IPython.core.magic import Magics, line_cell_magic, magics_class
    from IPython.core.magic_arguments import argument, magic_arguments, parse_argstring

    @magics_class
    class GGMagic(Magics):

        @line_cell_magic("gg")
        @magic_arguments()
        @argument("plotcode", type=str, nargs="*", help="R code")
        @argument("--help", action="store_true")
        @argument("-s", "--savesize", type=float, nargs=2, default=None, help="height, width")
        @argument("--scale", type=float, default=1, help="ggsave option scale")
        @argument("--units", type=str, default="in", help="ggsave option units")
        @argument("--dpi", type=int, default=300, help="ggsave option dpi")
        @argument("-w", "--dispwidth", type=float, default=None, help="display width")
        @argument("-h", "--dispheight", type=float, default=None, help="display width")
        @argument("--imageformat", type=str, default="png", choices=("png", "jpeg", "svg"), help="imagefile format")
        @argument("--libs", nargs="*", default=(), help="R libraries to use")
        @argument("--data", nargs="*", default=(), help="data frames mapping as {name in r}={name in python}")
        def gg(self, line, cell=None):
            args = parse_argstring(self.gg, line)
            if args.help:
                help(self.gg)
                return
            opts = vars(args)
            del opts["help"]
            #print(args)
            #print(opts)
            for d in opts.pop("data"):
                rname, pyname = d.split("=")
                rname = rname.strip()
                pyname = pyname.strip()
                assert pyname in self.shell.user_ns, "'{}' not found in the name space:\n{}".format(pyname, self.shell.user_ns)
                opts[rname] = self.shell.user_ns[pyname]
            opts["plotcode"] = " ".join(opts["plotcode"])

            if cell is not None:
                opts["plotcode"] = cell
            
            return ggshow(**opts, display=False)
            
    def load_ipython_extension(ipython):
        """
        Any module file that define a function named `load_ipython_extension`
        can be loaded via `%load_ext module.path` or be configured to be
        autoloaded by IPython at startup time.
        """
        # You can register the class itself without instantiating it.  IPython will
        # call the default constructor on it.
        ipython.register_magics(GGMagic)
except ImportError as e:
    pass
