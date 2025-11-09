package notes

import (
	"bytes"
	"context"
	"fmt"
	"os"
	"path/filepath"

	"prodos/internal/client"
	"prodos/internal/config"
	"prodos/internal/database"
	"prodos/internal/model"

	"github.com/adrg/frontmatter"
)

// Syncer handles the synchronization of work items to Obsidian notes.
type Syncer struct {
	db           *database.DB
	cfg          *config.Config
	todoistClient *client.TodoistClient
}

// NewSyncer creates a new Syncer.
func NewSyncer(db *database.DB, cfg *config.Config, todoistClient *client.TodoistClient) *Syncer {
	return &Syncer{db: db, cfg: cfg, todoistClient: todoistClient}
}

// Sync creates Obsidian notes for any work items that don't have one yet.
func (s *Syncer) Sync(ctx context.Context) error {
	fmt.Println("Fetching un-noted work items...")
	items, err := s.db.GetUnnotedWorkItems(ctx)
	if err != nil {
		return fmt.Errorf("could not get unnoted work items: %w", err)
	}

	if len(items) == 0 {
		fmt.Println("No new work items to create notes for.")
		return nil
	}

	fmt.Printf("Found %d new work items to create notes for.\n", len(items))

	absInboxPath := filepath.Join(s.cfg.GTD.VaultRoot, s.cfg.GTD.InboxPath)

	for _, item := range items {
		if err := s.createNoteForItem(ctx, item, absInboxPath); err != nil {
			return fmt.Errorf("could not create note for item %s: %w", item.ID, err)
		}

		if err := s.db.SetNoteCreated(ctx, item.Source, item.ID); err != nil {
			return fmt.Errorf("could not set note created for item %s: %w", item.ID, err)
		}

		fmt.Printf("Created note for work item: %s\n", item.Title)
	}

	return nil
}

func (s *Syncer) createNoteForItem(ctx context.Context, item model.WorkItem, inboxPath string) error {
	noteFilename := item.Title + ".md"
	absNotePath := filepath.Join(inboxPath, noteFilename)

	// Use a multi-line string for readability and to avoid escaping issues
	frontmatterContent := fmt.Sprintf(`---
source: %s
id: %s
---

# %s

%s`, item.Source, item.ID, item.Title, item.Description)

	return os.WriteFile(absNotePath, []byte(frontmatterContent), 0644)
}

// LocalNote represents the frontmatter of a local note.
type LocalNote struct {
	Source string `yaml:"source"`
	ID     string `yaml:"id"`
}

// Prune handles the deletion of notes.
func (s *Syncer) Prune(ctx context.Context) error {
	fmt.Println("Pruning deleted notes...")

	trashPath := filepath.Join(s.cfg.GTD.VaultRoot, s.cfg.GTD.InboxPath, ".trash")
	if err := os.MkdirAll(trashPath, 0755); err != nil {
		return fmt.Errorf("could not create trash directory: %w", err)
	}

	files, err := os.ReadDir(trashPath)
	if err != nil {
		return fmt.Errorf("could not read trash directory: %w", err)
	}

	if len(files) == 0 {
		fmt.Println("No notes to prune.")
		return nil
	}

	for _, file := range files {
		if file.IsDir() {
			continue
		}

		filePath := filepath.Join(trashPath, file.Name())
		content, err := os.ReadFile(filePath)
		if err != nil {
			fmt.Printf("WARN: could not read file %s: %v\n", filePath, err)
			continue
		}

		var note LocalNote
		_, err = frontmatter.Parse(bytes.NewReader(content), &note)
		if err != nil {
			fmt.Printf("WARN: could not parse frontmatter for %s: %v\n", file.Name(), err)
			continue
		}

		if note.Source == string(model.SourceTodoist) {
			fmt.Printf("Deleting Todoist task %s...\n", note.ID)
			if err := s.todoistClient.DeleteTask(ctx, note.ID); err != nil {
				fmt.Printf("WARN: could not delete todoist task %s: %v\n", note.ID, err)
			}
		}

		if err := os.Remove(filePath); err != nil {
			fmt.Printf("WARN: could not delete note %s: %v\n", filePath, err)
		}
	}

	return nil
}
