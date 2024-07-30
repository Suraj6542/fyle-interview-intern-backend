SELECT teacher_id, COUNT(*) AS grade_a_count
FROM assignments
WHERE grade = 'A'
GROUP BY teacher_id
ORDER BY COUNT(*) DESC
LIMIT 1;
