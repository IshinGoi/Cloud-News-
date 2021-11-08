# 国际时间转中国时间
import time

# 标准时间转中国时间
def std_to_cn(t = time.time()):
	# 手动增加8小时
	new_t = time.strptime(time.ctime(t + 8*60*60))
	return new_t
