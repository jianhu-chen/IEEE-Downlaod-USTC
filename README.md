# IEEE-Downlaod-USTC



## 环境

1. Python 3+
2. 安装第三方依赖库

```
pip install -r requirements.txt
```

## 使用方法

1. 准备索引文件，例如`ICRA2020.txt`，一篇文章的基本格式为：

   ```
   W. N. Greene and N. Roy, "Metrically-Scaled Monocular SLAM using Learned Scale Factors," 2020 IEEE International Conference on Robotics and Automation (ICRA), Paris, France, 2020, pp. 43-50.
   doi: 10.1109/ICRA40945.2020.9196900
   keywords: {Simultaneous localization and mapping;Feature extraction;Cameras;Loss measurement;Neural networks;Estimation},
   URL: http://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=9196900&isnumber=9196508
   ```

   - 第1行为`作者,  "文章名" 会议相关信息`

   - 第2行为 doi

   - 第3行为关键
   - 第4行为网页地址

2. 运行下载脚本

   ```
   python spider.py txt_file_path uid pwd
   ```

   uid和pwd分别为学号和密码，用于登陆VPN。

3. 待全部下载完毕后，可以在`./downlaods`文件夹中找到所有下载好的论文。

4. （可选）改名：改名前文件以`[doi].pdf`命名，改名后文件以`[name]_[doi].pdf`命名。

   ```
   python rename.py txt_file_path
   ```

   

   