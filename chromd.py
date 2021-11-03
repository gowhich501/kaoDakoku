from selenium import webdriver

#chromedriverの場所を指定
driver = webdriver.Chrome("C:/Goichi/App/chromedriver/chromedriver.exe")
driver.get("https://www.google.co.jp/")
search = driver.find_element_by_name('q')   # HTML内で検索ボックス(name='q')を指定する
search.send_keys('GOICHI ITABSHI')             # 検索ワードを送信する
search.submit()  