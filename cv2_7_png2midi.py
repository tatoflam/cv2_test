import numpy as np
import cv2
import pretty_midi
img = cv2.imread("../img_test/sample_png2midi.png")

h, w, c = img.shape  # get size of image
pm = pretty_midi.PrettyMIDI(resolution=960, initial_tempo=120)
instrument = pretty_midi.Instrument(0)  # Object to hold event information for a single instrument
for j in range(h): 
   for i in range(w): 
       luminance = img.item(j, i, 0) + img.item(j, i, 1) + img.item(j, i, 2) # add RGBvalue
       if luminance < 450: # check spaces in black
           note = pretty_midi.Note(velocity=100, pitch=h-j, start=i*0.25, end=i*0.25+0.25) #NoteOn->start、NoteOffE->end
           instrument.notes.append(note) #  add note
           
pm.instruments.append(instrument) #  append track
pm.write('./data/fromPng.mid')  #wite midi file
