package cmd

import (
	"context"
	"fmt"
	"log"
	"time"

	"prodos/internal/database"
	"prodos/internal/embedding" // New package

	"github.com/spf13/cobra"
)

var embedCmd = &cobra.Command{
	Use:   "embed",
	Short: "Generate and store embeddings for all work items",
	Long:  `Reads all work items from the local database, generates text embeddings, and stores them in a vector database for semantic search.`, 
	Run: func(cmd *cobra.Command, args []string) {
		ctx, cancel := context.WithTimeout(context.Background(), 10*time.Minute)
		defer cancel()
		fmt.Println("Starting embedding process...")

		// Init DB
		db, err := database.InitDB()
		if err != nil {
			log.Fatalf("Failed to initialize database: %v", err)
		}

		// Load all work items
		workItems, err := db.GetAllWorkItems(ctx) // New DB method
		if err != nil {
			log.Fatalf("Failed to load work items: %v", err)
		}

		// Init Embedding Client
		embedClient, err := embedding.NewChromaClient() // New client
		if err != nil {
			log.Fatalf("Failed to initialize ChromaDB client: %v", err)
		}

		// Generate and store embeddings
		if err := embedClient.EmbedAndStore(ctx, workItems); err != nil {
			log.Fatalf("Failed to embed and store work items: %v", err)
		}

		fmt.Printf("Embedding complete! %d items processed.\n", len(workItems))
	},
}

func init() {
	rootCmd.AddCommand(embedCmd)
}
