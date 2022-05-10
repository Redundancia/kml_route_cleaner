# process_kml

This python script parses a kml file, tries to clear up incorrect data, creates us an updated kml file and calculates the total distance between the updated coordinates.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the requirements.

```bash
pip install -r requirements.txt
```

## Usage

```
py process_kml.py
```

## Logic

Basically if I thought the current coordinate was too far away from the last approved coordinate, I decided it was invalid, and did not add it to my updated coordinates. I had no timestamps and thus speed to work and calculate with, so I just used an arbitrary number that seemed to fit my needs.

For the distance calculation, I iterated over the updated coordinate pairs, and used the haversine formula.