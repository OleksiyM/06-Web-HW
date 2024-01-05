SELECT groups.name AS group_name,
       round(AVG(grades.grade),2) AS average_grade
FROM groups
JOIN students ON groups.id = students.group_id
JOIN grades ON students.id = grades.student_id
JOIN subjects ON grades.subject_id = subjects.id
WHERE subjects.name = 'math'
GROUP BY groups.id, groups.name
ORDER BY average_grade DESC;