#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu 3.14 2013

@author: shuai.li
@notice: install unoconv & openoffice.org-writer
                           openoffice.org-calc
                           openoffice.org-impress
@notice: copy windows fonts to /usr/share/fonts/win/{windows fonts}, then run
         'sudo chmod -Rf 755 Fonts'
         'mkfontscale'
         'mkfontdir'
         'fc-cache -fv'
         'reboot'
@notice: swftools(pdf2swf) need xpdf language pack.
         Also add 'fontDir /usr/share/fonts/win' 
                  'displayCIDFontTT Adobe-GB1 /usr/share/fonts/win/simhei.ttf'
                  to /usr/local/xpdf-chinese-simplified/add-to-xpdfrc
"""
import os, sys, getopt, subprocess

def usage():
    print """
Usage:
        python trans_to_flash.py [option][value]...
option:
        -f  force transfer
        -i  input file/path; current dir is default
        -o  output path;input path is default
        -p  add prefix to filename: (/home/my.txt -> /home/P_my.txt)
        -s  add suffix to filename: (/home/my.txt -> /home/my_S.txt)
"""

def transfer(f = False, i = '.', o = None, p = '', s = '.swf'):
    """
    transfer(f = False, i = '.', o = None, p = '', s = '.swf')
        f: Force transfer, cover the file which may exist.
        i: The input path, current path is default.
        o: The output path, must specify before.
        p: The prefix added to the output file name.
        s: The suffix added to the output file name, default '.swf'.

    """


    opts = {"-f": f, "-i": i, "-o": o, "-p": p, "-s": s}
    #print opts
    all_files = []  #files to be transfered

    # specify the input path or file 
    if os.path.isfile(os.path.abspath(opts['-i'])):
        #default output path is the input path
        output_path = os.path.dirname(os.path.abspath(opts['-i']))
        all_files.append(os.path.abspath(opts['-i']))
    elif os.path.isdir(os.path.abspath(opts['-i'])):
        #default output path is the input path
        output_path = os.path.abspath(os.path.abspath(opts['-i']))
        for f in os.listdir(os.path.abspath(opts['-i'])):
            f = os.path.abspath(opts['-i']) + '/' + f
            all_files.append(os.path.abspath(f))
    
    # specify the output path
    if opts['-o'] is not None:
        output_path = os.path.abspath(opts['-o'])

    for src_file in all_files:
        if opts['-p'] is not None:
            dest_file_name = output_path + \
                                        '/' + \
                                        opts['-p'] + \
                                        '_' + \
                                        os.path.basename(src_file) + \
                                        opts['-s']
        else:
            dest_file_name = output_path + \
                                        '/' + \
                                        os.path.basename(src_file) + \
                                        opts['-s']

        if (not os.path.exists(dest_file_name)) or (opts['-f'] == True):
            returncode = _file_translation(src_file, dest_file_name)
            if (returncode == 0) and (len(all_files) == 1):
                sys.exit(0)
            elif (returncode == 1) and (len(all_files) == 1):
                sys.exit(1)

        #test
        print dest_file_name 


def _file_translation(src_file, dest_file_name = None):
    # using 'file' to get the filestyle
    p1 = subprocess.Popen(['file', src_file], stdout = subprocess.PIPE)
    p2 = subprocess.Popen(['cat'], stdin = p1.stdout, stdout = subprocess.PIPE)
    output = p2.communicate()[0]


    if "Macromedia" in output:
        subprocess.call(['cp', src_file, dest_file_name])
        return 0

    elif "PDF" in output:
        # use pdf2swf(swftools) to transfer from '.pdf' to '.swf' 
        subprocess.call(['/usr/bin/pdf2swf',
                            src_file, 
                            '-o',
                            dest_file_name, 
                            '-s', 
                            'languagedir=/usr/local/xpdf-chinese-simplified'
                            ])
        if os.path.exists(dest_file_name):
            return 0
        else:
            return 1
    else:
        # use unoconv to transfer from * to '.pdf' first
        subprocess.call(['unoconv', '-p', '8100', '-f', 'pdf', src_file])
        subprocess.call(['/usr/bin/pdf2swf', 
                            '-T', 
                            '9', 
                            src_file[:-3] + 'pdf', 
                            '-o', 
                            dest_file_name, 
                            '-s', 
                            'languagedir=/usr/local/xpdf-chinese-simplified'
                            ])
        if os.path.exists(dest_file_name):
            return 0
        else:
            return 1


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'fi:o:p:s:')
    except getopt.GetoptError, err:
        print str(err)
        usage()
        sys.exit(2)
    opt_value = dict()

    for item in opts:
        if item[0] == '-f':
            opt_value[item[0][1]] = True
        else:
            opt_value[item[0][1]] = item[1]
    print opt_value
    transfer(**opt_value)

if __name__ == "__main__":
    main()
