# coding=utf-8
import os
import sys
import time
import tqdm


from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

from utils.driver import check_webdriver

WEB_VPN = "https://wvpn.ustc.edu.cn/"
vpn_base_url = "https://wvpn.ustc.edu.cn/https/77726476706e69737468656265737421f9f244993f20645f6c0dc7a59d50267b1ab4a9/stampPDF/getPDF.jsp?tp=&arnumber={}&tag=1&ref="

class Driver(object):

    def __init__(self, gui_enable=True, save_path="./downloads"):
        self.gui_enable = gui_enable
        self.save_path = save_path
        os.makedirs(self.save_path, exist_ok=True)
        self._init_driver()

    def _init_driver(self):
        options = webdriver.chrome.options.Options()
        # GUI setting
        if not self.gui_enable:
            options.add_argument('--headless')

        options.add_argument('--disable-extensions')
        options.add_argument('--disable-gpu')  # avoid some bugs
        options.add_argument('--no-sandbox')
        options.add_argument('--mute-audio')
        options.add_argument('--window-size=800,800')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])

        prefs = {
            "profile.default_content_settings.popups": 0,
            "download.default_directory": self.save_path,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "plugins.always_open_pdf_externally": True,
            # "download.extensions_to_open": "applications/pdf"
        }
        options.add_experimental_option("prefs", prefs)

        driver_path = check_webdriver()

        self.driver = webdriver.Chrome(
            options=options, executable_path=driver_path)
        self.wait = WebDriverWait(self.driver, 20)

    def __del__(self):
        if hasattr(self, "driver"):
            try:
                self.driver.close()
            except Exception as e:
                print(f"退出时产生错误：{e}")


class Spider(Driver):

    def __init__(self, gui_enable, username, password, save_path):
        super().__init__(gui_enable=gui_enable, save_path=save_path)
        self.username = username
        self.password = password
        self._login_vpn()

    def _login_vpn(self):
        self.driver.get(WEB_VPN)
        time.sleep(1)
        assert "身份认证" in self.driver.title, self.driver.title
        username_input = self.driver.find_element_by_id("username")
        username_input.send_keys(self.username)
        password_input = self.driver.find_element_by_id("password")
        password_input.send_keys(self.password)
        login_btn = self.driver.find_element_by_id("login")
        login_btn.click()
        time.sleep(1)
        assert "WEBVPN" in self.driver.title, self.driver.title

    def download(self, file_path):
        assert os.path.isfile(file_path), file_path
        dois = []
        with open(file_path, "r") as f:
            lines = f.readlines()
        for item in lines:
            if item.startswith("doi: "):
                item = item.replace("doi: ", "")
                doi = item.split(".")[-1].strip()
                dois.append(doi)

        for doi in tqdm.tqdm(dois):
            print(doi)
            if "0{}.pdf".format(doi) in os.listdir(self.save_path):
                print("Skip!")
                continue
            url = vpn_base_url.format(doi)
            self.download_sigle(url)

        print("Done!")
        time.sleep(100)

    def download_sigle(self, url):
        self.driver.get(url)
        time.sleep(2)


if __name__=="__main__":

    assert len(sys.argv) == 4, (
        "\n".join([
            f"命令错误: python {' '.join(sys.argv)}",
            "="*30,
            "运行环境：python 3.5+",
            "安装第三方包：pip install -r requirements.txt",
            "使用方法: python spider.py txt_file_path uid pwd",
            "例如：python spider.py ./ICRA2020.txt SA18225034 123456"
        ])
    )

    file_path = sys.argv[1]
    params = {
        "username": sys.argv[2],
        "password": sys.argv[3],
        "save_path": f"{os.path.abspath('.')}/downloads",
    }


    d = Spider(gui_enable=True, **params)

    d.download(file_path=file_path)
