CREATE SCHEMA IF NOT EXISTS polytech;

SET search_path TO polytech, public;

CREATE INDEX IF NOT EXISTS idx_main_project_category ON main_project(category_id);
CREATE INDEX IF NOT EXISTS idx_main_project_created_at ON main_project(created_at);
CREATE INDEX IF NOT EXISTS idx_main_project_title ON main_project USING GIN(to_tsvector('russian', title));
CREATE INDEX IF NOT EXISTS idx_main_project_short_description ON main_project USING GIN(to_tsvector('russian', short_description));

DROP VIEW IF EXISTS project_with_category_view CASCADE;
CREATE VIEW project_with_category_view AS
SELECT 
    p.id,
    p.title,
    p.duration AS semesters,
    p.short_description,
    p.created_at,
    p.updated_at,
    c.name AS category_name
FROM main_project p
LEFT JOIN main_category c ON p.category_id = c.id;

CREATE OR REPLACE FUNCTION update_project_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trigger_update_project_timestamp ON main_project;
CREATE TRIGGER trigger_update_project_timestamp
BEFORE UPDATE ON main_project
FOR EACH ROW
EXECUTE FUNCTION update_project_timestamp();

INSERT INTO main_category (name) VALUES ('ИТ'), ('Дизайн'), ('Инженерия')
ON CONFLICT DO NOTHING;

INSERT INTO main_project (title, category_id, duration, short_description, created_at, updated_at)
VALUES 
    ('Проект 1', 1, 1, 'Описание проекта 1', '2025-05-01 00:00:00', '2025-05-01 00:00:00'),
    ('Проект 2', 2, 2, 'Описание проекта 2', '2025-04-15 00:00:00', '2025-04-15 00:00:00'),
    ('Проект 3', 3, 3, 'Описание проекта 3', '2025-05-30 00:00:00', '2025-05-30 00:00:00')
ON CONFLICT DO NOTHING;

INSERT INTO main_projectimage (project_id, image)
VALUES (1, 'projects/images/project1.jpg')
ON CONFLICT DO NOTHING;