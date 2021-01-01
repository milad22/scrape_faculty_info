from selenium.webdriver.remote.command import Command
import cv2
import pandas as pd
import os,fnmatch

unis_dataframe = pd.read_excel('Physics_departments_formatted.xlsx', na_values = 'None')
webpages_path = '/home/miliverse/pages/'
#Make haar_cascade to be used later for face recognition
xml_file_path = '/home/miliverse/faculty_data_scrapping_project/scrape_faculty_info/scrape_faculty_info/face_recognition_xml_data/haarcascades/haarcascade_frontalface_alt.xml'
haar_cascade_face = cv2.CascadeClassifier(xml_file_path)

for index, row in unis_dataframe.iterrows():
    uni = row['University']
    #Make a list of photos inside the webpage files
    #https://stackabuse.com/python-list-files-in-a-directory/
    dir_path = webpages_path + uni + '_files/'
    photos_list = []
    pattern1 = '*jpg'
    pattern2 = '*jpeg'
    pattern3 = '*png'
    pattern4 = '*JPG'
    try:
        files_list = os.listdir(dir_path)
        for entry in files_list:
            if fnmatch.fnmatch(entry, pattern1) or fnmatch.fnmatch(entry, pattern2) or fnmatch.fnmatch(entry, pattern3) or fnmatch.fnmatch(entry, pattern4):
                photos_list.append(entry)            
        #print(len(photos_list))
    except:
        print("Couldn't find photos directory for {}".format(uni))
        continue
    #find number of personal photos for each directory webpage
    personal_photos_count = 0
    for photo in photos_list:
        photo_path = dir_path + photo
        try:
            frame = cv2.imread(photo_path)
            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame_gray = cv2.equalizeHist(frame_gray)
            faces = haar_cascade_face.detectMultiScale(frame_gray)
            if len(faces) == 1:
                personal_photos_count += 1
        except:
            print("Couldn't process the image {} in {} files".format(photo,uni))
    #print('Number of persnal photos for {} is {}'.format(uni,personal_photos_count))
    unis_dataframe.loc[index, 'directory_page_personal_photo_count'] = personal_photos_count
  

unis_dataframe.to_excel('Physics_departments_formatted_with_photo_counts.xlsx', index=False)