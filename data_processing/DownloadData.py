# -*- coding: utf-8 -*-
"""
Created on Fri Oct  4 22:16:53 2019

@author: Masters-PC
"""

'''
Each storm has an id. 
This is to download data for Dorian ('al052019'),
 Karen ('al122019'), and Lorenzo ('al132019').
 I believe the coding scheme is zone (al=Atlantic)
, storm number (05/12/13) and season (2019).
'''

import urllib.request
import time
ffolder = 'C:/Users/Masters-PC/Downloads/HurricaneData/'
print('Beginning file download with urllib2...')
urls = """al052019_5day_001.zip
al052019_5day_002.zip
al052019_5day_003.zip
al052019_5day_004.zip
al052019_5day_004A.zip
al052019_5day_005.zip
al052019_5day_005A.zip
al052019_5day_006.zip
al052019_5day_006A.zip
al052019_5day_007.zip
al052019_5day_007A.zip
al052019_5day_008.zip
al052019_5day_008A.zip
al052019_5day_009.zip
al052019_5day_009A.zip
al052019_5day_010.zip
al052019_5day_010A.zip
al052019_5day_011.zip
al052019_5day_011A.zip
al052019_5day_012.zip
al052019_5day_012A.zip
al052019_5day_013.zip
al052019_5day_013A.zip
al052019_5day_014.zip
al052019_5day_014A.zip
al052019_5day_015.zip
al052019_5day_015A.zip
al052019_5day_016.zip
al052019_5day_016A.zip
al052019_5day_017.zip
al052019_5day_017A.zip
al052019_5day_018.zip
al052019_5day_018A.zip
al052019_5day_019.zip
al052019_5day_020.zip
al052019_5day_021.zip
al052019_5day_022.zip
al052019_5day_023.zip
al052019_5day_024.zip
al052019_5day_024A.zip
al052019_5day_025.zip
al052019_5day_025A.zip
al052019_5day_026.zip
al052019_5day_026A.zip
al052019_5day_027.zip
al052019_5day_027A.zip
al052019_5day_028.zip
al052019_5day_028A.zip
al052019_5day_029.zip
al052019_5day_029A.zip
al052019_5day_030.zip
al052019_5day_030A.zip
al052019_5day_031.zip
al052019_5day_031A.zip
al052019_5day_032.zip
al052019_5day_032A.zip
al052019_5day_033.zip
al052019_5day_033A.zip
al052019_5day_034.zip
al052019_5day_034A.zip
al052019_5day_035.zip
al052019_5day_035A.zip
al052019_5day_036.zip
al052019_5day_036A.zip
al052019_5day_037.zip
al052019_5day_037A.zip
al052019_5day_038.zip
al052019_5day_038A.zip
al052019_5day_039.zip
al052019_5day_039A.zip
al052019_5day_040.zip
al052019_5day_040A.zip
al052019_5day_041.zip
al052019_5day_041A.zip
al052019_5day_042.zip
al052019_5day_042A.zip
al052019_5day_043.zip
al052019_5day_043A.zip
al052019_5day_044.zip
al052019_5day_044A.zip
al052019_5day_045.zip
al052019_5day_045A.zip
al052019_5day_046.zip
al052019_5day_046A.zip
al052019_5day_047.zip
al052019_5day_047A.zip
al052019_5day_048.zip
al052019_5day_048A.zip
al052019_5day_049.zip
al052019_5day_049A.zip
al052019_5day_050.zip
al052019_5day_050A.zip
al052019_5day_051.zip
al052019_5day_051A.zip
al052019_5day_052.zip
al052019_5day_052A.zip
al052019_5day_053.zip
al052019_5day_053A.zip
al052019_5day_054.zip
al052019_5day_054A.zip
al052019_5day_055.zip
al052019_5day_055A.zip
al052019_5day_056.zip
al052019_5day_056A.zip
al052019_5day_057.zip
al052019_5day_058.zip
al052019_5day_059.zip
al052019_5day_059A.zip
al052019_5day_060.zip
al052019_5day_060A.zip
al052019_5day_061.zip
al052019_5day_061A.zip
al052019_5day_062.zip
al052019_5day_062A.zip
al052019_5day_063.zip
al052019_5day_063A.zip
al052019_5day_064.zip
al122019_5day_001.zip
al122019_5day_001A.zip
al122019_5day_002.zip
al122019_5day_002A.zip
al122019_5day_003.zip
al122019_5day_003A.zip
al122019_5day_004.zip
al122019_5day_004A.zip
al122019_5day_005.zip
al122019_5day_005A.zip
al122019_5day_006.zip
al122019_5day_006A.zip
al122019_5day_007.zip
al122019_5day_007A.zip
al122019_5day_008.zip
al122019_5day_008A.zip
al122019_5day_009.zip
al122019_5day_009A.zip
al122019_5day_010.zip
al122019_5day_010A.zip
al122019_5day_011.zip
al122019_5day_011A.zip
al122019_5day_012.zip
al122019_5day_012A.zip
al122019_5day_013.zip
al122019_5day_014.zip
al122019_5day_015.zip
al122019_5day_016.zip
al122019_5day_017.zip
al122019_5day_018.zip
al122019_5day_019.zip
al122019_5day_020.zip
al122019_5day_021.zip
al122019_5day_022.zip
al122019_5day_023.zip
al132019_5day_001.zip
al132019_5day_002.zip
al132019_5day_003.zip
al132019_5day_004.zip
al132019_5day_005.zip
al132019_5day_006.zip
al132019_5day_007.zip
al132019_5day_008.zip
al132019_5day_009.zip
al132019_5day_010.zip
al132019_5day_011.zip
al132019_5day_012.zip
al132019_5day_013.zip
al132019_5day_014.zip
al132019_5day_015.zip
al132019_5day_016.zip
al132019_5day_017.zip
al132019_5day_018.zip
al132019_5day_019.zip
al132019_5day_020.zip
al132019_5day_021.zip
al132019_5day_022.zip
al132019_5day_023.zip
al132019_5day_024.zip
al132019_5day_025.zip
al132019_5day_026.zip
al132019_5day_027.zip
al132019_5day_028.zip
al132019_5day_029.zip
al132019_5day_030.zip
al132019_5day_031.zip
al132019_5day_031A.zip
al132019_5day_032.zip
al132019_5day_032A.zip
al132019_5day_033.zip
al132019_5day_033A.zip
al132019_5day_034.zip
al132019_5day_034A.zip
al132019_5day_035.zip
al132019_5day_035A.zip
al132019_5day_036.zip
al132019_5day_036A.zip
al132019_5day_037.zip
al132019_5day_037A.zip
al132019_5day_038.zip
al132019_5day_038A.zip
al132019_5day_039.zip
al132019_5day_039A.zip
al132019_5day_040.zip
al132019_5day_040A.zip
al132019_5day_041.zip"""
base = 'https://www.nhc.noaa.gov/gis/forecast/archive/'
urls = urls.split('\n')
for i in range(106,len(urls)):
    url = urls[i]
    print(i)
    while True:
        try:
            urllib.request.urlretrieve(base+url, ffolder+url)
            break
        except:
            print('error')
            time.sleep(0.5)
            continue


