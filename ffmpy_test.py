#!/usr/bin/python

## Takes input media file and transcodes and wraps to MPEG-2/WAV in MXF-30 OP1A.
import ffmpy
import sys
import time  
import os
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler  

##Watch folder to detect .mp4 file
watch_folder = '/home/pasdesignal/incoming'
dest = "/home/pasdesignal/outgoing/ztest.mxf"

class ingest_handler(PatternMatchingEventHandler):
    
    patterns = ["*.mp4"]

    def process(self, event):
        #print "Path =", event.src_path
        #print event.src_path, event.event_type
        input_file = event.src_path
        print "input_file:", input_file
        self.transcode(input_file)

    def on_modified(self, event):
        print "modified observer =", observer
        print event.src_path
        time.sleep(2)
        if os.path.exists(event.src_path):
            self.process(event)

    def on_created(self, event):
        print "created observer =", observer
        print event.src_path
        time.sleep(2)
        if os.path.exists(event.src_path):
            self.process(event)

    def transcode(self, input_file):
        ff = ffmpy.FFmpeg(
        inputs={input_file: None},
        outputs={dest: '-f mxf -c:v mpeg2video -c:a pcm_s24le -g 1 -pix_fmt yuv422p'
        ' -b:v 30M -r 25 -field_order tt -flags +ildct+ilme -dc 10 -top 1  -color_trc bt709 -y'}
        )
        print "attempting transcode using ffmpeg command:", ff.cmd
        try:
        	ff.run()
        	print "transcode succesfull (I think), removing", input_file
        	os.remove(input_file)
        except:
        	print "transcode unsuccesfull"

observer = Observer()                           #folder watchdog process to monitor outputxml from airodump-ng
observer.schedule(ingest_handler(), path=watch_folder)
scanning = 0
time_started = time.time()
print "starting folder watchdog..."
observer.start()
time.sleep(10)
print "times up, stopping watchdog..."
observer.stop()
