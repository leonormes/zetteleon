package logger

import (
	"bytes"
	"context"
	"encoding/json"
	"errors"
	"strings"
	"testing"
)

func TestNew(t *testing.T) {
	tests := []struct {
		name  string
		debug bool
	}{
		{
			name:  "info level",
			debug: false,
		},
		{
			name:  "debug level",
			debug: true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			logger := New(tt.debug)
			if logger == nil {
				t.Error("New() returned nil")
			}
			if logger.Logger == nil {
				t.Error("New() Logger field is nil")
			}
		})
	}
}

func TestLogger_Info(t *testing.T) {
	var buf bytes.Buffer
	logger := NewForTests(&buf, false)
	
	logger.Info("test message", "key", "value")
	
	output := buf.String()
	if !strings.Contains(output, "test message") {
		t.Errorf("Expected log output to contain 'test message', got: %s", output)
	}
	
	// Verify it's valid JSON
	var logEntry map[string]interface{}
	if err := json.Unmarshal(buf.Bytes(), &logEntry); err != nil {
		t.Errorf("Log output is not valid JSON: %v", err)
	}
	
	if logEntry["msg"] != "test message" {
		t.Errorf("Expected msg='test message', got: %v", logEntry["msg"])
	}
	
	if logEntry["key"] != "value" {
		t.Errorf("Expected key='value', got: %v", logEntry["key"])
	}
}

func TestLogger_Error(t *testing.T) {
	var buf bytes.Buffer
	logger := NewForTests(&buf, false)
	
	logger.Error("error occurred", "error", "something went wrong")
	
	output := buf.String()
	if !strings.Contains(output, "error occurred") {
		t.Errorf("Expected log output to contain 'error occurred', got: %s", output)
	}
	
	// Verify JSON structure
	var logEntry map[string]interface{}
	if err := json.Unmarshal(buf.Bytes(), &logEntry); err != nil {
		t.Errorf("Log output is not valid JSON: %v", err)
	}
	
	if logEntry["level"] != "ERROR" {
		t.Errorf("Expected level='ERROR', got: %v", logEntry["level"])
	}
}

func TestLogger_Debug(t *testing.T) {
	var buf bytes.Buffer
	
	// Debug disabled
	logger := NewForTests(&buf, false)
	logger.Debug("debug message")
	
	if buf.Len() > 0 {
		t.Error("Debug message logged when debug=false")
	}
	
	// Debug enabled
	buf.Reset()
	logger = NewForTests(&buf, true)
	logger.Debug("debug message")
	
	if buf.Len() == 0 {
		t.Error("Debug message not logged when debug=true")
	}
	
	output := buf.String()
	if !strings.Contains(output, "debug message") {
		t.Errorf("Expected log output to contain 'debug message', got: %s", output)
	}
}

func TestLogger_WithFields(t *testing.T) {
	var buf bytes.Buffer
	logger := NewForTests(&buf, false)
	
	fields := map[string]any{
		"user_id":  "123",
		"request":  "GET /api/items",
		"duration": 42,
	}
	
	loggerWithFields := logger.WithFields(fields)
	loggerWithFields.Info("request completed")
	
	var logEntry map[string]interface{}
	if err := json.Unmarshal(buf.Bytes(), &logEntry); err != nil {
		t.Errorf("Log output is not valid JSON: %v", err)
	}
	
	if logEntry["user_id"] != "123" {
		t.Errorf("Expected user_id='123', got: %v", logEntry["user_id"])
	}
	
	if logEntry["request"] != "GET /api/items" {
		t.Errorf("Expected request='GET /api/items', got: %v", logEntry["request"])
	}
	
	if logEntry["duration"] != float64(42) {
		t.Errorf("Expected duration=42, got: %v", logEntry["duration"])
	}
}

func TestLogger_WithError(t *testing.T) {
	var buf bytes.Buffer
	logger := NewForTests(&buf, false)
	
	testErr := errors.New("test error")
	loggerWithErr := logger.WithError(testErr)
	loggerWithErr.Error("operation failed")
	
	var logEntry map[string]interface{}
	if err := json.Unmarshal(buf.Bytes(), &logEntry); err != nil {
		t.Errorf("Log output is not valid JSON: %v", err)
	}
	
	if logEntry["error"] != "test error" {
		t.Errorf("Expected error='test error', got: %v", logEntry["error"])
	}
}

func TestLogger_WithComponent(t *testing.T) {
	var buf bytes.Buffer
	logger := NewForTests(&buf, false)
	
	componentLogger := logger.WithComponent("database")
	componentLogger.Info("connection established")
	
	var logEntry map[string]interface{}
	if err := json.Unmarshal(buf.Bytes(), &logEntry); err != nil {
		t.Errorf("Log output is not valid JSON: %v", err)
	}
	
	if logEntry["component"] != "database" {
		t.Errorf("Expected component='database', got: %v", logEntry["component"])
	}
}

func TestLogger_WithContext(t *testing.T) {
	var buf bytes.Buffer
	logger := NewForTests(&buf, false)
	
	ctx := context.Background()
	contextLogger := logger.WithContext(ctx)
	
	if contextLogger == nil {
		t.Error("WithContext() returned nil")
	}
	
	// Should still be able to log
	contextLogger.Info("message with context")
	
	if buf.Len() == 0 {
		t.Error("No log output after WithContext()")
	}
}

func TestLogger_MultipleFields(t *testing.T) {
	var buf bytes.Buffer
	logger := NewForTests(&buf, false)
	
	logger.
		WithComponent("api").
		WithFields(map[string]any{"endpoint": "/users"}).
		WithError(errors.New("not found")).
		Error("request failed")
	
	var logEntry map[string]interface{}
	if err := json.Unmarshal(buf.Bytes(), &logEntry); err != nil {
		t.Errorf("Log output is not valid JSON: %v", err)
	}
	
	if logEntry["component"] != "api" {
		t.Errorf("Expected component='api', got: %v", logEntry["component"])
	}
	
	if logEntry["endpoint"] != "/users" {
		t.Errorf("Expected endpoint='/users', got: %v", logEntry["endpoint"])
	}
	
	if logEntry["error"] != "not found" {
		t.Errorf("Expected error='not found', got: %v", logEntry["error"])
	}
	
	if logEntry["msg"] != "request failed" {
		t.Errorf("Expected msg='request failed', got: %v", logEntry["msg"])
	}
}
