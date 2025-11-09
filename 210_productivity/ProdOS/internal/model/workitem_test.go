package model

import (
	"database/sql/driver"
	"testing"
)

func TestStringSlice_Value(t *testing.T) {
	tests := []struct {
		name    string
		slice   StringSlice
		want    driver.Value
		wantErr bool
	}{
		{
			name:    "empty slice",
			slice:   StringSlice{},
			want:    "[]",
			wantErr: false,
		},
		{
			name:    "single item",
			slice:   StringSlice{"test"},
			want:    `["test"]`,
			wantErr: false,
		},
		{
			name:    "multiple items",
			slice:   StringSlice{"foo", "bar", "baz"},
			want:    `["foo","bar","baz"]`,
			wantErr: false,
		},
		{
			name:    "nil slice",
			slice:   nil,
			want:    "[]",
			wantErr: false,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got, err := tt.slice.Value()
			if (err != nil) != tt.wantErr {
				t.Errorf("StringSlice.Value() error = %v, wantErr %v", err, tt.wantErr)
				return
			}
			if got != tt.want {
				t.Errorf("StringSlice.Value() = %v, want %v", got, tt.want)
			}
		})
	}
}

func TestStringSlice_Scan(t *testing.T) {
	tests := []struct {
		name    string
		input   interface{}
		want    StringSlice
		wantErr bool
	}{
		{
			name:    "valid json array",
			input:   []byte(`["foo","bar"]`),
			want:    StringSlice{"foo", "bar"},
			wantErr: false,
		},
		{
			name:    "empty json array",
			input:   []byte(`[]`),
			want:    StringSlice{},
			wantErr: false,
		},
		{
			name:    "null value",
			input:   nil,
			want:    nil,
			wantErr: false,
		},
		{
			name:    "invalid json",
			input:   []byte(`not json`),
			want:    nil,
			wantErr: true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			var s StringSlice
			err := s.Scan(tt.input)
			if (err != nil) != tt.wantErr {
				t.Errorf("StringSlice.Scan() error = %v, wantErr %v", err, tt.wantErr)
				return
			}
			if !tt.wantErr {
				if len(s) != len(tt.want) {
					t.Errorf("StringSlice.Scan() length = %v, want %v", len(s), len(tt.want))
					return
				}
				for i := range s {
					if s[i] != tt.want[i] {
						t.Errorf("StringSlice.Scan()[%d] = %v, want %v", i, s[i], tt.want[i])
					}
				}
			}
		})
	}
}

func TestSourceType_String(t *testing.T) {
	tests := []struct {
		name   string
		source SourceType
		want   string
	}{
		{
			name:   "todoist",
			source: SourceTodoist,
			want:   "todoist",
		},
		{
			name:   "jira",
			source: SourceJira,
			want:   "jira",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if got := string(tt.source); got != tt.want {
				t.Errorf("SourceType = %v, want %v", got, tt.want)
			}
		})
	}
}

func TestStatus_String(t *testing.T) {
	tests := []struct {
		name   string
		status Status
		want   string
	}{
		{
			name:   "open",
			status: StatusOpen,
			want:   "open",
		},
		{
			name:   "in_progress",
			status: StatusInProgress,
			want:   "in_progress",
		},
		{
			name:   "done",
			status: StatusDone,
			want:   "done",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if got := string(tt.status); got != tt.want {
				t.Errorf("Status = %v, want %v", got, tt.want)
			}
		})
	}
}
