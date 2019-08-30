# opytic

Python library to simulate geometrical optics 

tst

Simulate the path of light beams in the approximation of geometrical optics. Currently supports the following optical objects:

 - Lenses
 - Mirrors
 - Optical interfaces

## Installation
```bash
pip3 install -r requirements.txt
```

## Usage
 You will find a file `opytic_example.py` where is runned an example of a simulation that opytic can run.
 Such a simulation is build as explained:
  - Create the optical objects : lenses, mirrors, interfaces
  - Create the light beams. You will have to give to their initial position and angle with the optical axis
  - Run each ray through the optical objects

After that, the beam objects will be updated and you will be able to access to their 'state' with the method `beam::state()`. This will return the angle of the final part of the ray with the optical axis and the last point where the ray have been deflected

Each optical objects and beams cam be drawn with the method `draw`

## Add new optical objects
Every optical object inherits from the class `optical_object` and must be equipped by the methods `simulate_beam` and `draw`. `simulate_beam` takes as input a `beam` object and returns a `beam` object which is the updated initial beam (updated with the method `beam::become()`). `simulate_beam` is called by `beam::go_through()`.
