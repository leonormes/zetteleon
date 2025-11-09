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

var notesSyncCmd = &cobra.Command{
	Use:   "sync",
	Short: "Create Obsidian notes for work items from the database",
	Run: func(cmd *cobra.Command, args []string) {
		// It is recommended to run `prodos sync` before this command
		// to ensure the local database is up-to-date.

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

		if err := syncer.Sync(context.Background()); err != nil {
			log.Fatalf("ERROR: Failed to sync notes: %v", err)
		}
	},
}

func init() {
	notesCmd.AddCommand(notesSyncCmd)
}
