-- Active: 1759892781881@@localhost@3306@tarea2
-- Crear usuario
CREATE USER 'cc5002'@'localhost' IDENTIFIED BY 'cc5002';

GRANT ALL ON 'tarea2'.* TO 'cc5002'@'localhost';

-- Eliminar usuario de ser necesario
DROP USER 'cc5002'@'localhost';
