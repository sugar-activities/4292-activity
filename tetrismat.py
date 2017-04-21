import olpcgames, pygame#, logging 

import math
import time
import datetime
import random
from pygame.locals import *

music = True
def splitImage(image,parts):
	images = []
	imrect = image.get_rect()
	for x in range(parts):
		tile = pygame.Surface((imrect.width/parts,imrect.height),SRCALPHA, 32)
		tile.blit(image,(0,0),(x*(imrect.width/parts),0,(imrect.width/parts),imrect.height))
		tile=tile.convert_alpha()
		images.append(tile)
	return images

def createBackground(image,width,height):
	res = pygame.Surface((width,height))
	for y in range(0,height,image.get_rect().height):
		for x in range(0,width,image.get_rect().width):
			res.blit(image,(x,y))
	res=res.convert()
	return res


class Frame():
	def __init__(self,resource_image,rect,rect_tile_1,rect_tile_2,rect_tile_3,rect_tile_4,rect_tile_5,rect_tile_6,rect_tile_7,rect_tile_8,rect_tile_9):
		self.rect = pygame.rect.Rect(rect)
		self.image =  pygame.Surface((self.rect.width,self.rect.height),SRCALPHA,32)
		self.image.blit(resource_image,(0,0),rect_tile_1)
		for x in range(rect_tile_1[2],self.rect.width-rect_tile_3[2],rect_tile_2[2]):
			self.image.blit(resource_image,(x,0),rect_tile_2)
		self.image.blit(resource_image,(self.rect.width-rect_tile_3[2],0),rect_tile_3)

		for y in range(rect_tile_1[3],self.rect.height-rect_tile_7[3],rect_tile_4[3]):
			self.image.blit(resource_image,(0,y),rect_tile_4)
			for x in range(rect_tile_4[2],self.rect.width-rect_tile_6[2],rect_tile_5[2]):
				self.image.blit(resource_image,(x,y),rect_tile_5)
			self.image.blit(resource_image,(self.rect.width-rect_tile_6[2],y),rect_tile_6)


		self.image.blit(resource_image,(0,self.rect.height-rect_tile_7[3]),rect_tile_7)
		for x in range(rect_tile_7[2],self.rect.width-rect_tile_9[2],rect_tile_8[2]):
			self.image.blit(resource_image,(x,self.rect.height-rect_tile_8[3]),rect_tile_8)
		self.image.blit(resource_image,(self.rect.width-rect_tile_9[2],self.rect.height-rect_tile_9[3]),rect_tile_9)
		self.image=self.image.convert_alpha()
	def draw(self,screen):
		screen.blit(self.image,(self.rect.x,self.rect.y))

class WaitIcon():
	def __init__(self):
		pass
	def draw(self,screen):
		screen.blit(img_graphics,(screen.get_rect().width/2-42,screen.get_rect().height/2-42),
		(815,293,84,84)
	)
	

class TextDisplay(pygame.sprite.Sprite):
	def __init__(self,rect,group,font,align,foreground,background):
		pygame.sprite.Sprite.__init__(self,group)
		self.rect = rect
		self.background = background
		self.foreground = foreground
		self.font=font
		self.align=align
		self.image=pygame.Surface((self.rect.width,self.rect.height))
		self.image.fill(self.background)

		self.text = ""

	def setText(self,text):
		if self.text != text:
			self.image.fill(self.background)
			imgtext = self.font.render(text, True, self.foreground)
			if self.align == "left" or self.align==None:
				self.image.blit(imgtext,(0,(self.image.get_rect().height/2) - (imgtext.get_rect().height/2)))
			elif self.align == "center":
				self.image.blit(imgtext,((self.image.get_rect().width/2) - (imgtext.get_rect().width/2)),(self.image.get_rect().height/2) - (imgtext.get_rect().height/2))
			elif self.align == "right":
				self.image.blit(imgtext,((self.image.get_rect().width) - (imgtext.get_rect().width)),(self.image.get_rect().height/2) - (imgtext.get_rect().height/2))
			self.text=text

class ScoreDisplay(TextDisplay):
	def __init__(self,group):
		TextDisplay.__init__(self,pygame.Rect(10,12,390,45),group,font40,"left",(255,255,255),(255,0,0))
		self.setText("Puntos: 0")
	def setValue(self,score):
		self.setText("Puntos: %d" % (score))



class LevelDisplay(TextDisplay):
	def __init__(self,group):
		TextDisplay.__init__(self,pygame.Rect(19,57,300,32),group,font30,"left",(255,255,255),(255,0,0))
		self.setText("Nivel: 1")
	def setValue(self,level):
		self.setText("Nivel: %d" % (level))


class TimerDisplay(TextDisplay):
	def __init__(self,group,location,width):
		self.width=width
		TextDisplay.__init__(self,pygame.Rect(location.x,location.y,width,45),group,font40,"left",(255,255,255),(255,0,0))
		self.setText("---")
		self.prev="---"

	def setValue(self,left):
		self.setText("%02d" % (left))
		
		


class StatusDisplay(TextDisplay):
	def __init__(self,group,location,width):
		TextDisplay.__init__(self,pygame.Rect(location.x,location.y,width,40),group,font30,"left",(255,255,255),(255,0,0))
		self.setText("")
	def setValue(self,status):
		self.setText(status)

class InGamePiece(pygame.sprite.Sprite):
	lastId=0
	def __init__(self,numberId,colorId):
		pygame.sprite.Sprite.__init__(self)
		InGamePiece.lastId = InGamePiece.lastId+1
		self.Id = InGamePiece.lastId
		self.value = numberId
		self.image = pygame.Surface([bsize,bsize],SRCALPHA, 32)
		self.back = pygame.Surface([bsize,bsize],SRCALPHA, 32)

		self.rect = self.image.get_rect()
		self.selector = None
		self.IsSelected = False
		self.image.blit(img_graphics,(0,0),(colorId*82,0,bsize,bsize))
		imgoffset = bsize
		if numberId > 9 and numberId<=19:
			imgoffset = 150
			numberId-=10

		elif numberId > 19 and numberId<=29:
			imgoffset = 215
			numberId-=20
		elif numberId > 29 and numberId<=39:
			imgoffset = 275
			numberId-=30
			
		self.image.blit(img_graphics,(0,0),(numberId*82,imgoffset,bsize,bsize))
		self.image = self.image.convert_alpha()
		self.back.blit(self.image,(0,0))
		self.back = self.back.convert_alpha()
		self.dirty=True
		self.IsSelected = False
		self.frameno = 0
	def select(self):
		self.IsSelected=True
	def unselect(self):
		self.IsSelected=False
		self.image.blit(self.back,(0,0))
		self.dirty=True
	def update(self):
		if self.IsSelected:
			self.image.blit(self.back,(0,0))
			self.image.blit(imgs_select[self.frameno],(0,0))
			self.frameno=self.frameno+1
			if self.frameno >7:
				self.frameno=0
			self.dirty=True


class IncommingPiece(pygame.sprite.Sprite):
	def __init__(self,piece,location,limitY,group,pieceGroup):
		pygame.sprite.Sprite.__init__(self,group)
		self.Vyo = math.sin(1.5707963267948966)
		self.cont=0
		self.sprite = piece
		self.spY = location.y
		self.ymax = limitY
		self.rect = self.sprite.rect
		self.rect.x = location.x
		self.rect.y = location.y
		piece.remove(piece.groups())
		self.image = self.sprite.image
		#self.sprite.rect.x=location.x
		self.pieceGroup=pieceGroup
	def update(self):
		self.cont = self.cont + 0.9
		dy = (self.Vyo * self.cont - 0.5 * 20 * self.cont ** 2) #* 10
		
		self.sprite.rect.y = self.spY - dy
		#if self.sprite.Id==1:
			#print(str(dy) +"  " + str(self.sprite.rect.y))
		self.rect.y = self.spY - dy
		if self.sprite.rect.y > self.ymax:
			self.sprite.rect.y = self.ymax -self.sprite.rect.height
			
			self.rect.y = self.ymax 
			self.sprite.add(self.pieceGroup)
			self.sprite.dirty=True
			self.kill()


class OutgoingPiece(pygame.sprite.Sprite):
	def __init__(self,piece,group,visibleRect):
		pygame.sprite.Sprite.__init__(self,group)
		self.limit = pygame.rect.Rect(visibleRect)
		self.spX = piece.rect.x
		self.spY = piece.rect.y
		self.angle = random.randrange(80,100) * math.pi/180.	#el angulo es en radianes
		self.rotate = 1
		self.speed = random.randrange(20,50)
		self.rs = random.randrange(-3,3)
		piece.remove(piece.groups())
		self.image = piece.image
		self.orig_image = self.image
		self.rect = piece.rect
		self.Vx = self.speed * math.cos(self.angle)
		self.Vyo = self.speed * math.sin(self.angle)
		self.cont =0

	def update(self):
		self.cont = self.cont + 0.9
		self.rotate = self.rotate+self.rs
		if self.rotate > 360:
			self.rotate = 1
		self.image = pygame.transform.rotate(self.orig_image,self.rotate)
		self.rect.width = self.image.get_rect().width
		self.rect.height = self.image.get_rect().height
		dx = (self.Vx * self.cont) #* 10
		dy = (self.Vyo * self.cont - 0.5 * 12 * self.cont ** 2) #* 10
		self.rect.x = self.spX + dx
		self.rect.y = self.spY - dy
		if not self.limit.colliderect(self.rect):
			self.kill()


class Timer():
	def __init__(self,value):
		self.value = value
		self.stopped=True
		self.start_time=datetime.datetime.today()
		self.end_time = self.start_time + datetime.timedelta(0,self.value)
		self.time_left = datetime.timedelta(0,self.value) - (datetime.datetime.today() - self.start_time)

	def start(self):
		self.stopped = False
		self.start_time = datetime.datetime.today()
		self.end_time = self.start_time + datetime.timedelta(0,self.value)
	def set(self,value):
		self.value = value

	def cicle(self):
		if not self.stopped:
			self.time_left = datetime.timedelta(0,self.value) - (datetime.datetime.today() - self.start_time)
			if self.time_left.seconds>self.value:
				return True
			if self.time_left.seconds<=0:
				return True
			else:
				return False
		else:
			return False
	
	def stop(self):
		self.stopped=True

class SimpleButton():
	def __init__(self,text,rect):
		self.rect = pygame.Rect(rect)
		self.image = pygame.Surface((self.rect.width,self.rect.height),SRCALPHA, 32)
		Frame(
			img_graphics,
			(0,0,self.rect.width,self.rect.height),
			(822,0,8,10),(822+11,0,8,10),(822+189,0,8,10),
			(822+0,10,8,10),(822+10,10,8,10),(822+189,10,8,10),
			(822+0,54,8,10),(822+10,54,8,10),(822+189,54,8,10)).draw(self.image)
		txt = font20.render(text, True, (255,255,255))
		self.image.blit(txt,(self.rect.width/2-txt.get_rect().width/2,self.rect.height/2-txt.get_rect().height/2))
	def draw(self,screen):
		screen.blit(self.image,(self.rect.x,self.rect.y))
	def checkEvent(self,event):
		if event.type == MOUSEBUTTONDOWN:
			if self.rect.collidepoint(event.pos):
				return True
		return False
		
class SimpleImageButton():
	def __init__(self,location,sourceRect):
		self.location=location
		sourceRect = pygame.Rect(sourceRect)
		self.rect = pygame.Rect((location.x,location.y,sourceRect.width,sourceRect.height))
		self.image = pygame.Surface((self.rect.width,self.rect.height),SRCALPHA, 32)
		self.image.blit(img_graphics,(0,0),sourceRect)
		self.image = self.image.convert_alpha()
	def draw(self,screen):
		screen.blit(self.image,(self.rect.x,self.rect.y))

	def checkEvent(self,event):
		if event.type == MOUSEBUTTONDOWN:
			if self.rect.collidepoint(event.pos):
				return True
		return False

		
class TwoStateImageButton():
	def __init__(self,location,sourceRect,value=True):
		self.location=location

		self.enabledRect = pygame.Rect(sourceRect)
		self.disabledRect=pygame.Rect(sourceRect)
		self.rect = pygame.Rect((location.x,location.y,self.enabledRect.width,self.enabledRect.height))

		self.enabledImg = pygame.Surface((self.rect.width,self.rect.height),SRCALPHA, 32)
		self.enabledImg.blit(img_graphics,(0,0),self.enabledRect)
		self.disabledRect.y += self.disabledRect.height
		self.disabledImg = pygame.Surface((self.rect.width,self.rect.height),SRCALPHA, 32)
		self.disabledImg.blit(img_graphics,(0,0),self.disabledRect)

		self.disabledImg = self.disabledImg.convert_alpha()
		self.enabledImg = self.enabledImg.convert_alpha()

		self.value = value
	def draw(self,screen):
		if self.value:
			screen.blit(self.enabledImg,(self.rect.x,self.rect.y))
		else:
			screen.blit(self.disabledImg,(self.rect.x,self.rect.y))

	
	def checkEvent(self,event):
		if event.type == MOUSEBUTTONDOWN:
			if self.rect.collidepoint(event.pos):
				self.value = not self.value
				return True
		return False
	


class GameLevel():
	def __init__(self,easiness):
		self.timer = Timer(0)
		self.level=1
		self.score=0
		self.easiness = easiness
		self.initialRows = 0
		self.timer.set(1)
		self.timer.start()
		self.count = 0
		self.high = 0
		self.incommingTime=20
	def update(self):
		self.timer.cicle()
	def incrementScore(self):
		self.score = self.score +10
		if self.score % 150 == 0:
			self.level=self.level+1
	def timeLeft(self):
		if self.initialRows >= 3:
			return self.timer.time_left.seconds
		return self.incommingTime

	def checkOperation(self,selection):
		l = len(selection)
		if l == 0:
			return False,"? ? ? = ?"
		elif l == 1:
			return False,"%d ? ? = ?" % (selection[0].value)
		elif l == 2:
			return False,"%d ? %d = ?" % (selection[0].value,selection[1].value)
		elif l == 3:
			
			operator = None
			if  selection[0].value + selection[1].value == selection[2].value:
				operator = "+"
			elif selection[0].value - selection[1].value == selection[2].value:
				operator = "-"
			elif selection[0].value * selection[1].value == selection[2].value:
				operator = "x"
			elif selection[1].value >0 and float(selection[0].value)/ float(selection[1].value) == float(selection[2].value):
				operator = "/"

			if operator == None:
				return False,"%d ? %d = %d !" % (selection[0].value,selection[1].value,selection[2].value)
			else:
				self.incrementScore()
				return True,"%d %s %d = %d Ok" % (selection[0].value,operator,selection[1].value,selection[2].value)
	def createPieces(self,count):
		res = []
		if self.initialRows < 2:
			if self.timer.cicle():
				valor = 0
				for x in range(0,count):
					#print(str(self.count) + "  " +str(self.count /50) + ">" +str(self.high)+ " === "+str(self.count /50 > self.high))
					if self.count >self.easiness:
						res.append(InGamePiece(random.randrange(10,40),random.randrange(0,10)))
						self.count=0
					else:
						res.append(InGamePiece(random.randrange(0,10),random.randrange(0,10)))
					self.count+=1
				self.initialRows=self.initialRows+1
				self.timer.set(1.3)
				self.timer.start()

		elif self.timer.cicle():
			for x in range(0,count):
				if self.count >self.easiness:
					res.append(InGamePiece(random.randrange(10,40),random.randrange(0,10)))
					self.count=0
				else:
					res.append(InGamePiece(random.randrange(0,10),random.randrange(0,10)))
				self.count+=1
			self.initialRows=self.initialRows+1
			newtime = self.incommingTime - (self.incommingTime * ((self.level-1) * 5))/100
			if newtime < 10:
				newtime=10

			self.timer.set(newtime)
			self.timer.start()
		return res

class PieceGroup(pygame.sprite.Group):
	def __init__(self):
		pygame.sprite.Group.__init__(self)
		self.dirtyrects = []

	def add(self,*sprites):
		for sprite in sprites:
			sprites.dirty=True
		pygame.sprite.Group.add(self,*sprites)

	def add_internal(self, sprite):
		sprite.dirty=True
		return pygame.sprite.Group.add_internal(self,sprite)
	def draw(self,surface):
		sprites = self.sprites()
		surface_blit = surface.blit
		for spr in sprites:
			if spr.dirty:
				surface_blit(spr.image, spr.rect)
				spr.dirty=False



class OutgoingPieceGroup(pygame.sprite.Group):
	def __init__(self,bsgroup):
		pygame.sprite.Group.__init__(self)
		self.bsgroup=bsgroup

	def	update(self):
		g = pygame.sprite.groupcollide(self.bsgroup,self,False,False)
		for spr in g:
			spr.dirty=True
		return pygame.sprite.Group.update(self)
		
class Location():
	def __init__(self,x,y):
		self.x = x
		self.y = y

class GameScreen():
	def __init__(self,screen,size):
		pass
	def handleEvent(self,event):
		pass	
	def updateScreen(self,screen):
		pass

class PlayScreen(GameScreen):
	def __init__(self,screen,size,gameLevel,mnuOnly=False):
		GameScreen.__init__(self,screen,size)
		self.gameLevel=gameLevel
		self.yoffset = 100		#100 pixels para la parte de arriba , nivel ,puntaje logo
		self.bcols = int(size[0]/bsize)
		self.xoffset = int((size[0]-(self.bcols*bsize))/2)
		if self.xoffset==0:
			self.bcols=self.bcols-1
		self.xoffset = int((size[0]-(self.bcols*bsize))/2)
		self.stacklimit = int((size[1]-self.yoffset-60)/bsize)
		self.background = createBackground(backgroundTile,self.bcols*bsize,self.stacklimit*bsize)	
		self.displayGroup = pygame.sprite.Group()
		self.gamePiecesGroup = PieceGroup()
		self.incommingGroup = pygame.sprite.Group()
		self.outgoingGroup = OutgoingPieceGroup(self.gamePiecesGroup)
		self.scoreDisplay = ScoreDisplay(self.displayGroup)
		self.levelDisplay = LevelDisplay(self.displayGroup)
		self.timerDisplay = TimerDisplay(self.displayGroup,Location(screen.get_rect().width/2-30,30),60)
		if not mnuOnly:
			self.statusDisplay = StatusDisplay(self.displayGroup,Location(20,self.yoffset+(self.stacklimit*bsize)+8),350)
		screen.blit(self.background,(self.xoffset,self.yoffset))
		#top
		self.create_decorpanel((0,0,size[0],self.yoffset),164).draw(screen)
		#left
		self.create_decorpanel((0,self.yoffset,self.xoffset,self.stacklimit*bsize),574).draw(screen)
		#right
		self.create_decorpanel((size[0] - self.xoffset,self.yoffset,self.xoffset,self.stacklimit*bsize),656).draw(screen)
		#bottom
		self.create_decorpanel((0,self.yoffset+(self.stacklimit*bsize),size[0],size[1]-self.yoffset+(self.stacklimit*bsize)),246).draw(screen)
		self.exitBtn = SimpleImageButton(Location(size[0]-100,size[1]-50),(914,167,52,39))
		#recuadros del texto
		
		Frame(img_graphics,(screen.get_rect().width/2-40,20,80,60),
			(822,0,8,10),(822+11,0,8,10),(822+189,0,8,10),
			(822+0,10,8,10),(822+10,10,8,10),(822+189,10,8,10),
			(822+0,54,8,10),(822+10,54,8,10),(822+189,54,8,10)).draw(screen)
		Frame(img_graphics,(8,7,400,86),
			(822,0,8,10),(822+11,0,8,10),(822+189,0,8,10),
			(822+0,10,8,10),(822+10,10,8,10),(822+189,10,8,10),
			(822+0,54,8,10),(822+10,54,8,10),(822+189,54,8,10)).draw(screen)
		if not mnuOnly:
			Frame(img_graphics,(6,self.yoffset+(self.stacklimit*bsize)+5,400,50),
			(822,0,8,10),(822+11,0,8,10),(822+189,0,8,10),
			(822+0,10,8,10),(822+10,10,8,10),(822+189,10,8,10),
			(822+0,54,8,10),(822+10,54,8,10),(822+189,54,8,10)).draw(screen)

		screen.blit(img_graphics,(size[0]-90,4),(822,185,74,98))
		screen.blit(img_graphics,(size[0]-190,4),(822,185,74,98))
		self.musicBtn = TwoStateImageButton(Location(size[0]-160,size[1]-50),(914,88,52,39),music)
		self.selection = []
		#Cargamos la musica
		pygame.mixer.music.set_volume(0.8)
		while pygame.mixer.music.get_busy():
			pygame.mixer.music.stop()
#		pygame.mixer.music.load(music_fileName)
		if mnuOnly:
			self.scoreDisplay.setText("Tetris Mat!")
			self.levelDisplay.setText("Version 1.0")
		else:
			self.exitBtn.draw(screen)
			self.musicBtn.draw(screen)

		self.displayGroup.update()
		self.displayGroup.draw(screen)

	def create_decorpanel(self,rect,tile_offset):
		return Frame(img_graphics,rect,
			(tile_offset,0,9,10),(tile_offset+11,0,9,10),(tile_offset+70,0,9,10),
			(tile_offset+0,10,9,10),(tile_offset+10,10,9,10),(tile_offset+70,10,9,10),
			(tile_offset+0,70,9,10),(tile_offset+10,70,9,10),(tile_offset+70,70,9,10))

	def handleEvent(self,event):
		global music
		if self.exitBtn.checkEvent(event):
			return "menu"

		if self.musicBtn.checkEvent(event):
			music = self.musicBtn.value
			if self.musicBtn.value and not pygame.mixer.music.get_busy():
				pygame.mixer.music.play()
			else:
				pygame.mixer.music.stop()


			
		if event.type == MOUSEBUTTONDOWN:
			for piece in self.gamePiecesGroup:
				if piece.rect.collidepoint(event.pos):
					if piece.IsSelected:
						for x in self.selection:
							x.unselect()
						self.selection=[]
					else:
						piece.select()
						self.selection.append(piece)
			res,status = self.gameLevel.checkOperation(self.selection)
			if len(self.selection) == 3:
				falling_list={}
				for x in self.selection:
					if res:
						for z in self.gamePiecesGroup:
							if not z.IsSelected and z.rect.x == x.rect.x and z.rect.y < x.rect.y:
								if z.Id in falling_list:
									falling_list[z.Id]["newpos"] = falling_list[z.Id]["newpos"]+x.rect.height
								else:
									falling_list[z.Id] = {"newpos":x.rect.height,"ptr":z}

						#los que vienen cayendo
						for z in self.incommingGroup:
							if z.rect.x == x.rect.x:
								z.ymax = z.ymax + x.rect.height
						x.unselect()
						OutgoingPiece(x,self.outgoingGroup,(self.xoffset,self.yoffset,bsize*self.bcols,bsize*self.stacklimit))
						if self.musicBtn.value:
							snd_zingpop.play()
					else:
						x.unselect()
				for s in falling_list.values():
					IncommingPiece(s["ptr"],Location(s["ptr"].rect.x,s["ptr"].rect.y),s["ptr"].rect.y+s["newpos"],self.incommingGroup,self.gamePiecesGroup)
				self.selection=[]
			self.statusDisplay.setValue(status)
					
	def update(self):

		self.gameLevel.update()
		self.scoreDisplay.setValue(self.gameLevel.score)
		self.levelDisplay.setValue(self.gameLevel.level)
		self.timerDisplay.setValue(self.gameLevel.timeLeft())
		if len(self.incommingGroup)==0:
			newPieces = self.gameLevel.createPieces(self.bcols)
		
			x=self.xoffset
			
			for piece in newPieces:
				# Calculamos la coordenada y donde va a ir a parar esta pieza
				y =10000
				for s in self.gamePiecesGroup:
					if s.rect.x== x and s.rect.y < y:
						y = s.rect.y
				if y==10000:
					y=((self.stacklimit-1)*bsize)+self.yoffset
				else:
					y=y-bsize
				if y<=self.yoffset-bsize:
					return "gameover"
				IncommingPiece(piece,Location(x,self.yoffset),y,self.incommingGroup,self.gamePiecesGroup)
				x=x+bsize
			if len(newPieces) >0 and self.musicBtn.value:
				snd_whoosh.play()

		self.gamePiecesGroup.update()
		self.incommingGroup.update()
		self.outgoingGroup.update()
		
	
	def updateScreen(self,screen):
		for r in self.incommingGroup.sprites():
			screen.blit(self.background,r.rect,(r.rect.x-self.xoffset,r.rect.y-self.yoffset,r.rect.width,r.rect.height))
		for r in self.outgoingGroup.sprites():
			screen.blit(self.background,r.rect,(r.rect.x-self.xoffset,r.rect.y-self.yoffset,r.rect.width,r.rect.height))

		res = self.update()
		screen.set_clip((self.xoffset,self.yoffset,bsize*self.bcols,bsize*(self.stacklimit)))
		self.gamePiecesGroup.draw(screen)
		self.incommingGroup.draw(screen)
		self.outgoingGroup.draw(screen)
		screen.set_clip();
		self.displayGroup.draw(screen)
		if self.musicBtn.value:
			if not pygame.mixer.music.get_busy(): # si la musica se detiene o no arranco la arrancamos
				pygame.mixer.music.play()
		self.musicBtn.draw(screen)
		return res

class GameOverScreen(GameScreen):
	def __init__(self,screen,size):
		GameScreen.__init__(self,screen,size)
		Frame(img_graphics,(size[0]/2-250,size[1]/2-100,500,200),
			(164,0,9,10),(164+11,0,9,10),(164+70,0,9,10),
			(164+0,10,9,10),(164+10,10,9,10),(164+70,10,9,10),
			(164+0,70,9,10),(164+10,70,9,10),(164+70,70,9,10)).draw(screen)
		txt=font40.render("Juego terminado", True, (255,0,0))	
		screen.blit(txt,(size[0]/2-txt.get_rect().width/2,(size[1]/2-txt.get_rect().height/2) - 20))
		self.btn = SimpleButton("Cerrar",(size[0]/2-80,size[1]/2+40,160,50))
		self.btn.draw(screen)
	def handleEvent(self,event):
		if self.btn.checkEvent(event):
			return "menu"


class CreditsScreen(GameScreen):
	def __init__(self,screen,size):
		#screen.fill((0,0,200))
		screen.blit(img_graphics,((size[0]/2)-(537/2),(size[1]/2)-(320/2)),(0,363,537,390))
	def handleEvent(self,event):
		if event.type == MOUSEBUTTONDOWN:
			return "menu"
	

#---------------------------------------------------------------------------------------------------------
class MenuScreen():
	def __init__(self,screen,size):
		PlayScreen(screen,size,GameLevel(0),True)
		font=font40
		self.color = (255,255,0)
		self.overcolor = (255,0,0)
		self.options =[
			{"caption":"Facil","option":"easy"},
			{"caption":"No tanto","option":"middle"},
			{"caption":"Dificil","option":"hard"},

			{"caption":"Creditos","option":"credits"},
			{"caption":"Salir","option":"os"}
		]
		height=0
		sep=0
		tile_offset=164
		rect = screen.get_rect()
		for op in self.options:
			op['image'] = font.render(op['caption'], True, self.color)
			op['imageover'] = font.render(op['caption'], True, self.overcolor)
			op['pos']=[rect.width/2 - op['image'].get_rect().width/2,0]
			op['over']=False
			height = height+op['image'].get_rect().height
		height=height+40
		y = rect.height/2
		y =y - height/2
		sep = height / len(self.options)
		for op in self.options:
			op['pos']=[op['pos'][0],y]
			screen.blit(op["image"],(op['pos'][0],y))
			op['rect'] = op["image"].get_rect()
			op['rect'].x=op['pos'][0]
			op['rect'].y = y
			y = y+sep

	def handleEvent(self,event):
		if event.type == MOUSEBUTTONDOWN:
			for op in self.options:
				if op['rect'].collidepoint(event.pos):
					return op['option']	


	def updateScreen(self,screen):
		pos = pygame.mouse.get_pos()
		for op in self.options:
			if op['rect'].collidepoint(pos):
				if not op['over']:
					screen.blit(op['imageover'],op['pos'])
					op['over']=True
			else:
				if op['over']:
					screen.blit(op['image'],op['pos'])
					op['over']=False

#---------------------------------------------------------------------------------------------------------
class GameControl():
	def __init__(self):
		pass

	def run(self,size,screen):
		global music_fileName,snd_whoosh,snd_zingpop,img_graphics,imgs_select,backgroundTile,font40,font20,font30,bsize
		img_graphics = pygame.image.load("eqr.png")
		WaitIcon().draw(screen)
		pygame.display.flip()
		clock = pygame.time.Clock()
		
		bsize=80
		#sonidos
		music_fileName = "Aoftodo.ogg"
		pygame.mixer.music.load(music_fileName)
		snd_whoosh =pygame.mixer.Sound("whoosh03.wav")
		snd_whoosh.set_volume(1.2)

		snd_zingpop=pygame.mixer.Sound("zingpop.wav")
		snd_zingpop.set_volume(0.2)
		#graficos
		imgs_select= splitImage(pygame.image.load("anselect.png"),8)
		backgroundTile = pygame.image.load("background.png")	
		#fuentes
		font40 = pygame.font.Font("BD_Cartoon_Shout.ttf",40)
		font20 = pygame.font.Font("BD_Cartoon_Shout.ttf",20)
		font30 = pygame.font.Font("BD_Cartoon_Shout.ttf",30)
		current_screen = MenuScreen(screen,size)
		while current_screen:
			clock.tick(20)
			next=None
			for event in  pygame.event.get():

				if event.type == QUIT:
					return
				next=current_screen.handleEvent(event)
			if next == None:
				next = current_screen.updateScreen(screen)
			
			pygame.display.flip()
			if next != None:
				if next != "os":
					WaitIcon().draw(screen)
					pygame.display.flip()

				if next == "os":
					return
				elif next=="menu":
					current_screen = MenuScreen(screen,size)
				elif next=="gameover":
					current_screen = GameOverScreen(screen,size)
				elif next=="easy":
					current_screen = PlayScreen(screen,size,GameLevel(1000))
				elif next=="middle":
					current_screen = PlayScreen(screen,size,GameLevel(20))
				elif next=="hard":
					current_screen = PlayScreen(screen,size,GameLevel(5))
				elif next=="credits":
					current_screen = CreditsScreen(screen,size)

def main():
	pygame.init()
	resolution = (1200,700)
	flags = 0
	if olpcgames.ACTIVITY:
		# Running as Activity
		resolution = olpcgames.ACTIVITY.game_size
	else:
		pass
		# flags = pygame.FULLSCREEN

	screen = pygame.display.set_mode(resolution, flags)
	#Copiado de conozco Uruguay
	xbm_cursor = (
		"XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX  ",
		"XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX ",
		"XXX.........................XXXX",
		"XXX..........................XXX",
		"XXX..........................XXX",
		"XXX.........................XXXX",
		"XXX.......XXXXXXXXXXXXXXXXXXXXX ",
		"XXX........XXXXXXXXXXXXXXXXXXX  ",
		"XXX.........XXX                 ",
		"XXX..........XXX                ",
		"XXX...........XXX               ",
		"XXX....X.......XXX              ",
		"XXX....XX.......XXX             ",
		"XXX....XXX.......XXX            ",
		"XXX....XXXX.......XXX           ",
		"XXX....XXXXX.......XXX          ",
		"XXX....XXXXXX.......XXX         ",
		"XXX....XXX XXX.......XXX        ",
		"XXX....XXX  XXX.......XXX       ",
		"XXX....XXX   XXX.......XXX      ",
		"XXX....XXX    XXX.......XXX     ",
		"XXX....XXX     XXX.......XXX    ",
		"XXX....XXX      XXX.......XXX   ",
		"XXX....XXX       XXX.......XXX  ",
		"XXX....XXX        XXX.......XXX ",
		"XXX....XXX         XXX.......XXX",
		"XXX....XXX          XXX......XXX",
		"XXX....XXX           XXX.....XXX",
		"XXX....XXX            XXX....XXX",
		"XXXX..XXXX             XXXXXXXX ",
		" XXXXXXX                XXXXXX  ",
		"  XXXXX                  XXXX   ")
	cursor= pygame.cursors.compile(xbm_cursor)
	pygame.mouse.set_cursor((32,32),(1,1),*cursor)
	GameControl().run(resolution,screen)

if __name__=='__main__':
	main()

