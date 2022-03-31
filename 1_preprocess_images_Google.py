import os
from bs4 import BeautifulSoup
import base64
import shutil
import requests

# path of collected images 
path_image = './collected_data_raw_top_200_Google/'

for file_folder in os.listdir(path_image):
    # process html file
    if (os.path.isfile(os.path.join(path_image, file_folder))):
        f_html = file_folder
        # read html file into soup 
        page = open(path_image + f_html, encoding='utf-8')
        soup = BeautifulSoup(page.read(), features='lxml')
        # identify all images 
        sources = soup.find_all('img', class_='rg_i Q4LuWd')
        # collect all images 
        list_src = []
        for i in range(len(sources)):
            try:
                src = sources[i].attrs['src']            
            except:
                try:
                    src = sources[i].attrs['data-src']
                except:
                    print ('error: {}'.format(sources[i]))
            list_src.append(src)
        # print (list_src)

        # we have three types of images sources: base64, already downloaded image, and image URL
        path_image_ranked = path_image.replace('collected_data_raw', 'collected_data_ranked') + f_html.split('.html')[0] + '_ranked/'
        os.makedirs(path_image_ranked, exist_ok=True)
        
        # collect images 
        for idx, src in enumerate(list_src):
            # base64
            if (src.startswith('data:image/')):
                # determine image format 
                img_format = src.split('data:image/')[-1].split(';')[0]
                if (img_format == 'jpeg'):
                    img_format = 'jpg'
                else:
                    print (img_format)
                str_base64 = src.split('base64,')[-1]
                dst = path_image_ranked + str(idx) + '.' + img_format
                # convert base64 into image 
                with open(dst, 'wb') as f:
                    f.write(base64.urlsafe_b64decode(str_base64))
            # already downloaded images 
            elif (src.startswith(f_html.split('.html')[0])):
                # determine image format 
                img_format = src.split('.')[-1]
                dst = path_image_ranked + str(idx) + '.' + img_format
                # copy image
                shutil.copyfile(path_image + src, dst)
            # image URL 
            elif (src.startswith('https://')):
                img_format = 'jpg'
                dst = path_image_ranked + str(idx) + '.' + img_format
                try:
                    # Open the url image, set stream to True, this will return the stream content.
                    r = requests.get(src, stream = True, proxies={"http": "http://111.233.225.166:1234"}, verify=False)
                    # Check if the image was retrieved successfully
                    if r.status_code == 200:
                        # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
                        r.raw.decode_content = True
                        # Open a local file with wb ( write binary ) permission.
                        with open(dst,'wb') as f:
                            shutil.copyfileobj(r.raw, f)
                    else:
                        print('{} image couldn\'t be retrieved'.format(src))
                except:
                    print ('an error occurs when retriving {}'.format(src))
            else:
                print ('cannot be processed image source: {}'.format(src))

