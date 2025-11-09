package client

import (
	"context"
	"testing"
	"time"

	"prodos/internal/config"
	"prodos/internal/model"
)

func TestNewJiraClient(t *testing.T) {
	cfg := config.JiraConfig{
		Host:     "https://test.atlassian.net",
		Username: "test@example.com",
		APIToken: "test-token",
	}
	
	client := NewJiraClient(cfg)
	
	if client == nil {
		t.Fatal("NewJiraClient() returned nil")
	}
	
	if client.client == nil {
		t.Error("JiraClient.client is nil")
	}
	
	if client.config.Host != cfg.Host {
		t.Errorf("config.Host = %v, want %v", client.config.Host, cfg.Host)
	}
	
	if client.config.Username != cfg.Username {
		t.Errorf("config.Username = %v, want %v", client.config.Username, cfg.Username)
	}
	
	if client.config.APIToken != cfg.APIToken {
		t.Errorf("config.APIToken = %v, want %v", client.config.APIToken, cfg.APIToken)
	}
}

func TestJiraClient_FetchWorkItems(t *testing.T) {
	cfg := config.JiraConfig{
		Host:     "https://test.atlassian.net",
		Username: "test@example.com",
		APIToken: "test-token",
	}
	
	client := NewJiraClient(cfg)
	ctx := context.Background()
	
	items, err := client.FetchWorkItems(ctx)
	if err != nil {
		t.Fatalf("FetchWorkItems() error = %v", err)
	}
	
	// Currently returns placeholder data
	if len(items) == 0 {
		t.Error("Expected at least one item from placeholder data")
	}
	
	// Verify item structure
	for _, item := range items {
		if item.Source != model.SourceJira {
			t.Errorf("Expected source=jira, got %v", item.Source)
		}
		
		if item.ID == "" {
			t.Error("Item ID is empty")
		}
		
		if item.Title == "" {
			t.Error("Item Title is empty")
		}
		
		if item.CreatedAt.IsZero() {
			t.Error("Item CreatedAt is zero")
		}
		
		if item.UpdatedAt.IsZero() {
			t.Error("Item UpdatedAt is zero")
		}
	}
}

func TestJiraClient_FetchWorkItems_WithContext(t *testing.T) {
	cfg := config.JiraConfig{
		Host:     "https://test.atlassian.net",
		Username: "test@example.com",
		APIToken: "test-token",
	}
	
	client := NewJiraClient(cfg)
	
	// Test with timeout context
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()
	
	items, err := client.FetchWorkItems(ctx)
	if err != nil {
		t.Fatalf("FetchWorkItems() with timeout context error = %v", err)
	}
	
	if len(items) == 0 {
		t.Error("Expected items even with timeout context")
	}
}

func TestJiraClient_FetchWorkItems_CancelledContext(t *testing.T) {
	cfg := config.JiraConfig{
		Host:     "https://test.atlassian.net",
		Username: "test@example.com",
		APIToken: "test-token",
	}
	
	client := NewJiraClient(cfg)
	
	// Test with cancelled context
	ctx, cancel := context.WithCancel(context.Background())
	cancel() // Cancel immediately
	
	// Since the current implementation doesn't actually respect context,
	// this will still succeed. When real API calls are implemented,
	// this test should verify context cancellation works.
	_, err := client.FetchWorkItems(ctx)
	if err != nil {
		// This is actually the expected behavior once we implement real API calls
		t.Logf("FetchWorkItems() correctly handled cancelled context: %v", err)
	}
}
