import sys
import random
import operator
from copy import deepcopy
from numpy.oldnumeric.random_array import randint

#################################################################
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
        #print "%s conflicts with %s" %(self.name,conflictCourse)
        ###print "%s conflict array had size %d" %(self.name,self.listOfConflictingCourses.__len__())
        self.listOfConflictingCourses.add(conflictCourse)
        #print "%s conflict array has size %d" %(self.name,self.listOfConflictingCourses.__len__())

################################################################
class Student:

    def __init__(self,ID):
        self.id = ID 
        self.listOfCourses = set([])      #contains course class object
        ###print "student %s" % self.id
        
    def _addCourses_(self, newCourse):
        #print "student %s adding %s" %(self.id,newCourse.name)
        for course in self.listOfCourses:
            #print "student %s already has course %s" %(self.id,course.name)
            course._addConflictingCourses_(newCourse.name)
            newCourse._addConflictingCourses_(course.name)
        
        self.listOfCourses.add(newCourse)
        #self.listOfCourses.append(newCourse)
        newCourse._addStudent_(self.id)
###################################################################

def GenerateExamTimeTable(examschedule):
    examschedule_dictionary = {}
    
    day_Slot = 1
    day = 1
    uniqueSlot = 1
    totalNumberOfSlots = 0
    for i in examschedule:
        tempPrintList = []
        for j in i:
            tempPrintList.append(j.name)
            examschedule_dictionary[j.name] = (day,day_Slot,uniqueSlot)
        #print "GenerateTimeTable"    
        #print tempPrintList
        day_Slot +=1
        uniqueSlot += 1
        if(day_Slot>5):
            day += 1
            day_Slot -= 5
        totalNumberOfSlots+=1

    return examschedule_dictionary,totalNumberOfSlots

################
def GenerateSolutionResultFromGivenSolution(examschedule_dictionary, courseDictionary,studentDictionary):
    totalNumberOfSlots = 0
    courseList = list()
    for key in examschedule_dictionary:
        courseList.append(key)
        if(examschedule_dictionary[key][2]>totalNumberOfSlots):
            totalNumberOfSlots = examschedule_dictionary[key][2]
            
    
    sorted(courseList)
    penalty = totalPenaltyCalculate(examschedule_dictionary,studentDictionary)
    
    Key_examschedule_dictionary_AsList=[]
    for key_eachExam in courseList:
        #print examschedule_dictionary[key_eachExam],key_eachExam
        (day,dayslot,actualSlot)= examschedule_dictionary[key_eachExam]
        Key_examschedule_dictionary_AsList.append((key_eachExam,day,dayslot,actualSlot))
    
    #print Key_examschedule_dictionary_AsList
    Key_examschedule_dictionary_AsImmutableTuple = tuple(Key_examschedule_dictionary_AsList)
    #print Key_examschedule_dictionary_AsImmutableTuple
    return examschedule_dictionary,totalNumberOfSlots,penalty,Key_examschedule_dictionary_AsImmutableTuple


################generate initial solutions for Objective Function 0 ##########################
def GenerateInitialSolution_OBJ0(aCourseListOrder, courseDictionary,studentDictionary):
    examschedule = []
    examAtEachIndex = set([])
    #print aCourseListOrder
    copyOfGivenCourseOrder = deepcopy(aCourseListOrder)
    key_tempExam = copyOfGivenCourseOrder.pop(0)
    tempExam = courseDictionary[key_tempExam]
    examAtEachIndex.add(tempExam)
    while(len(copyOfGivenCourseOrder)!= 0):
        conflictTotalList = set([])
        totalStudentsInSchedule = 0
        for exam in examAtEachIndex:
            conflictTotalList = conflictTotalList | exam.listOfConflictingCourses
            totalStudentsInSchedule += exam.numberOfStudents
            
            
        index_list = []
        rangeList = list(range(0,len(copyOfGivenCourseOrder)))  
        
        for i in range(0,len(copyOfGivenCourseOrder)):
            key_tempCopyExam = copyOfGivenCourseOrder[i]
            tempCopyExam = courseDictionary[key_tempCopyExam]
            
            if tempCopyExam.name not in conflictTotalList:
                if(totalStudentsInSchedule + tempCopyExam.numberOfStudents) <= roomSize:
                    examAtEachIndex.add(tempCopyExam)
                    conflictTotalList = conflictTotalList |tempCopyExam.listOfConflictingCourses
                    totalStudentsInSchedule += tempCopyExam.numberOfStudents
                    index_list.append(key_tempCopyExam)
                    
        for i in index_list:
            copyOfGivenCourseOrder.remove(i)
                    
        examschedule.append(examAtEachIndex)
        examAtEachIndex = set([])
        conflictTotalList = set([])
        if(len(copyOfGivenCourseOrder)!= 0):
            key_tempExam = copyOfGivenCourseOrder.pop(0)
            tempExam = courseDictionary[key_tempExam]
            examAtEachIndex.add(tempExam)
            if(len(copyOfGivenCourseOrder)== 0):
                examschedule.append(examAtEachIndex)      

    (examschedule_dictionary,totalNumberOfSlots) = GenerateExamTimeTable(examschedule)
    sortedCopyOfGivenCourseOrder = sorted(deepcopy(aCourseListOrder))
    #deepcopy(aCourseListOrder)
    #for key_eachExam in sortedCopyOfGivenCourseOrder:
    #    print examschedule_dictionary[key_eachExam],key_eachExam
        
    #print totalNumberOfSlots
    
    penalty = totalPenaltyCalculate(examschedule_dictionary,studentDictionary)
    #print penalty
    Key_examschedule_dictionary_AsList=[]
    for key_eachExam in sortedCopyOfGivenCourseOrder:
        #print examschedule_dictionary[key_eachExam],key_eachExam
        (day,dayslot,actualSlot)= examschedule_dictionary[key_eachExam]
        Key_examschedule_dictionary_AsList.append((key_eachExam,day,dayslot,actualSlot))
    
    #print Key_examschedule_dictionary_AsList
    Key_examschedule_dictionary_AsImmutableTuple = tuple(Key_examschedule_dictionary_AsList)
    #print Key_examschedule_dictionary_AsImmutableTuple
    return examschedule_dictionary,totalNumberOfSlots,penalty,Key_examschedule_dictionary_AsImmutableTuple


####################Total Penalty Calculate##########################
def totalPenaltyCalculate(examDictionary,student_dictionary):

    consecutivePenalty = 0
    for aStudent in student_dictionary:   
        for c1 in student_dictionary[aStudent].listOfCourses:
            for c2 in student_dictionary[aStudent].listOfCourses.difference(set([c1])):
                if c1.name in examDictionary and c2.name in examDictionary :
                    if(c1.name == c2.name):
                        print "Both exams are same? Impossible"
                    
                    (d1,t1,actualUniqueSlot1) = examDictionary[c1.name]
                    (d2,t2,actualUniqueSlot2) = examDictionary[c2.name]
                    dayDiff = -abs(d1 - d2)
                    if(dayDiff==0):
                        timeDiff = -abs(t1-t2)
                        ###print "DayDiff is zero"
                        penalty_1 = 10 * pow(2,timeDiff)
                        consecutivePenalty += penalty_1  
    
    overnightPenalty = 0       
    for aStudent in student_dictionary:           
        for c1 in student_dictionary[aStudent].listOfCourses:
            for c2 in student_dictionary[aStudent].listOfCourses.difference(set([c1])):
                ###print str(c1.name)+"Maps to"+str(c2.name)
                if c1.name in examDictionary and c2.name in examDictionary:
                    (d1,t1,actualUniqueSlot1) = examDictionary[c1.name]
                    (d2,t2,actualUniqueSlot2) = examDictionary[c2.name]
                    dayDiff = -abs(d1 - d2)
                    if(dayDiff!=0):
                        penalty_2 = pow(2,dayDiff)
                        overnightPenalty += penalty_2
    totalPenalty = consecutivePenalty + overnightPenalty
    return totalPenalty    
    
    #return 0

################generate initial solutions for Objective Function 1 ##########################
def GenerateInitialSolution_OBJ1(aCourseListOrder, courseDictionary,studentDictionary):
    examschedule = []
    examAtEachIndex = set([])
    copyOfGivenCourseOrder = deepcopy(aCourseListOrder)
    key_tempExam = copyOfGivenCourseOrder.pop(0)
    tempExam = courseDictionary[key_tempExam]
    examAtEachIndex.add(tempExam)
    while(len(copyOfGivenCourseOrder)!= 0):
        conflictTotalList = set([])
        totalStudentsInSchedule = 0
        for exam in examAtEachIndex:
            conflictTotalList = conflictTotalList | exam.listOfConflictingCourses
            totalStudentsInSchedule += exam.numberOfStudents
            
            
        index_list = []
        examDictionarySameSlot = {}
        examDictionaryNextSlot = {}
        for i in range(0,len(copyOfGivenCourseOrder)):
            key_tempCopyExam = copyOfGivenCourseOrder[i]
            tempCopyExam = courseDictionary[key_tempCopyExam]
            if tempCopyExam.name not in conflictTotalList:
                if(totalStudentsInSchedule + tempCopyExam.numberOfStudents) <= roomSize:
                    copy_A_ofExamAtEachIndex = deepcopy(examAtEachIndex)
                    copy_A_ofExamAtEachIndex.add(tempCopyExam)
                    copy_A_ofexamschedule = deepcopy(examschedule)
                    copy_A_ofexamschedule.append(copy_A_ofExamAtEachIndex)
                    (examschedule_copy_A_dictionary,copy_A_totalNumberOfSlots) = GenerateExamTimeTable(copy_A_ofexamschedule)
                    copy_A_penalty = totalPenaltyCalculate(examschedule_copy_A_dictionary,studentDictionary)
                    examDictionarySameSlot[key_tempCopyExam] = copy_A_penalty
                    break;
                    #print "CopyA:",copy_A_penalty
        for i in range(0,len(copyOfGivenCourseOrder)):
            key_tempCopyExam = copyOfGivenCourseOrder[i]
            tempCopyExam = courseDictionary[key_tempCopyExam]
            copy_B_ofExamAtEachIndex = deepcopy(examAtEachIndex)
            copy_B_ofexamschedule = deepcopy(examschedule)
            copy_B_ofexamschedule.append(copy_B_ofExamAtEachIndex)
            copy_B_ofExamAtEachIndex = set([])
            copy_B_ofExamAtEachIndex.add(tempCopyExam)
            copy_B_ofexamschedule.append(copy_B_ofExamAtEachIndex)
            (examschedule_copy_B_dictionary,copy_B_totalNumberOfSlots) = GenerateExamTimeTable(copy_B_ofexamschedule)
            copy_B_penalty = totalPenaltyCalculate(examschedule_copy_B_dictionary,studentDictionary)
            examDictionaryNextSlot[key_tempCopyExam] = copy_B_penalty
            #print "CopyB:",copy_B_penalty
            break
        
        #print "Out of the loop"
        
        if bool(examDictionarySameSlot) != False :
            min_PenaltyValueSameSlot = min(examDictionarySameSlot.itervalues())
            min_PenaltyValueKeySameSlot = [k for k in examDictionarySameSlot if examDictionarySameSlot[k] == min_PenaltyValueSameSlot]
            min_PenaltyValuedifferentSlot = min(examDictionaryNextSlot.itervalues())
            min_PenaltyValueKeydifferentSlot = [k for k in examDictionaryNextSlot if examDictionaryNextSlot[k] == min_PenaltyValuedifferentSlot]
            
            if(min_PenaltyValueSameSlot< min_PenaltyValuedifferentSlot):
                key_selected = random.choice(min_PenaltyValueKeySameSlot)
                tempExamSelected = courseDictionary[key_selected]
                examAtEachIndex.add(tempExamSelected)
                toRemove = None
                for courseName_asCounter in copyOfGivenCourseOrder:
                    if courseName_asCounter == key_selected:
                        toRemove = courseName_asCounter
                
                copyOfGivenCourseOrder.remove(toRemove)
                
            #elif(min_PenaltyValueSameSlot>min_PenaltyValuedifferentSlot):
            else:
                examschedule.append(examAtEachIndex)
                examAtEachIndex = set([])
                key_selected = random.choice(min_PenaltyValueKeydifferentSlot)
                tempExamSelected = courseDictionary[key_selected]
                examAtEachIndex.add(tempExamSelected)
                toRemove = None
                for courseName_asCounter in copyOfGivenCourseOrder:
                    if courseName_asCounter == key_selected:
                        toRemove = courseName_asCounter
                copyOfGivenCourseOrder.remove(toRemove)
        else:
            min_PenaltyValuedifferentSlot = min(examDictionaryNextSlot.itervalues())
            min_PenaltyValueKeydifferentSlot = [k for k in examDictionaryNextSlot if examDictionaryNextSlot[k] == min_PenaltyValuedifferentSlot]
            examschedule.append(examAtEachIndex)
            examAtEachIndex = set([])
            key_selected = random.choice(min_PenaltyValueKeydifferentSlot)
            tempExamSelected = courseDictionary[key_selected]
            examAtEachIndex.add(tempExamSelected)
            toRemove = None
            for courseName_asCounter in copyOfGivenCourseOrder:
                if courseName_asCounter == key_selected:
                    toRemove = courseName_asCounter
                    #print toRemove
            copyOfGivenCourseOrder.remove(toRemove)
            
        if(len(copyOfGivenCourseOrder)==0):
            examschedule.append(examAtEachIndex)
            
    #print "Hello"
    (examschedule_dictionary,totalNumberOfSlots) = GenerateExamTimeTable(examschedule)
    sortedCopyOfGivenCourseOrder = sorted(deepcopy(aCourseListOrder))
    #deepcopy(aCourseListOrder)
    #for key_eachExam in sortedCopyOfGivenCourseOrder:
    #    print examschedule_dictionary[key_eachExam],key_eachExam
        
    #print totalNumberOfSlots
    
    penalty = totalPenaltyCalculate(examschedule_dictionary,studentDictionary)
    #print penalty
    Key_examschedule_dictionary_AsList=[]
    for key_eachExam in sortedCopyOfGivenCourseOrder:
        #print examschedule_dictionary[key_eachExam],key_eachExam
        (day,dayslot,actualSlot)= examschedule_dictionary[key_eachExam]
        Key_examschedule_dictionary_AsList.append((key_eachExam,day,dayslot,actualSlot))
    
    #print Key_examschedule_dictionary_AsList
    Key_examschedule_dictionary_AsImmutableTuple = tuple(Key_examschedule_dictionary_AsList)
    #print Key_examschedule_dictionary_AsImmutableTuple
    return examschedule_dictionary,totalNumberOfSlots,penalty,Key_examschedule_dictionary_AsImmutableTuple
                

######### checking constraint violation for schedule ######################

def constraintViolation(schedule,totalSlot,studentDictionary,courseDictionary,roomSize):
    
    #parents themselves do not violate max total slots - so children wont either
    listOfSlots = range(1,totalSlot+1)
    print "constraint violation test"
    print listOfSlots
    
    slotDictionary = dict()
    for aSlot in listOfSlots:
        slotDictionary[aSlot] = set()
        
    for key in schedule:
        (temp_day,temp_day_Slot,temp_uniqueSlot) = schedule[key]
        #print (key,temp_day,temp_day_Slot,temp_uniqueSlot)
        slotDictionary[temp_uniqueSlot].add(key)
        
    for aSlot in listOfSlots:
        print aSlot,slotDictionary[aSlot] 
        if slotDictionary[aSlot] :
            print "full"
        else:
            print "Found a empty slot"
            print "violates hard constraint"
            return 0
        
    print "Does not violate hard constraint of empty slot"
    
    for key in schedule:
        (temp_day,temp_day_Slot,temp_uniqueSlot) = schedule[key]
        temp_examInSameSlot = deepcopy(slotDictionary[temp_uniqueSlot])
        temp_examInSameSlot.remove(key)
        #print "TEST"
        #print key,courseDictionary[key].name,courseDictionary[key].listOfConflictingCourses
        #print temp_examInSameSlot
        if  temp_examInSameSlot:
            #Check if these two sets have any common elements. if they do then conflict present. 
            conflicting_Courses = temp_examInSameSlot.intersection(courseDictionary[key].listOfConflictingCourses)
            if conflicting_Courses:
                print "Conflicting course found"
                return 0

    print "No Conflicting courses found"
    
    for oneSlot in slotDictionary:
        totalStudents = 0
        print "Each Slot test"
        for eachElement in slotDictionary[oneSlot]:
            #print oneSlot,courseDictionary[eachElement].name,courseDictionary[eachElement].numberOfStudents
            totalStudents += courseDictionary[eachElement].numberOfStudents
    
        print "totalStudents:",totalStudents
        if(totalStudents>roomSize):
            print "Room capacity problem in slot",oneSlot
            return 0    
            
    print "No room capacity exceed"
    return 1


#####Mutation Operator:trying to fix schedule################
def mutation_conflictingCourseResolve(originalSchedule,totalSlot,studentDictionary,courseDictionary,roomSize):
    
    schedule = deepcopy(originalSchedule)
    listOfSlots = range(1,totalSlot+1)
    slotDictionary_Course = dict()
    slotDictionary_Course_andConflictingCourse = dict()
    for aSlot in listOfSlots:
        slotDictionary_Course[aSlot] = set()
        slotDictionary_Course_andConflictingCourse[aSlot] = set()
        
    for key in schedule:
        print key, schedule[key]
        (temp_day,temp_day_Slot,temp_uniqueSlot) = schedule[key]
        slotDictionary_Course[temp_uniqueSlot].add(key)
        #slotDictionary_Course_andConflictingCourse[temp_uniqueSlot]
        slotDictionary_Course_andConflictingCourse[temp_uniqueSlot].update(courseDictionary[key].listOfConflictingCourses)
        #print temp_uniqueSlot,slotDictionary_Course_andConflictingCourse[temp_uniqueSlot]
        
    emptySlots = set()    
    for aSlot in listOfSlots:
        print aSlot,slotDictionary_Course[aSlot],slotDictionary_Course_andConflictingCourse[aSlot]
        if not slotDictionary_Course[aSlot] :
            emptySlots.add(aSlot)
            print "EmptyList"


    conflictFoundFlag = False
    for key in schedule:
        (temp_day,temp_day_Slot,temp_uniqueSlot) = schedule[key]
        temp_examInSameSlot = deepcopy(slotDictionary_Course[temp_uniqueSlot])
        temp_examInSameSlot.remove(key)
        print "mutation_conflictingCourseResolve_TEST"
        print key,courseDictionary[key].name,courseDictionary[key].listOfConflictingCourses
        print temp_examInSameSlot
        if  temp_examInSameSlot:
            #Check if these two sets have any common elements. if they do then conflict present. 
            conflictFoundFlag = True
            conflicting_Courses = temp_examInSameSlot.intersection(courseDictionary[key].listOfConflictingCourses)
            if conflicting_Courses:
                print key,"Conflicting course found"
                schedule_tempCopy = deepcopy(schedule)
                if emptySlots:
                    temporary_UniqueSlot = emptySlots.pop()
                    #random.choice(emptySlots)
                    #emptySlots.remove(temporary_UniqueSlot)
                    temp_Uniq_day = ((temporary_UniqueSlot-1) // 5) + 1
                    temp_Uniq_day_slot = temporary_UniqueSlot - (temp_Uniq_day-1)*5
                    schedule[key] = (temp_Uniq_day,temp_Uniq_day_slot,temporary_UniqueSlot)
                    
                    
                    slotDictionary_Course[temporary_UniqueSlot].add(key)
                    slotDictionary_Course_andConflictingCourse[temporary_UniqueSlot].update(courseDictionary[key].listOfConflictingCourses)
                    
                    slotDictionary_Course[temp_uniqueSlot].discard(key)
                    
                    for oneKey in slotDictionary_Course[temp_uniqueSlot]:
                        slotDictionary_Course_andConflictingCourse[temp_uniqueSlot].update(courseDictionary[oneKey].listOfConflictingCourses)
                        
                else:
                    tempListOfSlots = deepcopy(listOfSlots)
                    tempListOfSlots.remove(temp_uniqueSlot)
                    print tempListOfSlots
                    foundFlag = False
                    for otherslot in tempListOfSlots:
                        totalStudentInSlot = 0
                        for eachExam in slotDictionary_Course[otherslot]:
                            totalStudentInSlot = courseDictionary[eachExam].numberOfStudents

                        print "total Student in other",otherslot, "slot:",totalStudentInSlot
                        print "current student in exam",key,"is",courseDictionary[key].numberOfStudents
                        tempTotalStudentInCurrentSlot_After_Adding = totalStudentInSlot + courseDictionary[key].numberOfStudents
                        if key not in slotDictionary_Course_andConflictingCourse[otherslot] and tempTotalStudentInCurrentSlot_After_Adding <= roomSize:
                            
                            print slotDictionary_Course_andConflictingCourse[otherslot]
                            print "Putting in existing slot" ,otherslot
                            temp_Uniq_day = ((otherslot-1) // 5) + 1
                            temp_Uniq_day_slot = otherslot - (temp_Uniq_day-1)*5
                            schedule[key] = (temp_Uniq_day,temp_Uniq_day_slot,otherslot)
                            foundFlag = True
                            
                            slotDictionary_Course[otherslot].add(key)
                            slotDictionary_Course_andConflictingCourse[otherslot].update(courseDictionary[key].listOfConflictingCourses)
                            
                            slotDictionary_Course[temp_uniqueSlot].discard(key)
                            
                            for oneKey in slotDictionary_Course[temp_uniqueSlot]:
                                slotDictionary_Course_andConflictingCourse[temp_uniqueSlot].update(courseDictionary[oneKey].listOfConflictingCourses)

                            
                            break
                    
                    if foundFlag is False:
                        temporary_UniqueSlot = totalSlot+1
                        print "Putting in new slot" ,temporary_UniqueSlot
                        temp_Uniq_day = ((temporary_UniqueSlot-1) // 5) + 1
                        temp_Uniq_day_slot = temporary_UniqueSlot - (temp_Uniq_day-1)*5
                        schedule[key] = (temp_Uniq_day,temp_Uniq_day_slot,temporary_UniqueSlot)
                        
                        slotDictionary_Course[temporary_UniqueSlot] = set()
                        slotDictionary_Course_andConflictingCourse[temporary_UniqueSlot] = set()
                        slotDictionary_Course[temporary_UniqueSlot].add(key)
                        slotDictionary_Course_andConflictingCourse[temporary_UniqueSlot].update(courseDictionary[key].listOfConflictingCourses)
                        
                        slotDictionary_Course[temp_uniqueSlot].discard(key)
                        for oneKey in slotDictionary_Course[temp_uniqueSlot]:
                            slotDictionary_Course_andConflictingCourse[temp_uniqueSlot].update(courseDictionary[oneKey].listOfConflictingCourses)
                        
                        totalSlot = totalSlot+1
                        listOfSlots = range(1,totalSlot+1)
                        
                        
    for key in schedule:
        print key, schedule[key]
        
        
    for key in schedule:
        totalStudents = 0
        oneSlot = schedule[key][2]
        print oneSlot
        print "Each Slot test in size conflict resolve 1"
        for eachElement in slotDictionary_Course[oneSlot]:
            print oneSlot,courseDictionary[eachElement].name,courseDictionary[eachElement].numberOfStudents
            totalStudents += courseDictionary[eachElement].numberOfStudents
    
        print "totalStudents:",totalStudents
        if(totalStudents>roomSize):
            print "Room capacity problem in",oneSlot
            tempListOfSlots = deepcopy(listOfSlots)
            tempListOfSlots.remove(oneSlot)
            print tempListOfSlots
            foundFlag = False
            for otherslot in tempListOfSlots:
                totalStudentInSlot = 0
                for eachExam in slotDictionary_Course[otherslot]:
                    totalStudentInSlot += courseDictionary[eachExam].numberOfStudents

                print "total Student in other",otherslot, "slot:",totalStudentInSlot
                print "current student in exam",key,"is",courseDictionary[key].numberOfStudents
                tempTotalStudentInCurrentSlot_After_Adding = totalStudentInSlot + courseDictionary[key].numberOfStudents
                if key not in slotDictionary_Course_andConflictingCourse[otherslot] and tempTotalStudentInCurrentSlot_After_Adding <= roomSize:
                            
                    print slotDictionary_Course_andConflictingCourse[otherslot]
                    print "Putting in existing slot" ,otherslot
                    temp_Uniq_day = ((otherslot-1) // 5) + 1
                    temp_Uniq_day_slot = otherslot - (temp_Uniq_day-1)*5
                    schedule[key] = (temp_Uniq_day,temp_Uniq_day_slot,otherslot)
                    foundFlag = True
                    slotDictionary_Course[otherslot].add(key)
                    slotDictionary_Course_andConflictingCourse[otherslot].update(courseDictionary[key].listOfConflictingCourses)
                            
                    slotDictionary_Course[oneSlot].discard(key)
                    for oneKey in slotDictionary_Course[oneSlot]:
                        slotDictionary_Course_andConflictingCourse[oneSlot].update(courseDictionary[oneKey].listOfConflictingCourses)
                    break
                
                
                    
            if foundFlag is False:
                temporary_UniqueSlot = totalSlot+1
                print "Putting in new slot" ,temporary_UniqueSlot
                temp_Uniq_day = ((temporary_UniqueSlot-1) // 5) + 1
                temp_Uniq_day_slot = temporary_UniqueSlot - (temp_Uniq_day-1)*5
                schedule[key] = (temp_Uniq_day,temp_Uniq_day_slot,temporary_UniqueSlot)
                        
                slotDictionary_Course[temporary_UniqueSlot] = set()
                slotDictionary_Course_andConflictingCourse[temporary_UniqueSlot] = set()
                slotDictionary_Course[temporary_UniqueSlot].add(key)
                slotDictionary_Course_andConflictingCourse[temporary_UniqueSlot].update(courseDictionary[key].listOfConflictingCourses)
                        
                slotDictionary_Course[oneSlot].discard(key)
                for oneKey in slotDictionary_Course[oneSlot]:
                    slotDictionary_Course_andConflictingCourse[oneSlot].update(courseDictionary[oneKey].listOfConflictingCourses)
                        
                totalSlot = totalSlot+1
                listOfSlots = range(1,totalSlot+1)
                
        
    #Empty slot removal
        
    while(True):        
        emptySlots = set()    
        for aSlot in listOfSlots:
            #print aSlot,slotDictionary_Course[aSlot],slotDictionary_Course_andConflictingCourse[aSlot]
            if not slotDictionary_Course[aSlot] :
                print "Found a empty slot:"
                print aSlot,slotDictionary_Course[aSlot],slotDictionary_Course_andConflictingCourse[aSlot]
                emptySlots.add(aSlot)
                
        if emptySlots:
            print "Empty slot found after fixing for total students and conflicting courses"
            print "Putting everything of last slot to first empty slot"
            print emptySlots
            firstIndexInEmptySlots = emptySlots.pop()
            print firstIndexInEmptySlots
            print totalSlot
            for aExam in slotDictionary_Course[totalSlot]:
                print aExam
                temp_Uniq_day_emptySlot = ((firstIndexInEmptySlots-1) // 5) + 1
                temp_Uniq_day_slot_emptySlot = firstIndexInEmptySlots - (temp_Uniq_day_emptySlot-1)*5
                schedule[aExam] = (temp_Uniq_day_emptySlot,temp_Uniq_day_slot_emptySlot,firstIndexInEmptySlots)
                slotDictionary_Course[firstIndexInEmptySlots].add(aExam)
                slotDictionary_Course_andConflictingCourse[firstIndexInEmptySlots].update(courseDictionary[aExam].listOfConflictingCourses)
                
            del slotDictionary_Course[totalSlot]
            del slotDictionary_Course_andConflictingCourse[totalSlot]
            totalSlot = totalSlot - 1
            listOfSlots = range(1,totalSlot+1)
        else:
            print "removed all empty slots"
            break
        
    
    print "Should not have conflicts anymore"
    
    

        
    if constraintViolation(schedule,totalSlot,studentDictionary,courseDictionary,roomSize)!= 1:
        print "Recursion"
        #return mutation_conflictingCourseResolve(schedule,totalSlot,studentDictionary,courseDictionary,roomSize)
        #return originalSchedule
        #raise NameError('Exception raised')
        return originalSchedule
    else:
        print "resolved"
        return schedule


################Recombination operator######################
#First we apply recombination. If hard constraints violate, 
#we fix the child by applying a mutation that creates a feasible solution from hard constraint violating child
#If hard constraint is not violated in the child, then mutation is applied by only swapping two slots.
#If hard constraint is violated, then all the possible cases : conflicting courses, empty slots and room size violation is checked.
#First checking for conflicting courses are done. If there are conflicting courses in the same slot that has the same student, one of
#The conflicting courses is taken and if a empty slot is present - then put into there. If not, then put into another slot where other constraints can not
#be violated. This removes conflicting courses in the schedule - but still room size violation can occur, and some empty slots may be present. 
#At this point we check for possible room size violation for each exam. If a room size violation for a exam occurs in any slot - then that exam is moved 
#from that slot, and put into another slot where no course conflict or size limit exceed can occur.
#Running this for all exams fixes the size constraint. Now for the empty slot - the best way to keep most of the parent traits is to put the last
#slot contains into the first empty slot , and reduce the max slot size for that schedule. Keep doing it till all empty slots are filled.

def recombination_AndMutation(parent1schedule,parent1TotalSlot,parent2schedule,parent2TotalSlot,sortedCourseList_ByName,studentDictionary,courseDictionary,roomSize):
    print "Recombination"
    print "parent1:",parent1schedule
    print "parent2:",parent2schedule
    child1Schedule = dict()
    child2Schedule = dict()
    nonMatchingList = list()  
    parent1SlotDictionary=dict()
    parent2SlotDictionary=dict() 

    for aExam in sortedCourseList_ByName:
        parent1SlotDictionary[parent1schedule[aExam][2]] = set()
        parent2SlotDictionary[parent2schedule[aExam][2]] = set()

         
    #Implementing Respect, both child always inherits commonality of both parents
    for aExam in sortedCourseList_ByName:
        print aExam,parent1schedule[aExam][2],parent2schedule[aExam][2]
        if parent1schedule[aExam][2] == parent2schedule[aExam][2]:
            child1Schedule[aExam] = parent1schedule[aExam]
            child2Schedule[aExam] = parent1schedule[aExam]
            print child1Schedule[aExam],child2Schedule[aExam]
        else:
            nonMatchingList.append(aExam)
            
        parent1SlotDictionary[parent1schedule[aExam][2]].add(aExam)
        parent2SlotDictionary[parent2schedule[aExam][2]].add(aExam)
        
        #print parent1SlotDictionary[parent1schedule[aExam][2]]
        #print parent2SlotDictionary[parent2schedule[aExam][2]]
    
    print "Parent1 slot:"
    for index1 in range(1,parent1TotalSlot+1):
        print parent1SlotDictionary[index1]
    
    print "Parent2 slot:"
    for index2 in range(1,parent2TotalSlot+1):
        print parent2SlotDictionary[index2]

    
    print "nonMatchingList size:",len(nonMatchingList),nonMatchingList
    
    #Doing the Transmission, all components of offspring are coming from parents
    for aNonMatchingExam in nonMatchingList:
        randValue = random.uniform(0,1)
        if randValue <0.5:
            child1Schedule[aNonMatchingExam] = parent1schedule[aNonMatchingExam]
            child2Schedule[aNonMatchingExam] = parent2schedule[aNonMatchingExam]
        else:
            child1Schedule[aNonMatchingExam] = parent2schedule[aNonMatchingExam]
            child2Schedule[aNonMatchingExam] = parent1schedule[aNonMatchingExam]
                
    child1MaxSlot = 0
    child2MaxSlot = 0

    print "Determine slot"
    for aExam in sortedCourseList_ByName:
        print aExam,child1Schedule[aExam],child2Schedule[aExam]
        (day1, daySlot1, totalSlot1) = child1Schedule[aExam]
        (day2, daySlot2, totalSlot2) = child2Schedule[aExam]
        if(totalSlot1>child1MaxSlot):
            child1MaxSlot = totalSlot1
        if(totalSlot2>child2MaxSlot):
            child2MaxSlot = totalSlot2
    print "Recombination done. Chances are hard constraints will be violated. Fix child through mutation"
    print child1MaxSlot,child2MaxSlot
    


    
    child1HardConstraintVal = constraintViolation(child1Schedule,child1MaxSlot,studentDictionary,courseDictionary,roomSize)
    child2HardConstraintVal = constraintViolation(child2Schedule,child2MaxSlot,studentDictionary,courseDictionary,roomSize)
    mutatedChild1 = None
    mutatedChild2 = None
    
    print child1HardConstraintVal#,child2HardConstraintVal
    if child1HardConstraintVal == 0:
        print "Mutation Conflict resolve for child 1"
        mutatedChild1 = mutation_conflictingCourseResolve(child1Schedule,child1MaxSlot,studentDictionary,courseDictionary,roomSize)
    else:
        print "Mutation by slot swapping, wont produce conflict"
        mutatedChild1 = mutationBySlotSwap(child1Schedule,child1MaxSlot,studentDictionary,courseDictionary,roomSize)
        
    if child2HardConstraintVal == 0:
        print "Mutation Conflict resolve for child 2"
        mutatedChild2 = mutation_conflictingCourseResolve(child2Schedule,child2MaxSlot,studentDictionary,courseDictionary,roomSize)
    else:
        print "Mutation by slot swapping, wont produce conflict"
        mutatedChild2 = mutationBySlotSwap(child2Schedule,child2MaxSlot,studentDictionary,courseDictionary,roomSize)

    return mutatedChild1,mutatedChild2

#########Mutation by swapping exam slots####################
def mutationBySlotSwap(originalSchedule,totalSlot,studentDictionary,courseDictionary,roomSize):
    mutatedSchedule = deepcopy(originalSchedule)
    listOfSlots = range(1,totalSlot+1)
    slotDictionary_Course = dict()
    
    for aSlot in listOfSlots:
        slotDictionary_Course[aSlot] = set()
        
    for key in mutatedSchedule:
        print key, mutatedSchedule[key]
        (temp_day,temp_day_Slot,temp_uniqueSlot) = mutatedSchedule[key]
        slotDictionary_Course[temp_uniqueSlot].add(key)
        
    pickFromlistOfSlots = deepcopy(listOfSlots)
    slot1ForSwapping = random.choice(pickFromlistOfSlots)
    pickFromlistOfSlots.remove(slot1ForSwapping)
    slot2ForSwapping = random.choice(pickFromlistOfSlots)
    pickFromlistOfSlots.remove(slot2ForSwapping)

    print slot1ForSwapping,slot2ForSwapping
    
    temp = deepcopy(slotDictionary_Course[slot1ForSwapping])
    slotDictionary_Course[slot1ForSwapping] = deepcopy(slotDictionary_Course[slot2ForSwapping])
    slotDictionary_Course[slot2ForSwapping] = deepcopy(temp)
    
    #for key in 
    
    for aSlot in listOfSlots:
        for oneExam in slotDictionary_Course[aSlot]:
            temp_Uniq_day = ((aSlot-1) // 5) + 1
            temp_Uniq_day_slot = aSlot - (temp_Uniq_day-1)*5
            mutatedSchedule[oneExam] = (temp_Uniq_day,temp_Uniq_day_slot,aSlot)
            
    for key in mutatedSchedule:
        print key, mutatedSchedule[key]
        
    return mutatedSchedule
            
        


######### Main function #######################
arg1 = sys.argv[1]
arg2 = sys.argv[2]
arg3 = sys.argv[3]
arg4 = sys.argv[4]
courseFile = open(arg1,"r")
studentFile = open(arg2,"r")

#Read courses from .crs file
lineCounter = 0
roomSize = 0
maxSlot = 0
courseDictionary = {}
while 1:
    try:
        line = courseFile.next()
    except StopIteration:
        break
    else:
        #print line
        strings = line.split()
        #print strings
        if lineCounter==0:
            roomSize = int(strings[0])
            maxSlot = int(strings[1])
            print "given roomsize:",roomSize
            print "given maxslot:",maxSlot
        else:
            ###print strings
            #Have a object of course type and insert sizeOfStudents
            newCourse = Course(strings[0],int(strings[1]))
            #courseDictionary.append(newCourse)
            courseDictionary[strings[0]] = newCourse           
        lineCounter += 1

courseFile.close()

for courseAsKey in courseDictionary:
    print "%s %s" %(courseDictionary[courseAsKey].name,courseDictionary[courseAsKey].numberOfStudents)
    
#Read Students from .stu file
studentDictionary = {}
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

        for studentCourseName in studentCourses:
            #print (studentCounter,studentCourseName)
            tempCourse = courseDictionary[studentCourseName]
            #print "%s %s" %(tempCourse.name,tempCourse.numberOfStudents)
            newStudent._addCourses_(tempCourse)

        studentDictionary[studentCounter] = newStudent
        studentCounter+=1;           

#Close all the file object
studentFile.close()


#Testing if list of students and list of conflicting courses have been built
#Correctly or not
courseList = []
for courseAsKey in courseDictionary:
    #print "%s %s" %(courseDictionary[courseAsKey].name,courseDictionary[courseAsKey].numberOfStudents)
    #print courseDictionary[courseAsKey].listOfStudents
    #print courseDictionary[courseAsKey].listOfConflictingCourses
    courseList.append(courseDictionary[courseAsKey])

sortedCourseList = sorted(courseList, key = lambda course : (course.numberOfStudents ,  -len(course.listOfConflictingCourses)), reverse = True)

courseNameList = []
for courseAsKey in courseDictionary:
    courseNameList.append(courseAsKey)
sortedCourseList_ByName = sorted(courseNameList)


masterCourseList = []
listOfCourseList = []
for aCourse in sortedCourseList:
    masterCourseList.append(aCourse.name)
    #print (aCourse.name,aCourse.numberOfStudents,len(aCourse.listOfConflictingCourses))
#for aCourseKey in masterCourseList:
#    print aCourseKey, courseDictionary[aCourseKey].name, courseDictionary[aCourseKey].listOfStudents
#print masterCourseList
listOfCourseList.append(masterCourseList)
for i in range(1,100):
    tempOrderingOfCourse = deepcopy(masterCourseList)
    random.shuffle(tempOrderingOfCourse)
    listOfCourseList.append(tempOrderingOfCourse)
    
solutionSpace = dict()        
print arg4

if int(arg4)==0:    #Objective Function 0
    print "OBJ Function 1"
    allOutputFileName = "allOutput_1"+arg3
    listCounter = 0
    minTotalSlot = 0
    minTotalPenalty =0
    for aCourseList in listOfCourseList:
        #print aCourseList
        (schedule,totalSlot,penalty,Key)=GenerateInitialSolution_OBJ0(aCourseList,courseDictionary,studentDictionary)
        hardConstraintVal =  constraintViolation(schedule,totalSlot,studentDictionary,courseDictionary,roomSize)
        
        #calculating fitness function value
        fitnessFunctionValue = (hardConstraintVal * ((totalSlot *10000) + penalty))
        
        if(totalSlot<=maxSlot):
            #every solution has a unique key which is it's own schedule
            solutionSpace[Key]=(schedule,totalSlot,penalty,fitnessFunctionValue)
            print listCounter,totalSlot,penalty,Key
            if(listCounter==0):
                minTotalSlot = totalSlot
                minTotalPenalty = penalty
                outputFile = open(arg3,"wb+")
                outputFile.write(str(totalSlot)+"    "+str(penalty)+"\n")
                
                
                allOutputFile = open(allOutputFileName,"wb+")
                allOutputFile.write(str(fitnessFunctionValue)+"\n")
                for examKey in sortedCourseList_ByName:
                    (tempDate,tempDateSlot,tempActualSlot)= schedule[examKey]
                    outputFile.write(examKey+"    "+str(tempDate)+"    "+str(tempDateSlot)+"\n")
                    allOutputFile.write(examKey+"    "+str(tempActualSlot)+"\n")
                outputFile.close()
                allOutputFile.close()
            else:
                if(totalSlot<=minTotalSlot and penalty<minTotalPenalty):
                    minTotalSlot = totalSlot
                    minTotalPenalty = penalty
                    outputFile = open(arg3,"wb+")
                    outputFile.write(str(totalSlot)+"    "+str(penalty)+"\n")
                    for examKey in sortedCourseList_ByName:
                        (tempDate,tempDateSlot,tempActualSlot)= schedule[examKey]
                        outputFile.write(examKey+"    "+str(tempDate)+"    "+str(tempDateSlot)+"\n")
                    outputFile.close()
                
                allOutputFile = open(allOutputFileName,"a+")
                allOutputFile.write("\n\n")
                allOutputFile.write(str(fitnessFunctionValue)+"\n")
                for examKey in sortedCourseList_ByName:
                    (tempDate,tempDateSlot,tempActualSlot)= schedule[examKey]
                    allOutputFile.write(examKey+"    "+str(tempActualSlot)+"\n")
                allOutputFile.close()
                
            listCounter+=1
            
            
            
    for iterationLoop in range(1,100):   
             
        keyList = list()        
        for key_schedule in solutionSpace:
            keyList.append(key_schedule)
            
            
            (tempSchedule,tempNumberOfSlot,tempValOfPenalty,temp_fitnessFuncValue) = solutionSpace[key_schedule]
            print "HI:",tempNumberOfSlot,key_schedule

        print "Try Random Shuffle for tournament selection"
        print "Randomly select 2 chromosomes as parents, create two childlren, calculate fitness function for all and place the best two from 4 (2 parents and 2 children)."
        random.shuffle(keyList)

            #print tempNumberOfSlot,tempValOfPenalty
        #raise NameError('Exception raised1')            
            
    # a while loop    while
    
        index = 0
        while(index < len(keyList)):
        
            if(index+1==len(keyList)):
                break
        
            parentKey1 = index
            parentKey2 = index+1
            print len(keyList),parentKey2
            print keyList[parentKey1]
            print keyList[parentKey2]

            (tempSchedule1,tempNumberOfTotalSlot1,tempValOfPenalty1,temp_fitnessFuncValue1) = deepcopy(solutionSpace[keyList[parentKey1]])
            (tempSchedule2,tempNumberOfTotalSlot2,tempValOfPenalty2,temp_fitnessFuncValue2) = deepcopy(solutionSpace[keyList[parentKey2]])
            print tempSchedule2,tempNumberOfTotalSlot2
            
            (mutatedChild1_temp,mutatedChild2_temp) = recombination_AndMutation(tempSchedule1,tempNumberOfTotalSlot1,tempSchedule2,tempNumberOfTotalSlot2,sortedCourseList_ByName,studentDictionary,courseDictionary,roomSize)
            
            (mutatedChild1_schedule,totalSlot_M1,penalty_M1,Key_M1) = GenerateSolutionResultFromGivenSolution(mutatedChild1_temp,courseDictionary,studentDictionary)
            (mutatedChild2_schedule,totalSlot_M2,penalty_M2,Key_M2) = GenerateSolutionResultFromGivenSolution(mutatedChild2_temp,courseDictionary,studentDictionary)
            
            hardConstraintVal_mutatedChild1 =  constraintViolation(mutatedChild1_schedule,totalSlot_M1,studentDictionary,courseDictionary,roomSize)
            hardConstraintVal_mutatedChild2 =  constraintViolation(mutatedChild2_schedule,totalSlot_M2,studentDictionary,courseDictionary,roomSize)
            
            fitnessFunctionValue_M1 = (hardConstraintVal_mutatedChild1 * (totalSlot_M1 * 10000 + penalty_M1))
            fitnessFunctionValue_M2 = (hardConstraintVal_mutatedChild2 * (totalSlot_M2 * 10000 + penalty_M2))
            
            listToSelectFrom = list()
            listToSelectFrom.append((1,temp_fitnessFuncValue1))
            listToSelectFrom.append((2,temp_fitnessFuncValue2))
            listToSelectFrom.append((3,fitnessFunctionValue_M1))
            listToSelectFrom.append((4,fitnessFunctionValue_M2))
            
            listToSelectFrom.sort(key=lambda tup: tup[1])
            print listToSelectFrom
            selectedFromGeneration = list()
            selectedFromGeneration.append(listToSelectFrom.pop(0)[0])
            selectedFromGeneration.append(listToSelectFrom.pop(0)[0])
            
            del solutionSpace[keyList[parentKey1]]
            del solutionSpace[keyList[parentKey2]]
            for selectedElement in selectedFromGeneration:
                if selectedElement == 1:
                    #first parent selected
                    solutionSpace[keyList[parentKey1]] = (tempSchedule1,tempNumberOfTotalSlot1,tempValOfPenalty1,temp_fitnessFuncValue1)
                elif selectedElement == 2:
                    #second parent selected
                    solutionSpace[keyList[parentKey2]] = (tempSchedule2,tempNumberOfTotalSlot2,tempValOfPenalty2,temp_fitnessFuncValue2) 
                elif selectedElement == 3:
                    #first child selected
                    solutionSpace[Key_M1] = (mutatedChild1_schedule,totalSlot_M1,penalty_M1,fitnessFunctionValue_M1) 
                else:
                    #second child selected
                    solutionSpace[Key_M2] = (mutatedChild2_schedule,totalSlot_M2,penalty_M2,fitnessFunctionValue_M2) 
                
            index += 2
            
            
        temp_fitnessFuncValue = 0
        iterIndex = 0
        for key_schedule in solutionSpace:
            (print_Schedule,print_NumberOfSlot,print_ValOfPenalty,print_fitnessFuncValue) = solutionSpace[key_schedule]
            
            print "Fitness Function:",print_fitnessFuncValue
            if int(print_fitnessFuncValue):
                print "Hi"
            
            if(print_NumberOfSlot<=maxSlot):
                
                if iterIndex == 0:
                    temp_fitnessFuncValue = print_fitnessFuncValue
                    
                    outputFile = open(arg3,"wb+")
                    outputFile.write(str(print_NumberOfSlot)+"    "+str(print_ValOfPenalty)+"\n")
                    
                    allOutputFile = open(allOutputFileName,"a+")
                    allOutputFile.write("\n\n")
                    allOutputFile.write(str(print_fitnessFuncValue)+"\n")
                                   
                    for examKey in sortedCourseList_ByName:
                        (tempDate,tempDateSlot,tempActualSlot)= print_Schedule[examKey]
                        outputFile.write(examKey+"    "+str(tempDate)+"    "+str(tempDateSlot)+"\n")
                        allOutputFile.write(examKey+"    "+str(tempActualSlot)+"\n")
                    outputFile.close()
                    allOutputFile.close()
                    
                    
                else:
                    if print_fitnessFuncValue < temp_fitnessFuncValue:
                        temp_fitnessFuncValue = print_fitnessFuncValue
                    
                        outputFile = open(arg3,"wb+")
                        outputFile.write(str(print_NumberOfSlot)+"    "+str(print_ValOfPenalty)+"\n")
                        for examKey in sortedCourseList_ByName:
                            (tempDate,tempDateSlot,tempActualSlot)= print_Schedule[examKey]
                            outputFile.write(examKey+"    "+str(tempDate)+"    "+str(tempDateSlot)+"\n")
                        outputFile.close()
    
                    allOutputFile = open(allOutputFileName,"a+")
                    allOutputFile.write("\n\n")
                    allOutputFile.write(str(print_fitnessFuncValue)+"\n")
                    for examKey in sortedCourseList_ByName:
                        (tempDate,tempDateSlot,tempActualSlot)= print_Schedule[examKey]
                        allOutputFile.write(examKey+"    "+str(tempActualSlot)+"\n")
                    allOutputFile.close()
                    
                iterIndex += 1
    
else:
    print "OBJ Function 2"
    listCounter = 0
    minTotalSlot = 0
    minTotalPenalty =0
    
    allOutputFileName = "allOutput_2"+arg3


    
    for aCourseList in listOfCourseList:
        #print aCourseList
        (schedule,totalSlot,penalty,Key)=GenerateInitialSolution_OBJ1(aCourseList,courseDictionary,studentDictionary)
        hardConstraintVal =  constraintViolation(schedule,totalSlot,studentDictionary,courseDictionary,roomSize)
        
        #calculating fitness function value
        fitnessFunctionValue = hardConstraintVal * (penalty)

        
        if(totalSlot<=maxSlot):
            #every solution has a unique key which is it's own schedule
            solutionSpace[Key]=(schedule,totalSlot,penalty,fitnessFunctionValue)
            print listCounter,totalSlot,penalty,Key
            if(listCounter==0):
                minTotalSlot = totalSlot
                minTotalPenalty = penalty
                outputFile = open(arg3,"wb+")
                allOutputFile = open(allOutputFileName,"wb+")
                allOutputFile.write(str(fitnessFunctionValue)+"\n")
                
                outputFile.write(str(totalSlot)+"    "+str(penalty)+"\n")
                for examKey in sortedCourseList_ByName:
                    (tempDate,tempDateSlot,tempActualSlot)= schedule[examKey]
                    outputFile.write(examKey+"    "+str(tempDate)+"    "+str(tempDateSlot)+"\n")

                    allOutputFile.write(examKey+"    "+str(tempActualSlot)+"\n")
                
                outputFile.close()
                allOutputFile.close()
                
            else:
                if(penalty<minTotalPenalty):
                    #minTotalSlot = totalSlot
                    minTotalPenalty = penalty
                    outputFile = open(arg3,"wb+")
                    outputFile.write(str(totalSlot)+"    "+str(penalty)+"\n")
                    for examKey in sortedCourseList_ByName:
                        (tempDate,tempDateSlot,tempActualSlot)= schedule[examKey]
                        outputFile.write(examKey+"    "+str(tempDate)+"    "+str(tempDateSlot)+"\n")

                    outputFile.close()
                    
                allOutputFile = open(allOutputFileName,"a+")
                allOutputFile.write("\n\n")
                allOutputFile.write(str(fitnessFunctionValue)+"\n")
                
                for examKey in sortedCourseList_ByName:
                    (tempDate,tempDateSlot,tempActualSlot)= schedule[examKey]
                    allOutputFile.write(examKey+"    "+str(tempActualSlot)+"\n")
                allOutputFile.close()     
                    
                                   
                if(totalSlot < minTotalSlot):
                    minTotalSlot = totalSlot
                
            listCounter+=1
    

    for iterationLoop in range(1,100):   
             
        keyList = list()        
        for key_schedule in solutionSpace:
            keyList.append(key_schedule)
            
            
            (tempSchedule,tempNumberOfSlot,tempValOfPenalty,temp_fitnessFuncValue) = solutionSpace[key_schedule]
            print "HI:",tempNumberOfSlot,key_schedule

        print "Try Random Shuffle for tournament selection"
        print "Randomly select 2 chromosomes as parents, create two childlren, calculate fitness function for all and place the best two from 4 (2 parents and 2 children)."
        random.shuffle(keyList)
        #for element in keyList:
        #    print "Test RandShuffle:" ,element

        #raise NameError('Exception raised2')            

        
            #print tempNumberOfSlot,tempValOfPenalty
            
            
    # a while loop    while
    
        index = 0
        
        while(index < len(keyList)):
        
            if(index+1==len(keyList)):
                break
        
            parentKey1 = index
            parentKey2 = index+1
            print len(keyList),parentKey2
            print keyList[parentKey1]
            print keyList[parentKey2]

            (tempSchedule1,tempNumberOfTotalSlot1,tempValOfPenalty1,temp_fitnessFuncValue1) = deepcopy(solutionSpace[keyList[parentKey1]])
            (tempSchedule2,tempNumberOfTotalSlot2,tempValOfPenalty2,temp_fitnessFuncValue2) = deepcopy(solutionSpace[keyList[parentKey2]])
            print tempSchedule2,tempNumberOfTotalSlot2
            
            (mutatedChild1_temp,mutatedChild2_temp) = recombination_AndMutation(tempSchedule1,tempNumberOfTotalSlot1,tempSchedule2,tempNumberOfTotalSlot2,sortedCourseList_ByName,studentDictionary,courseDictionary,roomSize)
            
            (mutatedChild1_schedule,totalSlot_M1,penalty_M1,Key_M1) = GenerateSolutionResultFromGivenSolution(mutatedChild1_temp,courseDictionary,studentDictionary)
            (mutatedChild2_schedule,totalSlot_M2,penalty_M2,Key_M2) = GenerateSolutionResultFromGivenSolution(mutatedChild2_temp,courseDictionary,studentDictionary)
            
            hardConstraintVal_mutatedChild1 =  constraintViolation(mutatedChild1_schedule,totalSlot_M1,studentDictionary,courseDictionary,roomSize)
            hardConstraintVal_mutatedChild2 =  constraintViolation(mutatedChild2_schedule,totalSlot_M2,studentDictionary,courseDictionary,roomSize)
            
            fitnessFunctionValue_M1 = (hardConstraintVal_mutatedChild1 *  penalty_M1)
            fitnessFunctionValue_M2 = (hardConstraintVal_mutatedChild2 *  penalty_M2)
            
            listToSelectFrom = list()
            listToSelectFrom.append((1,temp_fitnessFuncValue1))
            listToSelectFrom.append((2,temp_fitnessFuncValue2))
            listToSelectFrom.append((3,fitnessFunctionValue_M1))
            listToSelectFrom.append((4,fitnessFunctionValue_M2))
            
            listToSelectFrom.sort(key=lambda tup: tup[1])
            print listToSelectFrom
            selectedFromGeneration = list()
            selectedFromGeneration.append(listToSelectFrom.pop(0)[0])
            selectedFromGeneration.append(listToSelectFrom.pop(0)[0])
            
            del solutionSpace[keyList[parentKey1]]
            del solutionSpace[keyList[parentKey2]]
            for selectedElement in selectedFromGeneration:
                if selectedElement == 1:
                    #first parent selected
                    solutionSpace[keyList[parentKey1]] = (tempSchedule1,tempNumberOfTotalSlot1,tempValOfPenalty1,temp_fitnessFuncValue1)
                elif selectedElement == 2:
                    #second parent selected
                    solutionSpace[keyList[parentKey2]] = (tempSchedule2,tempNumberOfTotalSlot2,tempValOfPenalty2,temp_fitnessFuncValue2) 
                elif selectedElement == 3:
                    #first child selected
                    solutionSpace[Key_M1] = (mutatedChild1_schedule,totalSlot_M1,penalty_M1,fitnessFunctionValue_M1) 
                else:
                    #second child selected
                    solutionSpace[Key_M2] = (mutatedChild2_schedule,totalSlot_M2,penalty_M2,fitnessFunctionValue_M2) 
                
            index += 2
            
            
        temp_fitnessFuncValue = 0
        iterIndex = 0
        for key_schedule in solutionSpace:
            (print_Schedule,print_NumberOfSlot,print_ValOfPenalty,print_fitnessFuncValue) = solutionSpace[key_schedule]
            
            print "Fitness Function:",print_fitnessFuncValue
            if int(print_fitnessFuncValue):
                print "Hi"
            
            if(print_NumberOfSlot<=maxSlot):

                if iterIndex == 0:
                    temp_fitnessFuncValue = print_fitnessFuncValue
                    
                    outputFile = open(arg3,"wb+")
                    outputFile.write(str(print_NumberOfSlot)+"    "+str(print_ValOfPenalty)+"\n")
                    
                    allOutputFile = open(allOutputFileName,"a+")
                    allOutputFile.write("\n\n")
                    allOutputFile.write(str(print_fitnessFuncValue)+"\n")
                                   
                    for examKey in sortedCourseList_ByName:
                        (tempDate,tempDateSlot,tempActualSlot)= print_Schedule[examKey]
                        outputFile.write(examKey+"    "+str(tempDate)+"    "+str(tempDateSlot)+"\n")
                        allOutputFile.write(examKey+"    "+str(tempActualSlot)+"\n")
                    outputFile.close()
                    allOutputFile.close()
                    
                else:
                    if print_fitnessFuncValue < temp_fitnessFuncValue:
                        temp_fitnessFuncValue = print_fitnessFuncValue
                    
                        outputFile = open(arg3,"wb+")
                        outputFile.write(str(print_NumberOfSlot)+"    "+str(print_ValOfPenalty)+"\n")
                        for examKey in sortedCourseList_ByName:
                            (tempDate,tempDateSlot,tempActualSlot)= print_Schedule[examKey]
                            outputFile.write(examKey+"    "+str(tempDate)+"    "+str(tempDateSlot)+"\n")
                        outputFile.close()
    
                    allOutputFile = open(allOutputFileName,"a+")
                    allOutputFile.write("\n\n")
                    allOutputFile.write(str(print_fitnessFuncValue)+"\n")
                    for examKey in sortedCourseList_ByName:
                        (tempDate,tempDateSlot,tempActualSlot)= print_Schedule[examKey]
                        allOutputFile.write(examKey+"    "+str(tempActualSlot)+"\n")
                    allOutputFile.close()
                    
                iterIndex += 1
