package model

import (
	"database/sql/driver"
	"encoding/json"
	"fmt"
	"time"
)

// StringSlice wraps []string to implement sql.Scanner and driver.Valuer for JSON storage.
type StringSlice []string

// Value implements driver.Valuer. It stores the slice as a JSON-encoded string.
func (s StringSlice) Value() (driver.Value, error) {
	if s == nil {
		return "[]", nil
	}
	b, err := json.Marshal([]string(s))
	if err != nil {
		return nil, err
	}
	return string(b), nil
}

// Scan implements sql.Scanner. It parses JSON stored in TEXT/BLOB into the slice.
func (s *StringSlice) Scan(value interface{}) error {
    if value == nil {
        *s = nil
        return nil
    }
    switch v := value.(type) {
    case []byte:
        var arr []string
        if err := json.Unmarshal(v, &arr); err != nil {
            return err
        }
        *s = arr
        return nil
    case string:
        var arr []string
        if err := json.Unmarshal([]byte(v), &arr); err != nil {
            return err
        }
        *s = arr
        return nil
    default:
        return fmt.Errorf("unsupported type for StringSlice Scan: %T", value)
    }
}

 // SourceType defines the origin of the work item (e.g., Jira, Todoist).
 type SourceType string

 const (
     SourceJira    SourceType = "jira"
     SourceTodoist SourceType = "todoist"
 )

 // Status represents the lifecycle stage of a work item.
 type Status string

 const (
     StatusOpen       Status = "open"
     StatusInProgress Status = "in_progress"
     StatusBlocked    Status = "blocked"
     StatusDone       Status = "done"
     StatusCanceled   Status = "canceled"
 )

 // WorkItem is a uniform data structure for tasks and issues from various sources.
 type WorkItem struct {
     ID          string     `db:"id" json:"id"`
     Source      SourceType `db:"source" json:"source"`
     Title       string     `db:"title" json:"title"`
     Description string     `db:"description" json:"description"`
     Status      Status     `db:"status" json:"status"`
     Project     string     `db:"project" json:"project"`
     ProjectID   string     `db:"project_id" json:"project_id"`
     URL         string     `db:"url" json:"url"`
     CreatedAt   time.Time  `db:"created_at" json:"created_at"`
     UpdatedAt   time.Time  `db:"updated_at" json:"updated_at"`
     DueAt       *time.Time `db:"due_at" json:"due_at"`
     CompletedAt *time.Time `db:"completed_at" json:"completed_at"`
     Priority    int        `db:"priority" json:"priority"`
     Labels      StringSlice `db:"labels" json:"labels"`
     Assignee    string     `db:"assignee" json:"assignee"`
     RawData     []byte     `db:"raw_data" json:"raw_data"`
     NoteCreated bool       `db:"note_created" json:"note_created"`
 }
