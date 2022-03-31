import os
from bs4 import BeautifulSoup
from PIL import Image
from webptools import dwebp

# path of collected images 
path_image = './collected_data_raw_top_200_Yandex/'

for file_folder in os.listdir(path_image):
    # process html file
    if (os.path.isfile(os.path.join(path_image, file_folder))):
        f_html = file_folder
        print (f_html)
        # read html file into soup 
        page = open(path_image + f_html, encoding='utf-8')
        soup = BeautifulSoup(page.read(), features='lxml')
        # identify all images 
        sources = soup.find_all('img', class_='serp-item__thumb justifier__thumb')
        # collect all images 
        list_src = []
        for i in range(len(sources)):
            try:
                src = sources[i].attrs['src']            
            except:
                print ('error: {}'.format(sources[i]))
            list_src.append(src)
        # print (list_src)

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
                    # only process the first 200 images 
                    if (count_valid < 200):
                        # shutil.copyfile(path_image + src, dst)
                        if (src.endswith('.webp')):
                            dwebp(input_image = path_image + src, output_image = dst, option="-o", logging="-v")
                        else:
                            im = Image.open(path_image + src).convert('RGB')
                            im.save(dst, 'jpeg')
                        count_valid += 1
                except:
                    print ('src: {}'.format(src))
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
            