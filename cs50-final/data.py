import sqlite3
import os

os.makedirs("databases", exist_ok=True)

# ── Auth Database ─────────────────────────────────────────────
with sqlite3.connect("databases/auth.db") as conn:
    conn.executescript("""
    
        CREATE TABLE IF NOT EXISTS users (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            email    TEXT    NOT NULL UNIQUE,
            password TEXT    NOT NULL,
            status   INTEGER NOT NULL CHECK(status BETWEEN 1 AND 7),
            state    INTEGER DEFAULT 1
        );
        CREATE TABLE IF NOT EXISTS moderation_log (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    actor_p_id  INTEGER NOT NULL REFERENCES profiles(p_id),
    target_p_id INTEGER NOT NULL REFERENCES profiles(p_id),
    action      TEXT NOT NULL CHECK(action IN ('warn','restrict','ban','unban')),
    reason      TEXT,
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
);
    """)
    print("auth.db created successfully")


# ── Main Database ─────────────────────────────────────────────
with sqlite3.connect("databases/main.db") as conn:
    conn.executescript("""
                       CREATE TABLE IF NOT EXISTS student_notes (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    p_id       INTEGER NOT NULL REFERENCES profiles(p_id),
    subject_id INTEGER REFERENCES subjects(id),
    content    TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS student_favorites (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    p_id        INTEGER NOT NULL REFERENCES profiles(p_id),
    entity_type TEXT NOT NULL CHECK(entity_type IN (
                    'subject', 'material', 'professor', 'assignment'
                )),
    entity_id   INTEGER NOT NULL,
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(p_id, entity_type, entity_id)
);

CREATE TABLE IF NOT EXISTS history (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    p_id        INTEGER NOT NULL REFERENCES profiles(p_id),
    entity_type TEXT NOT NULL CHECK(entity_type IN (
                    'subject', 'material', 'assignment'
                )),
    entity_id   INTEGER NOT NULL,
    visited_at  DATETIME DEFAULT CURRENT_TIMESTAMP
);
                       CREATE INDEX idx_student_subjects_pid ON student_subjects(p_id);
CREATE INDEX idx_ratings_entity ON ratings(entity_type, entity_id);
CREATE INDEX idx_materials_subject ON materials(subject_id);
CREATE INDEX idx_grades_pid ON student_grades(p_id);
CREATE INDEX idx_notes_pid ON student_notes(p_id);
CREATE INDEX idx_favorites_pid ON student_favorites(p_id);

        CREATE TABLE IF NOT EXISTS users (
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            email   TEXT    NOT NULL UNIQUE,
            p_id    INTEGER,
            status  INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS profiles (
            p_id    INTEGER PRIMARY KEY AUTOINCREMENT,
            email   TEXT    NOT NULL UNIQUE,
            name    TEXT,
            bio     TEXT,
            avatar  TEXT
        );

        CREATE TABLE IF NOT EXISTS student_subjects (
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            p_id    INTEGER NOT NULL REFERENCES profiles(p_id),
            sub_id  INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS years (
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            label   TEXT    NOT NULL UNIQUE
        );

        CREATE TABLE IF NOT EXISTS semesters (
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            year_id INTEGER NOT NULL REFERENCES years(id),
            name    TEXT    NOT NULL
        );

        CREATE TABLE IF NOT EXISTS subjects (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            code        TEXT    NOT NULL UNIQUE,
            name        TEXT    NOT NULL,
            description TEXT,
            semester_id INTEGER NOT NULL REFERENCES semesters(id)
        );

        CREATE TABLE IF NOT EXISTS professor_subjects (
            professor_id INTEGER NOT NULL REFERENCES users(id),
            subject_id   INTEGER NOT NULL REFERENCES subjects(id),
            semester_id  INTEGER NOT NULL REFERENCES semesters(id),
            PRIMARY KEY (professor_id, subject_id, semester_id)
        );

        CREATE TABLE IF NOT EXISTS materials (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            subject_id   INTEGER NOT NULL REFERENCES subjects(id),
            uploaded_by  INTEGER NOT NULL REFERENCES users(id),
            title        TEXT    NOT NULL,
            file_path    TEXT,
            content_type TEXT    NOT NULL CHECK(content_type IN (
                             'official',
                             'revision',
                             'final_revision',
                             'student_summary',
                             'public'
                         )),
            visibility   TEXT    NOT NULL DEFAULT 'public' CHECK(visibility IN ('public','private')),
            created_at   DATETIME DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS assignments (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            subject_id  INTEGER NOT NULL REFERENCES subjects(id),
            semester_id INTEGER NOT NULL REFERENCES semesters(id),
            title       TEXT    NOT NULL,
            description TEXT,
            visibility  TEXT    NOT NULL DEFAULT 'public' CHECK(visibility IN ('public','private')),
            created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS student_grades (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            p_id        INTEGER NOT NULL REFERENCES profiles(p_id),
            subject_id  INTEGER NOT NULL REFERENCES subjects(id),
            semester_id INTEGER NOT NULL REFERENCES semesters(id),
            grade       REAL    NOT NULL CHECK(grade BETWEEN 0.0 AND 4.0),
            UNIQUE(p_id, subject_id, semester_id)
        );

        CREATE TABLE IF NOT EXISTS ratings (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            p_id        INTEGER NOT NULL REFERENCES profiles(p_id),
            entity_type TEXT    NOT NULL CHECK(entity_type IN (
                            'subject',
                            'material',
                            'assignment',
                            'semester',
                            'year',
                            'professor'
                        )),
            entity_id   INTEGER NOT NULL,
            raw_score   INTEGER NOT NULL CHECK(raw_score BETWEEN 1 AND 5),
            difficulty  INTEGER CHECK(difficulty BETWEEN 1 AND 5),
            gpa_at_vote REAL,
            created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(p_id, entity_type, entity_id)
        );
                       CREATE TABLE student_material_progress (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    p_id        INTEGER NOT NULL REFERENCES profiles(p_id),
    material_id INTEGER NOT NULL REFERENCES materials(id),
    progress    TEXT,
    last_position INTEGER DEFAULT 0,
    last_visited DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(p_id, material_id)
);

    """)
    
    
    print("main.db created successfully")

print("All databases ready.")