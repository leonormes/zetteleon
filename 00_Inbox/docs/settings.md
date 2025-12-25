---
aliases: []
confidence: ""
created: 2025-12-24T22:05:55Z
epistemic: ""
last_reviewed: ""
modified: 2025-12-25T18:35:31Z
purpose: ""
review_interval: ""
see_also: []
source_of_truth: []
status: ""
tags: []
title: settings
type: ""
uid: 
updated: 
---

## Metadata Menu Settings

### Global Settings

#### `Scope`

You can choose to manage only frontmatter fields or frontmatter and inline-fields (could be slower with very large files)

Changing this setting requires the plugin to be reloaded.

#### `Display field options in context menu`

if toggled `on`: Metadata Menu will display one control item per field in the target note in the context menu. That could result in a very large context menu if the target note has many fields

if toggled `off`: Metadata Menu will display a "Field Options" item in the context menu. You can access control items through a modal display by clicking on "Field Options".

#### `Globally ignored fields`

the fields listed here (comma separated) won't be available in context menus

#### `Exclusions`

You can exclude files based on their path, their extension or their name based on a regex pattern

#### `First day of week`

For `Date` fields' datepicker, select the day the week should start with (default `Monday`)

### Preset Field Settings

If you want a field to be globally managed throughout your whole vault you can `add a new field setting`:

- Click on "+"
- Type the field name
- Select the [type](fields.md#field-type) of field
- Set the options

### Fileclass Settings

If you want the same field to have different behaviours depending on the note they belong to, you can define field settings based on the "class" of the "note".

This is a particular frontmatter attribute that you will have to give to your note.

By default, this attribute is named `fileClass`

A FileClass is a specific note located in a defined folder. In this note you will set the fields settings for each note that has a `fileClass` attribute equal to the name of the `fileClass` note (without.md extension).

> See # Fileclass section for details about how to write a fileClass

#### fileClass Files Folder

In Metadata Menu, you'll have to set the location of `fileClass` notes: type the path to the fileClass files folder in the `class Files Path` setting (don't forget the trailing slash)

#### fileClass Alias

You may find usefull to combine the fileClass attribute with an other attribute that you already use to categorize your notes (category, type, kind, area,....).

You can give an alias to fileClass attribute in `fileClass field alias` setting so that you can use the same name to manage the fields and for your other current usage.

#### Global fileClass

You can define a fileClass that will be applicable to all of your notes, even if there is no fileClass attribute defined in their frontmatter.

This is usefull if you are more confortable with setting your preset fields in a note rather than in the plugin settings.

If global fileClass is null or unproperly configured, the preset fields defined in the plugin settings will have the priority.

#### Result per Page

Default number of files per page in the table view and code blocks

#### Add a Fileclass after Create

Toggle on to display the fileclass list to choose from to be added to a new file

#### Fileclass Selector in Note Fields Modal

You can hide the fileClass selector automatically added to the note fields modal since it can be duplicated with fileclass inheritance or global fileclass

#### fileClass Queries

You can define fileClasses to be applicable to every file matching a dataview query. (same syntax as for `File` type fields)

If a File matches several queries, the last matching fileClass (starting from the top) will be applicable to this file.

#### Show Extra Button to Access Metadata Menu Form

When a note has one or more fileClass you can display a button next to the note's:

- links in reading mode
- links in live preview
- file in file explorer (will also toggle the "Fileclass folder add button")
- reference in search panel
- reference in backlinks panel
- tab header
- properties

each option has its own toggler
