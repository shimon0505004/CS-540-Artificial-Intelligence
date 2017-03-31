Implemented Randomized Iterative Improvement (RII) on local search,
and tabu search for solving examination timetabling problem.

Problem: Examination Timetable:
There is only one room with finite seating capacity available for timetabling examinations.
Five timeslots are available every day. 
The following are the list of hard and soft constraints:

Hard Constraints:

Each course has one exam, which is conducted only once, and all students enrolled for the course must take the exam in the same time slot.
The first day in the timetable is 1 and there are five time slots {1, 2, 3, 4, 5} available every day.
There are no holidays! Also, there must be no unused timeslots between the first and the last day of exams in the timetable.
Exams with one or more common students cannot be assigned to the same time slot, 
i.e. a student cannot take more than one exam in the same time slot.
Multiple exams can be assigned to a single time slot.
Total number of students taking exams in a given time slot should not exceed the room capacity specified in the problem.
The total number of time slots used by the timetable should not exceed the maximum number of timeslots specified in the problem.

Soft Constraints (Objective Functions):

Our version of the problem will allow for one of the following two objective functions:
Total number of timeslots used by the timetable should be minimized.
Total student cost should be minimized. 
[Description of heuristic can be found in :http://www.cs.colostate.edu/~cs540/spr2015/more_assignments/hw415.html]

Problem Objective:

The objective, here, is to space out the assignment of exams as much as possible so that students have more time to prepare 
between their exams. Therefore, you must try to minimize the total student cost. 
This heuristic allows for exams with more students to be preferred for spacing out.
