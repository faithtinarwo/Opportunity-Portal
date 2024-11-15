-- CREATE DATABASE opportunity_portal;

-- USE opportunity_portal;

/*CREATE TABLE employers (
    employer_id INT AUTO_INCREMENT PRIMARY KEY,
    company_name VARCHAR(100) NOT NULL,
    industry VARCHAR(50),
    contact_info VARCHAR(100)
);*/

/*CREATE TABLE job_listings (
    job_id INT AUTO_INCREMENT PRIMARY KEY,
    employer_id INT,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    requirements TEXT,
    location VARCHAR(100),
    status VARCHAR(20) DEFAULT 'active',
    FOREIGN KEY (employer_id) REFERENCES employers(employer_id)
);*/

/*CREATE TABLE candidates (
    candidate_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    contact_info VARCHAR(100),
    skills TEXT,
    experience TEXT
);*/

/*CREATE TABLE applications (
    application_id INT AUTO_INCREMENT PRIMARY KEY,
    candidate_id INT,
    job_id INT,
    application_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'applied',
    FOREIGN KEY (candidate_id) REFERENCES candidates(candidate_id),
    FOREIGN KEY (job_id) REFERENCES job_listings(job_id)
);*/

/*CREATE TABLE job_status_updates (
    update_id INT AUTO_INCREMENT PRIMARY KEY,
    job_id INT,
    status VARCHAR(20),
    update_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (job_id) REFERENCES job_listings(job_id)
);*/

-- USE opportunity_portal;

-- ALTER TABLE job_listings DROP FOREIGN KEY job_listings_ibfk_1;

-- DROP TABLE employers;

SHOW TABLES;
-- DROP TABLE IF EXISTS job_listing;
-- SHOW CREATE TABLE application;
-- ALTER TABLE application DROP FOREIGN KEY application_ibfk_1;

