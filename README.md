ggshow
======
[![](https://badge.fury.io/py/ggshow.svg)](https://badge.fury.io/py/ggshow)

Produce ggplot2 graphs from Python

## Install

```shell
# from pypi
pip install ggshow

# or from github
git clone --depth 1 https://github.com/kota7/ggshow.git
pip install -U ./ggshow
```

## Requirements

- Python 3.5+
- `Rscript` command and R environment with `ggplot2` package installed

## Functions

- `ggshow`: Draw graph using ggplot2 on R and return the Image object that you can show on Jupyter notebook
- `ggwrite`: Draw graph using ggplot2 on R and save it to a file.



```python
from ggshow import ggshow, ggwrite
```


```python
# Minimal example
# pass R code to produce ggplot graph to ggshow function
# note: ggplot2 is automatically imported
ggshow("""
  x <- c(1,2,3)
  y <- c(4,5,6)
  qplot(x, y, geom="line")
""", width=3, height=2)
```




    
<img src="README_files/README_3_0.png" width=400>
    




```python
# Example with data frames
# pass as data frames as keyword arguments
# then you can use them in the R code
import numpy as np
import pandas as pd
x = np.linspace(-20, 20, 500)
y = np.sin(x)
y2 = 0.4*np.cos(x)

df1 = pd.DataFrame({"x":x, "y":y})
df2 = pd.DataFrame({"x":x, "y":y2})
ggshow("""
  ggplot(a, aes(x, y)) + 
    geom_line(color="blue") +
    geom_line(data=b, linetype="dashed", color="red") +
    theme_bw()
""", dispwidth=400, width=4, height=2, a=df1, b=df2)
```




    
<img src="README_files/README_4_0.png" width=400>



```python
# Example to save the graph to a file
ggwrite("""
    x <- c(1,2,3)
    y <- c(4,5,6)
    qplot(x, y, geom="line")
""", "foo.jpg", width=4, height=2)
```


```python
from IPython.display import Image
Image("foo.jpg", width=400)
```




    
<img src="README_files/README_6_0.jpg" width=400>




```python
# By default, we use 'Rscript' as the command to run R code.
# If this is not a valid command on your environment,
# specify by set_rscript function.
from ggshow import config, set_rscript

set_rscript("/usr/bin/Rscript")  
print(config.rscript)
# this is just the full path of the command on this environment
# so the command will work in the same way
```

    /usr/bin/Rscript



