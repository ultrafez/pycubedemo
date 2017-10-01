# Rainbow Explosions
# Copyright (C) Ian Kernick

import cubehelper
import random

DT = 1.0/64

class Pattern(object):
	def init(self):
		
		self.cube.size
		
		self.neighbours_coords = []
		self.neighbours_colors = []
		
		return DT
		
	def getRandColour(self, color):
		seed = random.randint(0,5)
		
		hi = 0.2
		md = 0.0
		lo = 0.0
		
		if seed == 0:
			r = hi
			g = md
			b = lo
		if seed == 1:
			r = hi
			b = md
			g = lo
		if seed == 2:
			b = hi
			r = md
			g = lo
		if seed == 3:
			b = hi
			g = md
			r = lo
		if seed == 4:
			g = hi
			r = md
			b = lo
		if seed == 5:
			g = hi
			b = md
			r = lo
			
		if r > 1.0:
			r = 1.0
			
		if g > 1.0:
			g = 1.0
		
		if b > 1.0:
			b = 1.0
		
		return (color[0]-r, color[1]-g, color[2]-b)
			
	def addNeighbours(self, coord, color):
		(x, y, z) = coord
		
		if x != 0 and not self.filled[x-1][y][z]:
			self.neighbours_coords.append((x-1,y,z))
			self.neighbours_colors.append(self.getRandColour(color))
			self.filled[x-1][y][z] = True
		if  x != self.cube.size-1 and not self.filled[x+1][y][z]:
			self.neighbours_coords.append((x+1,y,z))
			self.neighbours_colors.append(self.getRandColour(color))
			self.filled[x+1][y][z] = True
			
		if y != 0 and not self.filled[x][y-1][z]:
			self.neighbours_coords.append((x,y-1,z))
			self.neighbours_colors.append(self.getRandColour(color))
			self.filled[x][y-1][z] = True
		if  y != self.cube.size-1 and not self.filled[x][y+1][z]:
			self.neighbours_coords.append((x,y+1,z))
			self.neighbours_colors.append(self.getRandColour(color))
			self.filled[x][y+1][z] = True
			
		if z != 0 and not self.filled[x][y][z-1]:
			self.neighbours_coords.append((x,y,z-1))
			self.neighbours_colors.append(self.getRandColour(color))
			self.filled[x][y][z-1] = True
		if  z != self.cube.size-1 and not self.filled[x][y][z+1]:
			self.neighbours_coords.append((x,y,z+1))
			self.neighbours_colors.append(self.getRandColour(color))
			self.filled[x][y][z+1] = True
			
	def drawPixel(self, coord, color):
		self.cube.set_pixel(coord, color)
		(x, y, z) = coord
		
		self.addNeighbours(coord, color)
	
	def newStart(self):
		self.cube.clear()
		self.filled = [[[False for x in range(self.cube.size)] for y in range(self.cube.size)] for z in range(self.cube.size)]
		x = random.randint(0,self.cube.size-1);
		y = random.randint(0,self.cube.size-1);
		z = random.randint(0,self.cube.size-1);
		
		self.drawPixel((x, y, z), (1.0, 1.0, 1.0))
		
			
	def tick(self):
		for i in range(0, 3):
			if len(self.neighbours_coords) == 0:
				self.newStart()
				print 'reset'
			else:
				id = random.randint(0, len(self.neighbours_coords)-1)
				self.drawPixel(self.neighbours_coords[id], self.neighbours_colors[id])
				self.neighbours_coords.pop(id)
				self.neighbours_colors.pop(id)
				
		if False:
			raise StopIteration