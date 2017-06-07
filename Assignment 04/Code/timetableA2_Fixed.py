import sys
import random
import operator
from copy import deepcopy
#Sfrom numpy.oldnumeric.random_array import randint

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
        
class ExamSerial:
    def __init__(self, course, serial):
        self.course = course
        self.serial = serial

class PossibleResult:
    def __init__(self, printableSchedule,totalPenalty,totalSlot):
        self.printableSchedule = printableSchedule
        self.totalPenalty = totalPenalty
        self.totalSlot = totalSlot

#Tabu search. Some ideas were taken from the following slide
#http://www.ida.liu.se/~zebpe/heuristic/lectures/TS_basic.pdf
#We are considering exchanging of two slots. In that case
#The validity of tabus is going to be based on the number of exam slots taken
#Two slots are being exchanged, so tabu validity is going to be integer division
#of number of slots taken (here serial) divided by 2. A Tabu move can not be 
#considered till the time the tabu tenure has expired
def printExamSchedule1_TabuSearch(examSchedule, studentList, basePenalty):
    examSerialList = {}
    serial = 1
    totalSlot = 0
    for examInEachIndex in examSchedule:
        for eachExam in examInEachIndex:
            ##print "Exam %s %d"%(eachExam.name, eachExam.numberOfStudents)
            temp = ExamSerial(eachExam.name,serial)
            examSerialList[eachExam.name] = serial
        serial += 1
        totalSlot+=1                
    
    tabuTable = {}
    for exam1 in examSerialList:
        for exam2 in examSerialList:
            tabuTable[(exam1,exam2)] = 0
            tabuTable[(exam2,exam1)] = 0
    
    #for keys in tabuTable:
    #    print keys        
    
    #Paired test, valid for total number of slots//2 iterations. if there are total 7 slots then 
    #tabu validity will be for 3 iterations
    totalSmallestPenalty = basePenalty
    for iteration_count in range(1,serial//2):
    #if there is anything in the tabu list who's validity is greater than zero
    #then at the execution of each loop it's validity reduces. If it is zero then it is no
    #longer valid    
        #print "TabuSearch"
        index1ToSwap = 0;
        index2ToSwap = 0
        temporaryDictionaryForBestMove = {}
        for index1 in range(1,serial-1):
            for index2 in range(index1+1,serial):   #ensuring only different indices will be swapped
                copyExamSerialList = deepcopy(examSerialList)
                index1Key = [k for k in copyExamSerialList if copyExamSerialList[k] == index1]
                index2Key = [j for j in copyExamSerialList if copyExamSerialList[j] == index2]
                #temp1 = copyExamSerialList[index2Key]
                for key1 in index1Key:
                    copyExamSerialList[key1] = index2
                for key2 in index2Key:
                    copyExamSerialList[key2] = index1
                    
                examDictionary_1 = {}    
                for aExam in copyExamSerialList:
                    examDictionary_1[aExam] = (((copyExamSerialList[aExam] - 1)//5)+1,((copyExamSerialList[aExam] - 1)%5)+1)
                    #print examDictionary[aExam]
    
                consecutivePenalty = 0
                for aStudent in studentList:   
                    ###print aStudent.id
                    #overnightPenalty = 0
                    ##print aStudent.id
                    for c1 in aStudent.listOfCourses:
                        for c2 in aStudent.listOfCourses.difference(set([c1])):
                            if c1.name in examDictionary_1 and c2.name in examDictionary_1:
                                (d1,t1) = examDictionary_1[c1.name]
                                (d2,t2) = examDictionary_1[c2.name]
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
                            if c1.name in examDictionary_1 and c2.name in examDictionary_1:
                                (d1,t1) = examDictionary_1[c1.name]
                                (d2,t2) = examDictionary_1[c2.name]
                                dayDiff = -abs(d1 - d2)
                                if(dayDiff!=0):
                                    ###print "DayDiff is zero"
                                    penalty = pow(2,dayDiff)
                                    overnightPenalty += penalty
                totalPenalty = consecutivePenalty + overnightPenalty
                temporaryDictionaryForBestMove[(index1,index2)] = totalPenalty
                #print "Test6"
                #print totalPenalty     
                           
                #if(iteration_count==1):
                #    totalSmallestPenalty = totalPenalty;
                #    index1ToSwap = index1
                #    index2ToSwap = index2
                #else:
        #sortedByPenaltyValue = sorted(temporaryDictionaryForBestMove.items(), key = operator.itemgetter(1))
        #print sortedByPenaltyValue
        #for element in sortedByPenaltyValue:
            
 
                
        for element in sorted(temporaryDictionaryForBestMove.items(), key = operator.itemgetter(1)):
            (tempIndex1,tempIndex2) = element[0]
            #if(totalPenalty < totalSmallestPenalty):
            index1_SearchKey = [k for k in examSerialList if examSerialList[k] == tempIndex1]
            index2_SearchKey = [j for j in examSerialList if examSerialList[j] == tempIndex2]
            testFlag = True
            for exam1_key in index1_SearchKey:
                for exam2_key in index2_SearchKey:
                    if(tabuTable[(exam1_key,exam2_key)] != 0 or tabuTable[(exam2_key,exam1_key)] != 0):
                        testFlag = False
                        break
            if(testFlag == True):    
                index1ToSwap = tempIndex1
                index2ToSwap = tempIndex2
                break
                    
            #print tempIndex1,tempIndex2

        index1_TrueKey = [k for k in examSerialList if examSerialList[k] == index1ToSwap]
        index2_TrueKey = [j for j in examSerialList if examSerialList[j] == index2ToSwap]
        for key1 in index1_TrueKey:
            examSerialList[key1] = index2ToSwap
        for key2 in index2_TrueKey:
            examSerialList[key2] = index1ToSwap
        
        for exam1 in examSerialList:
            for exam2 in examSerialList:
                if(tabuTable[(exam1,exam2)] != 0 ):
                    tabuTable[(exam1,exam2)] -= 1 
                if(tabuTable[(exam2,exam1)] != 0 ):
                    tabuTable[(exam2,exam1)] -= 1 
                    
                
        for exam1_key in index1_TrueKey:
            for exam2_key in index1_TrueKey:
                tabuTable[(exam1_key,exam2_key)] = serial//2
                tabuTable[(exam2_key,exam1_key)] = serial//2

            #for exam1 in index1Key:
            #    for exam2 in index2Key:
            #        tabuTable[(exam1.name,exam2.name)] = True
            #        tabuTable[(exam2.name,exam1.name)] = True
    examScheduleList = []
    #print "Test9"
    
    examList = []
    for examInEachIndex in examSchedule:
        for eachExam in examInEachIndex:
            examList.append(eachExam)
            
    for key in examSerialList:
        for exam in examList:
            if(key == exam.name):
                temp = ExamSchedule(exam,((examSerialList[key]-1)//5+1),((examSerialList[key]-1)%5+1))        
                examScheduleList.append(temp)
    
    sortedExamScheduleList = sorted(examScheduleList, key= lambda schedule: (schedule.course.name,schedule.date,schedule.slot))
    #print "Test8"
    #for exam in sortedExamScheduleList:
    #    print exam.course.name, exam.date , exam.slot

    
  
    #print "Test7"
    #print totalSmallestPenalty
    
    #print "Test10"
    #print totalPenaltyCalculate(sortedExamScheduleList,studentList)

    #print "Test11"
    #print totalSlot
    return (sortedExamScheduleList,totalPenalty,totalSlot)
        
def printExamSchedule0(examSchedule, studentList):
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
    totalPenalty = totalPenaltyCalculate(sortedExamScheduleList,studentList)
    return (sortedExamScheduleList,totalPenalty,totalSlot)


def totalPenaltyCalculate(sortedExamScheduleList,studentList):
    
    examDictionary = {}
    for i in sortedExamScheduleList:
        examDictionary[i.course.name] = (i.date,i.slot)
    consecutivePenalty = 0
    for aStudent in studentList:   
        for c1 in aStudent.listOfCourses:
            for c2 in aStudent.listOfCourses.difference(set([c1])):
                if c1.name in examDictionary and c2.name in examDictionary:
                    (d1,t1) = examDictionary[c1.name]
                    (d2,t2) = examDictionary[c2.name]
                    dayDiff = -abs(d1 - d2)
                    if(dayDiff==0):
                        timeDiff = -abs(t1-t2)
                        ###print "DayDiff is zero"
                        penalty = 10 * pow(2,timeDiff)
                        consecutivePenalty += penalty  
    overnightPenalty = 0       
    for aStudent in studentList:   
        
        for c1 in aStudent.listOfCourses:
            for c2 in aStudent.listOfCourses.difference(set([c1])):
                ###print str(c1.name)+"Maps to"+str(c2.name)
                if c1.name in examDictionary and c2.name in examDictionary:
                    (d1,t1) = examDictionary[c1.name]
                    (d2,t2) = examDictionary[c2.name]
                    dayDiff = -abs(d1 - d2)
                    if(dayDiff!=0):
                        penalty = pow(2,dayDiff)
                        overnightPenalty += penalty
    totalPenalty = consecutivePenalty + overnightPenalty
    return totalPenalty

#RII algorithm for first soft constraint
#Simple concept of this algorithm is that we have a fixed walk probability of 0.6. If
#above this threshold, then the neighbor chosen from the neighborhood has
#the maximum number of students and minimum number of conflict with other courses. (Iterative improvement)
#if below this threshold, then both these heuristics are relaxed and a uniform random walk is performed
#In both cases, if two exams are in the same slot, they never have the same students
#In both cases, in every slot we try to pack as much exams as possible without conflicting.
def GenerateExamSchedule0(originalSortedCourseList,startingExamIndex,walkProbablity):
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
            if(walkProbablity >=0.6):       #walk probability
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

#Building partial candidate solution, started from different parts of the partial candidate solution to 
#build candidate solutions with iterative best improvement
#Employing a greedy technique. Starting off with a exam at a slot and looking at only local information at this point
#Each iteration, we see the value of the partial objective function 2 of putting a non-conflicting exam in the same slot
#and another exam in the next slot. For each case I maintain two list - one list(List1) contains the best possible exams to put in the 
#same slot who have the least value of the partial objective function 2. (There can be multiple)
#and in another list(List2), I maintain the possible exams to put in the next slot which have the same least value of the partial objective function.
#Which list chosen is based on the partial objective function value of list 1 and 2. If both are equal, then any can be chosen and I make a random choice
#between the list. After a list is chosen, if that list contains multiple exam choices with same objective function value, 
#then one is chosen randomly. In all cases, all of these choices are the best possible choices and any one can be chosen. 
#This builds various schedules of various lengths - good for initialization to tabu search.

def GenerateExamSchedule1(originalSortedCourseList,startingExamIndex,studentList,maxSlot):
    examschedule = []
    examAtEachIndex = set([])
    sortedCourseList = deepcopy(originalSortedCourseList)
    tempExam = sortedCourseList.pop(startingExamIndex);
    examAtEachIndex.add(tempExam)
    print maxSlot
    while len(sortedCourseList)!= 0 :
        
        if len(examschedule) > maxSlot:
            examschedule.append(examAtEachIndex)
            break
        
        conflictTotalList = set([])
        totalStudentsInSchedule = 0
        for exam in examAtEachIndex:
            conflictTotalList = conflictTotalList | exam.listOfConflictingCourses
            totalStudentsInSchedule += exam.numberOfStudents

        index_list = []
        examDictionarySameSlot = {}
        examDictionaryNextSlot = {}
        
        #rangeList = list(range(0,len(sortedCourseList)))
        for i in range(0,len(sortedCourseList)):
            tempCopyExam = deepcopy(sortedCourseList[i])
            if tempCopyExam.name not in conflictTotalList:
                if(totalStudentsInSchedule + tempCopyExam.numberOfStudents) <= roomSize:
                    copy1OfExamAtEachIndex = deepcopy(examAtEachIndex)
                    copy1OfExamAtEachIndex.add(tempCopyExam)
                    copy1Ofexamschedule = deepcopy(examschedule)
                    copy1Ofexamschedule.append(copy1OfExamAtEachIndex)
                    (printableSchedule1,totalPenalty1,totalSlot1) = printExamSchedule0(copy1Ofexamschedule,studentList)
                    examDictionarySameSlot[tempCopyExam] = totalPenalty1
                    break
                    
        for i in range(0,len(sortedCourseList)):
            tempCopyExam = deepcopy(sortedCourseList[i])   
            copy2OfExamAtEachIndex = deepcopy(examAtEachIndex)
            copy2Ofexamschedule = deepcopy(examschedule)
            copy2Ofexamschedule.append(copy2OfExamAtEachIndex)
            copy2OfExamAtEachIndex = set([])
            copy2OfExamAtEachIndex.add(tempCopyExam)
            copy2Ofexamschedule.append(copy2OfExamAtEachIndex)
            (printableSchedule2,totalPenalty2,totalSlot2) = printExamSchedule0(copy2Ofexamschedule,studentList)
            examDictionaryNextSlot[tempCopyExam] = totalPenalty2
            break
        
        if bool(examDictionarySameSlot) != False :
            min_PenaltyValueSameSlot = min(examDictionarySameSlot.itervalues())
            min_PenaltyValueKeySameSlot = [k for k in examDictionarySameSlot if examDictionarySameSlot[k] == min_PenaltyValueSameSlot]
            min_PenaltyValuedifferentSlot = min(examDictionaryNextSlot.itervalues())
            min_PenaltyValueKeydifferentSlot = [k for k in examDictionaryNextSlot if examDictionaryNextSlot[k] == min_PenaltyValuedifferentSlot]
            if(min_PenaltyValueSameSlot<min_PenaltyValuedifferentSlot):
                selected = random.choice(min_PenaltyValueKeySameSlot)
                examAtEachIndex.add(selected)
                #print "Test1"
                #print selected.name
                #print "hi"
                toRemove = None
                for i in sortedCourseList:
                    #print i.name
                    if i.name == selected.name:
                        toRemove = i
                sortedCourseList.remove(toRemove)

            elif(min_PenaltyValueSameSlot>min_PenaltyValuedifferentSlot):
                examschedule.append(examAtEachIndex)
                examAtEachIndex = set([])
                selected = random.choice(min_PenaltyValueKeydifferentSlot)
                examAtEachIndex.add(selected)
                #print "Test2"
                #print selected.name
                #print "hi"
                toRemove = None
                for i in sortedCourseList:
                    #print i.name
                    if i.name == selected.name:
                        toRemove = i
                sortedCourseList.remove(toRemove)
            else:

                selected = random.choice(min_PenaltyValueKeySameSlot)
                examAtEachIndex.add(selected)
                    #print "Test3"
                    #print selected.name
                    #print "hi"
                toRemove = None
                for i in sortedCourseList:
                        #print i.name
                    if i.name == selected.name:
                        toRemove = i
                sortedCourseList.remove(toRemove)
                
                
        else:
            min_PenaltyValuedifferentSlot = min(examDictionaryNextSlot.itervalues())
            min_PenaltyValueKeydifferentSlot = [k for k in examDictionaryNextSlot if examDictionaryNextSlot[k] == min_PenaltyValuedifferentSlot]
            examschedule.append(examAtEachIndex)
            examAtEachIndex = set([])
            selected = random.choice(min_PenaltyValueKeydifferentSlot)
            examAtEachIndex.add(selected)
            #print "Test3"
            #print selected.name
            #print "hi"
            toRemove = None
            for i in sortedCourseList:
                #print i.name
                if i.name == selected.name:
                    toRemove = i
            sortedCourseList.remove(toRemove)       
                         
        if(len(sortedCourseList)== 0):
            examschedule.append(examAtEachIndex)    
        
        
        
                    
    if len(sortedCourseList)!= 0:
        #this means max slot has been exceeded. Do something!!
        while len(sortedCourseList)!= 0 :
            
            for index in range(0,len(examschedule)):
                
                examAtEachIndex = examschedule[index]
                
                conflictTotalList = set([])
                totalStudentsInSchedule = 0
                for exam in examAtEachIndex:
                    conflictTotalList = conflictTotalList | exam.listOfConflictingCourses
                    totalStudentsInSchedule += exam.numberOfStudents
        
                index_list = []
                examDictionarySameSlot = {}
                
                tempCopyExam = None
                FoundFlag = False
                Removalindex = -1
                for i in range(0,len(sortedCourseList)):
                    tempCopyExam = deepcopy(sortedCourseList[i])
                    if tempCopyExam.name not in conflictTotalList:
                        if(totalStudentsInSchedule + tempCopyExam.numberOfStudents) <= roomSize:
                            examAtEachIndex.add(tempCopyExam)
                            FoundFlag = True
                            Removalindex = i
                            break
            
                if FoundFlag is True:
                    print tempCopyExam.name,"Copy?"
                    for i in range(0,len(sortedCourseList)):
                        print sortedCourseList[i].name
                    sortedCourseList.remove(sortedCourseList[Removalindex])
        
    return examschedule      
             
    

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




#Building a priority queue sort of thing
sortedCourseList = sorted(courseList, key = lambda course : (course.numberOfStudents ,  -len(course.listOfConflictingCourses)), reverse = True)

print arg4

if int(arg4) == 0 :
    #For most packed schedule, implemented Randomized iterative improvement.
    #Started with a partial candidate solution, relaxing the hard constraint of maximum number of slots.
    
    #Ordering heuristic of partial candidate solution:
    #The partial candidate solution is the sorted list of exams, primarily sorted by the number of students.
    #If number of students in two course is equal, then the courses are sorted by increasing number of conflicting courses 
    #For example, in the given example, courses 002,001,008 and 007 conflict with course 003 because of same student. This is 
    #used as a heuristic for the starting partial candidate solution. 
    #Executing multiple runs, taking different starting point from the partial candidate solution to try to pack the
    #schedule. Finally, only those schedules are taken which already fulfills other hard constraints and also fulfills the 
    #max slot constraint. Idea of RII taken from Hoos and stuzle. RII can give the optimal solution to any problem instance if
    #the process is run long enough. That is why it is chosen. We keep track of the best packed schedules so far
    #and print a new schedule if only a better schedule is found. Primary criteria is packing. If two schedules have the 
    #Same number of slots taken only then we rank the results by the optional 2nd soft constraint
    print "OBJ FUNC 1"
    #possibleScheduleList=[]
    #index = 0
    
    allOutputFileName = "allOutput_1"+arg3
    
    
    minPossibleSlot = maxSlot
    minPossiblePenalty = 0
    counter = 0
    #for startingExam in sortedCourseList:  
    copyofSortedCourseList = deepcopy(sortedCourseList)
        #for i in range(1,5000):
    numberOfExams = len(sortedCourseList)
    print numberOfExams
    for index in range(0,10000):
        examschedule = GenerateExamSchedule0(copyofSortedCourseList,(index % numberOfExams),random.uniform(0,1))
            #print "Exam"
            #print index
        (printableSchedule,totalPenalty,totalSlot) = printExamSchedule0(examschedule,studentList)
        flag = False
        if counter == 0 and totalSlot<=maxSlot:
            minPossibleSlot = totalSlot
            minPossiblePenalty = totalPenalty
            possibleResult = PossibleResult(printableSchedule,totalPenalty,totalSlot)
            #possibleScheduleList.append(possibleResult)
            flag = True
            outputFile = open(arg3,"wb+")
            outputFile.write(str(possibleResult.totalSlot)+"    "+str(possibleResult.totalPenalty)+"\n")
            for oneExam in possibleResult.printableSchedule:
                outputFile.write(oneExam.course.name+"    "+str(oneExam.date)+"    "+str(oneExam.slot)+"\n")
            outputFile.close()

            secondOutputFileForTest = open(allOutputFileName,"wb+")
            secondOutputFileForTest.write(str(possibleResult.totalSlot)+"    "+str(possibleResult.totalPenalty)+"\n")
            for oneExam in possibleResult.printableSchedule:
                secondOutputFileForTest.write(oneExam.course.name+"    "+str(oneExam.date)+"    "+str(oneExam.slot)+"\n")
            secondOutputFileForTest.close()

        else:
            if(totalSlot<=minPossibleSlot and totalPenalty<minPossiblePenalty):
                minPossibleSlot = totalSlot
                minPossiblePenalty = totalPenalty
                possibleResult = PossibleResult(printableSchedule,totalPenalty,totalSlot)
                #possibleScheduleList.append(possibleResult)
                flag = True
                outputFile = open(arg3,"wb+")
                outputFile.write(str(possibleResult.totalSlot)+"    "+str(possibleResult.totalPenalty)+"\n")
                for oneExam in possibleResult.printableSchedule:
                    outputFile.write(oneExam.course.name+"    "+str(oneExam.date)+"    "+str(oneExam.slot)+"\n")
                outputFile.close()
    
                secondOutputFileForTest = open(allOutputFileName,"a+")
                secondOutputFileForTest.write(str(possibleResult.totalSlot)+"    "+str(possibleResult.totalPenalty)+"\n")
                for oneExam in possibleResult.printableSchedule:
                    secondOutputFileForTest.write(oneExam.course.name+"    "+str(oneExam.date)+"    "+str(oneExam.slot)+"\n")
                secondOutputFileForTest.close()
            
            print minPossibleSlot,minPossiblePenalty
            

        counter += 1;
    

else  :
    #For most spread schedule with least penalty, we used tabu search with random initialization. First we took 
    #the partial candidate solution, and started from different parts of the partial candidate solution to 
    #build candidate solutions with iterative best improvement. Then we fed our tabu search algoritm those results
    #The neighborhood contained neighbors that can be reached by exchanging two exam slots.  
    print "OBJ FUNC 2"
    parameter_IMPROVEMENT_TRIAL = 500
    
    allOutputFileName = "allOutput_2"+arg3
    
    copyofSortedCourseList = deepcopy(sortedCourseList)
    #minPossibleSlot = maxSlot
    minPossiblePenalty = 0
    counter = 0
    
    list1  = list(range(0,len(copyofSortedCourseList)))
    #print list1
    flag = False
    improvementTrial = 0
    
    for i in range(0,10000):   
        print "Counter:",counter    
        print "ImprovementTrial:",improvementTrial 
        examschedule = GenerateExamSchedule1(copyofSortedCourseList,list1[i%10],studentList,maxSlot)
        (initialPrintableSchedule,initialTotalPenalty,initTotalSlot) = printExamSchedule0(examschedule,studentList)
        #(printableSchedule,totalPenalty,totalSlot) = printExamSchedule1_TabuSearch(examschedule,studentList,initialTotalPenalty)
        
        (printableSchedule,totalPenalty,totalSlot) = (initialPrintableSchedule,initialTotalPenalty,initTotalSlot)
        
        #print totalPenalty,totalSlot
        if counter == 0 and totalSlot<=maxSlot:
                #minPossibleSlot = totalSlot
            minPossiblePenalty = totalPenalty
            possibleResult = PossibleResult(printableSchedule,totalPenalty,totalSlot)
            
            flag = True
            improvementTrial = 0
            print totalPenalty,totalSlot
            outputFile = open(arg3,"wb+")
            outputFile.write(str(possibleResult.totalSlot)+"    "+str(possibleResult.totalPenalty)+"\n")
            for oneExam in possibleResult.printableSchedule:
                outputFile.write(oneExam.course.name+"    "+str(oneExam.date)+"    "+str(oneExam.slot)+"\n")
            outputFile.close()
        
            secondOutputFileForTest = open(allOutputFileName,"wb+")
            secondOutputFileForTest.write(str(possibleResult.totalSlot)+"    "+str(possibleResult.totalPenalty)+"\n")
            for oneExam in possibleResult.printableSchedule:
                secondOutputFileForTest.write(oneExam.course.name+"    "+str(oneExam.date)+"    "+str(oneExam.slot)+"\n")
            secondOutputFileForTest.close()
            counter += 1;   
            
        else:
            if improvementTrial < parameter_IMPROVEMENT_TRIAL:
                if(totalPenalty<minPossiblePenalty):
                    #minPossibleSlot = totalSlot
                    minPossiblePenalty = totalPenalty
                    possibleResult = PossibleResult(printableSchedule,totalPenalty,totalSlot)
                    print totalPenalty,totalSlot
                    flag = True
                    improvementTrial = 0
                    
                    
                    outputFile = open(arg3,"wb+")
                    outputFile.write(str(possibleResult.totalSlot)+"    "+str(possibleResult.totalPenalty)+"\n")
                    for oneExam in possibleResult.printableSchedule:
                        outputFile.write(oneExam.course.name+"    "+str(oneExam.date)+"    "+str(oneExam.slot)+"\n")
                    outputFile.close()
        
                    secondOutputFileForTest = open(allOutputFileName,"a+")
                    secondOutputFileForTest.write(str(possibleResult.totalSlot)+"    "+str(possibleResult.totalPenalty)+"\n")
                    for oneExam in possibleResult.printableSchedule:
                        secondOutputFileForTest.write(oneExam.course.name+"    "+str(oneExam.date)+"    "+str(oneExam.slot)+"\n")
                    secondOutputFileForTest.close()    
                        
                else :
                    improvementTrial +=1
                    flag = False
                            

                    
            else :
                break;
            counter += 1;
        #print minPossiblePenalty
            
            
    #raise NameError('HiThere')

    numberOfExams = len(sortedCourseList)
    improvementTrial = 0
    for i in range(0,10000):   
        print "Counter_2:",counter     
        examschedule = GenerateExamSchedule0(copyofSortedCourseList,i % numberOfExams,random.uniform(0,1))
        (initialPrintableSchedule,initialTotalPenalty,initTotalSlot) = printExamSchedule0(examschedule,studentList)
        #(printableSchedule,totalPenalty,totalSlot) = printExamSchedule1_TabuSearch(examschedule,studentList,initialTotalPenalty)
        
        (printableSchedule,totalPenalty,totalSlot) = (initialPrintableSchedule,initialTotalPenalty,initTotalSlot)
        
        if counter == 0 and totalSlot<=maxSlot:
                #minPossibleSlot = totalSlot
            minPossiblePenalty = totalPenalty
            possibleResult = PossibleResult(printableSchedule,totalPenalty,totalSlot)
            print totalPenalty,totalSlot
            flag = True
            improvementTrial = 0
            
            outputFile = open(arg3,"wb+")
            outputFile.write(str(possibleResult.totalSlot)+"    "+str(possibleResult.totalPenalty)+"\n")
            for oneExam in possibleResult.printableSchedule:
                outputFile.write(oneExam.course.name+"    "+str(oneExam.date)+"    "+str(oneExam.slot)+"\n")
            outputFile.close()
        
            secondOutputFileForTest = open(allOutputFileName,"wb+")
            secondOutputFileForTest.write(str(possibleResult.totalSlot)+"    "+str(possibleResult.totalPenalty)+"\n")
            for oneExam in possibleResult.printableSchedule:
                secondOutputFileForTest.write(oneExam.course.name+"    "+str(oneExam.date)+"    "+str(oneExam.slot)+"\n")
            secondOutputFileForTest.close()
            counter += 1;   
            
        else:
            if improvementTrial < parameter_IMPROVEMENT_TRIAL:
                if(totalPenalty<minPossiblePenalty and totalSlot<=maxSlot):
                    #minPossibleSlot = totalSlot
                    print totalPenalty,totalSlot
                    minPossiblePenalty = totalPenalty
                    possibleResult = PossibleResult(printableSchedule,totalPenalty,totalSlot)
                    
                    flag = True
                    improvementTrial = 0
                    
                    
                    outputFile = open(arg3,"wb+")
                    outputFile.write(str(possibleResult.totalSlot)+"    "+str(possibleResult.totalPenalty)+"\n")
                    for oneExam in possibleResult.printableSchedule:
                        outputFile.write(oneExam.course.name+"    "+str(oneExam.date)+"    "+str(oneExam.slot)+"\n")
                    outputFile.close()
        
                    secondOutputFileForTest = open(allOutputFileName,"a+")
                    secondOutputFileForTest.write(str(possibleResult.totalSlot)+"    "+str(possibleResult.totalPenalty)+"\n")
                    for oneExam in possibleResult.printableSchedule:
                        secondOutputFileForTest.write(oneExam.course.name+"    "+str(oneExam.date)+"    "+str(oneExam.slot)+"\n")
                    secondOutputFileForTest.close()    
                        
                else :
                    improvementTrial +=1
                    flag = False
                            

                    
            else :
                break;
            counter += 1;
        #print minPossiblePenalty         



