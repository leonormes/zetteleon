// Package interfaces defines the core abstractions for the ProdOS application.
// These interfaces enable dependency injection, testing, and loose coupling between components.
package interfaces

import (
	"context"

	"prodos/internal/model"
)

// WorkItemFetcher defines the interface for fetching work items from external sources.
type WorkItemFetcher interface {
	// FetchWorkItems retrieves work items from the source.
	// Returns an error if the fetch operation fails.
	FetchWorkItems(ctx context.Context) ([]model.WorkItem, error)
}

// WorkItemStore defines the interface for persisting and retrieving work items.
type WorkItemStore interface {
	// UpsertWorkItems inserts or updates work items in the store.
	UpsertWorkItems(ctx context.Context, items []model.WorkItem) error

	// GetAllWorkItems retrieves all work items from the store.
	GetAllWorkItems(ctx context.Context) ([]model.WorkItem, error)
}

// EmbeddingStore defines the interface for generating and storing embeddings.
type EmbeddingStore interface {
	// EmbedAndStore generates embeddings for work items and stores them.
	EmbedAndStore(ctx context.Context, items []model.WorkItem) error

	// Query searches for similar work items based on a query string.
	Query(ctx context.Context, query string, n int) ([]QueryResult, error)

	// Count returns the number of documents in the collection.
	Count(ctx context.Context) (int, error)
}

// QueryResult represents a single query result with similarity score.
type QueryResult struct {
	ID         string
	Content    string
	Similarity float32
	Metadata   map[string]string
}

// Config defines the interface for configuration management.
type Config interface {
	// Validate checks if the configuration is valid.
	Validate() error
}
