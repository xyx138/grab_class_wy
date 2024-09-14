# grab_class_wy
捡漏**外语**课的python脚本



## 注意事项：
1. 运行该脚本时请**关闭科学上网**
2. 脚本的侧重点**自动化捡漏**，在放开选课的时间节点，不保证能选上课，且不建议在此时使用该脚本给学校的土豆服务器增加压力
3. python和ide的安装请自行查找资料

## 快速启动

1. 安装chrome浏览器及驱动( `resource` 文件夹中)
   - 安装chrome浏览器:  ChromeSetup.exe

   - 配置驱动到环境变量

     - 解压.zip文件，并复制解压后的文件地址

       ![image-20240914224242168](https://raw.githubusercontent.com/xyx138/cloudimg/master/img/image-20240914224242168.png)

     - 屏幕底部搜索 “编辑系统环境变量” 并打开

     - 点击 “环境变量”

     - 在 “系统变量” 中找到 Path ， 点击并添加刚才复制的地址

       ![image-20240914223932292](https://raw.githubusercontent.com/xyx138/cloudimg/master/img/image-20240914223932292.png)

       ![image-20240914224012962](https://raw.githubusercontent.com/xyx138/cloudimg/master/img/image-20240914224012962.png)

2. 下载相关库

   进入 `code` 目录，执行下面的命令

   ```bash
   pip install -r requirements.txt
   ```

3. 运行python程序

   进入 `code` 目录，执行下面的命令

   ```cmd
   python main.py
   ```

4. 扫码登录

​	弹出浏览器，扫码确定后，要等待几秒才能进入选课系统，**请不要关闭浏览器**。程序会自动点击几次打开的浏览器，然后**自动关闭**

5. 耐心等待

​	不要停止程序，抢到的课程会写入 `result.txt`

​	![image-20240914222010793](https://raw.githubusercontent.com/xyx138/cloudimg/master/img/image-20240914222010793.png)

