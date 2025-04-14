if not exists(SELECT * FROM sys.databases WHERE name='moze2')
    CREATE DATABASE moze2
GO 

USE moze2
GO 

-- DOWN 
if exists(SELECT * FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS
    WHERE CONSTRAINT_NAME='fk_jobs_job_submitted_by')
    ALTER TABLE jobs DROP CONSTRAINT fk_jobs_job_submitted_by
if exists(SELECT * FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS
    WHERE CONSTRAINT_NAME='fk_jobs_job_contracted_by')
    ALTER TABLE jobs DROP CONSTRAINT fk_jobs_job_contracted_by
if exists(SELECT * FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS
    WHERE CONSTRAINT_NAME='fk_contractors_contractor_state')
    ALTER TABLE contractors DROP CONSTRAINT fk_contractors_contractor_state
if exists(SELECT * FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS
    WHERE CONSTRAINT_NAME='fk_customers_customer_state')
    ALTER TABLE customers DROP CONSTRAINT fk_customers_customer_state
drop table if exists customers 
drop table if exists state_lookup
drop table if exists contractors 
drop table if exists jobs
GO
--UP Metadata
CREATE TABLE state_lookup(
    state_code char(2) not null, 
    CONSTRAINT pk_state_lookup_state_code PRIMARY KEY(state_code)
) 

CREATE TABLE customers(
    customer_id int IDENTITY not null, 
    customer_email varchar(50) not null, 
    customer_min_price money not null, 
    customer_max_price money not null, 
    customer_city varchar(50) not null, 
    customer_state char(2) not null, 
    CONSTRAINT pk_customers_customer_id PRIMARY KEY (customer_id),
    CONSTRAINT u_customer_email UNIQUE (customer_email),
    CONSTRAINT ck_min_max_price check (customer_min_price<=customer_max_price)
)
ALTER TABLE customers
    add CONSTRAINT fk_customer_state FOREIGN KEY (customer_state)
        REFERENCES state_lookup(state_code)

CREATE TABLE contractors(
    contractor_id int IDENTITY not null, 
    contractor_email varchar(50) not null, 
    contractor_rate money not null, 
    contractor_city varchar(50) not null, 
    contractor_state char(2) not null, 
    CONSTRAINT pk_contractors_contractor_id PRIMARY KEY (contractor_id),
    CONSTRAINT u_contractors_contractor_email UNIQUE (contractor_email),
    CONSTRAINT fk_contractors_contractor_state FOREIGN KEY (contractor_state)
        REFERENCES state_lookup(state_code)
)

CREATE TABLE jobs(
    job_id int IDENTITY not null, 
    job_submitted_by int not null, 
    job_requested_date DATE not null,
    job_contracted_by int null, 
    job_contracted_date INT null, 
    job_service_rate money null, 
    job_estimated_date DATE null, 
    job_completed_date DATE null, 
    job_customer_rating int null CHECK (job_customer_rating between 1 and 5),
    CONSTRAINT pk_jobs_job_id PRIMARY KEY (job_id),
    CONSTRAINT fk_jobs_job_submitted_by FOREIGN KEY (job_submitted_by)
    REFERENCES customers(customer_id),
    CONSTRAINT fk_jobs_job_contracted_by FOREIGN KEY (job_contracted_by)
    REFERENCES contractors (contractor_id),
    CONSTRAINT ck_jobs_valid_job_dates CHECK (job_requested_date <= job_estimated_date and job_estimated_date <= job_completed_date)

)

GO
--UP DATA 
INSERT INTO state_lookup (state_code) VALUES  
('NY'),('NJ'),('CT')
INSERT INTO customers
    (customer_email, customer_min_price, customer_max_price, customer_city, customer_state)
    VALUES 
    ('lkarforless@superrito.com', 50, 100, 'Syracuse', 'NY'),
    ('bdehatchett@dayrep.com', 25, 50, 'Syracuse', 'NY'),
    ('pmeaup@dayrep.com', 100, 150, 'Syracuse', 'NY'),
    ('tanott@gustr.com', 25, 75, 'Rochester', 'NY'),
    ('sboate@gustr.com', 50, 100, 'New Haven', 'CT')

INSERT INTO contractors 
(contractor_email, contractor_rate, contractor_city, contractor_state)
VALUES
('otyme@dayrep.com', 50.00, 'Syrcuse', 'NY'),
('meyezing@dayrep.com', 75.00, 'Syracuse', 'NY'),
('bitall@dayrep.com', 35.00, 'Rochester', 'NY'),
('sbeeches@dayrep.com', 85.00, 'Hartford', 'CT')

INSERT INTO jobs
(job_submitted_by, job_requested_date, job_contracted_by, job_service_rate, job_estimated_date, job_completed_date)
VALUES
(1, '2020-05-01', NULL, NULL, NULL, NULL),
(2, '2020-05-01', 1, 50.00, '2020-05-02', NULL), 
(5, '2020-05-01', 4, 85.00, '2020-05-03', '2020-05-03')

GO
--Verify 
SELECT * FROM state_lookup
SELECT * FROM customers 
SELECT * FROM contractors 
SELECT * FROM jobs 
