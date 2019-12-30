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

		if(course["prereqs_obj"]["invert"]):
			self.pre = Course.invert(self.pre)
		if(course["coreqs_obj"]["invert"]):
			self.coIn = Course.invert(self.coIn)

	def updateReqs(self, courseList):
		Course.updateReq(courseList, self, (lambda x: x.pre), (lambda x: x.post))
		Course.updateReq(courseList, self, (lambda x: x.coIn), (lambda x: x.coOut))

	def updateReq(courseList, core, coreAccess, otherAccess):
		for rl in coreAccess(core):
			for cn in rl:
				c = courseList.get(cn)
				if(c != None and core.courseNum not in otherAccess(c)):
					otherAccess(c).append(core.courseNum)

	def invert(reqs):
		newreq = []
		if(len(reqs) == 1):
			for course in reqs[0]:
				newreq.append([course])
			return newreq

		courses = reqs.pop(0)
		subreqs = Course.invert(reqs)

		for course in courses:
			for c in subreqs:
				copy = c.copy()
				copy.append(course)
				newreq.append(copy)

		return newreq

def loadCourses():
	with open("courseAPI.json") as json_file:
		courses = json.load(json_file)["courses"]
	courseList = {}

	for cn in courses:
		courseList[cn] = Course(cn, courses[cn])

	for cn in courseList:
		courseList[cn].updateReqs(courseList)

	return courseList

def generateEdgeList(courseList):
	edgeList = []
	for course in courseList:
		for p in courseList[course].post:
			tupl = (course, p)
			if(tupl not in edgeList):
				edgeList.append(tupl)
	return edgeList

def coursePrint(courseList, c):
	print("### " + c + " ###")
	print("prereqs: ", clist[c].pre)
	print("coreqs:", clist[c].coIn)
	print("used as coreq: ", clist[c].coOut)
	print("postreqs: ", clist[c].post)
	print()

def generate():
	clist = loadCourses()
	edgeList = generateEdgeList(clist)

	with open("edges.json", "w") as json_file:
		courses = json.dump(edgeList, json_file)

generate()
