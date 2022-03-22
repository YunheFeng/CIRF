import os
from bs4 import BeautifulSoup
import base64
import shutil
import requests
import os
import codecs
import shutil

# path of collected images 
path_image = './collected_data_raw_top_200_Naver/'

for file_folder in os.listdir(path_image):
    # process html file
    if (os.path.isfile(os.path.join(path_image, file_folder))):
        f_html = file_folder
        print (f_html)
        # read html file into soup 
        page = open(path_image + f_html, encoding='utf-8')
        soup = BeautifulSoup(page.read(), features='lxml')
        # identify all images 
        sources = soup.find_all('img', class_='_image _listImage')
        # collect all images 
        list_src = []
        for i in range(len(sources)):
            try:
                src = sources[i].attrs['src']            
            except:
                print ('Error: {}'.format(sources[i]))
            list_src.append(src)

        path_image_ranked = path_image.replace('collected_data_raw', 'collected_data_ranked') + f_html.split('.html')[0] + '_ranked/'
        os.makedirs(path_image_ranked, exist_ok=True)
        
        # collect images
        set_img_format_orig = set()
        count_valid = 0 
        list_invalid_src = []
        for idx, src in enumerate(list_src):
            # already downloaded images 
            if (src.startswith(f_html.split('.html')[0])):
                # determine image format 
                img_format_orig = src.split('.')[-1]
                set_img_format_orig.add(img_format_orig)
                img_format_dst = '.jpg'
                dst = path_image_ranked + str(idx) + img_format_dst
                # copy image
                try:
                    shutil.copyfile(path_image + src, dst)
                    count_valid += 1
                except:
                    print ('Error src: {} cannot be found'.format(src))
            # other images 
            else:
                # print (src)
                # print ('error when parsing downloaded images')
                list_invalid_src.append(src)
                
        # check warnings and errors 
        if (len(set_img_format_orig) > 1):
            print ('Error: set_img_format_orig: {}'.format(set_img_format_orig))
        if (count_valid < 200):
            print ('Attention: {} not enough images'.format(count_valid))
            if (list_invalid_src != []):
                print ('!!!!Error: invalid src must be parsed and saved')
        for invalid_src in list_invalid_src:
            if (invalid_src not in list_src[count_valid:]):
                print ('Error: {} can be found'.format(invalid_src))
        print ('')


