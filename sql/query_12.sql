SELECT s.name AS student_name,
	 groups.name AS group_name,
	 subjects.name as subject,
	 g.date as grade_date,
	 g.grade as grade
FROM students s
JOIN grades g ON s.id = g.student_id
JOIN subjects ON g.subject_id =  subjects.id
JOIN groups ON groups.id = s.group_id 
WHERE groups.id = 1
	AND subjects.id = 1
	AND g.date = (
    SELECT MAX(date) FROM grades g2
    WHERE g2.student_id = s.id
    AND g2.subject_id = subjects.id
    GROUP BY g2.student_id, g2.subject_id
)
ORDER BY s.name