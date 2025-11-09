
package client

import (
	"fmt"
	"net/url"
	"os/exec"
	"strings"
)

const obsidianURIBase = "obsidian://adv-uri"

// ObsidianClient is a client for interacting with the Obsidian Advanced URI plugin.
type ObsidianClient struct {
	VaultName string
}

// NewObsidianClient creates a new ObsidianClient.
func NewObsidianClient(vaultName string) *ObsidianClient {
	return &ObsidianClient{VaultName: vaultName}
}

// ExecuteURI constructs and executes an Obsidian Advanced URI.
func (c *ObsidianClient) ExecuteURI(params map[string]string) error {
	qs := url.Values{}
	qs.Set("vault", c.VaultName)
	for key, value := range params {
		qs.Set(key, value)
	}

	uri := fmt.Sprintf("%s?%s", obsidianURIBase, qs.Encode())
	uri = strings.ReplaceAll(uri, "+", "%20") // Obsidian URI scheme requires %20 for spaces

	cmd := exec.Command("open", "--background", uri)
	
	var stderr strings.Builder
    cmd.Stderr = &stderr

	if err := cmd.Run(); err != nil {
		return fmt.Errorf("failed to execute obsidian uri: %v, stderr: %s", err, stderr.String())
	}

	return nil
}
