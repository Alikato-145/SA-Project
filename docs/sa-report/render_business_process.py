"""Render the reviewed one-to-one business activities and use-case diagrams."""
from pathlib import Path
import json,sys,math,re
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parent;sys.path.insert(0,str(R));from build_report import wrap_label
cat=json.loads((R/'evidence/use-case-catalog.json').read_text()); cat={int(c['id'][2:]):c for c in cat}
assert set(cat) == set(range(1, 21)), 'Expected 20 unique use cases'
assert len({c['bp'] for c in cat.values()}) == 20, 'BP activities must be unique'
F='/System/Library/Fonts/Supplemental/Tahoma.ttf'
def font(n):return ImageFont.truetype(F,n)
def make(w,h):
 im=Image.new('RGB',(w,h),'white');return im,ImageDraw.Draw(im)
def text(d,xy,t,size=35,width=480,color='black'):
 lines=[]
 for para in t.split('\n'):lines+=wrap_label(d,para,font(size),width)
 y=xy[1]-(len(lines)*size*1.35)/2
 for line in lines:d.text((xy[0],y),line,font=font(size),fill=color,anchor='mt');y+=size*1.35

def arrow(d,a,b,dashed=False):
 color='#3c3c3c'
 if dashed:
  steps=max(1,int(math.dist(a,b)/20))
  for j in range(0,steps,2):
   p=lambda k:(a[0]+(b[0]-a[0])*k/steps,a[1]+(b[1]-a[1])*k/steps)
   d.line([p(j),p(min(j+1,steps))],fill=color,width=3)
 else:d.line([a,b],fill=color,width=3)
 ang=math.atan2(b[1]-a[1],b[0]-a[0]);d.polygon([b,(b[0]-17*math.cos(ang-.4),b[1]-17*math.sin(ang-.4)),(b[0]-17*math.cos(ang+.4),b[1]-17*math.sin(ang+.4))],fill=color)

def node(d,num,x,y):
 c=cat[num];d.rounded_rectangle((x-245,y-72,x+245,y+72),radius=12,outline='#333333',width=3,fill='white')
 d.ellipse((x-275,y-100,x+275,y+100),outline='#b54545',width=4)
 text(d,(x,y),c['bp']+' '+c['id']+'\n'+c['name'],33,460)

def dot(d,x,y,end=False):
 d.ellipse((x-15,y-15,x+15,y+15),fill='black')
 if end:d.ellipse((x-23,y-23,x+23,y+23),outline='black',width=3)

def lanes(d,h,labels=None):
 for i,label in enumerate(labels or ['พนักงาน / ผู้ใช้งาน','ผู้มีอำนาจพิจารณา','HR / เจ้าของร้าน']):
  x=40+i*580;d.rectangle((x,120,x+580,h-40),outline='#aaaaaa',width=2);d.rectangle((x,120,x+580,210),outline='#aaaaaa',fill='#f1f1f1',width=2);text(d,(x+290,165),label,32,550)

# Independent supporting activities, not mandatory steps in one chain.
im,d=make(1820,800);text(d,(910,65),'การเข้าถึงและการติดตามงาน',42,1650);lanes(d,800,["ผู้ใช้งานทุกบทบาท","ผู้ใช้ตามสิทธิ์","HR / เจ้าของร้าน"])
for n,x in [(1,330),(19,910),(20,1490)]:
 dot(d,x,280);arrow(d,(x,300),(x,350));node(d,n,x,450);arrow(d,(x,550),(x,620));dot(d,x,650,True)
text(d,(910,745),'เลือกดำเนินการตามสิทธิ์และความจำเป็น',30,1600);im.save(R/'figures/BP-support.png')
# Setup workflow in HR lane; account linkage follows employee creation.
im,d=make(1820,1600);text(d,(910,65),'การเตรียมข้อมูลหลัก',42,1650);lanes(d,1600);dot(d,1490,260)
prev=(1490,275)
for j,n in enumerate([2,4,3,5,6]):
 y=405+j*230;arrow(d,prev,(1490,y-100));node(d,n,1490,y);prev=(1490,y+100)
arrow(d,prev,(1490,1530));dot(d,1490,1560,True);im.save(R/'figures/BP-setup.png')
# Daily optional branches are event-driven. Pairs connect requester to approver.
im,d=make(1820,1820);text(d,(910,65),'งานประจำวันและคำขอตามเหตุการณ์',42,1650);lanes(d,1820)
text(d,(910,270),'เริ่มแต่ละเส้นทางเมื่อเกิดรายการนั้น',30,1600)
# Attendance, leave and OT each have their own start/end; no compulsory ordering between rows.
for row,(left,right) in enumerate([(7,None),(8,9),(10,11)]):
 y=450+row*300;dot(d,20,y);arrow(d,(35,y),(55,y))
 node(d,left,330,y)
 if right:
  arrow(d,(605,y),(635,y));node(d,right,910,y);arrow(d,(1185,y),(1240,y));dot(d,1270,y,True)
 else:arrow(d,(605,y),(660,y));dot(d,690,y,True)
# Financial requests are represented as one complete business workflow including decision.
node(d,12,910,1380);dot(d,560,1380);arrow(d,(580,1380),(635,1380));arrow(d,(1185,1380),(1240,1380));dot(d,1270,1380,True)
node(d,13,1490,1680);dot(d,1140,1680);arrow(d,(1160,1680),(1215,1680));arrow(d,(1765,1680),(1785,1680));dot(d,1795,1680,True)
# Explain the shared responsibility for UC12 explicitly.
text(d,(330,1380),'พนักงานยื่น\nผู้มีสิทธิ์พิจารณา',30,360)
im.save(R/'figures/BP-daily.png')
# Monthly main path with a readiness decision and a loop to source corrections.
im,d=make(1820,2070);text(d,(910,65),'การจัดทำเงินเดือนและการจ่าย',42,1650);lanes(d,2070);dot(d,1490,260)
for n,y in [(14,400),(15,650),(16,1130),(17,1430),(18,1700)]:node(d,n,1490,y)
arrow(d,(1490,280),(1490,300));arrow(d,(1490,500),(1490,550));arrow(d,(1490,750),(1490,795))
d.polygon([(1490,795),(1680,885),(1490,975),(1300,885)],outline='#333333',fill='#fafafa',width=3);text(d,(1490,885),'พร้อมล็อกรอบ?',31,330)
arrow(d,(1490,975),(1490,1030));text(d,(1550,1000),'ใช่',28,100)
d.line([(1300,885),(1000,885),(1000,650)],fill='#555555',width=3);arrow(d,(1000,650),(1215,650));text(d,(1000,770),'ไม่พร้อม\nแก้ข้อมูลต้นทาง',28,310)
arrow(d,(1490,1230),(1490,1330));d.line([(1490,1270),(910,1270),(910,1700)],fill="#555555",width=3);arrow(d,(910,1700),(1215,1700));text(d,(910,1440),"เลือกเอกสาร\nที่ต้องการจัดทำ",28,320);arrow(d,(1490,1530),(1210,1530));d.line([(1210,1530),(1210,1815),(1490,1815)],fill="#555555",width=3);arrow(d,(1490,1800),(1490,1840))
d.rounded_rectangle((1200,1840,1780,1960),radius=10,outline='#555555',width=3);text(d,(1490,1900),'จ่ายภายนอก แล้วบันทึกยืนยัน/ยกเลิกใน UC18',30,530);arrow(d,(1490,1960),(1490,2000));dot(d,1490,2030,True)
im.save(R/'figures/BP-payroll.png')
# UML use-case diagrams with an explicit boundary and actor associations.
groups=[('support','การเข้าถึงและการติดตามงาน',[1,19,20]),('setup','การเตรียมข้อมูลหลัก',[2,3,4,5,6]),('daily','การบันทึกและพิจารณารายการประจำวัน',[7,8,9,10,11,12,13]),('payroll','การจัดทำเงินเดือนและการจ่าย',[14,15,16,17,18])]
for key,title,ids in groups:
 h=300+len(ids)*220;im,d=make(1800,h);text(d,(900,55),title,40,1700)
 d.rectangle((480,115,1690,h-55),outline='black',width=3);text(d,(1085,155),'Haris Payroll',34,1000)
 # Actors are aggregate role labels; detailed scope is defined by the catalog/table.
 actors=[('ผู้ใช้ตามสิทธิ์',0.33),('HR / เจ้าของร้าน',0.7)] if key=='support' else [('พนักงาน',.25),('ผู้อนุมัติ',.55),('HR / เจ้าของร้าน',.8)] if key=='daily' else [('HR / เจ้าของร้าน',.45),('พนักงาน',.8)] if key=='payroll' else [('HR / เจ้าของร้าน',.35),('ผู้จัดการสาขา',.75)]
 for label,fraction in actors:
  x=210;y=200+fraction*(h-350);d.ellipse((x-24,y-70,x+24,y-22),outline='black',width=3);d.line((x,y-22,x,y+45),fill='black',width=3);d.line((x-42,y+5,x+42,y+5),fill='black',width=3);d.line((x,y+45,x-35,y+95),fill='black',width=3);d.line((x,y+45,x+35,y+95),fill='black',width=3);text(d,(x,y+140),label,30,380)
 for j,n in enumerate(ids):
  y=300+j*220;x=1090;c=cat[n];d.ellipse((x-500,y-80,x+500,y+80),outline='black',width=3);text(d,(x,y),c['id']+'\n'+c['name'],35,920)
  if key=='setup':indices=[0,1] if n in [4,5] else [0]
  elif key=='support':indices=[1] if n==20 else [0,1]
  elif key=='daily':indices=[0] if n in [8,10] else [1] if n in [9,11] else [0,1] if n==12 else [2] if n==13 else [0,2]
  else:indices=[0,1] if n==17 else [0]
  for idx in indices:
   _,fraction=actors[idx];ay=200+fraction*(h-350);d.line((260,ay+5,590,y),fill='#555555',width=2)
 im.save(R/f'figures/UC-{key}.png')
print('Rendered 4 business process diagrams and 4 UML use-case diagrams')
