SELECT student_id, COUNT(*)
FROM assignments
WHERE grade IS NOT NULL
GROUP BY student_id;
