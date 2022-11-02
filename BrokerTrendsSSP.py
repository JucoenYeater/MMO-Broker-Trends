# -*- coding: utf-8 -*-
"""
Created on Thu Sep 29 02:02:50 2022

@author: jucoe
"""

import cv2, csv, time, sched, schedule, imutils, re
import pytesseract
import PIL.ImageGrab
import numpy as np
import pyautogui as pag
from datetime import datetime, timedelta


# Compile search list, look into converting this to dictionary in future after mvp
# search_list = ['krono','succulent root','indium cluster','severed sandalwood','beryllium cluster',
#                'lambent material','ireheart radish','saguaro root','scaled leather pelt',
#                'rough pearl','vanadium cluster','cobalt cluster','severed ironwood']

mats = ['tin cluster','tuber strand','carbonite cluster','belladonna root','feyiron cluster',
        'tussah root','fulginate cluster','ashen root','indium cluster','succulent root',
        'severed sandalwood']

mats_rare = ['ireheart radish','lambent material','scaled leather pelt','rough pearl',
             'vanadium cluster','cobalt cluster']

item_hv = ['krono']

search_list = item_hv + mats_rare + mats


search_list3 = ['indium cluster']


# Clear Search Box Coordinates
search_loc_x = 232
search_loc_y = 52

# Find Button Coordinates
find_loc_x = 290
find_loc_y = 52




# Location of tesseract executable
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


#s = sched.scheduler(time.time, time.sleep)
#def do_something(sc):


# Definition for Schedule to run
s = sched.scheduler(time.time, time.sleep)
def BrokerTrendsMain(sc):
    # Iteration Start Time
    time1 = time.time()
    
    # Let user know next iteration is running
    print('Lets Trend that Broker baby!')
    
    # Ensure game window is forefront
    pag.click(search_loc_x, search_loc_y, duration=0.5)
    
    # Reset datetime list
    datetime_list = []
    
    # # Iterate through search_list and takes snippets of broker prices then saves thme as png
    for item in range(len(search_list)):
        
        # Click the x in the Broker search box
        pag.click(search_loc_x, search_loc_y, duration=0.5)
        time.sleep(0.5)
        
        # Input item to search from search_list
        pag.write(search_list[item],interval=0.05)
        time.sleep(0.5)
        
        # Click the Find Button
        pag.click(find_loc_x, find_loc_y, duration=0.5)
        time.sleep(1)
        
        # Take snip of name, quantity, price
        im_qty = PIL.ImageGrab.grab(bbox=(5,115,65,480))
        im_pri = PIL.ImageGrab.grab(bbox=(190,115,310,480))
    
        # Store datetime stamps to include in price file
        datetime_list.append(datetime.now() - timedelta(minutes=datetime.now().minute % 1,
                             seconds=datetime.now().second, microseconds=datetime.now().microsecond))
        
        # Save screenshot using item name (replacing ' ' with '_')
        im_qty.save(fr"C:\Users\jucoe\OneDrive\Personal\Video Games\EverquestII\BrokerTrends\ScreenshotsSP\{search_list[item].replace(' ', '_')}_qty.png")
        im_pri.save(fr"C:\Users\jucoe\OneDrive\Personal\Video Games\EverquestII\BrokerTrends\ScreenshotsSP\{search_list[item].replace(' ', '_')}_pri.png")
        #time.sleep(1)
    
    # Parameters
    p = 170 # threshold value (180 seems to be perfect for price text)sh
    q = 255 # Max value in threshold
    j = 0 # Increment for dictionary key value
    im_list = ['qty','pri'] # List to append to name of files
    param_list = [p,p,p] # threshold value list
    file_mode = 'a' # File write mode, 'a' is append, 'w' is write
    records = {} # Empty dictionary to set up records to send to MySql database
    records_bad = {} # Empty dictionary to set up bad records to fix later
    
    # Configure parameters for tesseract
    custom_config_qty = r'--psm 6 -c tessedit_char_whitelist=0123456789'
    custom_config_price = r'--psm 6 -c tessedit_char_whitelist=0123456789pgsc'
    custom_config_list = [custom_config_qty, custom_config_price]
    
    # Pull item name, quantity sold, and price from screenshots
    for y in range(len(im_list)):
        for x in range(len(search_list)):
            image = cv2.imread(rf"C:\Users\jucoe\OneDrive\Personal\Video Games\EverquestII\BrokerTrends\ScreenshotsSP\{search_list[x].replace(' ','_')}_{im_list[y]}.png")
            image = cv2.resize(image,None,fx=5,fy=5,interpolation=cv2.INTER_CUBIC)
            
            # Rotate Image test
            image = imutils.rotate_bound(image, 1)
            
            # hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            # Convert image to grayscale
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Invert white and black
            # gray_image = cv2.bitwise_not(gray_image)
            
            # Noise Removal
            # blur_image = cv2.GaussianBlur(gray_image,(5,5),0)
            
            if y == 0:
                continue
                # # Filter
                # kernel = np.ones((5,5),np.float32)/25
                # dst = cv2.filter2D(gray_image,-1,kernel)
            
                # Text has color so we must threshold to get accurate results
                threshold_image = cv2.threshold(gray_image, p, q, cv2.THRESH_BINARY)[1]# + cv2.THRESH_OTSU)[1]h
                
                
                nlabels, labels, stats, centroids = cv2.connectedComponentsWithStats(threshold_image, None, None, 8, cv2.CV_32S)
                areas = stats[1:,cv2.CC_STAT_AREA]
                
                result = np.zeros((labels.shape), np.uint8)
                
                for i in range(0, nlabels - 1):
                    if areas[i] >= 100:
                        result[labels == i+1] = 255
                        
                details_ti = pytesseract.image_to_data(result, output_type=pytesseract.Output.DICT, config=custom_config_list[y],lang='eng')
                
                
                details_gi = list(filter(None,details_ti['text']))
                
                parse_text_ti = []
                word_list_ti = []
                last_word_ti = ''
                
                for word_ti in details_ti['text']:
                    if word_ti != '':
                        word_list_ti.append(f'{search_list[x]}, {word_ti}, {datetime_list[x]}')
                        last_word_ti = word_ti
                    if (last_word_ti!='' and word_ti=='') or (word_ti==details_ti['text'][-1]):
                        parse_text_ti.append(word_list_ti)
                        word_list_ti=[]
                        
                with open(fr"C:\Users\jucoe\OneDrive\Personal\Video Games\EverquestII\BrokerTrends\ImageTextOutput\{search_list[x]} {im_list[y]}_ti.txt",file_mode,newline="") as file:
                    csv.writer(file,delimiter=" ").writerows(parse_text_ti)
                
            else:
                # Threshold the gray scale image
                threshold_image = cv2.threshold(gray_image,75,255,cv2.THRESH_BINARY)[1]
                
                threshold_image = cv2.bitwise_not(threshold_image)
                
                # Show each threshold image
                # cv2.imshow('black',threshold_image)
                # cv2.waitKey(0)
                # cv2.destroyAllWindows()
                
                # Image anaylsis using Tesseract.
                details_gi = pytesseract.image_to_data(threshold_image, output_type=pytesseract.Output.DICT, config=custom_config_list[y],lang='eng')
                
                # Remove empty values, should result with a list of ~8 non-empty elements
                details_gi_filter = list(filter(None,details_gi['text']))
                
                # Remove any extra elements
                if len(details_gi_filter) > 8:
                    # Keep removing until only 8 elements remain
                    while len(details_gi_filter) > 8:
                        del details_gi_filter[-1]
         
                # Used as a manual check
                print(details_gi_filter)
                
                # Set constants and reset lists
                parse_text_gi = []
                word_list_gi = []
                word_list_gi_int = [search_list[x]]
                word_list_gi_bad = [search_list[x]]
                last_word_gi = ''
                
                # New way that creates a dictionary to upload to MySql
                for word_gi in details_gi_filter:
                    # Append good data to records
                    if re.match(r"^(?:\d+p)?(?:\d\d?g)?(?:\d\d?s)?(?:\d\d?c)?$",word_gi):
                        # Append to list with item name and screenshot datetime
                        word_list_gi_int.append(word_gi)
                        word_list_gi_int.append(datetime_list[x].strftime("%Y-%m-%d %H:%M:%S"))
                    
                        # Update dictionary with new list that acts as a record
                        records[str(j)] = []
                        records.update({str(j): word_list_gi_int})
                        
                        # Increment Index
                        j += 1
                        
                        # Reset word_list_gi_int to set for the next record
                        word_list_gi_int = [search_list[x]]
                        
                    # Append bad data to records_bad
                    else:
                        # Append to list with item name and screenshot
                        word_list_gi_bad.append(word_gi)
                        word_list_gi_bad.append(datetime_list[x].strftime("%Y-%m-%d %H:%M:%S"))
                        
                        records_bad[str(j)] = []
                        records_bad.update({str(j): word_list_gi_bad})
                        
                        # Increent Index
                        j += 1
                    
                        # Reset word_list_gi_bad to set for the next record
                        word_list_gi_bad = [search_list[x]]
                 
                
                
                # # Old way so we can keep writing the data to a text file       
                # for word_gi in details_gi['text']:
                #     if word_gi != '':
                #         word_list_gi.append(word_gi)
                #         last_word_gi = word_gi
                #     if (last_word_gi!='' and word_gi=='') or (word_gi==details_gi['text'][-1]):
                #         parse_text_gi.append(word_list_gi)
                #         word_list_gi=[]
                        
                #parse_text_gi_dict = {item[0]: item[1:] for item in parse_text_gi}
                
    with open(r"C:\Users\jucoe\OneDrive\Personal\Video Games\EverquestII\BrokerTrends\ImageTextOutput\master_price_sp.txt",file_mode,newline="") as file:
        #file.write(json.dumps(records))
        for key, value in records.items():
            file.write(key + ', ' + value[0] + ', ' + value[1] + ', ' + value[2] + '\n')
            #csv.writer(file,delimiter=" ").writerow(key, value)
            print(key, value)
        file.close()
            
    with open(r"C:\Users\jucoe\OneDrive\Personal\Video Games\EverquestII\BrokerTrends\ImageTextOutput\master_price__sp_bad.txt",file_mode,newline="") as file:
        #file.write(json.dumps(records))
        for key, value in records_bad.items():
            file.write(key + ', ' + value[0] + ', ' + value[1] + ', ' + value[2] + '\n')
            #csv.writer(file,delimiter=" ").writerow(key, value)
            print(f"Bad Data: {key}, {value}")
        file.close()
        
    time2 = time.time() - time1
    
    s.enter(900 - time2, 1, BrokerTrendsMain, (sc,))

s.enter(0, 1, BrokerTrendsMain, (s,))
s.run()
                    
                # cv2.imshow('black',threshold_image)
                # cv2.waitKey(0)
                # cv2.destroyAllWindows()
            
            # Text has color so we must threshold to get accurate results
            # erthreshold_blur_image = cv2.threshold(blur_image, param_list[x], q, cv2.THRESH_BINARY)[1]# + cv2.THRESH_OTSU)[1]
        
            # Feed image to tesseract
            #details_i = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT, config=custom_config_list[y],lang='eng')
            #details_gi = pytesseract.image_to_data(gray_image, output_type=pytesseract.Output.DICT, config=custom_config_list[y],lang='eng')
            #details_bi = pytesseract.image_to_data(blur_image, output_type=pytesseract.Output.DICT, config=custom_config_list[y],lang='eng')
            #details_ti = pytesseract.image_to_data(result, output_type=pytesseract.Output.DICT, config=custom_config_list[y],lang='eng')
            #details_bti = pytesseract.image_to_data(threshold_blur_image, output_type=pytesseract.Output.DICT, config=custom_config_list[y],lang='eng')
        
        
            # ##################
            # # Accuracy Check #
            # ##################
            # total_boxes_i = len(details_i['text'])
            # total_boxes_gi = len(details_gi['text'])
            # total_boxes_ti = len(details_ti['text'])
            
            # for sequence_number in range(total_boxes_i):
            #     if int(details_i['conf'][sequence_number]) > 30:
            #         (x,y,w,h) = (details_i['left'][sequence_number],details_i['top'][sequence_number],
            #                      details_i['width'][sequence_number],details_i['height'][sequence_number])
                    
            #         threshold_image = cv2.rectangle(threshold_image,(x,y),(x+w,y+h),(0,255,0),2)
                    
            # Display image
            # cv2.imshow('captured text',threshold_image)
            
            # Maintain output windows until key press
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()
        
        
            #########################
            # Insert text into file #
            #########################
            # parse_text_i = []
            # word_list_i = []
            # last_word_i = ''
            
            # parse_text_gi = []
            # word_list_gi = []
            # last_word_gi = ''
            
            # parse_text_bi = []
            # word_list_bi = []
            # last_word_bi = ''
            
            # parse_text_ti = []
            # word_list_ti = []
            # last_word_ti = ''
            
            # parse_text_bti = []
            # word_list_bti = []
            # last_word_bti = ''
            
            # for word_i in details_i['text']:
            #     if word_i != '':
            #         word_list_i.append(word_i)
            #         last_word_i = word_i
            #     if (last_word_i!='' and word_i=='') or (word_i==details_i['text'][-1]):
            #         parse_text_i.append(word_list_i)
            #         word_list_i=[]
                    
            # for word_gi in details_gi['text']:
            #     if word_gi != '':
            #         word_list_gi.append(word_gi)
            #         last_word_gi = word_gi
            #     if (last_word_gi!='' and word_gi=='') or (word_gi==details_gi['text'][-1]):
            #         parse_text_gi.append(word_list_gi)
            #         word_list_gi=[]
                    
            # for word_bi in details_bi['text']:
            #     if word_bi != '':
            #         word_list_bi.append(word_bi)
            #         last_word_bi = word_bi
            #     if (last_word_bi!='' and word_bi=='') or (word_bi==details_bi['text'][-1]):
            #         parse_text_bi.append(word_list_bi)
            #         word_list_bi=[]
                    
            # for word_ti in details_ti['text']:
            #     if word_ti != '':
            #         word_list_ti.append(word_ti)
            #         last_word_ti = word_ti
            #     if (last_word_ti!='' and word_ti=='') or (word_ti==details_ti['text'][-1]):
            #         parse_text_ti.append(word_list_ti)
            #         word_list_ti=[]
                    
            # for word_bti in details_bti['text']:
            #     if word_bti != '':
            #         word_list_bti.append(word_bti)
            #         last_word_bti = word_bti
            #     if (last_word_bti!='' and word_bti=='') or (word_bti==details_bti['text'][-1]):
            #         parse_text_bti.append(word_list_bti)
            #         word_list_bti=[]
                    
            # Convert results to text file
            # with open(fr"C:\Users\jucoe\OneDrive\Personal\Video Games\EverquestII\BrokerTrends\ImageTextOutput\{search_list[x]} {im_list[y]}_i.txt",'w',newline="") as file:
            #     csv.writer(file,delimiter=" ").writerows(parse_text_i)
                
            # with open(fr"C:\Users\jucoe\OneDrive\Personal\Video Games\EverquestII\BrokerTrends\ImageTextOutput\{search_list[x]} {im_list[y]}_gi.txt",'w',newline="") as file:
            #     csv.writer(file,delimiter=" ").writerows(parse_text_gi)
                
            # with open(fr"C:\Users\jucoe\OneDrive\Personal\Video Games\EverquestII\BrokerTrends\ImageTextOutput\{search_list[x]} {im_list[y]}_bi.txt",'w',newline="") as file:
            #     csv.writer(file,delimiter=" ").writerows(parse_text_bi)
                
            # with open(fr"C:\Users\jucoe\OneDrive\Personal\Video Games\EverquestII\BrokerTrends\ImageTextOutput\{search_list[x]} {im_list[y]}_ti.txt",'w',newline="") as file:
            #     csv.writer(file,delimiter=" ").writerows(parse_text_ti)
                
            # with open(fr"C:\Users\jucoe\OneDrive\Personal\Video Games\EverquestII\BrokerTrends\ImageTextOutput\{search_list[x]} {im_list[y]}_bti.txt",'w',newline="") as file:
            #     csv.writer(file,delimiter=" ").writerows(parse_text_bti)
            
            
            # cv2.imshow('image',image)
            # cv2.waitKey(0)
            
            # print(pytesseract.image_to_string(Image.open(r"C:\Users\jucoe\OneDrive\Personal\Video Games\EverquestII\Screenshots\Capture.png")))
            
            # d = pytesseract.image_to_string(image)
            # print(d)