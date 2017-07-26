# python-itchat
基于[itchat](http://itchat.readthedocs.io/zh/latest) 的python微信个人项目

##### 步骤

项目主要文件是 gif 文件夹 和 weixin.py 下载这两个到本地电脑

1. 安装[pyhton3]( https://www.python.org/downloads/)最新版 安装时请加入到系统环境变量

2. 安装一个第三方库——Python Imaging Library 

   ```pip install Pillow```

3. 安装一个pymysql

   ```pip install pymysql```

4. 安装 [itchat](http://itchat.readthedocs.io/zh/latest) 库 

   ```pip install itchat```

5. 修改 weixin.py 113行key  请自行到图灵机器人官网申请key

   网址 http://www.tuling123.com

6. 修改数据库配置 weixin.py 167行 改为自己的 执行建表语句

```

 CREATE TABLE `friends` (
   `id` int(11) NOT NULL AUTO_INCREMENT,
   `NickName` varchar(255) DEFAULT NULL COMMENT '昵称',
   `PYInitial` varchar(255) DEFAULT NULL,
   `PYQuanPin` varchar(255) DEFAULT NULL,
   `RemarkName` varchar(255) DEFAULT NULL COMMENT '备注',
   `RemarkPYInitial` varchar(255) DEFAULT NULL,
   `RemarkPYQuanPin` varchar(255) DEFAULT NULL,
   `Sex` varchar(255) DEFAULT NULL COMMENT '性别 1 男 2 女',
   `Province` varchar(255) DEFAULT NULL COMMENT '省',
   `City` varchar(255) DEFAULT NULL COMMENT '城市',
   `Signature` varchar(255) DEFAULT NULL COMMENT '个人签名',
   PRIMARY KEY (`id`)
 ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;

```
7. 到当前目录命令行执行 
   ``` python weixin.py ```
   手机微信扫描登录


**目前实现功能**

-  图灵机器人自动回复文本信息 msg
-  随机回复图片信息 随机图片放在gif目录中
-  获取所有好友头像 合成为一张大图
-  下载用户发送的图片 附件 录音 视频文件 （[itchat](http://itchat.readthedocs.io/zh/latest) 存在问题,存在下载失败的情况）

