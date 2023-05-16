# Tektronix-MSO
A python wrapper to communicate with Tektronix MSO series 5 and 6 oscilloscopes

Installation:

Move inside the package folder and then

```
pip install -e .
```


Hello world:
```
from mso import TekScope

scope = tekscope.TekScope("1.1.1.1", 11)

scope.setup_save_traces('C:/pippo', 'ALL')
scope.setup_single_acquisition(50)
scope.acquisition_start()

scope.close()
```







# Reference
Oscilloscope programming manual: https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=1&ved=2ahUKEwj7k4v4sK3lAhUHJ1AKHUzbC6sQFjAAegQIAxAC&url=https%3A%2F%2Fdownload.tek.com%2Fmanual%2F5_6-Series-MSO54-MSO56-MSO58-MSO58L-MSO64-Programmer-Manual_EN-US_077130505.pdf&usg=AOvVaw3WAWUWrH804Fae0HA4aBxR
