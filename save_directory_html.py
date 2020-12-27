import os
import re
import pandas as pd

#Make a list of univesities which their faculty directory html file is saved 
os.system('ls /home/miliverse/pages/*html > html_files.txt')
present_unis = []
f = open('html_files.txt', mode='r')
lines = f.readlines()
for line in lines:
    line = line.replace('/home/miliverse/pages/','')
    line = line.replace(r'.html','')
    line = line[:-1]   
    present_unis.append(line)
f.close()


unis_dataframe = pd.read_excel('Physics_departments_original.xlsx', na_values = 'None')

files_dest = '/home/miliverse/pages/'
load_wait_time = str(10)
save_wait_time = str(15)
f = open('html_save_log.txt', mode='w')
absent_uni = []
for index, row in unis_dataframe.iterrows():
    # time.sleep(int(load_wait_time)+int(save_wait_time)+3)
    uni = row['University']
    uni = uni.replace('-','')
    uni = uni.replace('–','')
    uni = uni.replace(',','')
    uni = re.sub(r"\s+", '_', uni)
    url = row['url']
    # file_path = files_dest + uni + '.html'
    file_path = files_dest + str(index) +'.html'
    
    if uni not in present_unis:
        absent_uni.append(uni)
        print(uni)
        #command = './save_page_as {} -d {} --load-wait-time {} --save-wait-time {}'.format(url,file_path,load_wait_time,save_wait_time)
        command = './save_page_as {} -d {} --save-wait-time 60'.format(url,file_path)
        '''The savepage bash script is got from here: 
        #https://github.com/abiyani/automate-save-page-as
        
        # List all available command line options.
        $ ./save_page_as --help

        save_page_as: Open the given url in a browser tab/window, perform 'Save As' operation and close the tab/window.

        USAGE:
        save_page_as URL [OPTIONS]

        URL                      The url of the web page to be saved.

        options:
        -d, --destination      Destination path. If a directory, then file is saved with default name inside the directory, else assumed to be full path of target file. Default = '.'
        -s, --suffix           An optional suffix string for the target file name (ignored if --destination arg is a full path)
        -b, --browser          Browser executable to be used (must be one of 'google-chrome' or 'firefox'). Default = 'google-chrome'.
        --load-wait-time       Number of seconds to wait for the page to be loaded (i.e., seconds to sleep before Ctrl+S is 'pressed'). Default = 4
        --save-wait-time       Number of seconds to wait for the page to be saved (i.e., seconds to sleep before Ctrl+F4 is 'pressed'). Default = 8
        -h, --help             Display this help message and exit.
        '''
        os.system(command)
        # #time.sleep(2)
        f.write("saved the page for {}".format(uni))
f.close()
#print(present_unis)
print("List of still absent universities")
print(absent_uni)