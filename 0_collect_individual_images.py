import time
from selenium import webdriver
import pyautogui
from selenium.webdriver.common.keys import Keys
import os 
import pyperclip

def download_images(browser, keyword, category, search_engine, lang):
    """download images for given keywords and search engines

    Args:
        browser: Chrome or Firfox
        keyword (string): keyword
        category (string): category
        search_engine (string): can be one of 'Google', 'Baidu', 'Naver', and 'Yandex'
        lang: can be one of 'en', 'zh-cn', 'ko', 'ru'
    """    
    # settings
    count_page_down_press = 30
    sleep_time_per_press = 0.5
    sleep_time_for_save = 30 
    str_keywords = keyword.replace(' ', '+')
    str_keywords = str_keywords.replace(':', '+')
    str_keywords = str_keywords.replace('/', '')
    if (lang in ['en', 'zh-cn', 'ko', 'ru']):
        if (search_engine == 'Google'):
            url = 'https://www.google.com/search?q=' + str_keywords + '&tbm=isch'
        elif (search_engine == 'Baidu'):
            url = 'https://image.baidu.com/search/index?tn=baiduimage&word=' + str_keywords
        elif (search_engine == 'Naver'):
            # count_page_down_press = 7
            url = 'https://search.naver.com/search.naver?where=image&sm=tab_jum&query=' + str_keywords 
        elif (search_engine == 'Yandex'):
            url = 'https://yandex.com/images/search?text=' + str_keywords 
            # sleep_time_for_save = 10
        else:
            print ('unable to process ' + search_engine)
            return 
    else:
        print ('unable to process ' + lang)
        return 
    saved_file_name = search_engine + '_' + category + '_' + str_keywords + '_results.html'
    # initialize browser 
    # Chrome
    if (browser == 'Chrome'):
        if (os.name == 'nt'):
            options = webdriver.ChromeOptions()
            options.add_experimental_option('excludeSwitches', ['enable-logging'])
            driver = webdriver.Chrome(options=options)
        else:
            driver = webdriver.Firefox(executable_path=r'./geckodriver')
    # Firefox 
    elif (browser == 'Firefox'):
        if (os.name == 'nt'):
            driver = webdriver.Firefox()
        else:
            driver = webdriver.Firefox(executable_path=r'./geckodriver')
    else:
        print ('incorrect browser')
    driver.get(url)
    # scroll down and up the webpage
    try:
        html = driver.find_element_by_tag_name('html')
        for count in range(count_page_down_press):
            html.send_keys(Keys.PAGE_DOWN)
            time.sleep(sleep_time_per_press)
        for count in range(count_page_down_press):
            html.send_keys(Keys.PAGE_UP)
            time.sleep(sleep_time_per_press)
        for count in range(count_page_down_press):
            html.send_keys(Keys.PAGE_DOWN)
            time.sleep(sleep_time_per_press)
    except:
        pass
    # save all files 
    pyautogui.hotkey('ctrl', 's')
    time.sleep(5)
    # pyautogui.typewrite(saved_file_name)
    pyperclip.copy(saved_file_name)
    pyautogui.hotkey("ctrl", "v")
    pyautogui.hotkey('enter')
    pyautogui.hotkey('enter')
    time.sleep(sleep_time_for_save)
    driver.quit()

lang = 'en'
category = 'top_200'
search_engine = 'Google'
# search_engine = 'Baidu'
# search_engine = 'Naver'
# search_engine = 'Yandex'
# browser = 'Chrome'
browser = 'Firefox'

# path of processed category 
f_csv_name = './search_terms.csv'

flag_reverse = False
list_waiting = []
set_processed = set()
with open (f_csv_name, mode='r', encoding='utf-8') as f_r:
    # read keywords
    list_line = [line for line in f_r]
    if (flag_reverse):
        list_line.reverse()
    # list_line = list_line[:65]
    for line in list_line:
        keyword = line.strip()
        # check whether the keyword has been processed
        str_keywords = keyword.replace(' ', '+')
        str_keywords = str_keywords.replace(':', '+')
        str_keywords = str_keywords.replace('/', '')
        html_name = search_engine + '_' + category + '_' + str_keywords + '_results.html'
        if (html_name in set_processed):
            pass
        else:
            try:
                download_images(browser, keyword, category, search_engine, lang)
                # print (html_name)
                # list_waiting.append(html_name)
            except:
                pass 
