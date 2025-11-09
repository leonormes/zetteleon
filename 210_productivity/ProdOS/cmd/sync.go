package cmd

import (
	"context"
	"fmt"
	"log"
	"time"

	"prodos/internal/client"
	"prodos/internal/config"
	"prodos/internal/database"
	"prodos/internal/embedding"

	"github.com/spf13/cobra"
)

var syncCmd = &cobra.Command{
	Use:   "sync",
	Short: "Sync work items from all sources",
	Long:  `Fetches tasks and issues from sources like Jira and Todoist and saves them to the local database.`,
	Run: func(cmd *cobra.Command, args []string) {
		ctx, cancel := context.WithTimeout(context.Background(), 5*time.Minute)
		defer cancel()
		fmt.Println("Starting sync...")

		// Load Config
		cfg, err := config.LoadConfig()
		if err != nil {
			log.Fatalf("Failed to load configuration: %v", err)
		}

		// Init DB
		db, err := database.InitDB()
		if err != nil {
			log.Fatalf("Failed to initialize database: %v", err)
		}

		// Init Clients
		todoistClient := client.NewTodoistClient(cfg.Todoist)

		// Fetch from Todoist
		todoistItems, err := todoistClient.FetchWorkItems(ctx)
		if err != nil {
			log.Printf("Warning: Failed to fetch items from Todoist: %v", err)
		}

		// Optionally fetch from Jira if configured
		allItems := todoistItems
		if cfg.Jira.Host != "" && cfg.Jira.Username != "" && cfg.Jira.APIToken != "" {
			jiraClient := client.NewJiraClient(cfg.Jira)
			jiraItems, err := jiraClient.FetchWorkItems(ctx)
			if err != nil {
				log.Printf("Warning: Failed to fetch items from Jira: %v", err)
			} else {
				allItems = append(allItems, jiraItems...)
			}
		} else {
			log.Println("Jira not configured; skipping")
		}

		// upsert
		if err := db.UpsertWorkItems(ctx, allItems); err != nil {
			log.Fatalf("Failed to save work items to database: %v", err)
		}

		fmt.Printf("Sync complete! %d items processed.\n", len(allItems))

		// Automatically generate and store embeddings
		fmt.Println("Generating embeddings...")

		// Load all work items from database (including the newly synced ones)
		workItems, err := db.GetAllWorkItems(ctx)
		if err != nil {
			log.Fatalf("Failed to load work items for embedding: %v", err)
		}

		// Init Embedding Client
		embedClient, err := embedding.NewChromaClient()
		if err != nil {
			log.Fatalf("Failed to initialize ChromaDB client: %v", err)
		}

		// Generate and store embeddings
		if err := embedClient.EmbedAndStore(ctx, workItems); err != nil {
			log.Fatalf("Failed to embed and store work items: %v", err)
		}

		fmt.Printf("Embeddings generated! %d items embedded.\n", len(workItems))
	},
}

func init() {
	rootCmd.AddCommand(syncCmd)
}
