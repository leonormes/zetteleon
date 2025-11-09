package config

import (
	"os"
	"path/filepath"
	"testing"
)

func TestLoadConfig_FromFile(t *testing.T) {
	// Create temporary config file
	tmpDir := t.TempDir()
	
	configContent := `
todoist:
  api_token: "test-todoist-token"

jira:
  host: "https://test.atlassian.net"
  username: "test@example.com"
  api_token: "test-jira-token"
`
	
	// Set environment to use temp config FIRST
	oldHome := os.Getenv("HOME")
	os.Setenv("HOME", tmpDir)
	t.Cleanup(func() {
		os.Setenv("HOME", oldHome)
	})
	
	// Unset any env vars that might override
	oldTodoistToken := os.Getenv("TODOIST_API_TOKEN")
	oldJiraToken := os.Getenv("JIRA_API_TOKEN")
	os.Unsetenv("TODOIST_API_TOKEN")
	os.Unsetenv("JIRA_API_TOKEN")
	t.Cleanup(func() {
		if oldTodoistToken != "" {
			os.Setenv("TODOIST_API_TOKEN", oldTodoistToken)
		}
		if oldJiraToken != "" {
			os.Setenv("JIRA_API_TOKEN", oldJiraToken)
		}
	})
	
	// Create .config/prodos directory structure
	configDir := filepath.Join(tmpDir, ".config", "prodos")
	if err := os.MkdirAll(configDir, 0755); err != nil {
		t.Fatalf("Failed to create config dir: %v", err)
	}
	
	finalConfigPath := filepath.Join(configDir, "collector.yaml")
	if err := os.WriteFile(finalConfigPath, []byte(configContent), 0644); err != nil {
		t.Fatalf("Failed to write final config: %v", err)
	}
	
	cfg, err := LoadConfig()
	if err != nil {
		t.Fatalf("LoadConfig() error = %v", err)
	}
	
	if cfg.Todoist.APIToken != "test-todoist-token" {
		t.Errorf("Todoist.APIToken = %v, want %v", cfg.Todoist.APIToken, "test-todoist-token")
	}
	
	if cfg.Jira.Host != "https://test.atlassian.net" {
		t.Errorf("Jira.Host = %v, want %v", cfg.Jira.Host, "https://test.atlassian.net")
	}
	
	if cfg.Jira.Username != "test@example.com" {
		t.Errorf("Jira.Username = %v, want %v", cfg.Jira.Username, "test@example.com")
	}
	
	if cfg.Jira.APIToken != "test-jira-token" {
		t.Errorf("Jira.APIToken = %v, want %v", cfg.Jira.APIToken, "test-jira-token")
	}
}

func TestLoadConfig_FromEnv(t *testing.T) {
	// Set environment variables
	os.Setenv("TODOIST_API_TOKEN", "env-todoist-token")
	os.Setenv("JIRA_HOST", "https://env.atlassian.net")
	os.Setenv("JIRA_USERNAME", "env@example.com")
	os.Setenv("JIRA_API_TOKEN", "env-jira-token")
	
	t.Cleanup(func() {
		os.Unsetenv("TODOIST_API_TOKEN")
		os.Unsetenv("JIRA_HOST")
		os.Unsetenv("JIRA_USERNAME")
		os.Unsetenv("JIRA_API_TOKEN")
	})
	
	// Create empty home directory to avoid loading actual config
	tmpDir := t.TempDir()
	oldHome := os.Getenv("HOME")
	os.Setenv("HOME", tmpDir)
	t.Cleanup(func() {
		os.Setenv("HOME", oldHome)
	})
	
	cfg, err := LoadConfig()
	if err != nil {
		t.Fatalf("LoadConfig() error = %v", err)
	}
	
	// Environment variables should override
	if cfg.Todoist.APIToken != "env-todoist-token" {
		t.Errorf("Todoist.APIToken = %v, want %v", cfg.Todoist.APIToken, "env-todoist-token")
	}
	
	if cfg.Jira.Host != "https://env.atlassian.net" {
		t.Errorf("Jira.Host = %v, want %v", cfg.Jira.Host, "https://env.atlassian.net")
	}
	
	if cfg.Jira.Username != "env@example.com" {
		t.Errorf("Jira.Username = %v, want %v", cfg.Jira.Username, "env@example.com")
	}
	
	if cfg.Jira.APIToken != "env-jira-token" {
		t.Errorf("Jira.APIToken = %v, want %v", cfg.Jira.APIToken, "env-jira-token")
	}
}

func TestConfig_EnvOverridesFile(t *testing.T) {
	tmpDir := t.TempDir()
	
	// Create config file
	configDir := filepath.Join(tmpDir, ".config", "prodos")
	if err := os.MkdirAll(configDir, 0755); err != nil {
		t.Fatalf("Failed to create config dir: %v", err)
	}
	
	configContent := `
todoist:
  api_token: "file-token"
`
	
	configPath := filepath.Join(configDir, "collector.yaml")
	if err := os.WriteFile(configPath, []byte(configContent), 0644); err != nil {
		t.Fatalf("Failed to write config: %v", err)
	}
	
	// Set environment variable
	os.Setenv("TODOIST_API_TOKEN", "env-token")
	oldHome := os.Getenv("HOME")
	os.Setenv("HOME", tmpDir)
	
	t.Cleanup(func() {
		os.Unsetenv("TODOIST_API_TOKEN")
		os.Setenv("HOME", oldHome)
	})
	
	cfg, err := LoadConfig()
	if err != nil {
		t.Fatalf("LoadConfig() error = %v", err)
	}
	
	// Environment should override file
	if cfg.Todoist.APIToken != "env-token" {
		t.Errorf("Expected env to override file, got %v", cfg.Todoist.APIToken)
	}
}

func TestConfig_Validate(t *testing.T) {
	// Test valid config
	validConfig := Config{
		Todoist: TodoistConfig{APIToken: "token"},
		Jira:    JiraConfig{Host: "host", Username: "user", APIToken: "token"},
		GTD:     GTDConfig{VaultRoot: "root", InboxPath: "inbox", ProjectsPath: "projects"},
	}
	if err := validConfig.Validate(); err != nil {
		t.Errorf("Valid config should not error: %v", err)
	}

	// Test missing Todoist token
	invalidConfig1 := Config{Todoist: TodoistConfig{}}
	if err := invalidConfig1.Validate(); err == nil {
		t.Error("Missing Todoist token should error")
	}

	// Test partial Jira config
	invalidConfig2 := Config{
		Todoist: TodoistConfig{APIToken: "token"},
		Jira:    JiraConfig{Host: "host"}, // Missing username and APIToken
	}
	if err := invalidConfig2.Validate(); err == nil {
		t.Error("Partial Jira config should error")
	}

	// Test partial GTD config
	invalidConfig3 := Config{
		Todoist: TodoistConfig{APIToken: "token"},
		GTD:     GTDConfig{VaultRoot: "root"}, // Missing inbox and projects paths
	}
	if err := invalidConfig3.Validate(); err == nil {
		t.Error("Partial GTD config should error")
	}
}
