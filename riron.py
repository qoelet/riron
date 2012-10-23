#!/usr/local/bin/python
# -*- coding: utf-8 -*-

######################################################################################## ♫
# riron
# a simple music theory commandline environment
# author: kenny shen, kenny@northpole.sg

# usage:
# ./riron.py 
# >> CMD [ARGS] [OPTS]

######################################################################################## ♫
## IMPORTS
import argparse

######################################################################################## ♫
# in the beginning, we have notes. 
# A, A#/Bb, B, C, C#/Db, D, D#/Eb, E, F, F#/Gb, G, G#/Ab.. (back to A)
NOTES = ('A', 'A#/Bb', 'B', 'C', 'C#/Db', 'D', 'D#/Eb', 'E', 'F', 'F#/Gb', 'G', 'G#/Ab')
MINOR_CHOICES = ("harmonic", "melodic", "natural")

# let's make a class Note
class Note(object):
    def __init__(self, note):
        self.note = note
        self._note = note # for remembrance 
        self._idx = None
        self._max_idx = len(NOTES) - 1
        self._min_idx = 0

        try:
            self._idx = NOTES.index(note)
            self.note = note
        except ValueError:
            if len(note) == 2:
                try:
                    enharmonic = None
                    for n in NOTES:
                        if note in n:
                            enharmonic = n
                    self._idx = NOTES.index(enharmonic)
                    self.note = enharmonic
                except:
                    print "- Invalid note assigned: %s is not in %s" % (note, NOTES)
            else:
                print "- Invalid note assigned: %s is not in %s" % (note, NOTES)

    def __str__(self):
        return self.note

    def sharpen(self, semitones=1):
        assert self._idx != None
        for i in range(0, semitones):
            if ((self._idx + 1) > self._max_idx):
                self._idx = self._min_idx
                self.note = NOTES[self._idx]
            else:
                self._idx += 1
                self.note = NOTES[self._idx]

        return self.note

    def flatten(self, semitones=1):
        assert self._idx != None
        for i in range(0, semitones):
            if ((self._idx - 1) < 0):
                self._idx = self._max_idx
                self.note = NOTES[self._idx]
            else:
                self._idx -= 1
                self.note = NOTES[self._idx]

        return self.note

    def reset(self):
        # back to note initialized with
        self.note = self._note
        self._idx = NOTES.index(self.note)

# then there were triads
class Triad(object):
    def __init__(self, note, triad_type):
        self.tonic = Note(note.note)
        self.triad_type = triad_type
        self.notes = [self.tonic, None, None]
        self._create()

    def __str__(self):
        s = ""
        for note in self.notes:
            s += ("%s - " % note.note)
        return s[:-2]

    def _create(self):
        self.notes[0] = self.tonic # add root note

        root = self.tonic
        if self.triad_type == "major":
            self.notes[1] = Note(root.sharpen(4)) # major 3rd
        elif self.triad_type == "minor":
            self.notes[1] = Note(root.sharpen(3)) # minor 3rd
        root.reset()
        self.notes[2] = Note(root.sharpen(7)) # perfect 5th
        root.reset()

# then there were tetrachords
class Tetrachord(object):
    def __init__(self, note):
        self.tonic = Note(note.note)
        self.notes = [None, None, None, None]
        self._create()

    def __str__(self):
        s = ""
        for note in self.notes:
            s += ("%s - " % note.note)
        return s[:-2]

    def _create(self):
        self.notes[0] = self.tonic # add root note

        root = self.tonic
        self.notes[1] = Note(root.sharpen(2))
        self.notes[2] = Note(root.sharpen(2))
        self.notes[3] = Note(root.sharpen(1))

        root.reset()

    def is_diatonic(self):
        return self.diatonic

# then there were scales
class Scale(object):
    def __init__(self, note, scale_type):
        self.tonic = Note(note.note)
        self.scale_type = scale_type
        self.notes = []

    def __str__(self):
        s = ""
        for note in self.notes:
            s += ("%s - " % note.note)
        return s[:-2]

    def major(self):
        assert self.scale_type == "major"

        t1 = Tetrachord(self.tonic)
        link = Note(t1.notes[-1].sharpen(2))
        # reset last note used to get linking note, see todo
        t1.notes[-1].reset()
        t2 = Tetrachord(link)

        self.notes = t1.notes + t2.notes

        return self.notes

    def minor(self, minor_type="natural"):  # assumes natural unless specified: harmonic, melodic
        assert minor_type in MINOR_CHOICES and self.scale_type == "minor"
        if minor_type == "natural":
            self.notes = [None] * 8
            self.notes[0] = self.tonic # add root note

            root = self.tonic
            self.notes[1] = Note(root.sharpen(2))
            self.notes[2] = Note(root.sharpen(1))
            self.notes[3] = Note(root.sharpen(2))
            self.notes[4] = Note(root.sharpen(2)) # link
            self.notes[5] = Note(root.sharpen(1))
            self.notes[6] = Note(root.sharpen(2))
            self.notes[7] = Note(root.sharpen(2))

            root.reset

            return self.notes

######################################################################################## ♫
## TESTS
print "♫ riron\n\n\n"
print "Creating note C."
n = Note("C")
print "Creating major scale for note."
s = Scale(n, "major")
s.major()
print "Scale: %s" % s
print "Creating minor (natural) scale for note."
s = Scale(n, "minor")
s.minor("natural")
print "Scale: %s" % s
######################################################################################## ♫
## TODO
# [ ] Note.sharpen/flatten modifies the actual value, we should instead return a new Note object in the altered state
# [ ] Detect when 'note' is passed - is instance or string? Deal accordingly
# [ ] Interactive environment parsing

