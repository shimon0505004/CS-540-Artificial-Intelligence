import random
from copy import deepcopy

numberOfCourses = 150
numberOfStudents = 250
minNumberOfCourses = 2
maxNumberOfCourses = 5

courseName = range(1,numberOfCourses+1)
course = {}
for i in courseName:
    student = list()
    course[i] = student 
#    print i

for i in courseName:  
    print i,course[i] 

studentList = []
tempCourseList = deepcopy(courseName)
for student in range(0,numberOfStudents):
    randomNumberOfCoursesForStudent = random.choice(range(minNumberOfCourses,maxNumberOfCourses+1))
    #print "Student:",student,"#ofCourses:",randomNumberOfCoursesForStudent
    listOfCourses = set()
#    tempCourseList = deepcopy(courseName)
    #print "len:",len(tempCourseList)
    #print tempCourseList
    if len(tempCourseList) > randomNumberOfCoursesForStudent:
        for i in range(0,randomNumberOfCoursesForStudent):
            tempElement = tempCourseList.pop(random.randrange(len(tempCourseList)))
            listOfCourses.add(tempElement)             
            #print "element:",tempElement,listOfCourses
    else:
        count = 0
        tempSet = set()
        for i in range(0,len(tempCourseList)):
            tempElement = tempCourseList.pop(random.randrange(len(tempCourseList)))
            tempSet.add(tempElement)
            listOfCourses.add(tempElement)                
            #print "element:",tempElement,listOfCourses
            count += 1
        
        print tempSet    
        tempCourseList = deepcopy(courseName)
        print "copied master list"
        print tempCourseList
        print "removing from list"
        #removing previously added courses for current student
        for eachElement in tempSet:
            print eachElement
            tempCourseList.remove(eachElement)
        print tempCourseList
        
        #choosing courses from courses not previously added
        for i in range(count,randomNumberOfCoursesForStudent):
            tempElement = tempCourseList.pop(random.randrange(len(tempCourseList)))
            listOfCourses.add(tempElement)             
            #print "element:",tempElement,listOfCourses
        
        #all courses for the current student has been added. adding previously removed item from tempList
        #as this list is initialized for a new student now
        for eachElement in tempSet:
            print eachElement
            tempCourseList.append(eachElement)
        print "This list is for the next student"
        print tempCourseList
        
         
    studentList.append(listOfCourses)
  
print "printing student list"

studentFile = open("instance1.stu","wb+")    
for student in range(0,numberOfStudents):
    print "Student",student,studentList[student]   
    for courseNumber in studentList[student]:
        #print courseNumber
        #print course[courseNumber]
        course[courseNumber].append(student)
        #print course[courseNumber]
        studentFile.write(str(courseNumber)+"    ")
    if(student!=numberOfStudents-1):
        studentFile.write("\n")
    
studentFile.close()


print "Printing CourseList"
#determining number of students and max number of students in a course    
maxNumberOfStudents = 0;
for i in courseName:  
    print i,len(course[i]),course[i]
    if len(course[i]) >  maxNumberOfStudents:
        maxNumberOfStudents = len(course[i]) 
        
print "max number of students in a course",maxNumberOfStudents

#determine minimum number of students in a course
minNumberOfStudents = maxNumberOfStudents
for i in courseName: 
    #print i,len(course[i]),course[i]
    if len(course[i]) <  maxNumberOfStudents:
        minNumberOfStudents = len(course[i])
        
print "min number of students in a course",minNumberOfStudents 

#determining min number of seat in a room
minNumberOfSeatInARoom = 2*(maxNumberOfStudents+minNumberOfStudents)
print "min number of seat in a room :", minNumberOfSeatInARoom

#determining max number of timeslot
maxTimeSlot = numberOfCourses
print "max timeslot:",maxTimeSlot

#writing course file
courseFile = open("instance1.crs","wb+")
courseFile.write(str(minNumberOfSeatInARoom)+"    "+str(maxTimeSlot)+"\n"); 
for i in courseName:  
    print i,len(course[i]),course[i]
    courseFile.write(str(i)+"    "+str(len(course[i])))
    if(i != courseName[len(courseName)-1]):
        courseFile.write("\n")
courseFile.close()
            