SELECT p.name as professor_name, 
       ROUND(AVG(g.grade),2) as average_grade
FROM professors p 
JOIN grades g ON g.subject_id = s.id
JOIN subjects s ON p.id = s.professor_id
WHERE p.id = 5
GROUP BY p.id 