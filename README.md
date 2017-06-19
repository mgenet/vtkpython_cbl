# vtkpython_cbl
A library of vtkpython tools for cardiac biomechanics.
### Requirements
First you need to install [myPythonLibrary](https://github.com/mgenet/myPythonLibrary) as well as [myVTKPythonLibrary](https://github.com/mgenet/myVTKPythonLibrary)
### Installation
Get the code:
```
git clone https://github.com/mgenet/vtkpython_cbl
```
To load the library within python, the simplest is to add the folder containing vtkpython_cbl to `PYTHONPATH`:
```
export PYTHONPATH=$PYTHONPATH:/path/to/folder
```
(To make this permanent, add the line to `~/.bashrc`.)
Then you can load the library within python:
```
import vtkpython_cbl as cbl
```
