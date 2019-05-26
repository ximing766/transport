#!/usr/bin/env python
# coding: utf-8

# In[1]:

#!/usr/bin/env python
# coding: utf-8

# In[272]:

import pandas as pd
import numpy as np
#import folium
import matplotlib.pyplot as plt
import geocoder 
#from arcgis.gis import GIS
#from IPython.display import display
get_ipython().run_line_magic('matplotlib', 'inline')
# # fer

# In[348]:


wcondition = pd.read_csv(r'D:\CAllData\7C\weatherC.csv')
data = pd.read_csv(r'D:\CAllData\7C\450\AB00261.csv')

# In[349]:


#data.info()


# # 急减速急减速情况

# In[350]:


time = data['location_time'].tolist()
time_s = []
for i in range(0,len(time)):
    a=time[i].split(':')
    time_s.append(int(a[-1]))     #时间 ，秒级
type(time_s[2])


# In[351]:


len(data)
len(time_s)


# In[352]:


speed=data['gps_speed'].tolist()                   # 算出平均加速度
acceleration = []
for i in range(0,len(time_s) - 1):
    if time_s[i+1] > time_s[i]:
        Delta_time = time_s[i+1] - time_s[i]
    else:
        Delta_time = time_s[i+1] - time_s[i] + 60
    Delta_speed = speed[i+1] - speed[i]
    acceleration.append(Delta_speed / Delta_time)

len(acceleration)


# In[353]:


#pd.Series(acceleration).value_counts()
for j in range(0,20):
    for i in range(0,len(acceleration)):
        try:
            if abs(acceleration[i]) > 3:                  # 清除加速度异常值 阈值为 + - 3
                del acceleration[i]
        except:
            pass
len(acceleration)
for i in range(0,len(acceleration)):
    if acceleration[i] > 3 or acceleration[i] < -3:
        print(acceleration[i])


# In[354]:


Rapid_acceleration_deceleration_counts = 0             #这里判断急加速为连续的2秒以上加速度大于2.5 则判定为急加速
for i in range(0,len(acceleration),3):
    if abs(acceleration[i]) > 2.5 and abs(acceleration[i+1]) > 2.5 and abs(acceleration[i+2]) > 2.5 : 
        Rapid_acceleration_deceleration_counts = Rapid_acceleration_deceleration_counts +1
    

print('急加速急减速统计次数为：',Rapid_acceleration_deceleration_counts)       #打印急加速急减速情况


# In[ ]:





# # 熄火滑行情况

# In[355]:


data['acc_state'].value_counts()


# In[356]:


#acc为0 ，速度不为0的数据数量
acc = data['acc_state'].tolist()
acc_0 =[]
for i in range(0,len(acc)):
    if acc[i]==0:
        acc_0.append(i)
acc_0_speedNonestop = 0
for i in acc_0:
    if speed[i] != 0:
        acc_0_speedNonestop = acc_0_speedNonestop + 1

print('熄火滑行统计次数为：',acc_0_speedNonestop)


# In[ ]:





# # 怠速(超长，预热）

# In[357]:


#acc为1 ，速度为0 判断为怠速 内含超长怠速 和怠速预热
acc_1 =[]
for i in range(0,len(acc)):
    if acc[i]==1:
        acc_1.append(i)
acc_1_speed_0_sum = 0
acc_1_speed_0 = []
for i in acc_1:
    if speed[i] == 0:
        acc_1_speed_0_sum = acc_1_speed_0_sum +1
        acc_1_speed_0.append(i)
    
#print('怠速数据统计为:',acc_1_speed_0_sum)
          


# In[358]:


#超长怠速判断
import datetime
'''time=data['location_time'].tolist()
d1 = datetime.datetime.strptime(time[0], '%Y-%m-%d %H:%M:%S')
d2 = datetime.datetime.strptime(time[89462], '%Y-%m-%d %H:%M:%S')
#a=d2-d1
run_time_s=d2.__sub__(d1)
a=run_time_s
a                   '''                         #数据总时间 4 天半左右


# In[359]:


idling_index=[acc_1_speed_0[0]]  
for i in range(0,len(acc_1_speed_0)):
    try:
      
        if acc_1_speed_0[i+1] - acc_1_speed_0[i] > 1 :                  #  单独
            idling_index.append(acc_1_speed_0[i])
            idling_index.append(acc_1_speed_0[i+1])
    except:
        pass
                     # 拿到每段怠速的开始和结束下标
idling_index       #   ！！！ 这里 第一个第一段怠速开头下标 第二个为第一段怠速结尾下标  以此类推
                  #若只有一个怠速值 则会在列表连续出现两次 方便后面计算怠速时间
                #  ！！！用偶数个下标减去奇数个小标


# In[360]:


t1 = datetime.datetime.strptime(time[idling_index[36]], '%Y-%m-%d %H:%M:%S')   #测试
t2 = datetime.datetime.strptime(time[idling_index[37]], '%Y-%m-%d %H:%M:%S')
idling_time=t2.__sub__(t1)
idling_index[37]


# In[361]:


idling_time_sum =[]
for i in range(0,int(len(idling_index)),2):
    try:
        t1 = datetime.datetime.strptime(time[idling_index[i]], '%Y-%m-%d %H:%M:%S')
        t2 = datetime.datetime.strptime(time[idling_index[i+1]], '%Y-%m-%d %H:%M:%S')
        idling_time=t2.__sub__(t1).seconds
        idling_time_sum.append(idling_time)          #拿到怠速时间段时间
    except:
        pass


# In[362]:


#若怠速时间大于5分钟则判断为超长怠速
long_idling =[]
for i in idling_time_sum:
    if i > 300:
        long_idling.append(i)
long_idling

#for i in long_idling:
   # print('超长怠速的时间为（s）：',i)
print('超长怠速统计次数为：',len(long_idling))


# # 怠速预热

# In[363]:


pd.set_option('max_colwidth',100)


# In[ ]:





# In[364]:


#data.loc[(data['acc_state']==1) & (data['gps_speed']==0),['acc_state','gps_speed']][600:650]


# In[365]:


acc_0_index = [acc_0[0]]              #acc_0里是acc状态为0的数据的下标
for i in range(0,len(acc_0)):
    try:
        if acc_0[i+1] -acc_0[i] >1:
            acc_0_index.append(acc_0[i])
            acc_0_index.append(acc_0[i+1])                    #acc为0 的下标段
    except:
        pass   
        


# In[366]:


stall_time_sum =[]                 #熄火时间段总和
for i in range(0,int(len(acc_0_index)),2):
    try:
        t1 = datetime.datetime.strptime(time[acc_0_index[i]], '%Y-%m-%d %H:%M:%S')
        t2 = datetime.datetime.strptime(time[acc_0_index[i+1]], '%Y-%m-%d %H:%M:%S')
        stall_time=t2.__sub__(t1).seconds
        stall_time_sum.append(stall_time)               #拿到怠速时间段时间
    except:
        pass
    
#stall_time_sum
len(stall_time_sum)


# In[367]:


long_stall_index=[]
for i in range(0,len(stall_time_sum)):
    if stall_time_sum[i] > 3600:                     #判断熄火达一个小时以上      只有该情况司机可能会怠速预热
        long_stall_index.append(i)                     #返回熄火长时间的下标 ，这个下标 * 2是对应acc_0的下标  acc_0里的值为原始数据下标
                                                        #可以此找回原始数据下标
long_stall_index   

index1=[]
for i in range(0,len(long_stall_index)):
    #index1.append(index1(i*2))
    index1.append(index1(i*2+1))                   #拿对应acc_0_index下标   acc_0_index内装有原始数据下标
                                                    #这里只有后一位，就是长时间熄火时间段的最后一个下标
    
origDataIndex = []
for i in index1:
    origDataIndex.append(acc_0_index[i])            #长时间熄火后的原始数据下标


# In[368]:


IdlePreheating = 0                             #怠速预热初始值为0
aa=0
for i in origDataIndex:                                  
    for j in range(0,60):                          #判断长时间熄火后的后60条数据有没有怠速情况   判断是否有怠速预热
        if speed[i+j] == 0:
            aa=aa+1
    if aa > 59:
        IdlePreheating = IdlePreheating + 1         #怠速预热情况 加1

print('怠速预热次数统计为：',IdlePreheating)


# In[ ]:





# # 超速

# In[369]:


#这里因为每辆车的运行路线不同  所以超速对应速度值的判断也不同
#这里以AF0098路线图来看，它主要路线都是高速，所以超速的判断定为90
spd=pd.Series(speed).value_counts()                 #查看速度情况


# In[370]:


spd.index.max()                


# In[371]:


speeding = 0
for i in range(0,len(speed)):
    if speed[i] > 90:
        speeding = speeding +1
print('超速统计次数为：',speeding)
        


# In[ ]:





# # 急变道

# In[372]:


#转向角突然有较大变化   这里既然是急 那就以来不及打转向灯的情况分析
DA=data['direction_angle'].tolist()


# In[391]:


RapidChangeRode = 0
for i in range(0,len(DA),3):          #数据精度为1秒或2秒  这里以每3条数据为一个单位来看 否则因路况导致的行驶不稳方向角改变的数据会大量采集进去
    try:                            #考虑到变道的情况 ，方向角的变化不会太大，这里阈值制定为30-45 最符合汽车变道时的方向角改变情况
        if 30 < abs(DA[i+1] - DA[i]) < 45:
            RapidChangeRode = RapidChangeRode +1
        elif 30 < 360 - abs(DA[i+1] - DA[i]) < 45:
            RapidChangeRode = RapidChangeRode +1
    except:
        pass
RapidChangeRode
print('急变道统计次数为：',int(RapidChangeRode/10))

#急变道考虑到还有转弯的情况难以分辨 故取1:10的比列


# In[ ]:





# # 转弯未打转向灯

# 

# In[374]:


data['right_turn_signals'].value_counts()


# In[375]:



data['right_turn_signals'].value_counts()


# In[376]:


R_T_S = data['right_turn_signals'].tolist()         #诺前后转向角大于22.5度 判断该车在转弯
L_T_S = data['left_turn_signals'].tolist()
CorneringLight = 0
for i in range(0,len(DA)):                         #数据精度每秒或两秒一条，正常不可能在这么短时间转向角大于90度，设置上限，放在在0度这个位置出现错误
    try:
        if 22.5 < abs(DA[i+1] - DA[i]) < 90:
            CorneringLight = CorneringLight+1
        elif 22.5 < 360 - abs(DA[i+1] - DA[i]) < 90:
            CorneringLight = CorneringLight +1
    except:
        pass
    
print('转弯未打转向灯统计次数为:',CorneringLight)


# In[377]:


len(data)


# # 疲劳驾驶

# In[378]:


d1 = datetime.datetime.strptime(time[0], '%Y-%m-%d %H:%M:%S')
d2 = datetime.datetime.strptime(time[len(data)-1], '%Y-%m-%d %H:%M:%S')
#a=d2-d1
run_time_s=d2.__sub__(d1)
a=run_time_s
a


# In[379]:


time[0].split(':')


# In[380]:


time_m = []
for i in range(0,len(time)):
    a=time[i].split(':')
    time_m.append(int(a[1]))     #时间 ，秒级


# In[381]:


TimeSliceIndex = [0]
for i in range(0,len(time_m)):
    try:
        if time_m[i+1] - time_m[i] > 1:                   #0位为第一个时间段开始位  1位为第一个时间段结束位 以此类推
            TimeSliceIndex.append(i)
            TimeSliceIndex.append(i+1) 
    except:
        pass


# In[382]:


TimeSlice = []
for i in range(0,int(len(TimeSliceIndex)),2):
    try:
        t1 = datetime.datetime.strptime(time[TimeSliceIndex[i]], '%Y-%m-%d %H:%M:%S')
        t2 = datetime.datetime.strptime(time[TimeSliceIndex[i+1]], '%Y-%m-%d %H:%M:%S')
        aa=t2.__sub__(t1).seconds
        TimeSlice.append(aa)
    except:
        pass
len(TimeSlice)                   #拿到汽车运输的每段时间段长度 ，单位秒


# In[383]:


FatigueDriving = 0
for i in TimeSlice:                   #国家规定，一次连续驾驶时长不能大于4小时  这里以4小时为疲劳驾驶的判断
    if i > 14400:
        FatigueDriving = FatigueDriving + 1

print('疲劳驾驶统计次数为（开车时间大于4小时）:',FatigueDriving)
        


# In[ ]:





# In[ ]:





# # 和积法，创建比较矩阵

# In[415]:


# 疲劳驾驶  急加减  急变道  超速  熄火滑行  超长怠速  转弯没开转向灯  怠速预热
A = np.mat([[1,2,2,3,3,4,5,7],
           [1/2,1,1,2,2,3,4,5],
           [1/2,1,1,2,2,3,4,5],
           [1/3,1/2,1/2,1,1,2,3,4],
           [1/3,1/2,1/2,1,1,2,3,4],
           [1/4,1/3,1/3,1/2,1/2,1,2,3],
           [1/5,1/4,1/4,1/3,1/3,1/2,1,2],
           [1/7,1/5,1/5,1/4,1/4,1/3,1/2,1]])
A


# In[416]:


B=sum(A)             #求列和
B


# In[417]:


C=A/B          # 对矩阵做归一化
C


# In[418]:


C_T=C.transpose()            #求矩阵行和   拿到初始未归一化权重向量
C_T
W_T=sum(C_T)
#W_T=W_T.transpose()
W_T


# In[419]:


W_S = sum(W_T.transpose())                   #求权重向量和 为权重归一化做准备
W_S


# In[420]:


W_T=W_T/W_S                     # 对权重向量归一化  拿到最终权重
W_T
Wx = W_T.copy()
Wx
                         #将权重取出放入列表为后面计算做准备


# In[428]:


Wx[0,1]
WX=[]
for i in range(0,8):
    WX.append(Wx[0,i])
Wx=WX.copy()
Wx


# In[421]:


AW = np.dot(A,W_T.transpose())                     #求权重和 矩阵A的乘  准备计算判断矩阵最大特征根lambada
AW = AW.transpose()
AW


# In[422]:


Lambada=0                                   #得到Lambada

for i in range(0,len(AW)):
    Lambada = Lambada + AW[0,i] / W_T[0,i]

Lambada = Lambada / len(AW)
Lambada


# In[423]:


AW


# In[424]:


# 判断矩阵一致性指标 C.I.   CI = (lambada - n) / n -1   小于0.1则规范
CI = Lambada - 8
CI = CI / 7
CI


# In[342]:


# 疲劳驾驶  急加减  急变道  超速  熄火滑行  超长怠速  转弯没开转向灯  怠速预热


# In[ ]:





# # 搭建参数分数模型

# In[407]:


parameter_group =[FatigueDriving,Rapid_acceleration_deceleration_counts,RapidChangeRode,
                  speeding,acc_0_speedNonestop,len(long_idling),CorneringLight,IdlePreheating]


# In[408]:


score_group =[]
for i in range(0,8):
    if parameter_group[i] < 100:
        score_group.append((100 - parameter_group[i]))
    else:
        score_group.append(0)
score_group


# In[409]:


parameter_group


# In[432]:


single_score= 0 
totle_score = 0
for i in range(0,8):
    single_score = Wx[i] * score_group[i]
    totle_score = totle_score + single_score
    
print('该司机此次安全评价总得分为:',totle_score)


# In[ ]:







# In[2]:


'''wcondition = pd.read_csv(r'D:\CAllData\7C\weatherC.csv')
data = pd.read_csv(r'D:\CAllData\7C\450\AA00036.csv')
'''

# In[3]:


rode = data.copy()
rode.head(1)


# In[4]:


len(rode)


# In[5]:



time=data['location_time'].tolist()
speed=data['gps_speed'].tolist()
time_d=[]
for i in range(0,len(time)):
    a=time[i].split(' ')[0]
    
    b=a.split('-')[2]

    time_d.append(int(b))
time_d[0]
# '''for i in range(0,len(time)):
#     if time_h[i] > 11:
#         print(time_h[i])  '''             #拿到小时级时间

for i in range(0,len(rode)):
    a=rode['location_time'][i].split(' ')[0]
    b=a.split('-')[2]
    b=int(b)
    if b>31:
        rode.drop(index=[i])


# In[6]:


a = rode['location_time'][1].split(' ')[0]
b=a.split('-')[2]
b=int(b)
b


# In[7]:


type(rode['location_time'][0])


# In[8]:


data.head()


# In[ ]:





# # 拼接两个文件和数据处理

# In[9]:


import datetime
time=rode['location_time'].tolist()
speed=rode['gps_speed'].tolist()
lng=rode['lng'].tolist()
lat=rode['lat'].tolist()
time[2]
d1 = datetime.datetime.strptime(time[0], '%Y-%m-%d %H:%M:%S')
d2 = datetime.datetime.strptime(time[len(data)-1], '%Y-%m-%d %H:%M:%S')
#a=d2-d1
run_time_s=d2.__sub__(d1)
a=run_time_s
a


# In[10]:


data.head(1)


# In[11]:


Time = []
for i in range(0,len(time)):
    a=time[i].split(' ')[0]
    b=a.split('-')
    
    c=list(b[2])
    d=list(b[1])
    if c[0]=='0' and d[0] == '0':            
        str = '%s/%s/%s' % (c[1],d[1],b[0])
    elif c[0]=='0' and d[0] !='0':
        str = '%s/%s/%s' % (c[1],b[1],b[0])               #调整日期格式 准备拼接
    elif c[0]!='0' and d[0] == '0':
        str = '%s/%s/%s' % (b[2],d[1],b[0])
    Time.append(str)    
Time[0]


# In[12]:


rode['location_time']=Time


# In[13]:


rode.head()


# In[14]:



jwd = list(zip(lat,lng))
for i in range(0,len(jwd)):
    jwd[i]=list(jwd[i])  


# In[15]:


a = geocoder.osm(jwd[0],method='reverse')
address = a.address
address


# In[16]:


address = address.split(',')
address


# In[17]:


county = address[2].strip(' ')
county = list(county)[0:2]
county = county[0]+county[1]
gg = geocoder.arcgis(jwd[0], method='reverse')
city = gg.city
city = list(city)[0:2]
city = city[0] + city[1]                      # 拿到经纬度对应的符合数据格式的地址
print(city)
print(county)


# In[18]:


data.head()
wc=wcondition.loc[(wcondition["prefecture_city"] ==city)  & (wcondition["county"] ==county)]
wc.head()


# In[19]:


pre=wc['precipitation'].tolist()
#type(pre[0])


# In[20]:


wc['relative_humidity'].value_counts()


# In[21]:


mean = pd.DataFrame(wc['relative_humidity'].value_counts())
mean
mean1 = pd.DataFrame(wc['precipitation'].value_counts())
mean1


# In[22]:


a = list(mean.index)
a


# In[23]:


a1 = list(mean1.index)
a1


# In[24]:


Mean = []
for i in range(0,len(a)):                    #计算湿度降水量平均值
    bb=list(a[i])
    f=bb[0]+bb[1]
    Mean.append(int(f))
Mean
k=0
for i in range(0,len(Mean)):
    k=Mean[i] + k
try:
    k=k/len(Mean)
except:
    k=0


# In[25]:


RR=wc['relative_humidity'].tolist()


# In[26]:


for i in range(0,len(pre)):
    pre[i]=0.2


# In[27]:


for i in range(0,len(RR)):
    RR[i]=k


# In[28]:

pd.set_option('mode.chained_assignment',None)
wc['relative_humidity']=RR


# In[29]:


wc['precipitation']=pre
wc.head()


# In[30]:


RodeEnviorment=pd.merge(rode,wc,how='left',left_on='location_time',right_on='record_date')
#RodeEnviorment.head(5)


# In[31]:


rode.head()


# In[32]:


RodeEnviorment.head(5)


# In[33]:


RodeEnviorment
len(RodeEnviorment)


# In[ ]:





# In[34]:


# data['relative_humidity'].fillna(data['relative_humidity'].mean(),inplace=True)


# # 效率和节能

# In[35]:


RodeEnviorment.head()


# # ACC状态占比

# In[36]:


#acc状态在行车中占比



acc=RodeEnviorment['acc_state'].tolist()
acc_sum=0
for i in range(0,len(RodeEnviorment)):
    if acc[i]==1:
        acc_sum = acc_sum + 1
len1=len(RodeEnviorment)
accProportion = acc_sum/len1       

print('acc状态在运输中的占比为：%.2f%%' % (accProportion * 100))
        


# In[ ]:





# # 开车拉手刹

# In[37]:


#带着手刹跑



speed = RodeEnviorment['gps_speed'].tolist()
speed_Not0 =[]
for i in range(0,len(speed)):
    if speed[i] !=0:
        speed_Not0.append(i)
len(speed_Not0)


# In[38]:


hand_brake = RodeEnviorment['hand_brake'].tolist()

hand_brake_run=0
for i in speed_Not0:
    if hand_brake[i] == 1:
        hand_brake_run = hand_brake_run + 1 
print('开车拉手刹的次数为:',hand_brake_run)


# In[ ]:





# # 超长怠速

# In[39]:


#acc为1 ，速度为0 判断为怠速 内含超长怠速 和怠速预热
acc=RodeEnviorment['acc_state'].tolist()
acc_1 =[]
for i in range(0,len(acc)):
    if acc[i]==1:
        acc_1.append(i)
acc_1_speed_0_sum = 0
acc_1_speed_0 = []
for i in acc_1:
    if speed[i] == 0:
        acc_1_speed_0_sum = acc_1_speed_0_sum +1
        acc_1_speed_0.append(i)
    
#print('怠速数据统计为:',acc_1_speed_0_sum)
          


# In[40]:


#超长怠速判断
import datetime


# In[41]:


idling_index=[acc_1_speed_0[0]]  
for i in range(0,len(acc_1_speed_0)):
    try:
      
        if acc_1_speed_0[i+1] - acc_1_speed_0[i] > 1 :                  #  单独
            idling_index.append(acc_1_speed_0[i])
            idling_index.append(acc_1_speed_0[i+1])
    except:
        pass
                     # 拿到每段怠速的开始和结束下标
                   #   ！！！ 这里 第一个第一段怠速开头下标 第二个为第一段怠速结尾下标  以此类推
                  #若只有一个怠速值 则会在列表连续出现两次 方便后面计算怠速时间
                #  ！！！用偶数个下标减去奇数个小标


# In[42]:


t1 = datetime.datetime.strptime(time[idling_index[36]], '%Y-%m-%d %H:%M:%S')   #测试
t2 = datetime.datetime.strptime(time[idling_index[37]], '%Y-%m-%d %H:%M:%S')
idling_time=t2.__sub__(t1)
idling_index[37]


# In[43]:


idling_time_sum =[]
for i in range(0,int(len(idling_index)),2):
    try:
        t1 = datetime.datetime.strptime(time[idling_index[i]], '%Y-%m-%d %H:%M:%S')
        t2 = datetime.datetime.strptime(time[idling_index[i+1]], '%Y-%m-%d %H:%M:%S')
        idling_time=t2.__sub__(t1).seconds
        idling_time_sum.append(idling_time)          #拿到怠速时间段时间
    except:
        pass


# In[44]:


#若怠速时间大于5分钟则判断为超长怠速
long_idling =[]
for i in idling_time_sum:
    if i > 300:
        long_idling.append(i)
long_idling

# for i in long_idling:
#     print('超长怠速的时间为（s）：',i)
long_idling=len(long_idling)
print('超长怠速统计次数为：',long_idling)


# In[ ]:





# # 怠速预热

# In[45]:


acc_0 =[]
for i in range(0,len(acc)):
    if acc[i]==0:
        acc_0.append(i)


# In[46]:


acc_0_index = [acc_0[0]]              #acc_0里是acc状态为0的数据的下标

for i in range(0,len(acc_0)):
    try:
        if acc_0[i+1] -acc_0[i] >1:
            acc_0_index.append(acc_0[i])
            acc_0_index.append(acc_0[i+1])                    #acc为0 的下标段
    except:
        pass   
        


# In[47]:


stall_time_sum =[]                 #熄火时间段总和
for i in range(0,int(len(acc_0_index)),2):
    try:
        t1 = datetime.datetime.strptime(time[acc_0_index[i]], '%Y-%m-%d %H:%M:%S')
        t2 = datetime.datetime.strptime(time[acc_0_index[i+1]], '%Y-%m-%d %H:%M:%S')
        stall_time=t2.__sub__(t1).seconds
        stall_time_sum.append(stall_time)               #拿到怠速时间段时间
    except:
        pass
    
#stall_time_sum
len(stall_time_sum)


# In[48]:


long_stall_index=[]
for i in range(0,len(stall_time_sum)):
    if stall_time_sum[i] > 3600:                     #判断熄火达一个小时以上      只有该情况司机可能会怠速预热
        long_stall_index.append(i)                     #返回熄火长时间的下标 ，这个下标 * 2是对应acc_0的下标  acc_0里的值为原始数据下标
                                                        #可以此找回原始数据下标
long_stall_index   

index1=[]
for i in range(0,len(long_stall_index)):
    #index1.append(index1(i*2))
    index1.append(index1(i*2+1))                   #拿对应acc_0_index下标   acc_0_index内装有原始数据下标
                                                    #这里只有后一位，就是长时间熄火时间段的最后一个下标
    
origDataIndex = []
for i in index1:
    origDataIndex.append(acc_0_index[i])            #长时间熄火后的原始数据下标


# In[49]:


IdlePreheating = 0                             #怠速预热初始值为0
aa=0
for i in origDataIndex:                                  
    for j in range(0,60):                          #判断长时间熄火后的后60条数据有没有怠速情况   判断是否有怠速预热
        if speed[i+j] == 0:
            aa=aa+1
    if aa > 59:
        IdlePreheating = IdlePreheating + 1         #怠速预热情况 加1

print('怠速预热次数统计为：',IdlePreheating)


# In[ ]:





# # 频繁刹车

# In[50]:


RodeEnviorment.head()


# In[51]:


hand_brake = RodeEnviorment['hand_brake'].tolist()
foot_brake = RodeEnviorment['foot_brake'].tolist()
hand_brake_index = []
foot_brake_index = []
for i in range(0,len(hand_brake)):
    if hand_brake[i] == 1:
        hand_brake_index.append(i)
    elif foot_brake[i] == 1:
        foot_brake_index.append(i)
hand_brake_index
foot_brake_index


# In[52]:


idling_time_sum =[]
for i in range(0,int(len(idling_index)),2):
    try:
        t1 = datetime.datetime.strptime(time[idling_index[i]], '%Y-%m-%d %H:%M:%S')
        t2 = datetime.datetime.strptime(time[idling_index[i+1]], '%Y-%m-%d %H:%M:%S')
        idling_time=t2.__sub__(t1).seconds
        idling_time_sum.append(idling_time)          #拿到怠速时间段时间
    except:
        pass


# In[53]:


pf=1000                        # 判断指标 1000条数据 ，
a=0                            # 看1000条数据里 检测到刹车是否超过100次
FrequentBraking = 0
for i in range(0,len(hand_brake_index)):
    if i < pf:
        a = a +1
    elif a > 100 :
        FrequentBraking = FrequentBraking + 1
        a =0
        pf=pf+1000
    else:
        pass

print('频繁刹车次数统计为：',FrequentBraking)


# In[54]:


rode.head()


# # 短距离行驶

# In[55]:


# 通过速度状态判断
speedNot0_index=[]
for i in range(0,len(speed)):
    if speed[i] != 0:
        speedNot0_index.append(i)     #拿到所有有速度的下标


# In[56]:


runingSectionIndex=[speedNot0_index[0]]
for i in range(0,len(speedNot0_index)):
    try:
        if speedNot0_index[i+1] - speedNot0_index[i] > 1:
            runingSectionIndex.append(speedNot0_index[i])
            runingSectionIndex.append(speedNot0_index[i+1])
    except:
         pass
                # 拿到速度不为0 即运行段的开始结束下标


# In[57]:


mileage = RodeEnviorment['mileage'].tolist()
distance = []
for i in range(0,int(len(runingSectionIndex)),2):
    try:
        a = runingSectionIndex[i+1] - runingSectionIndex[i]
        distance.append(a)
    except:
        pass


# In[58]:


ShortDistanceDriving =0
for i in distance:
    if 0 < i < 5 :
        ShortDistanceDriving = ShortDistanceDriving + 1
print('统计短距离行驶次数为:',ShortDistanceDriving)
        


# In[ ]:





# In[ ]:





# # 权重

# In[59]:



A1 = np.mat([[1,1/5,2,1/5,1/3,1/6],
            [5,1,5,1,3,1/2,],
            [1/2,1/5,1,1/5,1/3,1/7],
            [5,1,5,1,2,1/2],
            [3,1/3,3,1/2,1,1/2],
            [6,2,7,2,2,1]])
A1


# In[60]:


B1 = sum(A1)             #求列和
B1


# In[61]:


C1 = A1 / B1          # 对矩阵做归一化
C1


# In[62]:


C_T1 = C1.transpose()            #求矩阵行和   拿到初始未归一化权重向量
C_T1
W_T1=sum(C_T1)
#W_T=W_T.transpose()
W_T1


# In[63]:


W_S1 = sum(W_T1.transpose())                   #求权重向量和 为权重归一化做准备
W_S1


# In[64]:


W_T1 = W_T1 / W_S1                     # 对权重向量归一化  拿到最终权重
W_T1
Wx1 = W_T1.copy()
Wx1
                         #将权重取出放入列表为后面计算做准备


# In[65]:


Wx1[0,1]
WX1 = []
for i in range(0,6):
    WX1.append(Wx1[0,i])
Wx1= WX1.copy()                 #权重换位列表后面用
Wx1


# In[66]:


AW1 = np.dot(A1,W_T1.transpose())                     #求权重和 矩阵A的乘  准备计算判断矩阵最大特征根lambada
AW1 = AW1.transpose()
AW1


# In[67]:


Lambada1=0                                   #得到Lambada

for i in range(0,len(AW1)):
    Lambada1 = Lambada1 + AW1[0,i] / W_T1[0,i]

Lambada1 = Lambada1 / len(AW1)
Lambada1


# In[68]:


AW1


# In[69]:


# 判断矩阵一致性指标 C.I.   CI = (lambada - n) / n -1   小于0.1则规范
CI1 = Lambada1 - 6
CI1 = CI1 / 5
CI1


# In[70]:


accProportion


# # 搭建参数分数模型

# In[71]:


parameter_group =[ShortDistanceDriving,FrequentBraking,IdlePreheating,long_idling,hand_brake_run,accProportion]


# In[72]:


score_group =[]
for i in range(0,6):
    if parameter_group[i] < 100 and i != 5:
        score_group.append(100 - parameter_group[i])
    elif i == 5 and parameter_group[i] < 0.2:
        score_group.append(100)
    elif i == 5 and parameter_group[i] < 0.4:
        score_group.append(80)
    elif i == 5 and parameter_group[i] < 0.6:
        score_group.append(60)
    elif i == 5 and parameter_group[i] < 0.8:
        score_group.append(0)
    else:
        score_group.append(0)
score_group


# In[73]:


single_score= 0 
effic_score = 0
for i in range(0,6):
    single_score = Wx1[i] * score_group[i]
    effic_score = effic_score + single_score
    
print('该司机此次运输效率节能总得分为:',totle_score)


# In[ ]:





# #   RodeEnviorment

# In[74]:


RodeEnviorment.sample(frac=0.1)


# In[75]:


days = len(RodeEnviorment['record_date'].value_counts())    # 汽车运行天数
days


# In[76]:


#抽取数据的下标   按天取   为后面算平均数做准备
idx = []
try:
    for i in range(0,len(RodeEnviorment),int(len(RodeEnviorment)/days)):
        idx.append(i)
except:
        idx=[0]


# In[ ]:





# # 运输时平均高温

# In[77]:


# high_temp = RodeEnviorment['high_temp'].tolist()
# high_temp[1:6]
high_temp =[]
for i in idx:
    high_temp.append(RodeEnviorment['high_temp'][i])
high_temp


# In[78]:


tm = []
for i in range(0,len(high_temp)):                        # 平均高温度
    bb=list(high_temp[i])
    f=bb[0]+bb[1]
    tm.append(int(f))
tm

tempMean = 0
for i in range(0,len(tm)):
    tempMean = tempMean + tm[i]
tempMean = tempMean / len(tm)
tempMean
print('运输时平均高温:',tempMean)


# In[ ]:





# # 运输时平均低温

# In[79]:


# 平均低温
low_temp =[]
for i in idx:
    low_temp.append(RodeEnviorment['low_temp'][i])
low_temp


# In[80]:


tm1 = []
for i in range(0,len(low_temp)):                        # 平均低温度
    bb=list(low_temp[i])
    f=bb[0]+bb[1]
    tm1.append(int(f))
tm1

lowtempMean = 0
for i in range(0,len(tm1)):
    lowtempMean = lowtempMean + tm1[i]
lowtempMean = lowtempMean / len(tm1)
lowtempMean
print('运输时平均低温:',lowtempMean)


# # 运输时平均湿度

# In[81]:


#运输过程相对湿度平均数
r_h =[]
for i in idx:
    r_h.append(RodeEnviorment['relative_humidity'][i])


# In[82]:


mean_rh = 0
for i in r_h:
    mean_rh = mean_rh +i
mean_rh = mean_rh / len(r_h)
mean_rh
if mean_rh < 70:
    print('{0} {1} {2}'.format('运输时平均湿度：',mean_rh,'舒适'))
elif 70 <= mean_rh < 80:
    print('{0} {1} {2}'.format('运输时平均湿度：',mean_rh,'不舒适'))
else:
    print('{0} {1} {2}'.format('运输时平均湿度：',mean_rh,'难受'))


# In[ ]:





# # 运输时平均降水量

# In[83]:


#运输时间段的平均降水量
precip =[]
for i in idx:
    precip.append(RodeEnviorment['precipitation'][i])
precip


# In[84]:


mean_pre = 0
for i in precip:
    mean_pre = mean_pre + i
mean_pre = mean_pre / len(precip)
mean_pre
if mean_pre < 10:
    print('{0} {1} {2}'.format('运输时平均降水量（mm）：',mean_pre,'小雨'))
elif 10<= mean_pre < 25:
    print('{0} {1} {2}'.format('运输时平均降水量（mm）：',mean_pre,'中雨'))
elif 25<= mean_pre <50:
    print('{0} {1} {2}'.format('运输时平均降水量（mm）：',mean_pre,'大雨'))
elif 50<= mean_pre:
    print('{0} {1} {2}'.format('运输时平均降水量（mm）：',mean_pre,'暴雨'))


# In[85]:


wc.head(1)


# In[ ]:





# # 运输时天气状态

# In[86]:


conditions = []
for i in idx:
    conditions.append(RodeEnviorment['conditions'][i])
conditions
condition = []
for i in conditions:
    condition = condition + list(i)               #拿到平均天气情况的单字符列表


# In[87]:


rain = 0
snow = 0
fog = 0
for i in condition:
    if i == '雨':
        rain = rain + 1
    elif i == '雪':
        snow = snow + 1
    elif i == '雾':
        fog = fog +1
    else:
        pass


# In[88]:


weacondit = 0                                    # 天气情况 正常 1   雨 2  雪 3  雾 4
for i in range(0,1):
    if snow != 0:
        weacondit = 3
    elif snow ==0 and rain!=0:
        weacondit = 2
    elif snow ==0 and rain ==0 and fog!=0:
        weacondit = 4
    else:
        weacondit = 1
if weacondit == 1:
    print('天气情况：正常')
elif weacondit == 2:
    print('天气情况：下雨')
elif weacondit == 3:
    print('天气情况：雪')
elif weacondit == 4:
    print('天气情况：雾')


# In[89]:


wc.head(1)


# # 运输时平均风力
# 

# In[90]:


wind1 =[]
for i in idx:
    wind1.append(RodeEnviorment['wind_power'][i])
wind1


# In[91]:


wind =[]
for i in wind1:
    cc = list(i)[:-1]
    cc = int(cc[-1])
    wind.append(cc)
wind


# In[92]:


meanWind = 0
for i in wind:
    meanWind = meanWind + i 
meanWind = meanWind / len(wind)
meanWind
print('运输时平均风力:',meanWind)


# In[ ]:





# # 运输时环境条件评分

# In[93]:


parameterGroup = [meanWind,weacondit,mean_pre,mean_rh,lowtempMean,tempMean]
parameterGroup


# In[94]:


meanWindScore = 0
weaconditScore = 0
mean_preScore =0
mean_rhScore =0
tempMeanScore =0
for i in parameterGroup:
    if parameterGroup[0] <=5:               #风力
        meanWindScore = 100
    elif parameterGroup[0] ==6:
        meanWindScore = 80
    elif parameterGroup[0] ==7:
        meanWindScore = 60
    elif parameterGroup[0] >7:
        meanWindScore =0
    else:
        pass
    
for i in parameterGroup:    
    if parameterGroup[1] ==1:             #天气情况 雨雪雾
        weaconditScore = 100
    elif parameterGroup[1] ==2:
        weaconditScore =60
    elif parameterGroup[1] ==3:
        weaconditScore = 40
    elif parameterGroup[1] ==4:
        weaconditScore = 80
    else:
        pass
    
        
for i in parameterGroup:    
    if parameterGroup[2] < 10:                 #降水量
        mean_preScore = 100
    elif 10<= parameterGroup[2] <25:
        mean_preScore = 80
    elif 25<= parameterGroup[2] <50:
        mean_preScore = 60
    elif parameterGroup[2] >50:
        mean_preScore = 0
    else:
        pass
        
for i in parameterGroup:    
    if parameterGroup[3] <70:               #湿度
        mean_rhScore =100
    elif 70<= parameterGroup[3] <70:
        mean_rhScore =80
    elif parameterGroup[3] >80:
        mean_rhScore =40
    else:
        pass
        
for i in parameterGroup:        
    if parameterGroup[4]>=25 and parameterGroup[5]<=35:    #温度
        tempMeanScore=100
    elif parameterGroup[4]<25 and parameterGroup[5]>35:    #温度
        tempMeanScore=0
    else:
        pass
        
    
    


# In[95]:


ScoreGroup=[meanWindScore,weaconditScore,mean_preScore,mean_rhScore,tempMeanScore]
ScoreGroup


# In[96]:


envScore = 0
for i in ScoreGroup:
    envScore=envScore+i*0.2
envScore
print('运输时天气状态评分为:',envScore)


# # 夜晚占的比重

# In[97]:


time=data['location_time'].tolist()
speed=data['gps_speed'].tolist()
time_h=[]
for i in range(0,len(time)):
    a=time[i].split(':')[0]
    
    b=a.split(' ')[1]

    time_h.append(int(b))
#time_h[49999]
'''for i in range(0,len(time)):
    if time_h[i] > 11:
        print(time_h[i])               #拿到小时级时间

'''
# In[98]:


len(time_h)


# In[99]:


white = 0
for i in time_h:
    if 8 < i <= 20:
        white = white + 1
dark = len(time_h) - white
darkProporion = dark / len(time_h)
whiteProporion = white / len(time_h)
darkProporion


# In[100]:


# 白天黑夜运输影响
whiteDark = 1 * whiteProporion + 0.7 * darkProporion
whiteDark


# In[101]:

envScoreDW = envScore*whiteDark
print('运输天气状态评分（加上白天黑夜因素）:',envScoreDW)


# In[ ]:


#!/usr/bin/env python
# coding: utf-8

# # 综合评价权重计算

# In[ ]:


A11 = np.mat([[1,2,3],
            [1/2,1,1],
            [1/3,1,1],
           ])
A11


# In[ ]:


B11 = sum(A11)             #求列和
B11


# In[ ]:


C11 = A11 / B11          # 对矩阵做归一化
C11


# In[ ]:


C_T11 = C11.transpose()            #求矩阵行和   拿到初始未归一化权重向量
C_T11
W_T11=sum(C_T11)
#W_T=W_T.transpose()
W_T11


# In[ ]:


W_S11 = sum(W_T11.transpose())                   #求权重向量和 为权重归一化做准备
W_S11


# In[ ]:


W_T11 = W_T11 / W_S11                     # 对权重向量归一化  拿到最终权重
W_T11
Wx11 = W_T11.copy()
Wx11
                         #将权重取出放入列表为后面计算做准备


# In[ ]:


Wx11[0,1]
WX11 = []
for i in range(0,3):
    WX11.append(Wx11[0,i])
Wx11= WX11.copy()                 #权重换位列表后面用
Wx11


# In[ ]:


AW11 = np.dot(A11,W_T11.transpose())                     #求权重和 矩阵A的乘  准备计算判断矩阵最大特征根lambada
AW11 = AW11.transpose()
AW11


# In[ ]:


Lambada11=0                                   #得到Lambada

for i in range(0,len(AW1)):
    Lambada11 = Lambada11 + AW11[0,i] / W_T11[0,i]

Lambada11 = Lambada11 / len(AW11)
Lambada11


# In[ ]:


AW11


# In[ ]:


# 判断矩阵一致性指标 C.I.   CI = (lambada - n) / n -1   小于0.1则规范
CI11 = Lambada11 - 3
CI11 = CI11 / 2
CI11


# In[ ]:





# # 综合评价函数

# In[ ]:


# 评判标准 安全>效率>环境
param = [effic_score,totle_score,envScore,envScoreDW]


# In[ ]:


totleScore = 0
totleScoreDW = 0
singleScore = 0
for i in range(0,3):
    singleScore = Wx11[i] * param[i]
    totleScore = totleScore + singleScore
    
totleScoreDW = Wx11[0] * param[0] + Wx11[1] * param[1] + Wx11[2] * param[3]

print('综合评分为（不考虑夜晚）:',totleScore)
print('综合评分问（考虑夜晚）:',totleScoreDW)



