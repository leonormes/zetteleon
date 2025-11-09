package cmd

import (
	"context"
	"log"

	"prodos/internal/client"
	"prodos/internal/config"
	"prodos/internal/database"
	"prodos/internal/notes"

	"github.com/spf13/cobra"
)

var notesPruneCmd = &cobra.Command{
	Use:   "prune",
	Short: "Prune deleted Obsidian notes and update the corresponding work items",
	Run: func(cmd *cobra.Command, args []string) {
		cfg, err := config.LoadConfig()
		if err != nil {
			log.Fatalf("ERROR: Failed to load configuration: %v", err)
		}

		db, err := database.InitDB()
		if err != nil {
			log.Fatalf("ERROR: Failed to initialize database: %v", err)
		}

		todoistClient := client.NewTodoistClient(cfg.Todoist)

		syncer := notes.NewSyncer(db, cfg, todoistClient)

		if err := syncer.Prune(context.Background()); err != nil {
			log.Fatalf("ERROR: Failed to prune notes: %v", err)
		}
	},
}

func init() {
	notesCmd.AddCommand(notesPruneCmd)
}
