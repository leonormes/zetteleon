
package cmd

import (
	"github.com/spf13/cobra"
)

// todoistCmd represents the base command when called without any subcommands
var todoistCmd = &cobra.Command{
	Use:   "todoist",
	Short: "A set of commands to interact with Todoist",
	Long:  `Manage and sync items with Todoist.`,
}

func init() {
	rootCmd.AddCommand(todoistCmd)
}
