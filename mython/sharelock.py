"""
Module for accessing Sharelock Holmes
"""
#import cookielib
import csv
import http
import io
import pprint
import re
import os
import os.path
import shutil
import subprocess
import sys

#import mechanize

import mython.csvmc as csvmc

# import pandas # apt-installable

#sys.path.append('/home/mcarter/repos/nokilli/python')

import mython.pytext as pytext

#ROOT = os.getenv("DOCS") + "/sharelock"
ROOT=os.getenv("HOME") + "/.fortran"
MISC_DIR =  ROOT + "/int/misc"
COOKIES_FILE = MISC_DIR + "/cookies.txt"
#STATS_FILE = MISC_DIR + "/StatsList.csv"
STATS_FILE = ROOT + "/StatsList.csv"

def fixfile(filename = STATS_FILE):
    txt01 = pytext.load(filename)
    txt02 = txt01.replace("\r", "\n")
    for (ori, rep) in [('F.EPIC', 'EPIC'), ('F.Sector', 'SECTOR'),
                       ('MarketCap', 'MKT'), ('Piotroski_Score', "PIO")]:
        txt02 = txt02.replace(ori, rep, 1)
    #txt03 = txt02.replace(' "', '"')
    #txt03 = re.sub(r',$', '', txt02)
    
    #rdr = csv.reader(io.StringIO(txt02))
    #hdr = rdr.next()
    #print(hdr)
                     
    #txt3 = ''                
    rows01 = list(csv.reader(io.StringIO(txt02)))
    len0 = len(rows01[0])
    
    rows02 = []
    for r in rows01:
        cols = [c.strip() for c in r]
        rows02.append(cols[0:len0])
    #rows02 = [row[0:len0] for row in rows01]
    #rows02 = rows01+body

    csv.writer(open(filename, 'w')).writerows(rows02)
    return rows02

    

def csvnameXXX():
    "Return the full path of the latest downloaded StatList*.csv file"
    cmd = "ls -t ~/Downloads/StatsList*.csv | head -1"
    filein = subprocess.check_output(cmd, shell=True)
    filein = filein.strip()
    filein = os.path.expanduser(filein)
    return filein

CLEAN_STATSLISTXXX = ROOT + "/int/misc/clean-statslist.csv"
def clean_latest_statslist():
    "Identify latest StatsList file, and clean it up"
    global CLEAN_STATSLISTXXX
    fixfile(csvname)
    shutil.copyfile(filein, CLEAN_STATSLIST)
    



def loadclean():
    global CLEAN_STATSLIST
    clean_latest_statslist()
    return pandas.read_csv(CLEAN_STATSLIST)

def prdf(df):
    'print a data frame'
    print()
    print(df.to_string())

def read_calcsXXX():
    "Read the calculations csv file as a pandas dataframe"
    global ROOT
    return pandas.read_csv(ROOT + "/int/misc/calcs.csv")

def read_csv():
    return csvmc.read_dict(ROOT + "/int/misc/calcs.csv")

############################################################################
# automation of the rs6 file

def print_forms(br):
    "Useful for debugging purposes"
    for form in br.forms():
        print(form)
        print("--------------------------------")

def print_links(br):
    "Useful for debugging purposes"
    for link in br.links():
        # print link
        # Link(base_url='http://www.example.com/', url='http://www.rfc-editor.org/rfc/rfc2606.txt', text='RFC 2606', tag='a', attrs=[('href', 'http://www.rfc-editor.org/rfc/rfc2606.txt')])
        # print link.url
        # print
        pass


def get_stats(query_name):
    """Fetch rs6 from Sharelock, and save it in a canonical place
    You may have to periodically update your cookies
    """
    global COOKIES_FILE, STATS_FILE
    br = mechanize.Browser()
    br.set_handle_equiv(True)
    #br.set_handle_gzip(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    cj = cookielib.MozillaCookieJar()
    br.set_cookiejar(cj)
    cj.load(COOKIES_FILE, ignore_discard=False, ignore_expires=False)

    #r = br.open('http://www.sharelockholmes.com/StatsList.aspx')
    br.open('http://www.sharelockholmes.com/')
    br.follow_link(url='StatsList.aspx')
    br.select_form(name="Form1")
    # br.select_form(name="Fc")
    control=br.form.find_control(name="cmbQuery")
    control.value = [query_name]
    br.submit(name="cmdExport")

    output = br.response().read()
    open(STATS_FILE, "w").write(output)
    fixfile(STATS_FILE)


def get_rs6(): get_stats("rs6")

############################################################################

def main():   
    df = loadclean()
    print(df) # print descriptive info
    #df = df[(df.EV_EBITDA <=6.5) & (df.Yield >= 4.0)] # this works
    df = df[df.EV_EBITDA <=6.5]

    df = df[['EPIC', 'EV_EBITDA', 'Yield']]
    df = df.sort_index(by='EV_EBITDA')

    df.index = range(1, 1+ len(df)) # renumber the rows sequentially
    print(df.to_string())
    print("Number of rows:", len(df))

    print('Finished')
