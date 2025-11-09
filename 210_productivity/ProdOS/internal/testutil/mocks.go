package testutil

import (
	"context"

	"prodos/internal/interfaces"
	"prodos/internal/model"
)

// MockWorkItemFetcher is a mock implementation of WorkItemFetcher.
type MockWorkItemFetcher struct {
	FetchFunc func(ctx context.Context) ([]model.WorkItem, error)
}

func (m *MockWorkItemFetcher) FetchWorkItems(ctx context.Context) ([]model.WorkItem, error) {
	if m.FetchFunc != nil {
		return m.FetchFunc(ctx)
	}
	return NewTestWorkItems(3), nil
}

// MockWorkItemStore is a mock implementation of WorkItemStore.
type MockWorkItemStore struct {
	UpsertFunc      func(ctx context.Context, items []model.WorkItem) error
	GetAllFunc      func(ctx context.Context) ([]model.WorkItem, error)
	StoredItems     []model.WorkItem
}

func (m *MockWorkItemStore) UpsertWorkItems(ctx context.Context, items []model.WorkItem) error {
	if m.UpsertFunc != nil {
		return m.UpsertFunc(ctx, items)
	}
	m.StoredItems = append(m.StoredItems, items...)
	return nil
}

func (m *MockWorkItemStore) GetAllWorkItems(ctx context.Context) ([]model.WorkItem, error) {
	if m.GetAllFunc != nil {
		return m.GetAllFunc(ctx)
	}
	return m.StoredItems, nil
}

// MockEmbeddingStore is a mock implementation of EmbeddingStore.
type MockEmbeddingStore struct {
	EmbedFunc func(ctx context.Context, items []model.WorkItem) error
	QueryFunc func(ctx context.Context, query string, n int) ([]interfaces.QueryResult, error)
	CountFunc func(ctx context.Context) (int, error)
	ItemCount int
}

func (m *MockEmbeddingStore) EmbedAndStore(ctx context.Context, items []model.WorkItem) error {
	if m.EmbedFunc != nil {
		return m.EmbedFunc(ctx, items)
	}
	m.ItemCount = len(items)
	return nil
}

func (m *MockEmbeddingStore) Query(ctx context.Context, query string, n int) ([]interfaces.QueryResult, error) {
	if m.QueryFunc != nil {
		return m.QueryFunc(ctx, query, n)
	}
	return []interfaces.QueryResult{
		{
			ID:         "test-1",
			Content:    "Test content",
			Similarity: 0.95,
			Metadata:   map[string]string{"source": "todoist"},
		},
	}, nil
}

func (m *MockEmbeddingStore) Count(ctx context.Context) (int, error) {
	if m.CountFunc != nil {
		return m.CountFunc(ctx)
	}
	return m.ItemCount, nil
}
