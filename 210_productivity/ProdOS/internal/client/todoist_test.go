package client

import (
	"testing"
	"time"

	"prodos/internal/config"
	"prodos/internal/model"
)

func TestNewTodoistClient(t *testing.T) {
	cfg := config.TodoistConfig{
		APIToken: "test-token",
	}
	
	client := NewTodoistClient(cfg)
	
	if client == nil {
		t.Fatal("NewTodoistClient() returned nil")
	}
	
	if client.client == nil {
		t.Error("TodoistClient.client is nil")
	}
	
	if client.config.APIToken != cfg.APIToken {
		t.Errorf("config.APIToken = %v, want %v", client.config.APIToken, cfg.APIToken)
	}
}


func TestTransformTodoistTask(t *testing.T) {
	projects := map[string]string{
		"proj-1": "Test Project",
	}
	task := TodoistTask{
		ID:          "task-123",
		Content:     "Test Task",
		Description: "Task Description",
		ProjectID:   "proj-1",
		Priority:    4,
		Labels:      []string{"urgent", "bug"},
		IsCompleted: false,
		CreatedAt:   time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC),
		UpdatedAt:   time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC),
		Due: &TodoistDue{
			Date: "2024-01-15",
		},
	}
	
	item := transformTodoistTask(task, projects)
	
	if item.ID != "task-123" {
		t.Errorf("ID = %v, want %v", item.ID, "task-123")
	}
	
	if item.Source != model.SourceTodoist {
		t.Errorf("Source = %v, want %v", item.Source, model.SourceTodoist)
	}
	
	if item.Title != "Test Task" {
		t.Errorf("Title = %v, want %v", item.Title, "Test Task")
	}
	
	if item.Description != "Task Description" {
		t.Errorf("Description = %v, want %v", item.Description, "Task Description")
	}
	
	if item.Status != model.StatusOpen {
		t.Errorf("Status = %v, want %v", item.Status, model.StatusOpen)
	}
	
	if item.Project != "Test Project" {
		t.Errorf("Project = %v, want %v", item.Project, "Test Project")
	}
	
	if item.Priority != 4 {
		t.Errorf("Priority = %v, want %v", item.Priority, 4)
	}
	
	if len(item.Labels) != 2 {
		t.Errorf("Labels length = %d, want 2", len(item.Labels))
	}
	
	if item.DueAt == nil {
		t.Error("DueAt should be set when due date is set")
	}
}

func TestTransformTodoistTask_CompletedTask(t *testing.T) {
	task := TodoistTask{
		ID:          "task-123",
		Content:     "Completed Task",
		ProjectID:   "proj-1",
		IsCompleted: true,
		CreatedAt:   time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC),
		UpdatedAt:   time.Date(2024, 1, 10, 15, 30, 0, 0, time.UTC),
	}
	
	item := transformTodoistTask(task, nil)
	
	if item.Status != model.StatusDone {
		t.Errorf("Status = %v, want %v", item.Status, model.StatusDone)
	}
	
	// Note: The current implementation doesn't set CompletedAt
	// This would need to be added when we parse completed_at from the API response
	if item.CompletedAt != nil {
		t.Log("CompletedAt is set:", item.CompletedAt)
	}
}
