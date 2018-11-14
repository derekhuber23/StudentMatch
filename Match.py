#!/usr/bin/python

## programe-Shapley algorithm
# http://www.nrmp.org/match-process/match-algorithm/
# http://www.nber.org/papers/w6963

# From http://rosettacode.org/wiki/Stable_marriage_problem
# Uses deepcopy to make actual copy of the contents of the dictionary in a new object
# http://pymotw.com/2/copy/

import copy
from collections import defaultdict

#Create python dictionary with names as keys, values as list
studentprefers = {
    'Alex':  ['American', 'Mercy', 'County', 'Mission', 'General', 'Fairview', 'Saint Mark', 'City', 'Deaconess', 'Park'],
    'Brian':  ['County', 'Deaconess', 'American', 'Fairview', 'Mercy', 'Saint Mark', 'City', 'General', 'Mission', 'Park'],
    'Cassie':  ['Deaconess', 'Mercy', 'American', 'Fairview', 'City', 'Saint Mark', 'Mission', 'Park', 'County', 'General'],
    'Dana':  ['Mission', 'Saint Mark', 'Fairview', 'Park', 'Deaconess', 'Mercy', 'General', 'City', 'County', 'American'],
    'Edward':   ['General', 'Fairview', 'City', 'County', 'Saint Mark', 'Mercy', 'American', 'Mission', 'Deaconess', 'Park'],
    'Faith': ['City', 'American', 'Fairview', 'Park', 'Mercy', 'Mission', 'County', 'General', 'Deaconess', 'Saint Mark'],
    'George':  ['Park', 'Mercy', 'Mission', 'City', 'County', 'American', 'Fairview', 'Deaconess', 'General', 'Saint Mark'],
    'Hannah':  ['American', 'Mercy', 'Deaconess', 'Saint Mark', 'Mission', 'County', 'General', 'City', 'Park', 'Fairview'],
    'Ian':  ['Park', 'County', 'Fairview', 'Deaconess', 'City', 'American', 'Saint Mark', 'Mission', 'General', 'Mercy'],
    #'Ian':  ['Park'],
    'Jessica':  ['American', 'Saint Mark', 'General', 'Park', 'Mercy', 'City', 'Fairview', 'County', 'Mission', 'Deaconess']}
programprefers = {
    'American':  ['Brian', 'Faith', 'Jessica', 'George', 'Ian', 'Alex', 'Dana', 'Edward', 'Cassie', 'Hannah'],
    'City':  ['Brian', 'Alex', 'Cassie', 'Faith', 'George', 'Dana', 'Ian', 'Edward', 'Jessica', 'Hannah'],
    'County': ['Faith', 'Brian', 'Edward', 'George', 'Hannah', 'Cassie', 'Ian', 'Alex', 'Dana', 'Jessica'],
    'Fairview':  ['Faith', 'Jessica', 'Cassie', 'Alex', 'Ian', 'Hannah', 'George', 'Dana', 'Brian', 'Edward'],
    'Mercy':  ['Jessica', 'Hannah', 'Faith', 'Dana', 'Alex', 'George', 'Cassie', 'Edward', 'Ian', 'Brian'],
    'Saint Mark':  ['Brian', 'Alex', 'Edward', 'Ian', 'Jessica', 'Dana', 'Faith', 'George', 'Cassie', 'Hannah'],
    'Park':  ['Jessica', 'George', 'Hannah', 'Faith', 'Brian', 'Alex', 'Cassie', 'Edward', 'Dana', 'Ian'],
    'Deaconess': ['George', 'Jessica', 'Brian', 'Alex', 'Ian', 'Dana', 'Hannah', 'Edward', 'Cassie', 'Faith'],
    'Mission':  ['Ian', 'Cassie', 'Hannah', 'George', 'Faith', 'Brian', 'Alex', 'Edward', 'Jessica', 'Dana'],
    'General':  ['Edward', 'Hannah', 'George', 'Alex', 'Brian', 'Jessica', 'Cassie', 'Ian', 'Faith', 'Dana']}
programSlots = {
    'American': 1,
    'City': 1,
    'County': 1,
    'Fairview': 1,
    'Mercy': 1,
    'Saint Mark': 2,
    'Park': 1,
    'Deaconess': 2,
    'Mission': 2,
    'General': 9}

students = sorted(studentprefers.keys())
programs = sorted(programprefers.keys())



def matchmaker():
    studentsfree = students[:]
    studentslost = []
    matched = {}
    for programName in programs:
        if programName not in matched:
            matched[programName] = list()
    studentprefers2 = copy.deepcopy(studentprefers)
    programprefers2 = copy.deepcopy(programprefers)
    while studentsfree:
        student = studentsfree.pop(0)
        print("%s is on the market" % (student))
        studentslist = studentprefers2[student]
        program = studentslist.pop(0)
        print("  %s (program's #%s) is checking out %s (student's #%s)" % (student, (programprefers[program].index(student)+1), program, (studentprefers[student].index(program)+1)) )
        tempmatch = matched.get(program)
        if len(tempmatch) < programSlots.get(program):
            # Program's free
            if student not in matched[program]:
                matched[program].append(student)
                print("    There's a spot! Now matched: %s and %s" % (student.upper(), program.upper()))
        else:
            # The student proposes to an full program!
            programslist = programprefers2[program]
            for (i, matchedAlready) in enumerate(tempmatch):
                if programslist.index(matchedAlready) > programslist.index(student):
                    # Program prefers new student
                    if student not in matched[program]:
                        matched[program][i] = student
                        print("  %s dumped %s (program's #%s) for %s (program's #%s)" % (program.upper(), matchedAlready, (programprefers[program].index(matchedAlready)+1), student.upper(), (programprefers[program].index(student)+1)))
                        if studentprefers2[matchedAlready]:
                            # Ex has more programs to try
                            studentsfree.append(matchedAlready)
                        else:
                            studentslost.append(matchedAlready)
                else:
                    # Program still prefers old match
                    print("  %s would rather stay with %s (their #%s) over %s (their #%s)" % (program, matchedAlready, (programprefers[program].index(matchedAlready)+1), student, (programprefers[program].index(student)+1)))
                    if studentslist:
                        # Look again
                        studentsfree.append(student)
                    else:
                        studentslost.append(student)
    print
    for lostsoul in studentslost:
        print('%s did not match' % lostsoul)
    return (matched, studentslost)





def check(matched):
    inversematched = defaultdict(list)
    for programName in matched.keys():
        for studentName in matched[programName]:
            inversematched[programName].append(studentName)

    for programName in matched.keys():
        for studentName in matched[programName]:

            programNamelikes = programprefers[programName]
            programNamelikesbetter = programNamelikes[:programNamelikes.index(studentName)]
            helikes = studentprefers[studentName]
            helikesbetter = helikes[:helikes.index(programName)]
            for student in programNamelikesbetter:
                for p in inversematched.keys():
                    if student in inversematched[p]:
                        studentsprogram = p
                studentlikes = studentprefers[student]

                ## Not sure if this is correct
                try:
                    studentlikes.index(studentsprogram)
                except ValueError:
                    continue

                if studentlikes.index(studentsprogram) > studentlikes.index(programName):
                    print("%s and %s like each other better than "
                          "their present match: %s and %s, respectively"
                          % (programName, student, studentName, studentsprogram))
                    return False
            for program in helikesbetter:
                programsstudents = matched[program]
                programlikes = programprefers[program]
                for programsstudent in programsstudents:
                    if programlikes.index(programsstudent) > programlikes.index(studentName):
                        print("%s and %s like each other better than "
                              "their present match: %s and %s, respectively"
                              % (studentName, program, programName, programsstudent))
                        return False
    return True


print('\nPlay-by-play:')
(matched, studentslost) = matchmaker()

print('\nCouples:')
print('  ' + ',\n  '.join('%s is matched to %s' % couple
                          for couple in sorted(matched.items())))
print
print('Match stability check PASSED'
      if check(matched) else 'Match stability check FAILED')

print('\n\nSwapping two matches to introduce an error')
matched[programs[0]], matched[programs[1]] = matched[programs[1]], matched[programs[0]]
for program in programs[:2]:
    print('  %s is now matched to %s' % (program, matched[program]))
print
print('Match stability check PASSED'
      if check(matched) else 'Match stability check FAILED')