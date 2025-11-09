package cmd

import (
	"github.com/spf13/cobra"
)

var notesCmd = &cobra.Command{
	Use:   "notes",
	Short: "Manage Obsidian notes for work items",
}

func init() {
	rootCmd.AddCommand(notesCmd)
}