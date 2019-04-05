# -*- coding: utf-8 -*-
import arcpy
import os
import shutil
import pandas as pd
import numpy as np
import xlrd
import xlwt
import re

import re
def dms2dd(degrees,minutes,seconds,direction):
    dd=float(degrees)+float(minutes)/60.0+float(seconds)/(3600.0);
    if direction=='E' or direction=='N':
        dd*=-1
    return dd;

def dd2dms(deg):
    d=int(deg)
    md=abs(deg-d)*60
    m=int(md)
    sd=(md-m)*60
    return [d,m,sd]

def parse_dms(dms):
    parts=re.split('[^\d\w]+',dms)
    lat=dms2dd(parts[0],parts[1],parts[2],parts[3])
    return lat

if __name__ == '__main__':
    dd=parse_dms(u'3\xb039\'40"S'.encode('utf8'))
    print(dd)