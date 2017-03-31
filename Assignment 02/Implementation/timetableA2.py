import sys
import random
from copy import deepcopy
from numpy.oldnumeric.random_array import randint

class Course:
    
    def __init__(self,newName,number):
        self.name = newName
        self.numberOfStudents = number
        self.listOfStudents = set([])
        self.listOfConflictingCourses = set([]) 
    
    
    def _addStudent_(self,newStudent):
        #self.listOfStudents.append(newStudent)
        self.listOfStudents.add(newStudent)
        
    def _addConflictingCourses_(self,conflictCourse):
        ###print "%s conflicts with %s" %(self.name,conflictCourse)
        ###print "%s conflict array had size %d" %(self.name,self.listOfConflictingCourses.__len__())
        self.listOfConflictingCourses.add(conflictCourse)
        ###print "%s conflict array has size %d" %(self.name,self.listOfConflictingCourses.__len__())





class Student:

    def __init__(self,ID):
        self.id = ID 
        self.listOfCourses = set([])      #contains course class object
        ###print "student %s" % self.id


        
    def _addCourses_(self, newCourse):
        ###print "student %s adding %s" %(self.id,newCourse.name)
        for course in self.listOfCourses:
            ###print "student %s already has course %s" %(self.id,course.name)
            course._addConflictingCourses_(newCourse.name)
            newCourse._addConflictingCourses_(course.name)
        
            
        self.listOfCourses.add(newCourse)
        #self.listOfCourses.append(newCourse)
        newCourse._addStudent_(self.id)

class ExamSchedule:
    def __init__(self, course, date, slot):
        self.course = course
        self.date = date
        self.slot = slot

class PossibleResult:
    def __init__(self, printableSchedule,totalPenalty,totalSlot):
        self.printableSchedule = printableSchedule
        self.totalPenalty = totalPenalty
        self.totalSlot = totalSlot
            
        
def printExamSchedule(examSchedule, studentList):
    examScheduleList = []
    slot = 1
    day = 1
    totalSlot = 0
    for examInEachIndex in examSchedule:
        for eachExam in examInEachIndex:
            ##print "Exam %s %d"%(eachExam.name, eachExam.numberOfStudents)
            temp = ExamSchedule(eachExam,day,slot)
            examScheduleList.append(temp)
        slot += 1
        if(slot>5):
            day += 1
            slot -=5        #each day has five slots
        totalSlot+=1     
        
    sortedExamScheduleList = sorted(examScheduleList, key= lambda schedule: (schedule.date,schedule.slot))
    
    ###print str(totalSlot)
    
    examDictionary = {}
    for i in sortedExamScheduleList:
        ###print i.course.name
        examDictionary[i.course.name] = (i.date,i.slot)
        ##print examDictionary[i.course.name],i.course.name

    #for i in examDictionary:
        ###print examDictionary[i],i.name
    #Penalty calculation
    #Tested, gives accurate output    
    consecutivePenalty = 0
    for aStudent in studentList:   
        ###print aStudent.id
        #overnightPenalty = 0
        ##print aStudent.id
        for c1 in aStudent.listOfCourses:
            for c2 in aStudent.listOfCourses.difference(set([c1])):
                ###print str(c1.name)+"Maps to"+str(c2.name)
                (d1,t1) = examDictionary[c1.name]
                ###print (d1,t1),c1.name
                (d2,t2) = examDictionary[c2.name]
                ###print (d2,t2),c2.name
                dayDiff = -abs(d1 - d2)
                if(dayDiff==0):
                    timeDiff = -abs(t1-t2)
                    ###print "DayDiff is zero"
                    penalty = 10 * pow(2,timeDiff)
                    consecutivePenalty += penalty  
    overnightPenalty = 0       
    for aStudent in studentList:   
        ###print aStudent.id
        #overnightPenalty = 0
        
        for c1 in aStudent.listOfCourses:
            for c2 in aStudent.listOfCourses.difference(set([c1])):
                ###print str(c1.name)+"Maps to"+str(c2.name)
                (d1,t1) = examDictionary[c1.name]
                (d2,t2) = examDictionary[c2.name]
                dayDiff = -abs(d1 - d2)
                if(dayDiff!=0):
                    ###print "DayDiff is zero"
                    penalty = pow(2,dayDiff)
                    overnightPenalty += penalty
    totalPenalty = consecutivePenalty + overnightPenalty
    
    ###print totalPenalty  

    
    
    return (sortedExamScheduleList,totalPenalty,totalSlot)


#Starting with different candidate partial solution. Relaxing maximum number of slot 
#constraint. Choosing a neighbor at random. 
def GenerateExamSchedule(originalSortedCourseList,startingExamIndex,u):
    examschedule = []
    examAtEachIndex = set([])
    #startingIndex = sortedCourseList.index(startingExam)
    ###print "printing index"
    ###print startingIndex
    sortedCourseList = deepcopy(originalSortedCourseList)
    tempExam = sortedCourseList.pop(startingExamIndex);
    ##print "popped %s"%tempExam.name
    #for xm in sortedCourseList:
        ##print "Left exam%s"%xm.name
    examAtEachIndex.add(tempExam)
    while len(sortedCourseList)!= 0 :
        conflictTotalList = set([])
        totalStudentsInSchedule = 0
        for exam in examAtEachIndex:
            conflictTotalList = conflictTotalList | exam.listOfConflictingCourses
            totalStudentsInSchedule += exam.numberOfStudents
            ###print totalStudentsInSchedule
            ###print conflictTotalList
        
        index_list = []
        rangeList = list(range(0,len(sortedCourseList)))
        ##print rangeList
        for i in range(0,len(sortedCourseList)):
            #tempCopyExam = deepcopy(sortedCourseList[i])
            if(u==0):
                tempCopyExam = sortedCourseList[i]
            else:
                selection = random.choice(rangeList)
                rangeList.remove(selection)
                ##print selection
                tempCopyExam = sortedCourseList[selection]
            ###print tempCopyExam
            
            if tempCopyExam.name not in conflictTotalList:
                if(totalStudentsInSchedule + tempCopyExam.numberOfStudents) <= roomSize:
                    examAtEachIndex.add(tempCopyExam);
                    conflictTotalList = conflictTotalList |tempCopyExam.listOfConflictingCourses
                    totalStudentsInSchedule += tempCopyExam.numberOfStudents
                    index_list.append(tempCopyExam)
        
        for i in index_list:
            sortedCourseList.remove(i)
        
        examschedule.append(examAtEachIndex)
        examAtEachIndex = set([])
        conflictTotalList = set([])
        if(len(sortedCourseList)!= 0):
            tempExam = sortedCourseList.pop(0);
            ##print "huh!"
            ##print tempExam.name
            examAtEachIndex.add(tempExam)
            if(len(sortedCourseList)== 0):
                examschedule.append(examAtEachIndex)
    #for i in examschedule:
        #for j in i:
            ##print j.name
    
    return examschedule

def CheckIfInList(possibleScheduleList,printableSchedule):
    copyOfPossibleScheduleList = deepcopy(possibleScheduleList)
    copyOfPrintableSchedule = deepcopy(printableSchedule)
    sortedCopyOfPrintableSchedule = sorted(copyOfPrintableSchedule , key=lambda schedule: schedule.course.name)
    ##print "Sorted Version of Schedule"
    for aSchedule in copyOfPossibleScheduleList:
        #for i in aSchedule:
            ##print i.course,i.date, i.slot
        sorted_VersionofASchedule = sorted(aSchedule, key=lambda schedule: schedule.course.name)
        #for i in sorted_VersionofASchedule:
            ##print i.course,i.date, i.slot
        ##print "Target schedule"
        #for i in sortedCopyOfPrintableSchedule:
            ##print i.course,i.date, i.slot
        
             
    

arg1 = sys.argv[1]
arg2 = sys.argv[2]
arg3 = sys.argv[3]
arg4 = sys.argv[4]

###print arg1 
###print arg2 
###print arg3 
###print arg4

courseFile = open(arg1,"r")
studentFile = open(arg2,"r")
###print courseFile.name
###print studentFile.name
###print outputFile.name

#Read coursesFromCourseFiles
lineCounter = 0
roomSize = 0
maxSlot = 0
courseList = []
while 1:
    try:
        line = courseFile.next()
        ###print line
        #strings = line.split()
        ###print strings
    except StopIteration:
        break
    else:
        ###print line
        strings = line.split()
        ###print strings
        if lineCounter==0:
            #reading the first line, means first input is roomCapacity
            #second input is max timeSlots
            roomSize = int(strings[0])
            ###print "RoomSize: %d" %roomSize
            maxSlot = int(strings[1])
            ###print "Maximum Slots: %d" %maxSlot
        else:
            ###print strings
            #Have a object of course type and insert sizeOfStudents
            newCourse = Course(strings[0],int(strings[1]))
            courseList.append(newCourse)
            
        lineCounter += 1

courseFile.close()



#for course in courseList:
#    ##print "%s %s" %(course.name,course.numberOfStudents)          


#Read Students from .stu file
studentList = []
studentCounter = 1
while 1:
    try:
        studentLine = studentFile.next()
        ###print line
        #strings = line.split()
        ###print strings
    except StopIteration:
        break
    else:
        ###print studentLine
        studentCourses = studentLine.split()
        ###print studentStrings
        newStudent = Student(studentCounter)

        for studentCourse in studentCourses:
            for course in courseList:
                if studentCourse==course.name:
                    ###print course.name
                    newStudent._addCourses_(course)
        ###print "***"          
        studentList.append(newStudent) 
        studentCounter+=1;           



#Close all the file object
studentFile.close()


#for student in studentList:
#    ##print "%s" %(student.id)
#    for course_number in student.listOfCourses:
#        ##print "%s " %course_number.name         
#
#for course in courseList:
#    ##print "-*#-*#-*#-"
#    ##print "%s %s" %(course.name,course.numberOfStudents)    
#    ##print "-*-*-*-"
#    for conflictingCourse in course.listOfConflictingCourses:
#        ##print conflictingCourse
#        
#for course in courseList:
#     ##print course.numberOfStudents
#     ##print sorted(course.listOfConflictingCourses)


#Building a priority queue sort of thing
sortedCourseList = sorted(courseList, key = lambda course : (course.numberOfStudents ,  -len(course.listOfConflictingCourses)), reverse = True)

#for course in sortedCourseList:
    ##print "Course:"+course.name
    ##print course.numberOfStudents
    ##print sorted(course.listOfConflictingCourses)

##print "test"

#testing for most packed schedule. starting with different points - different initializations
#Constructive local search, starting from a partial candidate solution
#Target is to perturb the results from constructive local search
#Have only unique results in constructive local search to start perturbing from
#Keep adding them to possible schedule list
#intesification strategy applied, attempting to greedily improve solution

#Need to employ a randomness in to implement stocastic local search technique

#Neighbourhood: try k-exchange neighbourhood. exchange two exams - one exam in each slot?,

#Strategy: 
#Pick one of the given exams to put in the first slot. do it random?
#Have some solutions. in GenerateExamSchedule, apply randomization technique to pick up
#a exam from a list of viable exams to put in a slot

possibleScheduleList=[]
index = 0
minPossibleSlot = maxSlot
minPossiblePenalty = 0
counter = 0
for startingExam in sortedCourseList:  
    copyofSortedCourseList = deepcopy(sortedCourseList)
    #for i in range(1,5000):
    for i in range(0,1000):
        examschedule = GenerateExamSchedule(copyofSortedCourseList,index,1)
        ##print "Exam"
        ##print index
        (printableSchedule,totalPenalty,totalSlot) = printExamSchedule(examschedule,studentList)
        flag = False
        if counter == 0 and totalSlot<=maxSlot:
            minPossibleSlot = totalSlot
            minPossiblePenalty = totalPenalty
            possibleResult = PossibleResult(printableSchedule,totalPenalty,totalSlot)
            possibleScheduleList.append(possibleResult)
            flag = True
        else:
            if(totalSlot<=minPossibleSlot and totalPenalty<minPossiblePenalty):
                minPossibleSlot = totalSlot
                minPossiblePenalty = totalPenalty
                possibleResult = PossibleResult(printableSchedule,totalPenalty,totalSlot)
                possibleScheduleList.append(possibleResult)
                flag = True
        print minPossibleSlot,minPossiblePenalty
        
        if flag is True:
            outputFile = open(arg3,"wb+")
            outputFile.write(str(possibleResult.totalSlot)+"    "+str(possibleResult.totalPenalty)+"\n")
            for oneExam in possibleResult.printableSchedule:
                outputFile.write(oneExam.course.name+"    "+str(oneExam.date)+"    "+str(oneExam.slot)+"\n")
            outputFile.close()

            
        #CheckIfInList(possibleScheduleList,printableSchedule)
        
        #possibleScheduleList.append(possibleResult)
        counter += 1;
    index +=1
##print "test2"
##print len(possibleScheduleList)
#(printableSchedule,totalPenalty,totalSlot) = printExamSchedule(examschedule,studentList)
outputFile = open("allResult.sol","wb+")
for onePossibleSchedule in possibleScheduleList:
    ###print onePossibleSchedule
    outputFile.write(str(onePossibleSchedule.totalSlot)+"    "+str(onePossibleSchedule.totalPenalty)+"\n")
    for oneExam in onePossibleSchedule.printableSchedule:
        outputFile.write(oneExam.course.name+"    "+str(oneExam.date)+"    "+str(oneExam.slot)+"\n")
#outputFile.write(str(totalSlot)+"    "+str(totalPenalty)+"\n")
#for oneExam in printableSchedule:
#    outputFile.write(oneExam.course.name+"    "+str(oneExam.date)+"    "+str(oneExam.slot)+"\n")
#outputFile.write(printableSchedule)    
outputFile.close()
