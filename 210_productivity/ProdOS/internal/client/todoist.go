package client

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
	"net/url"
	"strings"
	"time"

	"prodos/internal/config"
	"prodos/internal/model"
)

const todoistAPI = "https://api.todoist.com/sync/v9/sync"

// --- API Response Structs ---
type TodoistSyncResponse struct {
	Items    []TodoistTask    `json:"items"`
	Projects []TodoistProject `json:"projects"`
}

type TodoistTask struct {
	ID          string      `json:"id"`
	Content     string      `json:"content"`
	Description string      `json:"description"`
	ProjectID   string      `json:"project_id"`
	Priority    int         `json:"priority"`
	Due         *TodoistDue `json:"due"`
	Labels      []string    `json:"labels"`
	URL         string      `json:"url"`
	ResponsibleUID *string  `json:"responsible_uid"`
	IsCompleted bool        `json:"checked"`
	CreatedAt   time.Time   `json:"added_at"`
	UpdatedAt   time.Time   `json:"updated_at"`
}

type TodoistProject struct {
	ID   string `json:"id"`
	Name string `json:"name"`
}

type TodoistDue struct {
	Date      string `json:"date"`
	IsRecurring bool   `json:"is_recurring"`
	Datetime  string `json:"datetime"`
	String    string `json:"string"`
	Timezone  string `json:"timezone"`
}

type TodoistErrorResponse struct {
	Error      string `json:"error"`
	ErrorCode  int    `json:"error_code"`
	ErrorExtra struct {
		RetryAfter int `json:"retry_after"`
	} `json:"error_extra"`
	ErrorTag string `json:"error_tag"`
	HTTPCode int    `json:"http_code"`
}

// --- Client Implementation ---

// TodoistClient is a client for interacting with the Todoist API.
type TodoistClient struct {
	client   *http.Client
	config   config.TodoistConfig
}

// NewTodoistClient creates a new TodoistClient.
func NewTodoistClient(cfg config.TodoistConfig) *TodoistClient {
	return &TodoistClient{
		client:   &http.Client{Timeout: 20 * time.Second},
		config:   cfg,
	}
}

func (c *TodoistClient) doRequestWithRetry(req *http.Request) (*http.Response, error) {
	var resp *http.Response
	var err error

	const maxRetries = 3
	backoffDuration := 1 * time.Second

	for i := 0; i < maxRetries; i++ {
		// We need to be able to read the body multiple times
		if req.GetBody != nil {
			body, err := req.GetBody()
			if err != nil {
				return nil, fmt.Errorf("failed to get request body: %w", err)
			}
			req.Body = body
		}

		resp, err = c.client.Do(req)
		if err != nil {
			return nil, fmt.Errorf("failed to execute request: %w", err)
		}

		if resp.StatusCode == http.StatusTooManyRequests {
			bodyBytes, _ := io.ReadAll(resp.Body)
			resp.Body.Close() // Close the body to allow for reuse of connection

			var errorResponse TodoistErrorResponse
			if json.Unmarshal(bodyBytes, &errorResponse) == nil && errorResponse.ErrorExtra.RetryAfter > 0 {
				backoffDuration = time.Duration(errorResponse.ErrorExtra.RetryAfter) * time.Second
			}

			log.Printf("WARN: Todoist API rate limit hit. Retrying after %v...", backoffDuration)
			time.Sleep(backoffDuration)
			backoffDuration *= 2 // Exponential backoff
			continue
		}

		// if we are here, it means the request was successful or failed with a non-retryable error
		return resp, nil
	}

	// if we are here, it means we have exhausted all retries
	body, _ := io.ReadAll(resp.Body)
	return nil, fmt.Errorf("todoist api returned non-200 status after %d retries: %d %s", maxRetries, resp.StatusCode, string(body))
}

// FetchWorkItems fetches all tasks from Todoist and transforms them into WorkItems.
func (c *TodoistClient) FetchWorkItems(ctx context.Context) ([]model.WorkItem, error) {
	fmt.Println("Fetching items from Todoist...")

	syncResp, err := c.fetchRawTodoistData(ctx)
	if err != nil {
		return nil, err
	}

	workItems := transformTodoistTasks(syncResp)

	fmt.Printf("Fetched and transformed %d items from Todoist\n", len(workItems))
	return workItems, nil
}

// fetchRawTodoistData fetches the raw data from the Todoist Sync API.
func (c *TodoistClient) fetchRawTodoistData(ctx context.Context) (*TodoistSyncResponse, error) {
	data := url.Values{}
	data.Set("sync_token", "*")
	data.Set("resource_types", `["items","projects"]`)

	req, err := http.NewRequest("POST", todoistAPI, strings.NewReader(data.Encode()))
	if err != nil {
		return nil, fmt.Errorf("failed to create todoist request: %w", err)
	}
	req.GetBody = func() (io.ReadCloser, error) {
		return io.NopCloser(strings.NewReader(data.Encode())), nil
	}

	req.Header.Add("Authorization", "Bearer "+c.config.APIToken)
	req.Header.Add("Content-Type", "application/x-www-form-urlencoded")

	resp, err := c.doRequestWithRetry(req)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		body, _ := io.ReadAll(resp.Body)
		return nil, fmt.Errorf("todoist api returned non-200 status: %d %s", resp.StatusCode, string(body))
	}

	var syncResp TodoistSyncResponse
	if err := json.NewDecoder(resp.Body).Decode(&syncResp); err != nil {
		return nil, fmt.Errorf("failed to decode todoist response: %w", err)
	}

	return &syncResp, nil
}

// transformTodoistTasks transforms the raw Todoist tasks into a slice of WorkItems.
func transformTodoistTasks(syncResp *TodoistSyncResponse) []model.WorkItem {
	projByID := make(map[string]string, len(syncResp.Projects))
	for _, p := range syncResp.Projects {
		projByID[p.ID] = p.Name
	}

	workItems := make([]model.WorkItem, 0, len(syncResp.Items))
	for _, task := range syncResp.Items {
		workItems = append(workItems, transformTodoistTask(task, projByID))
	}

	return workItems
}

func transformTodoistTask(task TodoistTask, projByID map[string]string) model.WorkItem {
    var dueAt *time.Time
    if task.Due != nil {
        // Todoist dates can be just YYYY-MM-DD or a full RFC3339 datetime
        parsedTime, err := time.Parse("2006-01-02", task.Due.Date)
        if err != nil {
            parsedTime, _ = time.Parse(time.RFC3339, task.Due.Datetime)
        }
        if !parsedTime.IsZero() {
            dueAt = &parsedTime
        }
    }

    status := model.StatusOpen
    if task.IsCompleted {
        status = model.StatusDone
    }

    // The raw response can be stored if needed for more complex transformations
    raw, _ := json.Marshal(task)

    updatedAt := task.UpdatedAt
    if updatedAt.IsZero() {
        updatedAt = task.CreatedAt
    }

    projectName := projByID[task.ProjectID]

    assignee := ""
    if task.ResponsibleUID != nil {
        assignee = *task.ResponsibleUID
    }

    return model.WorkItem{
        ID:          task.ID,
        Source:      model.SourceTodoist,
        Title:       task.Content,
        Description: task.Description,
        Status:      status,
        Project:     projectName,
        ProjectID:   task.ProjectID,
        URL:         task.URL,
        CreatedAt:   task.CreatedAt,
        UpdatedAt:   updatedAt,
        DueAt:       dueAt,
        Priority:    task.Priority,
        Labels:      model.StringSlice(task.Labels),
        Assignee:    assignee,
        RawData:     raw,
    }
}

const todoistRESTAPI = "https://api.todoist.com/rest/v2"

// CreateTask creates a new task in Todoist.
func (c *TodoistClient) CreateTask(ctx context.Context, content, projectID string) (*TodoistTask, error) {
	apiURL := fmt.Sprintf("%s/tasks", todoistRESTAPI)

	body := map[string]interface{}{
		"content":    content,
		"project_id": projectID,
	}

	jsonBody, err := json.Marshal(body)
	if err != nil {
		return nil, fmt.Errorf("failed to marshal request body: %w", err)
	}

	req, err := http.NewRequestWithContext(ctx, "POST", apiURL, bytes.NewReader(jsonBody))
	if err != nil {
		return nil, fmt.Errorf("failed to create request: %w", err)
	}
	req.GetBody = func() (io.ReadCloser, error) {
		return io.NopCloser(bytes.NewReader(jsonBody)), nil
	}

	req.Header.Add("Authorization", "Bearer "+c.config.APIToken)
	req.Header.Add("Content-Type", "application/json")

	resp, err := c.doRequestWithRetry(req)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		respBody, _ := io.ReadAll(resp.Body)
		return nil, fmt.Errorf("todoist api returned non-200 status: %d %s", resp.StatusCode, string(respBody))
	}

	var newTask TodoistTask
	if err := json.NewDecoder(resp.Body).Decode(&newTask); err != nil {
		return nil, fmt.Errorf("failed to decode response: %w", err)
	}

	return &newTask, nil
}

// CompleteTask marks a task as complete in Todoist.
func (c *TodoistClient) CompleteTask(ctx context.Context, taskID string) error {
	apiURL := fmt.Sprintf("%s/tasks/%s/close", todoistRESTAPI, taskID)

	req, err := http.NewRequestWithContext(ctx, "POST", apiURL, nil)
	if err != nil {
		return fmt.Errorf("failed to create request: %w", err)
	}

	req.Header.Add("Authorization", "Bearer "+c.config.APIToken)

	resp, err := c.doRequestWithRetry(req)
	if err != nil {
		return err
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusNoContent {
		respBody, _ := io.ReadAll(resp.Body)
		return fmt.Errorf("todoist api returned non-204 status: %d %s", resp.StatusCode, string(respBody))
	}

	return nil
}

// DeleteTask deletes a task in Todoist.
func (c *TodoistClient) DeleteTask(ctx context.Context, taskID string) error {
	apiURL := fmt.Sprintf("%s/tasks/%s", todoistRESTAPI, taskID)

	req, err := http.NewRequestWithContext(ctx, "DELETE", apiURL, nil)
	if err != nil {
		return fmt.Errorf("failed to create request: %w", err)
	}

	req.Header.Add("Authorization", "Bearer "+c.config.APIToken)

	resp, err := c.doRequestWithRetry(req)
	if err != nil {
		return err
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusNoContent {
		respBody, _ := io.ReadAll(resp.Body)
		return fmt.Errorf("todoist api returned non-204 status: %d %s", resp.StatusCode, string(respBody))
	}

	return nil
}
