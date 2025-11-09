package database

import (
	"context"
	"os"
	"path/filepath"
	"testing"
	"time"

	"prodos/internal/model"
)

func setupTestDB(t *testing.T) *DB {
	tmpDir := t.TempDir()
	
	// Temporarily override home directory
	oldHome := os.Getenv("HOME")
	os.Setenv("HOME", tmpDir)
	t.Cleanup(func() {
		os.Setenv("HOME", oldHome)
	})
	
	// Create .prodos directory
	prodosDir := filepath.Join(tmpDir, ".prodos")
	if err := os.MkdirAll(prodosDir, 0755); err != nil {
		t.Fatalf("Failed to create prodos dir: %v", err)
	}
	
	db, err := InitDB()
	if err != nil {
		t.Fatalf("Failed to initialize test database: %v", err)
	}
	
	return db
}

func TestInitDB(t *testing.T) {
	db := setupTestDB(t)
	
	if db == nil {
		t.Fatal("InitDB() returned nil")
	}
	
	// Verify table exists
	var tableName string
	err := db.Get(&tableName, "SELECT name FROM sqlite_master WHERE type='table' AND name='work_items'")
	if err != nil {
		t.Errorf("work_items table not created: %v", err)
	}
}

func TestDB_UpsertWorkItems(t *testing.T) {
	db := setupTestDB(t)
	ctx := context.Background()
	
	items := []model.WorkItem{
		{
			ID:          "test-1",
			Source:      model.SourceTodoist,
			Title:       "Test Task 1",
			Description: "Description 1",
			Status:      model.StatusOpen,
			Project:     "Project A",
			ProjectID:   "proj-1",
			CreatedAt:   time.Now(),
			UpdatedAt:   time.Now(),
			Labels:      model.StringSlice{"label1", "label2"},
		},
		{
			ID:          "test-2",
			Source:      model.SourceJira,
			Title:       "Test Task 2",
			Description: "Description 2",
			Status:      model.StatusInProgress,
			Project:     "Project B",
			ProjectID:   "proj-2",
			CreatedAt:   time.Now(),
			UpdatedAt:   time.Now(),
			Labels:      model.StringSlice{"label3"},
		},
	}
	
	err := db.UpsertWorkItems(ctx, items)
	if err != nil {
		t.Fatalf("UpsertWorkItems() error = %v", err)
	}
	
	// Verify items were inserted
	var count int
	err = db.Get(&count, "SELECT COUNT(*) FROM work_items")
	if err != nil {
		t.Fatalf("Failed to count items: %v", err)
	}
	
	if count != 2 {
		t.Errorf("Expected 2 items, got %d", count)
	}
}

func TestDB_UpsertWorkItems_Update(t *testing.T) {
	db := setupTestDB(t)
	ctx := context.Background()
	
	// Insert initial item
	items := []model.WorkItem{
		{
			ID:          "test-1",
			Source:      model.SourceTodoist,
			Title:       "Original Title",
			Description: "Original Description",
			Status:      model.StatusOpen,
			Project:     "Project A",
			ProjectID:   "proj-1",
			CreatedAt:   time.Now(),
			UpdatedAt:   time.Now(),
		},
	}
	
	err := db.UpsertWorkItems(ctx, items)
	if err != nil {
		t.Fatalf("Initial UpsertWorkItems() error = %v", err)
	}
	
	// Update the item
	items[0].Title = "Updated Title"
	items[0].Description = "Updated Description"
	items[0].Status = model.StatusDone
	
	err = db.UpsertWorkItems(ctx, items)
	if err != nil {
		t.Fatalf("Update UpsertWorkItems() error = %v", err)
	}
	
	// Verify update
	var item model.WorkItem
	err = db.Get(&item, "SELECT * FROM work_items WHERE id = ? AND source = ?", "test-1", model.SourceTodoist)
	if err != nil {
		t.Fatalf("Failed to get item: %v", err)
	}
	
	if item.Title != "Updated Title" {
		t.Errorf("Title = %v, want %v", item.Title, "Updated Title")
	}
	
	if item.Description != "Updated Description" {
		t.Errorf("Description = %v, want %v", item.Description, "Updated Description")
	}
	
	if item.Status != model.StatusDone {
		t.Errorf("Status = %v, want %v", item.Status, model.StatusDone)
	}
	
	// Verify only one item exists
	var count int
	err = db.Get(&count, "SELECT COUNT(*) FROM work_items")
	if err != nil {
		t.Fatalf("Failed to count items: %v", err)
	}
	
	if count != 1 {
		t.Errorf("Expected 1 item after update, got %d", count)
	}
}

func TestDB_GetAllWorkItems(t *testing.T) {
	db := setupTestDB(t)
	ctx := context.Background()
	
	// Insert test items
	items := []model.WorkItem{
		{
			ID:        "test-1",
			Source:    model.SourceTodoist,
			Title:     "Task 1",
			Status:    model.StatusOpen,
			ProjectID: "proj-1",
			CreatedAt: time.Now(),
			UpdatedAt: time.Now(),
		},
		{
			ID:        "test-2",
			Source:    model.SourceJira,
			Title:     "Task 2",
			Status:    model.StatusInProgress,
			ProjectID: "proj-2",
			CreatedAt: time.Now(),
			UpdatedAt: time.Now(),
		},
	}
	
	err := db.UpsertWorkItems(ctx, items)
	if err != nil {
		t.Fatalf("UpsertWorkItems() error = %v", err)
	}
	
	// Get all items
	retrieved, err := db.GetAllWorkItems(ctx)
	if err != nil {
		t.Fatalf("GetAllWorkItems() error = %v", err)
	}
	
	if len(retrieved) != 2 {
		t.Errorf("Expected 2 items, got %d", len(retrieved))
	}
	
	// Verify items match
	for i, item := range retrieved {
		if item.ID != items[i].ID {
			t.Errorf("Item[%d].ID = %v, want %v", i, item.ID, items[i].ID)
		}
		if item.Title != items[i].Title {
			t.Errorf("Item[%d].Title = %v, want %v", i, item.Title, items[i].Title)
		}
		if item.Source != items[i].Source {
			t.Errorf("Item[%d].Source = %v, want %v", i, item.Source, items[i].Source)
		}
	}
}

func TestDB_UpsertWorkItems_EmptySlice(t *testing.T) {
	db := setupTestDB(t)
	ctx := context.Background()
	
	err := db.UpsertWorkItems(ctx, []model.WorkItem{})
	if err != nil {
		t.Errorf("UpsertWorkItems() with empty slice should not error, got %v", err)
	}
}

func TestDB_GetAllWorkItems_Empty(t *testing.T) {
	db := setupTestDB(t)
	ctx := context.Background()
	
	items, err := db.GetAllWorkItems(ctx)
	if err != nil {
		t.Fatalf("GetAllWorkItems() error = %v", err)
	}
	
	if len(items) != 0 {
		t.Errorf("Expected 0 items from empty database, got %d", len(items))
	}
}
