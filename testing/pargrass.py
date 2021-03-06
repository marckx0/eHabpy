# Code by Javier Martinez-Lopez
from multiprocessing import cpu_count,Pool,Lock
import subprocess
import os
import sys
import csv
import time
import numpy as np
from datetime import datetime

GISBASE = os.environ['GISBASE'] = "/usr/local/grass-7.1.svn"
GRASSDBASE = os.path.join("/home/javier/Desktop/grassdb")
MYLOC = "nc_spm_08_reduced"
mapset = "user1"

sys.path.append(os.path.join(os.environ['GISBASE'], "etc", "python"))

import grass.script as grass
import grass.script.setup as gsetup
 
gsetup.init(GISBASE,
            GRASSDBASE, MYLOC, mapset)

print grass.gisenv()

def function(elem):
 #print elem
 mymapset = 'm'+str(elem)
 grass.run_command('g.mapset',mapset=mymapset,loc=MYLOC,flags='c')
 spn0= str(GRASSDBASE)+'/'+str(MYLOC)+'/'+str(mymapset)+'WIND'
 print elem+' '+spn0
 checkit = os.path.isfile(spn0)
 while checkit == False:
  time.sleep(0.1)
 else:
  gge = grass.gisenv()
  spn= str(GRASSDBASE)+'/'+str(MYLOC)+'/'+str(mymapset)+'/SEARCH_PATH'
  wb = open(spn,'a')
  wb.write('PERMANENT')
  wb.write('\n') 
  wb.write('user1')
  wb.write('\n')
  wb.write(str(mymapset))
  wb.write('\n')
  wb.close()
  pa0 = 's'+str(elem)
  comm2 = 'cat = '+str(elem)
  grass.run_command('g.region',rast='elevation')
  grass.run_command('g.region',res=elem)
  varx = grass.read_command ('g.region',flags='g'). splitlines ()
  wb = open('results.txt','a')
  var = str(elem)+' '+str(gge)+' '+str(varx)
  wb.write(var)
  wb.write('\n')
  wb.close()
  elem=None
  mymapset=None

elems = '100','200','300','400'

pool = Pool()
pool.map(function,elems)
pool.close()
pool.join()


print 'END'
