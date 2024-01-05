SELECT p.name as professor_name, 
	   s.name as subject
FROM professors p
JOIN subjects s ON p.id = s.professor_id
WHERE p.id =3;