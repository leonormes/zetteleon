// ProdOS vault note frontmatter — validates extracted YAML/JSON objects.
// Human spec: 30_Library/SoT/SoT - ProdOS Note Metadata (Frontmatter).md
// Usage: cue vet prodos_frontmatter.cue some-note.json
// JSON is typically produced from the first YAML block of each .md file.

package prodos

#Kind: "head" | "sot" | "protocol" | "moc" | "atomic" | "project" | "ops" | "prompt" | "journal"

#Lifecycle: "seedling" | "active" | "stable" | "evergreen" | "archived"

#Trust: "low" | "working" | "stable" | "authoritative"

#AtomicForm: "concept" | "claim" | "definition" | "metaphor" | "hypothesis" | "strategy" | "insight"

#Review: {
	interval?:     string
	last_reviewed?: string
}

#Chronos: {
	last_synthesis?:  string
	synthesis_count?: int & >=0
}

#ProtocolBlock: close({
	applies_to?:      [...string]
	binary_checklist?: bool
})

#MocBlock: close({
	hub_for?:       [...string]
	entry_points?:  [...string]
})

#AtomicBlock: close({
	form!: #AtomicForm
})

#OpsBlock: {
	tool?:              string
	target_service?:    string
	hop_level?:         string
	requires_tunnel?:   bool
	prerequisites?:     [...string]
	[string]:           _ // allow extra ops-specific keys
}

#PromptBlock: close({
	description?: string
	inject_as?:   string
	model_hints?: string
})

#ProjectBlock: {
	area?:   string
	status?: string
	owner?:  string
	[string]: _
}

// kind-specific prodos (closed per-variant so atomic cannot carry protocol, etc.)
#ProdosAtomic: {
	kind!:       "atomic"
	lifecycle!:  #Lifecycle
	trust?:      #Trust
	review?:     #Review
	id?:         string
	atomic!:     #AtomicBlock
}

#ProdosProtocol: {
	kind!:       "protocol"
	lifecycle!:  #Lifecycle
	trust?:      #Trust
	review?:     #Review
	id?:         string
	protocol!:   #ProtocolBlock
}

#ProdosOther: {
	kind!:      "head" | "sot" | "moc" | "project" | "ops" | "prompt" | "journal"
	lifecycle!: #Lifecycle
	trust?:     #Trust
	review?:    #Review
	id?:        string
	chronos?:   #Chronos
	moc?:       #MocBlock
	ops?:       #OpsBlock
	prompt?:    #PromptBlock
	project?:   #ProjectBlock
}

#Prodos: #ProdosAtomic | #ProdosProtocol | #ProdosOther

// Open top-level: legacy keys (type, status, …) remain valid alongside prodos.
#Frontmatter: {
	title!:    string & != ""
	created!:  string
	modified!: string
	tags!: [...string]
	prodos!: #Prodos
	aliases?: [...string]
	see_also?: [...string]
	supersedes?:    string
	superseded_by?: string
	[string]: _
}
