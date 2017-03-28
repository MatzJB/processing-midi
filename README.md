# processing-midi
Processing midi files using midi-python library. At the moment it supports "inversion" and getting the range of notes.

Usage
----
Install python-midi https://github.com/vishnubob/python-midi

To invert all files in a given directory
`python midiProcess.py "c:/temp/midis/" -i`

Note: output is same directory with a added "_out" string
