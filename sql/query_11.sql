SELECT students.name AS student_name,
	 p.name AS professor_name,
	 ROUND(AVG(g.grade),2) as average_grade
FROM students
JOIN grades g ON students.id = g.student_id
JOIN subjects ON g.subject_id =  subjects.id
JOIN professors p ON p.id = subjects.professor_id 
WHERE students.id = 1
  AND p.id = 5