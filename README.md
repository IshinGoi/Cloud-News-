# 使用简介

## 步骤一 

申请企业微信	- 	https://work.weixin.qq.com/

然后打开 	-	<https://work.weixin.qq.com/wework_admin/frame#profile>

点击	-	我的企业 （英文`My Company`）

获得企业ID(Company ID)（`corpid`）

![image-20211108170922062](https://github.com/IshinGoi/Cloud-News-/blob/main/img/image-20211108170922062.png)

## 步骤二

> 生成一个企业微信应用，获得`AgentId` 和 `Secret`，这样可以通过企业微信API发送信息推送。

1. 应用管理（App Management）-> 创造一个应用(Create an app)

2. 填入你想要的应用名称和简介。
3. 点进应用中，查看`Secret`

![image-20211102201242650](https://github.com/IshinGoi/Cloud-News-/blob/main/img/image-20211102201242650.png)

## 步骤三

> 获得自身访问中国天气网时的cookie

1. 打开 http://www.weather.com.cn/weather1d/101280800.shtml
2. 填入你所在的城市后，点击搜索
3. `.shtml`前面的一串数字如`101280800`就是你城市的`ID`。
4. 按F12，点击Network选项卡，刷新网页，点击捕获的第一个包，在Headers里面找到`cookie`。

![image-20211108173228460](https://github.com/IshinGoi/Cloud-News-/blob/main/img/image-20211108173228460.png)

## 步骤四

1. 下载好该目录下的所有文件

2. 打开`main.py`，把开头`area_id`,`cookie`,`corpid`,`SECRET`修改成你的。

3. 尝试运行一下代码，看看有无问题。

   



## 步骤五

>  配置到云函数的具体教程

### 将代码和依赖库打包上传到云函数

```python
cd desktop/Cloud-news # 在cmd中CD到文件夹的位置
pip install requests -t . # 将需要的库指定导入到文件夹
```

### 同时在该目录下创建函数入口文件`index.py` （这一步我已经帮你做好了）

![image-20211102233925284](https://github.com/IshinGoi/Cloud-News-/blob/main/img/image-20211102233925284.png)

### 在文件夹内部将全部文件解压成zip后上传到云函数

![image-20211102234535075](https://github.com/IshinGoi/Cloud-News-/blob/main/img/image-20211102234535075.png)

### 上传至云端

![image-20211102233338423](https://github.com/IshinGoi/Cloud-News-/blob/main/img/image-20211102233338423.png)

### 设置定时触发器

![image-20211102233418949](https://github.com/IshinGoi/Cloud-News-/blob/main/img/image-20211102233418949.png)

