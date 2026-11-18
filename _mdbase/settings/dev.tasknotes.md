---
mdbase_type: tasknotes-settings
app: dev.tasknotes
scope: collection
settings_version: 1
nlp_triggers:
- property_id: tags
  trigger: '#'
  enabled: true
- property_id: contexts
  trigger: '@'
  enabled: true
- property_id: projects
  trigger: +
  enabled: true
- property_id: status
  trigger: '*'
  enabled: true
- property_id: priority
  trigger: '!'
  enabled: false
template_enabled: false
template_path: ''
occurrence_template_enabled: false
occurrence_template_path: ''
move_on_archive: false
archive_folder: TaskNotes/Archive
auto_stop_time_tracking_on_complete: true
reset_body_checkboxes_on_recurrence: false
link_write_format: wikilink
status_behavior:
  none:
    exclude_from_cycle: false
    auto_archive: false
    auto_archive_delay_minutes: 5
  open:
    exclude_from_cycle: false
    auto_archive: false
    auto_archive_delay_minutes: 5
  in-progress:
    exclude_from_cycle: false
    auto_archive: false
    auto_archive_delay_minutes: 5
  done:
    next_status: open
    exclude_from_cycle: false
    auto_archive: false
    auto_archive_delay_minutes: 5
permalink: llmeon/mdbase/settings/dev.tasknotes
---

