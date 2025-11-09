package client

import (
	"context"
	"fmt"
	"net/http"
	"time"

	"prodos/internal/config"
	"prodos/internal/model"
)

// JiraClient is a client for interacting with the Jira API.
type JiraClient struct {
	client *http.Client
	config config.JiraConfig
}

// NewJiraClient creates a new JiraClient.
func NewJiraClient(cfg config.JiraConfig) *JiraClient {
	return &JiraClient{
		client: &http.Client{Timeout: 10 * time.Second},
		config: cfg,
	}
}

// FetchWorkItems retrieves work items from Jira.
func (c *JiraClient) FetchWorkItems(ctx context.Context) ([]model.WorkItem, error) {
	// For now, this is a placeholder. In a real implementation, we would make an HTTP request
	// to the Jira API to fetch issues assigned to the user.
	fmt.Println("Fetching items from Jira...")

	// Placeholder data
	items := []model.WorkItem{
		{
			ID:        "PROJ-123",
			Source:    model.SourceJira,
			Title:     "Implement feature X",
			Status:    model.StatusInProgress,
			Project:   "Main Project",
			ProjectID: "10001",
			CreatedAt: time.Now().Add(-24 * time.Hour),
			UpdatedAt: time.Now(),
			Labels:    model.StringSlice{"bug", "backend"},
		},
	}

	fmt.Printf("Fetched %d items from Jira\n", len(items))
	return items, nil
}
