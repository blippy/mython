import cookielib
import csv
import pprint
import re
import os
import os.path
import shutil
import subprocess
import sys

import mechanize

import csvmc

# import pandas # apt-installable

#sys.path.append('/home/mcarter/repos/nokilli/python')

import pytext

ROOT = os.getenv("DOCS") + "/sharelock"
MISC_DIR =  ROOT + "/int/misc"
COOKIES_FILE = MISC_DIR + "/cookies.txt"
STATS_FILE = MISC_DIR + "/statslist.csv"


def fixfile(filename):
    with open(filename, 'rU') as fp:
        rdr = csv.reader(fp)
        hdr = rdr.next()
        #hdr = hdr[:-1]
        numcols = len(hdr)
        try: epic_col = hdr.index("EPIC")
        except ValueError: epic_col = None
        data = []
        for row in rdr:
            if epic_col is not None: 
                row[epic_col] =  row[epic_col].replace(' ', '')
            row = row[0:numcols]
            row = [ c.strip() for c in row]
            #data.append( row[:-1])
            data.append(row)
    
    with open(filename, 'wb') as f:
        writer = csv.writer(f)
        writer.writerows([hdr] + data)
    

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
    print
    print df.to_string()

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
        print form
        print "--------------------------------"

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
    print df # print descriptive info
    #df = df[(df.EV_EBITDA <=6.5) & (df.Yield >= 4.0)] # this works
    df = df[df.EV_EBITDA <=6.5]

    df = df[['EPIC', 'EV_EBITDA', 'Yield']]
    df = df.sort_index(by='EV_EBITDA')

    df.index = range(1, 1+ len(df)) # renumber the rows sequentially
    print df.to_string()
    print "Number of rows:", len(df)

    print 'Finished'
