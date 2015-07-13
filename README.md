# lucid-utils

A Python library containing tools for accessing, parsing, analysing and interpreting data from the LUCID experiment.

## Installation

### Requirements

* NumPy
* SciPy
* PyEphem
* PIL

Or,

```bash
$ sudo apt-get install python-numpy python-scipy python-imaging
$ sudo pip install PyEphem
```


Once all of the above libraries have been installed, simply clone the repo:

```bash
$ git clone https://github.com/calhewitt/lucid-utils
```

and copy or link it to your Python libraries folder, for example:

```bash
$ cp lucid-utils /usr/lib/python2.7/lucid_utils
```

(Note the underscore in the directory name, as Python cannot import module names containing a hyphen)

## Usage Examples

* Finding particle counts in a frame stored as an XYC text file

```python
from lucid_utils import xycreader, blobbing
from lucid_utils.classification.old_algorithm import classify

frame = xycreader.read("mydata.txt")

clusters = blobbing.find(frame)

counts = {'alpha': 0, 'beta': 0, 'gamma': 0, 'other': 0}

for cluster in clusters:
  particle_type = classify(cluster)
  counts[particle_type] += 1

print counts
```

* Downloading a data file (100 frames) from the data browser API and analysing it

```python
from lucid_utils import data_api, blobbing
from lucid_utils.classification.old_algorithm import classify

print "Fetching data..."
# Here, run refers to the start date of the 2 day slot, and id the unique identification number given to each specific data file
frames = data_api.get_frames({'run': "2015-07-07", 'id': 537403456})

print "Analysing particle tracks"
counts = {'alpha': 0, 'beta': 0, 'gamma': 0, 'other': 0}

for frame in frames:
  for i in range(5):
    if frame.channels[i] != None:
      # As LUCID data is still often 'bitty', the blobbing radius is usually best set higher than its default
      clusters = blobbing.find(frame.channels[i], 11)
      for cluster in clusters:
        particle_type = classify(cluster)
        counts[particle_type] += 1

print counts
```

* Generating an image of an XYC frame:

```python
from lucid_utils import xycreader, frameplot

frame = xycreader.read("mydata.txt")

image = frameplot.get_image(frame, "RGB")
image.show()
```

* Finding the current geographical location of LUCID

```python
from lucid_utils import telemetry

position = telemetry.get_current_position()

print "Latitude: " + str(position.latitude)
print "Longitude: " + str(position.longitude)

# And plot it on a map...
telemetry.get_map(position.latitude, position.longitude).show()
```
