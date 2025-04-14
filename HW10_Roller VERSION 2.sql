use master;
GO

use demo;
GO

DROP TABLE IF EXISTS fudgenbooks
GO

CREATE TABLE fudgenbooks
(
    isbn VARCHAR(20) NOT NULL,
    title VARCHAR(50) NOT NULL,
    price MONEY,
    author1 VARCHAR(20) NOT NULL,
    author2 VARCHAR(20) NULL,
    author3 VARCHAR(20) NULL, 
    subjects VARCHAR(100) NOT NULL,
    pages INT NOT NULL,
    pub_no INT NOT NULL,
    pub_name VARCHAR(50) NOT NULL,
    pub_website VARCHAR(50) NOT NULL,
    CONSTRAINT pk_fudgenbooks_isbn PRIMARY KEY (isbn)
)
GO

INSERT INTO fudgenbooks VALUES
('372317842','Introduction to Money Laundering', 29.95,'Mandafort', 'Made-Off', NULL, 'scams,money laundering',367,101,'Rypoff','http://www.rypoffpublishing.com'),
('472325845','Imbezzle Like a Pro',34.95,'Made-Off','Moneesgon', NULL,'imbezzle,scams',670,101,'Rypoff','http://www.rypoffpublishing.com'),
('535621977','The Internet Scammer''s Bible',44.95, 'Screwm', 'Sucka', NULL, 'phising,id theft,scams',944,102, 'BS Press','http://www.bspress.com/books'),
('635619239','Art of the Ponzi Scheme', 39.95, 'Dewey','Screwm','Howe','scams,ponzi',450,102,'BS Press','http://www.bspress.com/books')
GO

SELECT * FROM fudgenbooks
GO

/* 
    Homework 10
*/
-- DROP CONSTRAINTS
IF EXISTS (
    SELECT * 
    FROM INFORMATION_SCHEMA.CONSTRAINT_TABLE_USAGE
    WHERE CONSTRAINT_NAME = 'fk_book_authors_isbn')
    ALTER TABLE fb_book_authors DROP fk_book_authors_isbn;

IF EXISTS (
    SELECT * 
    FROM INFORMATION_SCHEMA.CONSTRAINT_TABLE_USAGE
    WHERE CONSTRAINT_NAME = 'fk_book_authors_author_name')
    ALTER TABLE fb_book_authors DROP fk_book_authors_author_name;

IF EXISTS (
    SELECT * 
    FROM INFORMATION_SCHEMA.CONSTRAINT_TABLE_USAGE
    WHERE CONSTRAINT_NAME = 'fk_book_subjects_isbn')
    ALTER TABLE fb_book_subjects DROP fk_book_subjects_isbn;

IF EXISTS (
    SELECT * 
    FROM INFORMATION_SCHEMA.CONSTRAINT_TABLE_USAGE
    WHERE CONSTRAINT_NAME = 'fk_book_subjects_subject')
    ALTER TABLE fb_book_subjects DROP fk_book_subjects_subject;

IF EXISTS (
    SELECT * 
    FROM INFORMATION_SCHEMA.CONSTRAINT_TABLE_USAGE
    WHERE CONSTRAINT_NAME = 'fk_book_pub_no')
    ALTER TABLE fb_books DROP fk_book_pub_no;

-- DOWN DROP Tables
DROP TABLE IF EXISTS 
    fudgenbooks_1nf, fb_authors,
    fb_book_authors, fb_subjects,
    fb_book_subjects,
    fb_books, fb_publishers;
GO

-- 1.1
CREATE TABLE fudgenbooks_1nf (
    isbn VARCHAR(20) PRIMARY KEY,
    title VARCHAR(255),
    price DECIMAL(10, 2),
    pages INT,
    pub_no INT,
    pub_name VARCHAR(255),
    pub_website VARCHAR(255)
);
GO

INSERT INTO fudgenbooks_1nf (isbn, title, price, pages, pub_no, pub_name, pub_website)
    SELECT isbn, title, price, pages, pub_no, pub_name, pub_website
    FROM fudgenbooks;
GO

SELECT * FROM fudgenbooks_1nf;
GO

-- 1.2
CREATE TABLE fb_authors
(
    author_name VARCHAR(20) PRIMARY KEY NOT NULL,
);

INSERT INTO fb_authors (author_name) (
    SELECT author1 AS author_name FROM fudgenbooks WHERE author1 IS NOT NULL
        UNION
    SELECT author2 FROM fudgenbooks WHERE author2 IS NOT NULL
        UNION
    SELECT author3 FROM fudgenbooks WHERE author3 IS NOT NULL);
GO

SELECT * FROM fb_authors;
GO

-- 1.3
CREATE TABLE fb_book_authors (
    isbn VARCHAR(20) NOT NULL,
    author_name VARCHAR(20) NOT NULL,
    CONSTRAINT pl_fb_book_authors PRIMARY KEY (isbn, author_name)
);
GO

INSERT INTO fb_book_authors (isbn, author_name)
    SELECT isbn, author_name
    FROM (
        SELECT isbn, author1, author2, author3
        FROM fudgenbooks
    ) AS upvt_books
    UNPIVOT (
        author_name FOR author_column IN (author1, author2, author3)
    ) AS upvt_author;
GO

SELECT * FROM fb_book_authors;
GO

-- 1.4
CREATE TABLE fb_subjects
(
    subject VARCHAR(20) PRIMARY KEY NOT NULL,
);

INSERT INTO fb_subjects
    SELECT DISTINCT VALUE AS subject 
    FROM fudgenbooks CROSS APPLY STRING_SPLIT(subjects, ',');
GO

-- 1.5
CREATE TABLE fb_book_subjects
(
    isbn VARCHAR(20) NOT NULL,
    subject VARCHAR(20) NOT NULL,
    CONSTRAINT pl_fb_book_subjects PRIMARY KEY (isbn, subject)
);
GO

INSERT INTO fb_book_subjects (isbn, subject)
    SELECT isbn, value as subject
    FROM fudgenbooks CROSS APPLY STRING_SPLIT(subjects, ',');
GO

SELECT * FROM fb_book_subjects

--3.1
CREATE TABLE fb_books (
    isbn VARCHAR(20) PRIMARY KEY NOT NULL,
    title VARCHAR(50) NOT NULL,
    price MONEY NOT NULL,
    pages INT NOT NULL,
    pub_no INT NOT NULL
);

INSERT INTO fb_books (isbn, title, price, pages, pub_no)
    SELECT isbn, title, price, pages, pub_no
    FROM fudgenbooks_1nf;
GO

--3.2 
SELECT DISTINCT pub_no, pub_name, pub_website
FROM fudgenbooks_1nf

--4.0
CREATE TABLE fb_publishers (
    pub_no INT PRIMARY KEY NOT NULL,
    pub_name VARCHAR(50) NOT NULL,
    pub_website VARCHAR(50) NOT NULL
);

INSERT INTO fb_publishers (pub_no, pub_name, pub_website)
    SELECT DISTINCT pub_no, pub_name, pub_website
    FROM fudgenbooks_1nf;
GO

SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME LIKE 'fb_%';
GO

ALTER TABLE fb_book_authors 
    ADD CONSTRAINT fk_book_authors_isbn FOREIGN KEY (isbn)
    REFERENCES fb_books(isbn);
ALTER TABLE fb_book_authors 
    ADD CONSTRAINT fk_book_authors_author_name FOREIGN KEY (author_name)
    REFERENCES fb_authors(author_name);
GO

ALTER TABLE fb_book_subjects 
    ADD CONSTRAINT fk_book_subjects_isbn FOREIGN KEY (isbn)
    REFERENCES fb_books(isbn);
ALTER TABLE fb_book_subjects 
    ADD CONSTRAINT fk_book_subjects_subject FOREIGN KEY (subject)
    REFERENCES fb_subjects(subject);
GO

ALTER TABLE fb_books
    ADD CONSTRAINT fk_books_pub_no FOREIGN KEY (pub_no)
    REFERENCES fb_publishers(pub_no);
GO





--end fudge n books 


--begin xyz consulting

DROP TABLE IF EXISTS xyz_consulting
GO

CREATE TABLE xyz_consulting (
    project_id INT NOT NULL,
    project_name VARCHAR(50) NOT NULL,
    employee_id INT NOT NULL,
    employee_name VARCHAR(50) NOT NULL,
    rate_category CHAR(1) NOT NULL,
    rate_amount MONEY NOT NULL,
    billable_hours INT NOT NULL,
    total_billed MONEY NOT NULL,
    CONSTRAINT pk_xyz_consulting PRIMARY KEY (project_id, employee_id)
);

INSERT INTO xyz_consulting VALUES
(1023,	'Madagascar travel site',	11,	'Carol Ling',	'A',	 60.00, 	5,	 300.00 ),
(1023,	'Madagascar travel site',	12,	'Chip Atooth',	'B',	 50.00, 	10,	 500.00 ),
(1023,	'Madagascar travel site',	16,	'Charlie Horse',	'C',	 40.00, 	2,	 80.00), 
(1056,	'Online estate agency',	11,	'Carol Ling',	'D',	 90.00, 	5,	 450.00 ),
(1056,	'Online estate agency',	17,	'Avi Maria',	'B',	 50.00, 	2,	 100.00 ),
(1099,	'Open travel network',	11,	'Carol Ling',	'A',	 60.00, 	6,	 360.00 ),
(1099,	'Open travel network',	12,	'Chip Atooth',	'C',	 40.00, 	8,	 320.00 ),
(1099,	'Open travel network',	14,	'Arnie Hurtz',	'D',	 90.00, 	3,	 270.00 )
GO

SELECT * FROM xyz_consulting

SELECT DISTINCT project_id, project_name FROM xyz_consulting ORDER BY project_name;

/*
    HW 10
*/
-- DOWN DROP Constraints
IF EXISTS (
    SELECT * 
    FROM INFORMATION_SCHEMA.CONSTRAINT_TABLE_USAGE
    WHERE CONSTRAINT_NAME = 'fk_billable_project_id')
    ALTER TABLE billable DROP fk_billable_project_id;

IF EXISTS (
    SELECT * 
    FROM INFORMATION_SCHEMA.CONSTRAINT_TABLE_USAGE
    WHERE CONSTRAINT_NAME = 'fk_billable_employee_id')
    ALTER TABLE billable DROP fk_billable_employee_id;

IF EXISTS (
    SELECT * 
    FROM INFORMATION_SCHEMA.CONSTRAINT_TABLE_USAGE
    WHERE CONSTRAINT_NAME = 'fk_billable_rate_category')
    ALTER TABLE billable DROP fk_billable_rate_category;
GO

-- DOWN DROP Tables
DROP TABLE IF EXISTS
    projects, employees,
    ratecards, billable;
GO

-- UP CREATE Tables
CREATE TABLE projects (
    project_id INT PRIMARY KEY,
    project_name VARCHAR(50) NOT NULL,
)

CREATE TABLE employees (
    employee_id INT PRIMARY KEY,
    employee_name VARCHAR(50) NOT NULL
)

CREATE TABLE ratecards (
    rate_category VARCHAR PRIMARY KEY,
    rate_amount MONEY NOT NULL
)

CREATE TABLE billable (
    project_id INT NOT NULL,
    employee_id INT NOT NULL,
    rate_category VARCHAR NOT NULL,
    billable_hours INT NOT NULL,
)
GO

-- UP INSERT Data
INSERT INTO projects (project_id, project_name)
    SELECT DISTINCT project_id, project_name
    FROM xyz_consulting;
GO

INSERT INTO employees (employee_id, employee_name)
    SELECT DISTINCT 
        employee_id, 
        employee_name
    FROM xyz_consulting
GO

INSERT INTO ratecards (rate_category, rate_amount)
    SELECT DISTINCT 
        rate_category,
        rate_amount
    FROM xyz_consulting
GO

INSERT INTO billable (project_id, employee_id, rate_category, billable_hours)
    SELECT 
        project_id,
        employee_id,
        rate_category,
        billable_hours
    FROM xyz_consulting;
GO

-- UP FK Constraints
ALTER TABLE billable 
    ADD CONSTRAINT fk_billable_project_id FOREIGN KEY (project_id)
    REFERENCES projects(project_id);
ALTER TABLE billable 
    ADD CONSTRAINT fk_billable_employee_id FOREIGN KEY (employee_id)
    REFERENCES employees(employee_id);
ALTER TABLE billable 
    ADD CONSTRAINT fk_billable_rate_category FOREIGN KEY (rate_category)
    REFERENCES ratecards(rate_category);
GO


-- The modifications I would have made to take the database from 0NF to 1NF seem to already have been completed. 
-- That is, we started with a homogenous clump of a table and in the first part of the code we have already split the table up.
-- Splitting the one large table up into 4 seperate tables was the necessarry step to take the database from 0NF to 1NF. 


--END 0NF to 1NF code





--BEGIN 1NF to 2NF code
-- CREATE TABLE in 1NF

DROP TABLE IF EXISTS xyz_consulting
GO

CREATE TABLE xyz_consulting (
    project_id INT NOT NULL,
    project_name VARCHAR(50) NOT NULL,
    employee_id INT NOT NULL,
    employee_name VARCHAR(50) NOT NULL,
    rate_category CHAR(1) NOT NULL,
    rate_amount MONEY NOT NULL,
    billable_hours INT NOT NULL,
    total_billed MONEY NOT NULL,
    CONSTRAINT pk_xyz_consulting PRIMARY KEY (project_id, employee_id)
);

-- INSERT data into the table
INSERT INTO xyz_consulting VALUES
(1023, 'Madagascar travel site', 11, 'Carol Ling', 'A', 60.00, 5, 300.00),
(1023, 'Madagascar travel site', 12, 'Chip Atooth', 'B', 50.00, 10, 500.00),
(1023, 'Madagascar travel site', 16, 'Charlie Horse', 'C', 40.00, 2, 80.00), 
(1056, 'Online estate agency', 11, 'Carol Ling', 'D', 90.00, 5, 450.00),
(1056, 'Online estate agency', 17, 'Avi Maria',  'B', 50.00, 2, 100.00),
(1099, 'Open travel network', 11, 'Carol Ling', 'A', 60.00, 6, 360.00),
(1099, 'Open travel network', 12, 'Chip Atooth', 'C', 40.00, 8, 320.00),
(1099, 'Open travel network', 14, 'Arnie Hurtz', 'D', 90.00, 3, 270.00);
GO

-- SELECT all data
SELECT * FROM xyz_consulting;

-- SELECT DISTINCT project details
SELECT DISTINCT project_id, project_name FROM xyz_consulting ORDER BY project_name;

-- DOWN: DROP constraints if they exist
IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.CONSTRAINT_TABLE_USAGE WHERE CONSTRAINT_NAME = 'fk_billable_project_id')
    ALTER TABLE billable DROP CONSTRAINT fk_billable_project_id;

IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.CONSTRAINT_TABLE_USAGE WHERE CONSTRAINT_NAME = 'fk_billable_employee_id')
    ALTER TABLE billable DROP CONSTRAINT fk_billable_employee_id;

IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.CONSTRAINT_TABLE_USAGE WHERE CONSTRAINT_NAME = 'fk_billable_rate_category')
    ALTER TABLE billable DROP CONSTRAINT fk_billable_rate_category;
GO

-- DOWN: DROP tables if they exist
DROP TABLE IF EXISTS projects, employees, ratecards, billable;
GO

-- UP: CREATE tables
CREATE TABLE projects (
    project_id INT PRIMARY KEY,
    project_name VARCHAR(50) NOT NULL
);

CREATE TABLE employees (
    employee_id INT PRIMARY KEY,
    employee_name VARCHAR(50) NOT NULL
);

CREATE TABLE ratecards (
    rate_category CHAR(1) PRIMARY KEY,
    rate_amount MONEY NOT NULL
);

CREATE TABLE billable (
    project_id INT NOT NULL,
    employee_id INT NOT NULL,
    rate_category CHAR(1) NOT NULL,
    billable_hours INT NOT NULL,
    CONSTRAINT pk_billable PRIMARY KEY (project_id, employee_id, rate_category)
);
GO

-- UP: INSERT data into normalized tables
INSERT INTO projects (project_id, project_name)
    SELECT DISTINCT project_id, project_name FROM xyz_consulting;
GO

INSERT INTO employees (employee_id, employee_name)
    SELECT DISTINCT employee_id, employee_name FROM xyz_consulting;
GO

INSERT INTO ratecards (rate_category, rate_amount)
    SELECT DISTINCT rate_category, rate_amount FROM xyz_consulting;
GO

INSERT INTO billable (project_id, employee_id, rate_category, billable_hours)
    SELECT project_id, employee_id, rate_category, billable_hours FROM xyz_consulting;
GO

-- UP: ADD foreign key constraints
ALTER TABLE billable 
    ADD CONSTRAINT fk_billable_project_id FOREIGN KEY (project_id)
    REFERENCES projects(project_id);

ALTER TABLE billable 
    ADD CONSTRAINT fk_billable_employee_id FOREIGN KEY (employee_id)
    REFERENCES employees(employee_id);

ALTER TABLE billable 
    ADD CONSTRAINT fk_billable_rate_category FOREIGN KEY (rate_category)
    REFERENCES ratecards(rate_category);
GO

--To move from 1NF to 2NF added an additional constraint on the primary key in the table billable
-- this constraint makes the key a composite key making all values in the table dependent on the composite key
-- To my understanding this removes the partial dependency and satisfies the requirements. 
-- All other tables already satisfy this requirement and require no further modification to satisft 2NF. 
-- Or at least I hope that is the case. 



-- End 1NF to 2NF code



-- BEGIN 2NF to 3NF code

DROP TABLE IF EXISTS xyz_consulting
GO

CREATE TABLE xyz_consulting (
    project_id INT NOT NULL,
    project_name VARCHAR(50) NOT NULL,
    employee_id INT NOT NULL,
    employee_name VARCHAR(50) NOT NULL,
    rate_category CHAR(1) NOT NULL,
    rate_amount MONEY NOT NULL,
    billable_hours INT NOT NULL,
    -- total_billed MONEY NOT NULL, -- Remove this column to eliminate transitive dependency
    CONSTRAINT pk_xyz_consulting PRIMARY KEY (project_id, employee_id)
);

-- INSERT data into the table
INSERT INTO xyz_consulting VALUES
(1023, 'Madagascar travel site', 11, 'Carol Ling', 'A', 60.00, 5),
(1023, 'Madagascar travel site', 12, 'Chip Atooth', 'B', 50.00, 10),
(1023, 'Madagascar travel site', 16, 'Charlie Horse', 'C', 40.00, 2), 
(1056, 'Online estate agency', 11, 'Carol Ling', 'D', 90.00, 5),
(1056, 'Online estate agency', 17, 'Avi Maria',  'B', 50.00, 2),
(1099, 'Open travel network', 11, 'Carol Ling', 'A', 60.00, 6),
(1099, 'Open travel network', 12, 'Chip Atooth', 'C', 40.00, 8),
(1099, 'Open travel network', 14, 'Arnie Hurtz', 'D', 90.00, 3);
GO

-- SELECT all data
SELECT * FROM xyz_consulting;

-- SELECT DISTINCT project details
SELECT DISTINCT project_id, project_name FROM xyz_consulting ORDER BY project_name;

-- DOWN: DROP constraints if they exist
IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.CONSTRAINT_TABLE_USAGE WHERE CONSTRAINT_NAME = 'fk_billable_project_id')
    ALTER TABLE billable DROP CONSTRAINT fk_billable_project_id;

IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.CONSTRAINT_TABLE_USAGE WHERE CONSTRAINT_NAME = 'fk_billable_employee_id')
    ALTER TABLE billable DROP CONSTRAINT fk_billable_employee_id;

IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.CONSTRAINT_TABLE_USAGE WHERE CONSTRAINT_NAME = 'fk_billable_rate_category')
    ALTER TABLE billable DROP CONSTRAINT fk_billable_rate_category;
GO

-- DOWN: DROP tables if they exist
DROP TABLE IF EXISTS projects, employees, ratecards, billable;
GO

-- UP: CREATE tables
CREATE TABLE projects (
    project_id INT PRIMARY KEY,
    project_name VARCHAR(50) NOT NULL
);

CREATE TABLE employees (
    employee_id INT PRIMARY KEY,
    employee_name VARCHAR(50) NOT NULL
);

CREATE TABLE ratecards (
    rate_category CHAR(1) PRIMARY KEY,
    rate_amount MONEY NOT NULL
);

CREATE TABLE billable (
    project_id INT NOT NULL,
    employee_id INT NOT NULL,
    rate_category CHAR(1) NOT NULL,
    billable_hours INT NOT NULL,
    CONSTRAINT pk_billable PRIMARY KEY (project_id, employee_id, rate_category)
);
GO

-- UP: INSERT data into normalized tables
INSERT INTO projects (project_id, project_name)
    SELECT DISTINCT project_id, project_name FROM xyz_consulting;
GO

INSERT INTO employees (employee_id, employee_name)
    SELECT DISTINCT employee_id, employee_name FROM xyz_consulting;
GO

INSERT INTO ratecards (rate_category, rate_amount)
    SELECT DISTINCT rate_category, rate_amount FROM xyz_consulting;
GO

INSERT INTO billable (project_id, employee_id, rate_category, billable_hours)
    SELECT project_id, employee_id, rate_category, billable_hours FROM xyz_consulting;
GO

-- UP: ADD foreign key constraints
ALTER TABLE billable 
    ADD CONSTRAINT fk_billable_project_id FOREIGN KEY (project_id)
    REFERENCES projects(project_id);

ALTER TABLE billable 
    ADD CONSTRAINT fk_billable_employee_id FOREIGN KEY (employee_id)
    REFERENCES employees(employee_id);

ALTER TABLE billable 
    ADD CONSTRAINT fk_billable_rate_category FOREIGN KEY (rate_category)
    REFERENCES ratecards(rate_category);
GO

-- Calculate total_billed when needed
SELECT 
    b.project_id, 
    p.project_name,
    b.employee_id,
    e.employee_name,
    b.rate_category,
    r.rate_amount,
    b.billable_hours,
    (r.rate_amount * b.billable_hours) AS total_billed
FROM 
    billable b
JOIN 
    projects p ON b.project_id = p.project_id
JOIN 
    employees e ON b.employee_id = e.employee_id
JOIN 
    ratecards r ON b.rate_category = r.rate_category;


-- To resolve all tables to being 3NF we change total_billed to not have transitive dependencies and to instead 
-- only be calulated when needed and not in the table as a value. 