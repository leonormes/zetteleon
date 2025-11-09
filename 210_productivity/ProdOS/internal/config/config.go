package config

import (
	"fmt"
	"os"
	"path/filepath"

	"gopkg.in/yaml.v3"
)

// Config holds the configuration for the application.
type Config struct {
	Jira    JiraConfig    `yaml:"jira"`
	Todoist TodoistConfig `yaml:"todoist"`
	GTD     GTDConfig     `yaml:"gtd"`
}

// JiraConfig holds Jira-specific credentials.
type JiraConfig struct {
	Host     string `yaml:"host"`
	Username string `yaml:"username"`
	APIToken string `yaml:"api_token"`
}

// TodoistConfig holds Todoist-specific credentials.
type TodoistConfig struct {
	APIToken string `yaml:"api_token"`
}

// GTDConfig holds the paths for the GTD workflow.
type GTDConfig struct {
	VaultRoot    string `yaml:"vault_root"`
	InboxPath    string `yaml:"inbox_path"`
	ProjectsPath string `yaml:"projects_path"`
	TemplatePath string `yaml:"template_path"`
	StateFile    string `yaml:"state_file"`
}

// Validate checks if the configuration is valid and has required fields.
func (c *Config) Validate() error {
	// Todoist is mandatory
	if c.Todoist.APIToken == "" {
		return fmt.Errorf("Todoist API token is required. Set TODOIST_API_TOKEN environment variable or configure in collector.yaml")
	}

	// Jira is optional, but if any Jira field is set, all must be present for consistency
	if c.Jira.Host != "" || c.Jira.Username != "" || c.Jira.APIToken != "" {
		if c.Jira.Host == "" || c.Jira.Username == "" || c.Jira.APIToken == "" {
			return fmt.Errorf("Jira is partially configured. Either provide all fields (host, username, api_token) or omit them entirely")
		}
	}

	// GTD paths are optional but if set, ensure they are absolute or relative appropriately
	// For now, just ensure if VaultRoot is set, others should be considered
	if c.GTD.VaultRoot != "" && (c.GTD.InboxPath == "" || c.GTD.ProjectsPath == "") {
		return fmt.Errorf("GTD vault_root is set but inbox_path or projects_path is missing. Please configure all GTD paths")
	}

	return nil
}

// LoadConfig loads the configuration from the YAML file and environment variables.
// Environment variables take precedence over file configs for security.
func LoadConfig() (*Config, error) {
	home, err := os.UserHomeDir()
	if err != nil {
		return nil, fmt.Errorf("could not get user home directory: %w", err)
	}

	// Check for config in the current directory first, then home
	configPath := "collector.yaml"
	if _, err := os.Stat(configPath); os.IsNotExist(err) {
		configPath = filepath.Join(home, ".config", "prodos", "collector.yaml")
	}

	var cfg Config

	// Load from file if it exists
	if _, err := os.Stat(configPath); !os.IsNotExist(err) {
		data, err := os.ReadFile(configPath)
		if err != nil {
			return nil, fmt.Errorf("could not read config file: %w", err)
		}
		if err := yaml.Unmarshal(data, &cfg); err != nil {
			return nil, fmt.Errorf("could not parse config file: %w", err)
		}
	}

	// Override with environment variables (higher priority for security)
	if token := os.Getenv("TODOIST_API_TOKEN"); token != "" {
		cfg.Todoist.APIToken = token
	}
	if host := os.Getenv("JIRA_HOST"); host != "" {
		cfg.Jira.Host = host
	}
	if username := os.Getenv("JIRA_USERNAME"); username != "" {
		cfg.Jira.Username = username
	}
	if token := os.Getenv("JIRA_API_TOKEN"); token != "" {
		cfg.Jira.APIToken = token
	}

	// Validate the final configuration
	if err := cfg.Validate(); err != nil {
		return nil, err
	}

	return &cfg, nil
}