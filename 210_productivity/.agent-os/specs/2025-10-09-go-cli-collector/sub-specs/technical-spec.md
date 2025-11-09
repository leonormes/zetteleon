# Technical Specification

This is the technical specification for the spec detailed in @.agent-os/specs/2025-10-09-go-cli-collector/spec.md

## Technical Requirements

1. **Go Version**: Go 1.21+
2. **Configuration**: API keys and endpoint URLs for Jira and Todoist will be managed via a YAML configuration file located at `~/.config/prodos/collector.yaml`.
3. **Database**: A local SQLite database will be used. The database file will be located at `~/.prodos/work.db`. The schema will be managed using `golang-migrate`.
4. **API Clients**: Standard `net/http` library for API calls. No heavy third-party frameworks.
5. **Data Model**: The canonical `WorkItem` struct will be the central data structure.

### `WorkItem` Struct Definition

```go
package collector

import "time"

// SourceType defines the origin of the work item (e.g., Jira, Todoist).
type SourceType string

const (
 SourceJira    SourceType = "jira"
 SourceTodoist SourceType = "todoist"
)

// Status represents the lifecycle stage of a work item.
type Status string

const (
 StatusOpen      Status = "open"
 StatusInProgress Status = "in_progress"
 StatusBlocked   Status = "blocked"
 StatusDone      Status = "done"
 StatusCanceled  Status = "canceled"
)

// WorkItem is a uniform data structure for tasks and issues from various sources.
type WorkItem struct {
 ID          string     `json:"id"`           // Unique identifier in the source system (e.g., "PROJ-123" or "12345678")
 Source      SourceType `json:"source"`       // The originating system (jira, todoist)
 Title       string     `json:"title"`        // The main title or summary of the item
 Description string     `json:"description"`  // Detailed description (can be markdown)
 Status      Status     `json:"status"`       // Normalized status
 Project     string     `json:"project"`      // Name of the project it belongs to
 ProjectID   string     `json:"project_id"`   // ID of the project in the source system
 URL         string     `json:"url"`          // Direct link to the item in the source system
 CreatedAt   time.Time  `json:"created_at"`   // When the item was created
 UpdatedAt   time.Time  `json:"updated_at"`   // When the item was last modified
 DueAt       *time.Time `json:"due_at"`       // Optional due date
 CompletedAt *time.Time `json:"completed_at"` // Optional completion date
 Priority    int        `json:"priority"`     // Normalized priority (e.g., 1-4)
 Labels      []string   `json:"labels"`       // Associated tags or labels
 Assignee    string     `json:"assignee"`     // Who the item is assigned to
 RawData     []byte     `json:"raw_data"`     // The original JSON payload from the source API
}
```

## External Dependencies

- **`github.com/spf13/cobra`**: For building the CLI command structure (`sync`).
- **`github.com/jmoiron/sqlx`**: For interacting with the SQLite database.
- **`github.com/mattn/go-sqlite3`**: SQLite driver for Go.
- **`gopkg.in/yaml.v3`**: For parsing the configuration file.
