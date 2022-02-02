import pygame
import random

pygame.init()

W,H=400,600
WIN=pygame.display.set_mode((W,H))
pygame.display.set_caption("RAINDROP METH")
PATH=r"C:\Users\HP\Pictures\GameS\Raindrop"
bg=pygame.image.load(PATH+r"\clouds.jpg")
water=pygame.image.load(PATH+r"\water.png")
drop=pygame.image.load(PATH+r"\raindropp.png")

interval=200
lvl=1
vel=3
rw=70
rh=25
dh=17
inp=[]
enter=False
nm=' '
FONT_COMM=pygame.font.SysFont("arial",rh,True)
FONT_DROP=pygame.font.SysFont("arial",dh,True)
CLK=pygame.time.Clock()
Points=0


class Raindrop():
	def __init__(self,x,y,n1,n2,op,res,v):
		self.x=x
		self.y=y
		self.n1=n1
		self.n2=n2
		self.operation=op
		self.result=res
		self.vel=v
		self.width=drop.get_width()
		self.height=drop.get_height()
	
	def draw(self):
		num1_txt=FONT_DROP.render(str(self.n1),1,(0,0,0))
		num2_txt=FONT_DROP.render(str(self.n2),1,(0,0,0))
		op_txt  =FONT_DROP.render(self.operation,1,(0,0,0))
		WIN.blit(drop,(self.x,self.y))		
		n1w=num1_txt.get_width()
		nh=num1_txt.get_height()
		n2w=num1_txt.get_width()
		y=self.y+self.height//2
		x=self.x+self.width//2 
		WIN.blit(num1_txt,(x-(n1w//2),y-(nh+2)))
		WIN.blit(op_txt,(x-4,y))
		WIN.blit(num2_txt,(x-n2w//2,y+nh+2))
	
	def move(self):
		self.y+=self.vel

x=random.randint(1,9)
y=random.randint(1,9)
z=random.choice(['+','-','/','*'])
drops=[Raindrop(random.randint(1,W-20),-50,x,y,'+',(x+y),vel)]
y_checker=drops[0].y

def likely_number_list(lvl,c=False):
	lst=[]
	l=lvl
	k=c
	while l+1:
		for i in range(10):
			lst.append(i)
		if l-1 >0:
			for i in range(10,19-3*k):
				lst.append(i)
		l-=1
	return lst



def dropp():
	global y_checker
	if y_checker>=interval-(10*(lvl//1.5)):
		z=random.choice(['+','-','/','x'])
		res=0
		if z=='+':
			x=random.choice(likely_number_list(lvl))
			y=random.choice(likely_number_list(lvl))			
			res=x+y
		elif z=='-':
			while True:
				x=random.choice(likely_number_list(lvl))
				y=random.choice(likely_number_list(lvl))
				if y<=x:
					break
			res=x-y
		elif z=='/':
			while True:
				x=random.choice(likely_number_list(lvl,True))
				y=random.choice(likely_number_list(lvl,True))
				if x%y==0:
					break
			res=x//y
		else:
			while True:
				x=random.choice(likely_number_list(lvl,True))
				y=random.choice(likely_number_list(lvl,True))
				if x>10 and y>10 and lvl <6:
					continue
			res=x*y

		drops.append(Raindrop(random.randint(1,W-80),-100,x,y,z,res,vel))
		y_checker=-50
	y_checker+=vel
	for drop in drops:
		drop.draw()
		drop.move()


def draw_inpbox():
	pygame.draw.rect(WIN,(255,255,255),[W//2-rw//2,560,rw,rh])

def take_inputs():
	global nm,enter,inp
	txt=FONT_COMM.render("".join(inp),0,(0,0,0))
	WIN.blit(txt,(W//2-rw//2,560))
	if enter:
		if len(inp):
			nm=int("".join(inp))
			enter=False
			inp=[]

def check_inputs():
	global Points,nm
	if not(nm==' '):
		for drop in drops:	
				if nm==drop.result:
					drops.remove(drop)
					Points+=(50)*lvl
	nm=" "


def disp_points():
	txt=FONT_COMM.render(str(Points),1,(0,0,0))
	WIN.blit(txt,(5,5))

def fell_to_water():
	global Life
	for drop in drops:
		if drop.y>500:
			drops.remove(drop)
			Life-=1
	if Life:
		return True
	else:
		return False


RUN=True
key=" "
Life=3
while RUN:
	CLK.tick(30)
	WIN.blit(bg,(-200,0))
	WIN.blit(water,(-100,450))
	if Points>=200*lvl:
		lvl+=1

	for event in pygame.event.get():
		if event.type==pygame.QUIT:
			RUN=False
			pygame.quit()

		if event.type==pygame.KEYDOWN:
			key=event.unicode
			if ord(key)>=48 and ord(key)<=57:
				inp.append(key)
			elif event.key==pygame.K_BACKSPACE:
				inp.pop(len(inp)-1)
			if event.key==13:
				enter=True



	draw_inpbox()
	take_inputs()
	dropp()
	check_inputs()
	disp_points()
	if not(fell_to_water()):
		RUN=False


	pygame.display.update()