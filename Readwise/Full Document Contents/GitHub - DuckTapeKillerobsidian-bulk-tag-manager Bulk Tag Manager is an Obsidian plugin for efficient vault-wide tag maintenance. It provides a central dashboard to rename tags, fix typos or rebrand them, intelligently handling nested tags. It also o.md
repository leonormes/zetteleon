# GitHub - DuckTapeKiller/obsidian-bulk-tag-manager: Bulk Tag Manager is an Obsidian plugin for efficient vault-wide tag maintenance. It provides a central dashboard to rename tags, fix typos or rebrand them, intelligently handling nested tags. It also offers real-time tag statistics, flexible casing and separator rules, Unicode support and safe b...

![rw-book-cover](https://opengraph.githubassets.com/45507ce42bb1cf69e8eaf68c49cf1e1423391df2dc2832fb4ea41a92b5523ea2/DuckTapeKiller/obsidian-bulk-tag-manager)

## Metadata
- Author: [[https://github.com/DuckTapeKiller/]]
- Full Title: GitHub - DuckTapeKiller/obsidian-bulk-tag-manager: Bulk Tag Manager is an Obsidian plugin for efficient vault-wide tag maintenance. It provides a central dashboard to rename tags, fix typos or rebrand them, intelligently handling nested tags. It also offers real-time tag statistics, flexible casing and separator rules, Unicode support and safe b...
- Category: #articles
- Summary: Bulk Tag Manager is an Obsidian plugin that provides a dashboard for vault-wide tag maintenance.  
It can rename tags, fix typos, handle nested tags, and apply casing or separator rules with Unicode support.  
Use it carefully and back up your vault because changes are permanent.
- URL: https://github.com/DuckTapeKiller/obsidian-bulk-tag-manager

## Full Document
### DuckTapeKiller/obsidian-bulk-tag-manager

main

Go to file

Code

Open more actions menu

### Bulk Tag Manager Walkthrough

Bulk Tag Manager provides a central dashboard for efficient, vault-wide tag management, including advanced renaming and normalisation tools.

#### Dashboard

Click the ribbon icon (dice) to open the Bulk Tag Manager dashboard. All actions and statistics are managed from this central interface.

#### Rename a Specific Tag

Use this feature to correct typos or apply rebranding consistently across the entire vault.

* **Find**: Enter the existing tag, for example `#brwoser`.
* **Replace**: Enter the corrected tag, for example `#browser`.
* **Smart handling**: Nested tags are automatically updated, for example `#brwoser/history` becomes `#browser/history`.

#### Dashboard Statistics and Settings

##### Statistics

* **Total unique tags**: Displays the number of distinct tags in the vault.
* **Tags to be updated**: Real-time count of tags affected by the current configuration.

##### Quick Settings

* **Case strategy**: Lowercase or uppercase.
* **Separator style**: Snake case, kebab case or preserve existing separators.
* **Remove special characters**: Optional sanitisation for improved consistency.

#### Actions

* **Convert all tags**: Applies the selected rules to all tags in the vault.
* **Generate tag list**: Creates an `All Tags.md` file containing a sorted list of all tags.

#### Core Features

* **Unicode support**: Fully compatible with international characters, for example `#café` and `#música`.
* **Flexible rules**: Casing and separator strategies can be combined as required.
* **Safety**: All updates are performed using the official Obsidian API.

#### Installation

1. Navigate to `.obsidian/plugins/`.
2. Create or rename a folder to `obsidian-bulk-tag-manager`.
3. Copy the following files into the folder:
	* `main.js`
	* `manifest.json`
4. Reload Obsidian and enable **Bulk Tag Manager** in the community plugins settings.

A note on safety:

Please be extremely cautious. Changes made to your tags are permanent and cannot be automatically reverted. While I have tested the plugin thoroughly and encountered no issues, you should back up your vault before use. I am sharing this plugin in good faith, but I cannot be held responsible for any issues resulting from its use.

[![ko-fi](https://camo.githubusercontent.com/201ef269611db7eb6b5d08e9f756ab8980df3014b64492770bdf13a6ed924641/68747470733a2f2f6b6f2d66692e636f6d2f696d672f676974687562627574746f6e5f736d2e737667)](https://ko-fi.com/ducktapekiller)
