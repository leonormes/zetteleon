package embedding

import (
	"context"
	"fmt"
	"os"
	"path/filepath"
	"strings"

	"github.com/philippgille/chromem-go"
	"prodos/internal/model"
)

// ChromaClient manages the connection to ChromaDB
type ChromaClient struct {
	db *chromem.DB
}

// NewChromaClient creates a new client and ensures the collection exists
func NewChromaClient() (*ChromaClient, error) {
	home, err := os.UserHomeDir()
	if err != nil {
		return nil, fmt.Errorf("could not get user home directory: %w", err)
	}
	// chromem.NewPersistentDB expects a directory path, not a file path
	dbPath := filepath.Join(home, ".prodos", "chromadb")

	db, err := chromem.NewPersistentDB(dbPath)
	if err != nil {
		return nil, fmt.Errorf("could not create persistent db: %w", err)
	}
	return &ChromaClient{db: db}, nil
}

// EmbedAndStore generates embeddings for a slice of WorkItems and upserts them
func (c *ChromaClient) EmbedAndStore(ctx context.Context, items []model.WorkItem) error {
	if len(items) == 0 {
		return nil
	}

	embeddingFunc := chromem.NewEmbeddingFuncOpenAI(os.Getenv("OPENAI_API_KEY"), chromem.EmbeddingModelOpenAI3Small)

	collection, err := c.db.GetOrCreateCollection("work_items", nil, embeddingFunc)
	if err != nil {
		return fmt.Errorf("failed to get or create collection: %w", err)
	}
	
	documents := make([]chromem.Document, len(items))
	for i, item := range items {
		metadata := make(map[string]string)
		metadata["source"] = string(item.Source)
		metadata["project_id"] = item.ProjectID
		metadata["status"] = string(item.Status)

		documents[i] = chromem.Document{
			ID:       string(item.Source) + "-" + item.ID,
			Content:  itemToDocument(item),
			Metadata: metadata,
		}
	}

	return collection.AddDocuments(context.Background(), documents, 10) // Using 10 concurrent requests
}

// itemToDocument converts a WorkItem into a text document for embedding
// Count returns the number of documents in the collection.
func (c *ChromaClient) Count(ctx context.Context) (int, error) {
	embeddingFunc := chromem.NewEmbeddingFuncOpenAI(os.Getenv("OPENAI_API_KEY"), chromem.EmbeddingModelOpenAI3Small)

	collection, err := c.db.GetOrCreateCollection("work_items", nil, embeddingFunc)
	if err != nil {
		return 0, fmt.Errorf("failed to get or create collection: %w", err)
	}
	return collection.Count(), nil
}

// Query finds work items similar to the query string.
func (c *ChromaClient) Query(ctx context.Context, query string, n int) ([]chromem.Result, error) {
	embeddingFunc := chromem.NewEmbeddingFuncOpenAI(os.Getenv("OPENAI_API_KEY"), chromem.EmbeddingModelOpenAI3Small)

	collection, err := c.db.GetOrCreateCollection("work_items", nil, embeddingFunc)
	if err != nil {
		return nil, fmt.Errorf("failed to get or create collection: %w", err)
	}
	return collection.Query(context.Background(), query, n, nil, nil)
}

func itemToDocument(item model.WorkItem) string {
	var builder strings.Builder
	builder.WriteString(fmt.Sprintf("Title: %s\n", item.Title))
	if item.Description != "" {
		builder.WriteString(fmt.Sprintf("Description: %s\n", item.Description))
	}
	builder.WriteString(fmt.Sprintf("Status: %s\n", item.Status))
	if item.Project != "" {
		builder.WriteString(fmt.Sprintf("Project: %s\n", item.Project))
	}
	if len(item.Labels) > 0 {
		builder.WriteString(fmt.Sprintf("Labels: %s\n", strings.Join(item.Labels, ", ")))
	}
	return builder.String()
}
