# 推送天气、新闻和美句到微信

import time
import requests
import json
import convert_time

# --------------- main	---------------
# 填入你的区域ID
area_id = "填入你的区域ID" 
# 填入浏览器cookie
cookie = " 填入你浏览器访问中国天气网时的cookie"	
# 填入企业ID
corpid = "填入你注册企业微信时获得的企业ID"
# 企业应用密钥 Secret
SECRET = "填入你创造应用时获得的企业应用密钥Secret"

# --------------- 爬中国天气网 ---------------
def get_weather_info(cookie,area_id):
	headers = {
		'Cookie': cookie,
		'Host': 'd1.weather.com.cn',
		'Referer': 'http://www.weather.com.cn/',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36',
	}

	timestamp = int(time.time()) # 时间戳
	#url = f"http://d1.weather.com.cn/weather_index/{area_id}.html?_={timestamp}"#这个API貌似会傻掉，温度显示999。
	url = f"http://d1.weather.com.cn/dingzhi/{area_id}.html?_={timestamp}"
	html = requests.get(url,headers=headers).content.decode('utf-8')

	# 将网页源代码转变成json格式
	weather_info = json.loads(html.replace(f"var cityDZ{area_id} =","").split(f";var alarmDZ{area_id}")[0])['weatherinfo'] 
	# 天气预警	当没有天气预警时，将为空{"w":[]}
	weather_warning = json.loads(html.split(f"var alarmDZ{area_id} =")[1])

	# 显示信息
	if weather_warning['w']:
		warning_info = ""
		for each in weather_warning['w']:
			warning_info += f"{each}\t"
	elif not weather_warning['w']:
		warning_info = "当前无预警信息"
	
	#print(weather_info) #用来检测原json元素

	weather_messages = f"""	城市名称：{weather_info['cityname']}
	当前温度：{weather_info['temp']}
	最低温度：{weather_info['tempn']}
	天气情况：{weather_info['weather']}
	风力风向：{weather_info['wd']}\t{weather_info['ws']}
	预警信息：{warning_info}"""
	#print(weather_messages)
	return weather_messages

# --------------- 爬取新浪新闻排行版 ---------------
def get_news(news_type_index=1,top_type="day"):

	# 排行榜种类字典
	news_type_dict = {
		1:"www_www_all_suda_suda",	# 新闻总排行
		2:"qbpdpl",					# 全部频道评论
		3:"video_news_all_by_vv",	# 视频排行
		4:"news_china_suda",		# 国内新闻
		5:"news_world_suda",		# 国际新闻
		6:"news_society_suda",		# 社会新闻
		7:"sports_suda",			# 体育新闻
	}
	news_type = news_type_dict.get(news_type_index)
	if news_type == None:
		print("新闻类型选择出错。")
		return False


	headers = {
		'Referer': 'http://news.sina.com.cn/',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36'
	}
	params = {
		"top_type":top_type,						# 新闻榜型(日榜或者周榜)
		"top_cat":news_type,						# 新闻类型
		"top_time":time.strftime("%Y%m%d"),			# 新闻时间
		"top_show_num":10, 							# 获取新闻的数量
		"top_order":"DESC",							# 排行顺序
		"js_var":"news_",							# 该参数可无视，注释掉结果一样
	}
	url = "http://top.news.sina.com.cn/ws/GetTopDataList.php"
	r = requests.get(url,headers=headers,params=params)
	if (r.status_code !=200):
		print("新浪新闻API连接Error!")
		return False

	html = r.content.decode("utf-8")
	# 国内的 JS 返回值的格式都是形如 "var xxx = {json格式}"
	# var_name = html.split(" = ")[0]
	# var_json = html.split(" = ")[1].replace(";","")
	js = json.loads(html.split(" = ")[1].replace(";",""))
	news_dict = {}
	for each in js["data"]:
		news_dict[each["title"]]=each["url"]
	return news_dict

# --------------- 企业微信推送 ---------------
def wechat_push(content):
	# 获取应用token
	url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={corpid}&corpsecret={SECRET}"
	r = requests.get(url)
	if (r.status_code != 200):
		print("获取企业微信access_token失败.")
		r.close()
		return False
	access_token = r.json()["access_token"]
	r.close()


	# 通过API进行消息推送
	url = f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}"

	# 文本消息格式
	text_json = {
	   "touser" : "@all",
	   "msgtype" : "text",
	   "agentid" : 1000003,
	   "text" : {
	       "content" : content
	   },
	   "safe":0,
	}

	r = requests.post(url,json=text_json)
	if (r.status_code != 200):
		print(f"发送企业微信推送失败... Error Code: {r.json()['errcode']}")
		r.close()
		return False
	r.close()
	return True


# 将任何列表转换成文本
def convert_list_to_text(news_dict):
	content = ""
	counter = 0
	for each in news_dict:
		counter += 1
		content += f"{counter}  <a href=\"{news_dict.get(each)}\">{each}</a>\n"
	return content

def show(weather_info,news_text):
	old_t = time.time()
	new_t = convert_time.std_to_cn(old_t)
	content = (
		f"{time.strftime('日期：%Y-%m-%d(%a) 执行时间：%H:%M:%S',new_t)}\n" +
		"---------- 今日天气 ----------\n" +
		f"{weather_info}\n" +
		"(------------------------------)\n\n" +
		"---------- 今日新闻 -----------\n" +
		f"{news_text}\n"
		)
	return content



def run():

	weather_info = get_weather_info(cookie,area_id)
	news_dict = get_news()

	if news_dict:
		news_text = convert_list_to_text(news_dict)
		content = show(weather_info,news_text)
		print(content)
		if wechat_push(content):
			print("推送发送成功。")
			return True
	return False

if __name__ == "__main__":
	run()
