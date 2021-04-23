CREATE DATABASE minio_ecg;
CREATE USER ecg_admin WITH PASSWORD '?zfQn[{wp;<%3MKq';
ALTER ROLE admin SET client_encoding TO 'utf8';
ALTER ROLE ecg_admin SET default_transaction_isolation TO 'read committed';
ALTER ROLE ecg_admin SET timezone TO 'Europe/Moscow';
GRANT ALL PRIVILEGES ON DATABASE minio_ecg TO ecg_admin;