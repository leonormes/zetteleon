package cmd

import (
	"context"
	"fmt"
	"log"
	"time"

	"github.com/spf13/cobra"
	"prodos/internal/embedding"
)

var queryCmd = &cobra.Command{
	Use:   "query [query string]",
	Short: "Query for similar work items",
	Args:  cobra.ExactArgs(1),
	Run: func(cmd *cobra.Command, args []string) {
		ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
		defer cancel()
		fmt.Println("Querying for similar work items...")

		client, err := embedding.NewChromaClient()
		if err != nil {
			log.Fatalf("Failed to create chroma client: %v", err)
		}

		n, _ := cmd.Flags().GetInt("number")

		results, err := client.Query(ctx, args[0], n)
		if err != nil {
			log.Fatalf("Failed to query: %v", err)
		}

		if len(results) == 0 {
			fmt.Println("No results found. The collection may be empty or no matches were found.")
			return
		}

		fmt.Printf("\nFound %d results:\n\n", len(results))
		for i, result := range results {
			fmt.Printf("%d. ID: %s (Score: %.4f)\n", i+1, result.ID, result.Similarity)
			fmt.Printf("   Content: %s\n", result.Content)
			fmt.Println()
		}
	},
}

func init() {
	rootCmd.AddCommand(queryCmd)
	queryCmd.Flags().IntP("number", "n", 5, "Number of results to return")
}
