import json

class Course:
	
	def __init__(self, courseNum, course):
		self.courseNum = courseNum
		self.pre = course["prereqs_obj"]["reqs_list"]
		self.coIn = course["coreqs_obj"]["reqs_list"]
		self.coOut = []
		self.post = []
		
		if(self.pre == None):
			self.pre = []
		if(self.coIn == None):
			self.coIn = []
	
	def updateReq(self, courseList):
		for rl in self.pre:
			for cn in rl:
				c = courseList.get(cn)
				if(c != None and not(self.courseNum in c.post)):
					c.post.append(self.courseNum)
		
		for rl in self.coIn:
			for cn in rl:
				c =  courseList.get(cn)
				if(c != None and not(self.courseNum in c.coOut)):
					c.coOut.append(self.courseNum)

def loadCourses():
	with open("out.json") as json_file:
		courses = json.load(json_file)["courses"]
	courseList = {}
	
	for cn in courses:
		courseList[cn] = Course(cn, courses[cn])
		
	for cn in courseList:
		courseList[cn].updateReq(courseList)
		
	return courseList

def coursePrint(courseList, c):
	print("### " + c + " ###")
	print("prereqs: ", clist[c].pre)
	print("coreqs:", clist[c].coIn)
	print("used as coreq: ", clist[c].coOut)
	print("postreqs: ", clist[c].post)
	print()
	
clist = loadCourses()

coursePrint(clist, "15-122")
coursePrint(clist, "15-251")
coursePrint(clist, "21-127")
