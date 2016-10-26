#! /usr/bin/python

 
import os
from gps import *
from time import *
from datetime import datetime, timedelta
import time
import threading
import picamera
from pexif import JpegFile
import math
 
gpsd = None #seting the global variable
camera = None
 
os.system('clear') #clear the terminal (optional)
 
class GpsPoller(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    global gpsd #bring it in scope
    gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
    self.current_value = None
    self.running = True #setting the thread running to true
 
  def run(self):
    global gpsd
    while gpsp.running:
      gpsd.next() #this will continue to loop and grab EACH set of gpsd info to clear the buffer

def set_exif(long,lat,filename):
    try:
        ef = JpegFile.fromFile(filename)
        ef.set_geo(lat, long)
    except IOError:
        type, value, traceback = sys.exc_info()
        print >> sys.stderr, "Error opening file:", value
    except JpegFile.InvalidFile:
        type, value, traceback = sys.exc_info()
        print >> sys.stderr, "Error opening file:", value

    try:
        ef.writeFile(filename)
    except IOError:
        type, value, traceback = sys.exc_info()
        print >> sys.stderr, "Error saving file:", value

      
if __name__ == '__main__':
  gpsp = GpsPoller() # create the thread
  try:
    gpsp.start() # start it up
	f= open("LOG_GpiScam.csv","a")
    #camera = picamera.PiCamera()
    piccounter=0
    with picamera.PiCamera() as camera:

        camera.resolution = camera.MAX_IMAGE_RESOLUTION
        time.sleep(2)    

        #init system
        while math.isnan(float(gpsd.fix.latitude)) and math.isnan(float(gpsd.fix.longitude)) or gpsd.fix.latitude==0 and gpsd.fix.longitude==0:
			print 'No valid GPS data!'
            print 'lat: ' + str(float(gpsd.fix.latitude))
            print 'long: ' + str(float(gpsd.fix.longitude))
            time.sleep(0.2)
            
        flag_firstRun=True
        print 'System ready....'    
        print 'GPS ready....'
        print 'Camera ready... :-)'        
        
        while flag_firstRun:
          
          #capture pic with utc system time ->RTC
          filename=str(datetime.now())+'_image.jpg'
          camera.capture(filename)
          
          
          lat=float(gpsd.fix.latitude)
          long=float(gpsd.fix.longitude)
          #set new exif data
          if  not math.isnan(lat) and not math.isnan(long) and lat>0 and long>0:
              print
              print 'Capture GPS'
              print '----------------------------------------'
              print 'Lat: ' + str(gpsd.fix.latitude) + 'Long: ' + str(gpsd.fix.longitude) 
              print 'time utc    ' , gpsd.utc,' + ', gpsd.fix.time
              print 'altitude (m)' , gpsd.fix.altitude
              #print 'eps         ' , gpsd.fix.eps
              #print 'epx         ' , gpsd.fix.epx
              #print 'epv         ' , gpsd.fix.epv
              #print 'ept         ' , gpsd.fix.ept
              print 'speed (m/s) ' , gpsd.fix.speed
              #print 'climb       ' , gpsd.fix.climb
              #print 'track       ' , gpsd.fix.track
              print 'mode        ' , gpsd.fix.mode
              #print
              #print 'sats        ' , gpsd.satellites
            
              camera.exif_tags['IFD0.Copyright'] = 'codegrafix.de'
              #camera.exif_tags['GPSInfo.GPSLatitude'] = bytes(gpsd.fix.latitude)
              #camera.exif_tags['GPSInfo.GPSLongitude'] = bytes(gpsd.fix.longitude)
              #camera.exif_tags['GPS.GPSutc'] = str(gpsd.utc)
              #camera.exif_tags['GPS.GPSSatellites']=str(gpsd.satellites)
              #camera.exif_tags['GPSInfo.GPSMeasureMode']=str(gpsd.fix.mode)
              #camera.exif_tags['IFD0.fixtime'] = str(gpsd.fix.time)
      
              #capture pic      
              set_exif(long,lat,filename)

          else:
              print 'No valid GPS Signal'
              
              #print 'System not ready'
            #pass
          print filename + ' Nr:' + str(piccounter)
          piccounter=piccounter+1
          time.sleep(1) #set to whatever
            
  except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
    print "\nKilling Thread..."
    gpsp.running = False
    gpsp.join() # wait for the thread to finish what it's doing
  print "Done.\nExiting."
  
  
