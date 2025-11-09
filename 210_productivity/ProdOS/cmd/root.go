package cmd

import (
	"fmt"
	"os"

	"github.com/spf13/cobra"
)

var rootCmd = &cobra.Command{
	Use:   "prodos",
	Short: "ProdOS is a universal collector for your work items.",
	Long:  `A CLI tool to aggregate tasks and issues from various sources like Jira and Todoist into a unified local database.`,
}

func Execute() {
	err := rootCmd.Execute()
	if err != nil {
		fmt.Fprintf(os.Stderr, "Whoops. There was an error while executing your CLI '%s'", err)
		os.Exit(1)
	}
}
