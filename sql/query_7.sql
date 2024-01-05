SELECT grades.grade as grade, 
       students.name as studemt_name, 
       subjects.name as subject
FROM grades
JOIN students ON grades.student_id = students.id
JOIN subjects ON grades.subject_id = subjects.id
WHERE students.group_id = 1 
	  AND subjects.id = 1
ORDER BY students.name;