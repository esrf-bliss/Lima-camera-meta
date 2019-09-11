[![License](https://img.shields.io/github/license/esrf-bliss/lima.svg?style=flat)](https://opensource.org/licenses/GPL-3.0)
[![Gitter](https://img.shields.io/gitter/room/esrf-bliss/lima.svg?style=flat)](https://gitter.im/esrf-bliss/LImA)
[![Conda](https://img.shields.io/conda/dn/esrf-bcu/lima-camera-meta.svg?style=flat)](https://anaconda.org/esrf-bcu)
[![Version](https://img.shields.io/conda/vn/esrf-bcu/lima-camera-meta.svg?style=flat)](https://anaconda.org/esrf-bcu)
[![Platform](https://img.shields.io/conda/pn/esrf-bcu/lima-camera-meta.svg?style=flat)](https://anaconda.org/esrf-bcu)

# LImA Meta Camera Plugin

Meta camera Hw interface for building mosaic of cameras

## Install

### Camera python

conda install -c esrf-bcu lima-camera-meta

# LImA

Lima ( **L** ibrary for **Im** age **A** cquisition) is a project for the unified control of 2D detectors. The aim is to clearly separate hardware specific code from common software configuration and features, like setting standard acquisition parameters (exposure time, external trigger), file saving and image processing.

Lima is a C++ library which can be used with many different cameras. The library also comes with a [Python](http://python.org) binding and provides a [PyTango](http://pytango.readthedocs.io/en/stable/) device server for remote control.

## Documentation

The documentation is available [here](https://lima.blissgarden.org)



## An python code example: mosaic of 2 simulator cameras

```python       
from Lima import Core, Simulator, Meta        

cam1 = Simulator.Camera()
cam2 = Simulator.Camera()
hwint1 = Simulator.Interface(cam1)
hwint2 = Simulator.Interface(cam2)

meta_config = '2x1'
#meta_config = '1x2'
# and so on .... 2x2 3x3 3x2 ...., no limit !!

meta_hwint = Meta.Interface()
if meta_config == '2x1':
    # make a meta detector of 2048x1024 pixels
    meta_hwint.addInterface(0,0, hwint1)
    meta_hwint.addInterface(1,0, hwint2)
            
elif meta_config == '1x2':
    # make a meta detector of 1024x2048 pixels
    meta_hwint.addInterface(0,0, hwint1)
    meta_hwint.addInterface(0,1, hwint2)
    
ct = Core.CtControl(meta_hwint)

ct.prepareAcq()
ct.startAcq()
```

