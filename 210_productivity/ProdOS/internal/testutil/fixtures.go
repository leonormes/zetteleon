// Package testutil provides testing utilities and fixtures for the ProdOS application.
package testutil

import (
	"time"

	"prodos/internal/model"
)

// NewTestWorkItem creates a test WorkItem with default values.
func NewTestWorkItem() model.WorkItem {
	return model.WorkItem{
		ID:          "test-123",
		Source:      model.SourceTodoist,
		Title:       "Test Task",
		Description: "This is a test task",
		Status:      model.StatusOpen,
		Project:     "Test Project",
		ProjectID:   "proj-123",
		URL:         "https://example.com",
		CreatedAt:   time.Now().Add(-24 * time.Hour),
		UpdatedAt:   time.Now(),
		Priority:    3,
		Labels:      model.StringSlice{"test", "unit"},
	}
}

// NewTestWorkItemWithID creates a test WorkItem with a specific ID.
func NewTestWorkItemWithID(id string, source model.SourceType) model.WorkItem {
	item := NewTestWorkItem()
	item.ID = id
	item.Source = source
	return item
}

// NewTestWorkItems creates a slice of test WorkItems.
func NewTestWorkItems(count int) []model.WorkItem {
	items := make([]model.WorkItem, count)
	for i := 0; i < count; i++ {
		items[i] = NewTestWorkItemWithID(
			string(rune('A'+i)),
			model.SourceTodoist,
		)
	}
	return items
}
