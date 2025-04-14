USE tinyu
GO

SELECT * FROM students

DROP FUNCTION IF EXISTS f_concat
GO
CREATE FUNCTION f_concat (
    @a varchar(50), 
    @b varchar(50)
)
RETURNS varchar(101)
AS BEGIN
    RETURN @a + ' ' + @b 
END; 
GO

SELECT dbo.f_concat(student_firstname,student_lastname) as student_fullname
FROM students
GO

SELECT dbo.f_concat('Timmy','DaTooth') as tooth_men

DROP VIEW IF EXISTS v_students
GO

CREATE VIEW v_students AS 
SELECT s.student_id, dbo.f_concat(s.student_firstname, s.student_lastname) AS student_fullname,
s.student_lastname + ',' + s.student_firstname AS student_name, s.student_gpa, m.major_name 
FROM students s
JOIN majors m ON s.student_major_id = m.major_id;
GO

SELECT * FROM v_students;
GO

SELECT m.major_id, m.major_code, major_keywords.value AS major_keyword
FROM majors m
CROSS APPLY string_split(m.major_name, ' ') AS major_keywords
GO

DROP FUNCTION IF EXISTS f_search_majors
GO
CREATE FUNCTION f_search_majors()
RETURNS @keywords TABLE (
    major_id INT, 
    major_code VARCHAR(10),
    major_name VARCHAR(100)
)
AS BEGIN 
INSERT INTO @keywords
SELECT m.major_code, m.major_id, major_keywords.value AS major_keywords
FROM majors m
CROSS APPLY string_split(m.major_name,' ') AS major_keywords;
RETURN;
END;
GO

SELECT *
FROM dbo.f_search_majors();
GO

SELECT * 
FROM dbo.f_search_majors()
WHERE @keywords= 'Science';
GO

DROP FUNCTION IF EXISTS dbo.f_search_majors;
GO

CREATE FUNCTION dbo.f_search_majors()
RETURNS @keywords TABLE (
    major_id INT, 
    major_code VARCHAR(10),
    major_keyword VARCHAR(100)
)
AS 
BEGIN 
    INSERT INTO @keywords
    SELECT 
        m.major_id, 
        m.major_code, 
        major_keywords.value AS major_keyword
    FROM 
        majors m
    CROSS APPLY 
        STRING_SPLIT(m.major_name, ' ') AS major_keywords;
    RETURN;
END;
GO

SELECT *
FROM dbo.f_search_majors()
WHERE major_keyword='Science'
OR major_keyword='Sciences';
GO


ALTER TABLE students
ADD student_active CHAR (1) DEFAULT 'Y' NOT NULL, 
    student_inactive_date DATE NULL; 
GO 

SELECT * FROM students

DROP TRIGGER IF EXISTS trg_student_update;
GO

CREATE TRIGGER trg_student_update
ON students
AFTER INSERT, UPDATE 
AS BEGIN 
    UPDATE students
    SET students.student_active = CASE 
    WHEN students.student_inactive_date IS NOT NULL THEN 'N'
    ELSE 'Y'
   END 
FROM inserted i 
WHERE students.student_id=i.student_id
END; 
GO 

UPDATE students
SET student_inactive_date = '2024-05-21'
WHERE student_id = 1;


SELECT * FROM students;

UPDATE students 
SET student_inactive_date = '2020-08-01'
WHERE student_year_name= 'Graduate';
GO

SELECT * FROM students;
GO

UPDATE students 
SET student_inactive_date = NULL 
WHERE student_year_name = 'Graduate';
GO

SELECT * FROM students 