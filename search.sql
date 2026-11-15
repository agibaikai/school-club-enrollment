SELECT c.club_id, c.name, c.category,
       c.capacity - (SELECT COUNT(*) FROM enrollments e
                     WHERE e.club_id = c.club_id) AS available_places
FROM clubs c
WHERE c.capacity > (SELECT COUNT(*) FROM enrollments e
                    WHERE e.club_id = c.club_id)
  AND (c.category = 'Technology' OR c.category = 'Communication')
ORDER BY c.club_id;
