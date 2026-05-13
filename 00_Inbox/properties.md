> ### **Role: Obsidian Data Architect & Systems Designer**
> **Context:** > I am building a highly structured, data-oriented personal knowledge management (PKM) system in Obsidian. I need your help designing a metadata schema, query systems, and automated workflows.
> **Technical Framework:**
>  1. **Obsidian Properties (YAML):** All metadata must be stored in the YAML frontmatter of Markdown files.
>    * **Types to Use:** Text, List, Number, Checkbox, Date, and Date & Time.
>    * **Naming Convention:** Use plural keys for lists (e.g., tags, aliases) and avoid singular versions like alias, which are deprecated. Use snake_case or kebab-case for keys to ensure compatibility with query engines.
>  2. **Dataview Query Language (DQL):** For basic dashboards, use LIST, TABLE, TASK, or CALENDAR queries.
>  3. **DataviewJS:** For complex logic, relative dates (e.g., "last week"), and interactive elements, use JavaScript-based queries.
>  4. **Bases (Core Plugin):** Since mid-2025, Obsidian includes a native "Bases" plugin for interactive filtering, sorting, and database-like views. Schema designs should be compatible with Bases' ability to batch-edit properties.
>  5. **Atomic Design:** Notes should be "atomic"—focused on a single concept—to maximise linkability and data granularity.
> **The Task:**
> I want you to design a schema for the following domain: **[INSERT YOUR DOMAIN, e.g., Academic Research / Project Management / Cooking]**.
> **Please provide:**
>  * **A Property Schema:** A list of YAML keys with their corresponding data types (e.g., status: text, due_date: date).
>  * **A Template Example:** A raw YAML block I can put into an Obsidian template.
>  * **Primary Queries:** 3–5 Dataview (DQL) queries to build an overview dashboard for this data.
>  * **Advanced View:** 1 DataviewJS snippet for a more dynamic calculation (e.g., progress tracking or a "stale note" finder).
>  * **Relationship Mapping:** How these notes should link to other folders or tags to create a functional knowledge graph.
> **Constraints:**
>  * Prioritise "local-first" principles; do not rely on external APIs.
>  * Ensure the YAML is valid according to Obsidian’s standard property formatting.
>  * Use British English spelling (e.g., 'organise', 'optimise').
> 
