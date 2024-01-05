SELECT DISTINCT subjects.name AS subject,
	        students.name AS student_name
FROM students
JOIN grades g ON students.id = g.student_id
JOIN subjects ON g.subject_id =  subjects.id
WHERE students.id = 1