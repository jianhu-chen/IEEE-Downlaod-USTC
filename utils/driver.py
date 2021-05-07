# -*- encoding: utf-8 -*-
# here put the import lib
import os
import sys
import requests
import zipfile


def unzip(zip_path: str):
    extra_path = os.path.dirname(zip_path)
    with zipfile.ZipFile(zip_path) as f:
        f.extractall(extra_path)
    os.remove(zip_path)


def download_driver(os_name, save_path):
    url_prefix = "http://chromedriver.storage.googleapis.com"
    latest_url = "http://chromedriver.storage.googleapis.com/LATEST_RELEASE"
    latest_version = requests.get(latest_url).text
    print(f"The latest version is: {latest_version}")

    if os_name == "linux":
        file_name = "chromedriver_linux64.zip"
    elif os_name == "windows":
        file_name = "chromedriver_win32.zip"
    else:
        file_name = "chromedriver_mac64.zip"

    url = '/'.join([url_prefix, latest_version, file_name])
    response = requests.get(url)

    zip_path = os.path.join(save_path, file_name)
    if os.path.exists(zip_path):
        os.remove(zip_path)
    with open(zip_path, "wb") as f:
        f.write(response.content)

    unzip(zip_path)


def check_webdriver():
    os_name = sys.platform
    if "darwin" in os_name:
        os_name = "Mac OS"
    elif "win" in os_name:
        os_name = "Windows"
    elif "linux" in os_name:
        os_name = "Linux"
    else:
        raise RuntimeError(f"Unknow OS: {os_name}")

    print(f"OS: {os_name}")

    driver_root = os.path.abspath(__file__).split("utils")[0]
    save_path = os.path.join(driver_root, "webdriver")
    os.makedirs(save_path, exist_ok=True)

    driver_path = os.path.abspath(os.path.join(save_path, "chromedriver"))

    if "win" in os_name:
        driver_path += ".exe"

    if os.path.exists(driver_path):
        print(f"检测到webdriver, 路径为: {driver_path}")
    else:
        print("开始自动下载chrome webdriver ...",)
        download_driver(os_name, save_path=save_path)
        assert os.path.exists(driver_path), ("自动下载chrome webdriver失败, 请尝试重新运行或手动下载.")
        print(f"下载成功, 保存至: {driver_path} ...")
        if "win" not in os_name:
            print(f"chmod +x {driver_path}")
            os.system(f"chmod +x {driver_path}")

    return driver_path


if __name__ == "__main__":
    check_webdriver()
