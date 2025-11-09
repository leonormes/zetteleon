package database

import (
	"context"
	"fmt"
	"os"
	"path/filepath"

	"prodos/internal/model"

	"github.com/jmoiron/sqlx"
	_ "github.com/mattn/go-sqlite3"
)

// DB represents the database connection.
type DB struct {
	*sqlx.DB
}

// InitDB initializes the database connection and runs migrations.
func InitDB() (*DB, error) {
	home, err := os.UserHomeDir()
	if err != nil {
		return nil, fmt.Errorf("could not get user home directory: %w", err)
	}

	dbPath := filepath.Join(home, ".prodos", "work.db")
	if err := os.MkdirAll(filepath.Dir(dbPath), 0755); err != nil {
		return nil, fmt.Errorf("could not create database directory: %w", err)
	}

	db, err := sqlx.Connect("sqlite3", dbPath)
	if err != nil {
		return nil, fmt.Errorf("could not connect to database: %w", err)
	}

	if err := runMigrations(db); err != nil {
		return nil, fmt.Errorf("could not run migrations: %w", err)
	}

	return &DB{db}, nil
}

// runMigrations creates the necessary tables in the database.
func runMigrations(db *sqlx.DB) error {
	schema := `
	CREATE TABLE IF NOT EXISTS work_items (
		id TEXT NOT NULL,
		source TEXT NOT NULL,
		title TEXT NOT NULL,
		description TEXT,
		status TEXT NOT NULL,
		project TEXT,
		project_id TEXT,
		url TEXT,
		created_at DATETIME NOT NULL,
		updated_at DATETIME NOT NULL,
		due_at DATETIME,
		completed_at DATETIME,
		priority INTEGER,
		labels TEXT,
		assignee TEXT,
		raw_data BLOB,
		note_created BOOLEAN DEFAULT FALSE,
		PRIMARY KEY (id, source)
	);
	`
	_, err := db.Exec(schema)
	return err
}

// UpsertWorkItems inserts or updates a slice of work items in the database.
func (db *DB) UpsertWorkItems(ctx context.Context, items []model.WorkItem) error {
	if len(items) == 0 {
		return nil
	}

	txn, err := db.BeginTxx(ctx, nil)
	if err != nil {
		return err
	}
	defer txn.Rollback()

	stmt, err := txn.PrepareNamed(`
		INSERT OR REPLACE INTO work_items (id, source, title, description, status, project, project_id, url, created_at, updated_at, due_at, completed_at, priority, labels, assignee, raw_data, note_created)
		VALUES (:id, :source, :title, :description, :status, :project, :project_id, :url, :created_at, :updated_at, :due_at, :completed_at, :priority, :labels, :assignee, :raw_data, :note_created)
	`)
	if err != nil {
		return err
	}

	for _, item := range items {
		_, err := stmt.Exec(struct {
			model.WorkItem
			Labels model.StringSlice `db:"labels"`
		}{
			WorkItem: item,
			Labels:   item.Labels,
		})
		if err != nil {
			return fmt.Errorf("could not insert work item %s: %w", item.ID, err)
		}
	}

	return txn.Commit()
}

// GetAllWorkItems retrieves all work items from the database.
func (db *DB) GetAllWorkItems(ctx context.Context) ([]model.WorkItem, error) {
	var items []model.WorkItem
	err := db.SelectContext(ctx, &items, "SELECT * FROM work_items")
	if err != nil {
		return nil, fmt.Errorf("could not get all work items: %w", err)
	}
	return items, nil
}

// GetUnnotedWorkItems retrieves all work items from the database where note_created is false.
func (db *DB) GetUnnotedWorkItems(ctx context.Context) ([]model.WorkItem, error) {
	var items []model.WorkItem
	err := db.SelectContext(ctx, &items, "SELECT * FROM work_items WHERE note_created = FALSE")
	if err != nil {
		return nil, fmt.Errorf("could not get unnoted work items: %w", err)
	}
	return items, nil
}

// SetNoteCreated marks a work item as having a note created.
func (db *DB) SetNoteCreated(ctx context.Context, source model.SourceType, id string) error {
	_, err := db.ExecContext(ctx, "UPDATE work_items SET note_created = TRUE WHERE source = ? AND id = ?", source, id)
	if err != nil {
		return fmt.Errorf("could not set note created for %s-%s: %w", source, id, err)
	}
	return nil
}
