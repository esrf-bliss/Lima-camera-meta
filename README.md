# Lima-camera-meta

Meta camera Hw interface for mosaic of cameras

## An python code example: mosaic of 2 simulator cameras

```python       
from Lima import Core, Simulator, Meta        

cam1 = Simulator.Camera()
cam2 = Simulator.Camera()
hwint1 = Simulator.Interface(cam1)
hwint1 = Simulator.Interface(cam2)

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