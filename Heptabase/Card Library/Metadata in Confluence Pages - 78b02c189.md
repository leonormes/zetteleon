**Metadata in Confluence Pages - 78b02c189**

**User:**

I am using confluence to document our application features mapped to requirements mapped to FAQ. What is the best way to add metadata to each page? I am imagining the pages like objects in oop and being able to build links between them.

**Abacus AI ChatLLM:**

> Routing to GPT-4.1

That's a cool way to think about your Confluence pages! Treating them like objects in OOP to build relationships makes a lot of sense for documentation.

Confluence doesn't have a built-in metadata system exactly like you might find in a database, but there are definitely ways to add metadata and create those links you're looking for. Here are a few approaches, ranging from simple to more advanced:

1. **Labels:** This is the simplest way to add metadata. You can add labels to any Confluence page. For example, you could label a page with "feature-x", "requirement-y", or "faq". You can then search for pages with specific labels or use the "Label Content" macro to display pages with certain labels on a page.

2. **Page Properties and Page Property Report Macro:** This is a more structured approach. You can add a "Page Properties" macro to a page and define columns for metadata like "Feature", "Requirement", "Status", etc. Then, on another page, you can use the "Page Property Report" macro to display a table of these properties from other pages. This is great for creating overviews and summaries.

3. **Info Macro:** The Info macro is a simple way to display key metadata points at the top of the page.

4. **Confluence Custom Fields (with a Marketplace App):** For more robust metadata management, you'll likely need a Marketplace app. Apps like "Metadata for Confluence" or "Comala Metadata" allow you to define custom fields that can be added to pages. This gives you a lot more control over the types of metadata you can store and how it's displayed.

5. **Links and Mentions:** Don't forget the power of simple links and mentions! You can easily link between pages using the `[page name]` syntax or mention users with `@username`. This helps create direct relationships between your pages.

6. **The "Children Display" Macro:** This macro automatically lists all child pages of a given page. This can be useful for structuring documentation where parent pages represent features and child pages represent specific aspects or FAQs related to that feature.

To best advise you, what level of complexity are you comfortable with? Are you open to using Marketplace apps, or would you prefer to stick with built-in Confluence features?

**User:**

I want to build up an interconnected web of pages that detail our product so that you can find an endpoint and traverse the graph of knowledge easily. You might start with a FAQ and that means you too both the requirements for the feature as well as the description of the feature. You could start with the requirements and be able to get to the FAQ or feature that satisfies that requirement. Each page is atomic and self contained and can be updated but it's the single source of truth on that particular aspect. What advice do you have

**Abacus AI ChatLLM:**

> Routing to GPT-4.1

Web Search

best practices for building interconnected web of documentation pages in Confluence for product knowledge, with atomic pages and traversable links between FAQ, requirements, and features

Search Results

- [Develop Technical Documentation in Confluence](https://confluence.atlassian.com/doc/develop-technical-documentation-in-confluence-226166494.html) (Web Search Result)
   There are 3 macros that allow you to re-use content: The Excerpt macro to define a re-usable section, or 'excerpt', on a page – add content inside this macro, and you can reuse it on as many pages as you like.; The Excerpt Include macro (excerpt-include) to include the contents of an excerpt on another page.; The Include Page macro (include) to include the entire content of a page on another ...

- [Tips for creating impactful pages in Confluence](https://community.atlassian.com/forums/Confluence-articles/Tips-for-creating-impactful-pages-in-Confluence/ba-p/2968576) (Web Search Result)
   Some Smart Links for tools like Dropbox will show additional options like Download and Previews. And finally, Smart Links embeds is exactly as it suggests: a full embed of the contents from the pasted link. Read and edit a Google Drive document, manipulate your Figma file and more — all within a Confluence page with Smart Links embeds.

- [Confluence Best Practices - Atlassian](https://www.atlassian.com/software/confluence/resources/guides/get-started/best-practices) (Web Search Result)
   To help you navigate the many powerful ways of using Confluence, we’ve curated a collection of best practices. Before you dive in, sign up for your free Confluence Cloud site and read the following sections: set up your site and spaces, create content in Confluence, and navigate Confluence.

- [Confluence documentation guide: Best practices and tips](https://www.refined.com/blog/confluence-documentation-best-practices) (Web Search Result)
   Best practices for maintaining confluence documentation. Creating high-quality documentation is only half the battle – keeping it accurate, up to date, and accessible is just as important. Here are some best practices we’ve identified to ensure your Confluence documentation remains valuable over time.

- [Confluence for End User Documentation: Tips and Best Practices](https://www.gliffy.com/blog/developing-user-documentation) (Web Search Result)
   Blog: 4 Ways to Supercharge Your Confluence Documentation; Blog: Software Architecture Documentation Dos and Don’ts; Blog: 5 Confluence Apps for Your Internal Knowledge Base; To keep up with the latest Confluence and documentation tips and best practices, make sure to follow us on LinkedIn and subscribe to our newsletter. Get More ...

- [5 Best Practices to Create & Manage your Documentation Hub ... - Vectors](https://covectors.io/blog/5-best-practices-to-create-manage-your-documentation-hub-with-confluence/) (Web Search Result)
   Perhaps one of the most common use cases for Confluence is documentation. Be it internal or external, product or process oriented, documentation requires thorough planning, continuous collaboration and knowledge sharing. This is why it is crucial to follow a set of best practices to make the most out of Confluence and streamline the whole process.

- [Best Practices for Documentation in Confluence](https://maddevs.io/blog/best-practices-for-documentation-in-confluence/) (Web Search Result)
   Confluence, a popular collaboration tool, enables organizations to manage and share information efficiently. By adhering to best practices in documentation, teams can enhance communication, reduce redundancy, and ensure that critical information is easily accessible.

- [Confluence Features and Best Practices - Atlassian Documentation](https://confluence.atlassian.com/confkb/confluence-features-and-best-practices-338365505.html) (Web Search Result)
   This section of the Confluence Knowledge Base contains articles based on the mostly commonly asked questions pertaining to Confluence usage, features, and best practices. Articles in this section include. Confluence Admin Permission Levels Explained; Does Confluence provide integration with chat clients?

Your vision of an interconnected, traversable web of atomic, self-contained Confluence pages is right in line with modern documentation best practices. Here’s how you can achieve this in Confluence, drawing from Atlassian’s own recommendations and expert community advice:

## 1\. **Atomic, Self-Contained Pages as Single Sources of Truth**

Each page should focus on a single concept—be it a feature, requirement, or FAQ. This makes maintenance easier and ensures each page is the definitive source for that topic. When updates are needed, you only have to change one page, and all references to it remain accurate.

## 2\. **Interlinking Pages to Build a Traversable Knowledge Graph**

- **Use Smart Links and Internal Links:** Confluence makes it easy to link to other pages. Paste the page URL or use the `[page name]` syntax to create links. Smart Links will display the page title and even a preview, making navigation intuitive and visually appealing (\[Atlassian Community\](<https://community.atlassian.com/forums/Con>

fluence-articles/Tips-for-creating-impactful-pages-in-Confluence/ba-p/2968576)).

- **Link Requirements, Features, and FAQs:** On each page, add a section like “Related Pages” or “See Also” to link to the requirement(s) a feature fulfills, the feature(s) that satisfy a requirement, and the FAQ(s) that reference either. This allows users to start anywhere and traverse the graph in any direction.

## 3\. **Metadata And Structure**

- **Labels:** Use Confluence labels to tag pages by type (e.g., `feature`, `requirement`, `faq`) and by related topics or modules. This helps with search and organization.

- **Page Properties Macro:** Add a “Page Properties” macro to each page to store structured metadata (e.g., status, owner, related Jira ticket, version). Use the “Page Properties Report” macro to aggregate and display this metadata across multiple pages ([Atlassian Documentation](https://confluence.atlassian.com/doc/develop-technical-documentation-in-confluence-226166494.html)).

- **Templates:** Create page

templates for each type (feature, requirement, FAQ) to ensure consistency and that all necessary metadata and links are included ([Atlassian Best Practices](https://www.atlassian.com/software/confluence/resources/guides/get-started/best-practices)).

## 4\. **Navigation And Discovery**

- **Table of Contents and Index Pages:** Use the “Children Display” macro or manually curated index pages to help users discover related content.

- **Search and Labels:** Encourage users to use Confluence’s search and label filters to find related pages quickly.

## 5\. **Content Reuse**

- **Excerpt and Include Macros:** If you have content that needs to appear in multiple places (like a requirement description), use the “Excerpt” and “Excerpt Include” macros to avoid duplication and ensure updates propagate everywhere ([Atlassian Documentation](https://confluence.atlassian.com/doc/develop-technical-documentation-in-confluence-226166494.html)).

## 6\. **Visual Cues and Summaries**

- **Info Panels and Status Macros:** Use

these to highlight key information, page summaries, or the status of a feature/requirement.

- **Page Summaries:** Add a TL;DR or summary section at the top of each page for quick context ([Atlassian Community](https://community.atlassian.com/forums/Confluence-articles/Tips-for-creating-impactful-pages-in-Confluence/ba-p/2968576)).

---

**In summary:**
Treat each page as an atomic object, use strong interlinking, leverage metadata (labels, page properties), and provide clear navigation aids. This will let users start at any point—FAQ, requirement, or feature—and traverse your documentation graph with ease.

For more detailed best practices, check out these resources:

- [Develop Technical Documentation in Confluence](https://confluence.atlassian.com/doc/develop-technical-documentation-in-confluence-226166494.html)

- [Tips for creating impactful pages in Confluence](https://community.atlassian.com/forums/Confluence-articles/Tips-for-creating-impactful-pages-in-Confluence/ba-p/2968576)

- \[Confluence Best

Practices\](<https://www.atlassian.com/software/confluence/resources/guides/get-started/best-practices>)

**User:**

How do I set up semantic search in confluence? Someone might have a question, but not have the exact same language as the FAQ in the knowledge base. I need a search than can use to find the appropriate content no just based on matching

**Abacus AI ChatLLM:**

> Routing to GPT-4.1

Web Search

How to set up semantic search in Confluence knowledge base

Search Results

- [Semantic Search - Luma Knowledge - Confluence - Atlassian](https://serviceaide.atlassian.net/wiki/spaces/LKms/pages/27035140228/Semantic+Search) (Web Search Result)
   Semantic search is an advanced information retrieval technique that enhances search accuracy by understanding the user's intent and the contextual meaning of query terms. Unlike traditional keyword-based searches, semantic search delves into the broader context, considering the relationships between words and the meanings of phrases.

- [Semantic Search in Confluence Wiki With LlamaIndex and Pinecone](https://medium.com/better-programming/semantic-search-in-confluence-wiki-with-llamaindex-and-pinecone-eb39c1d8c004) (Web Search Result)
   In this article, we explored a good use case — converting your company’s Confluence Wiki into an intelligent knowledge base where you can do semantic search to retrieve useful information.

- [Use Atlassian Intelligence to search for answers](https://support.atlassian.com/confluence-cloud/docs/use-atlassian-intelligence-to-search-for-answers/) (Web Search Result)
   Search Confluence with Atlassian Intelligence. Get answers from Atlassian Intelligence in both quick search and advanced search. If you need more information about an answer, review the linked sources. You can also rate or report the response.

- [Create a searchable knowledge base on Confluence - Atlassian Community](https://community.atlassian.com/t5/Confluence-questions/Create-a-searchable-knowledge-base-on-Confluence/qaq-p/2363922) (Web Search Result)
   Set up custom statuses "Irrelevant", "Expired", "Duplicate" and the corresponding CQL queries to find irrelevant content (party plans), outdated ideas, bug replications, etc. Then the app will classify each page and blog post and assign one of these statuses.

- [Confluence Search Syntax | Confluence Data Center 9.4 | Atlassian ...](https://confluence.atlassian.com/doc/confluence-search-syntax-158720.html) (Web Search Result)
   To create a search query using Confluence syntax: Click the search field at the top right of Confluence to open the expanded search panel. Type your query using syntax supported by Confluence. You can use multiple search words and operators in your query. Screenshot: an example of a search query using Confluence search syntax. Search for an ...

- [Knowledge base with Confluence - Atlassian](https://www.atlassian.com/software/confluence/resources/guides/best-practices/knowledge-base) (Web Search Result)
   Choose Space Settings in the left sidebar, then select “Space permissions” to set desired access for the space, including anonymous access. Use the Create button in the top navigation bar and use a how-to article template, troubleshooting article template, or others to create your first knowledge base document.

- [Semantic search for Confluence - Atlassian Community](https://community.atlassian.com/forums/Jira-Cloud-Admins-discussions/Semantic-search-for-Confluence/td-p/2139786) (Web Search Result)
   @Peter Richter I apologize as I didn't understand the semantic type of search. I believe your correct as this is not built into Confluence. My only other answer would be to look into the market place for an add-on that might offer this but I am not sure one exist. Both Jira and Confluence are both based on keywords and CQL and JQL for query ...

- [Confluence search syntax | Confluence Cloud - Atlassian Support](https://support.atlassian.com/confluence-cloud/docs/confluence-search-syntax/) (Web Search Result)
   To return ‘chicken' or 'chickpea’, search for: chick\* Multiple wildcards. Use multiple wildcards in your search to replace single and multiple characters. Example. To return 'chick', 'coconut', or 'chickpea', search for: c*c* You can also combine wildcard characters in one search. For example, the search term below will return 'chick' but ...

To set up **semantic search** in Confluence—so users can find relevant content even if their query doesn't exactly match the wording in your FAQs or documentation—here are your main options:

---

## 1\. **Atlassian Intelligence (Confluence Cloud Premium/Enterprise)**

Atlassian has introduced **Atlassian Intelligence**, which brings AI-powered semantic search to Confluence Cloud. With this feature, users can type natural language questions into the search bar, and the AI will return relevant answers based on the meaning, not just keyword matches. This is the most seamless way to get semantic search if you’re on a Premium or Enterprise plan.

- **How it works:** Users ask questions in their own words, and Atlassian Intelligence finds the best-matching content—even if the language is different.

- **How to enable:** It’s automatically activated for Premium and Enterprise plans, but admins can manage its availability.

- **More info:** \[Use Atlassian Intelligence to search for

answers\](<https://support.atlassian.com/confluence-cloud/docs/use-atlassian-intelligence-to-search-for-answers/>)

---

## 2\. **Third-Party Semantic Search Solutions**

If you’re not on a Premium/Enterprise plan, or want more control, you can integrate external semantic search tools. For example, you can use **LlamaIndex** to ingest your Confluence content and store embeddings in a vector database like **Pinecone**. This allows you to build a custom semantic search or chatbot interface over your Confluence knowledge base.

- **How it works:** Extract Confluence content, generate vector embeddings, and use a vector database to perform semantic search.

- **Example guide:** [Semantic Search in Confluence Wiki With LlamaIndex and Pinecone (Medium)](https://medium.com/better-programming/semantic-search-in-confluence-wiki-with-llamaindex-and-pinecone-eb39c1d8c004)

- **Note:** This approach requires technical setup and possibly developer resources.

---

## 3\. **Marketplace Apps**

Currently, there are limited plug-and-play semantic search apps for Confluence in the Atlassian Marketplace, but this is a space to watch as AI search becomes more common. Some apps may offer enhanced search or AI-powered features—search the [Atlassian Marketplace](https://marketplace.atlassian.com/) for "semantic search" or "AI search" for the latest options.

---

## 4\. **Best Practices for Improving Search (if Semantic search isn’t available)**

- Use **labels** and **consistent terminology** across pages.

- Organize content into logical spaces and use macros like "Content by Label" or "Live Search" to help users filter results.

- Train users to use advanced search syntax, but this is still keyword-based ([Confluence Search Syntax](https://confluence.atlassian.com/doc/confluence-search-syntax-158720.html)).

---

## **Summary Table**

| Solution | Semantic? | Setup Effort | Notes | 
|---|---|---|---|
| Atlassian Intelligence | Yes | Low |  | 
| Built-in for Premium/Enterprise Cloud |  |  |  | 

| LlamaIndex + Pinecone (Custom) | Yes | High | Developer resources needed |

| Marketplace Apps | Maybe | Medium | Check for latest offerings |

| Labels, Macros, Syntax | No | Low | Improves keyword search only |

---

**Recommendation:**
If you’re on Confluence Cloud Premium or Enterprise, enable and use Atlassian Intelligence for the best out-of-the-box semantic search. If not, and you have technical resources, consider building a custom solution with LlamaIndex and Pinecone. Otherwise, focus on content organization and labeling to improve traditional search.

Let me know if you want a step-by-step guide for any of these options!

**User:**

Describe this same knowledge base idea but using the m365 ecosystem. How could I achieve the same thing

**Abacus AI ChatLLM:**

> Routing to GPT-4.1

Great question! The Microsoft 365 (M365) ecosystem offers a rich set of tools for building a **semantic, interconnected, atomic knowledge base**—similar to what you’d do in Confluence, but with Microsoft’s stack. Here’s how you can achieve the same effect, with some best practices and tool recommendations:

---

## **1\. Core Tools for a Knowledge Base in M365**

- **SharePoint Online:** The primary platform for building structured, interlinked documentation and knowledge bases.

- **Microsoft Search:** Provides enterprise-wide search, including semantic capabilities (especially with Copilot and AI integrations).

- **OneNote:** For more informal, atomic notes or team wikis.

- **Viva Topics:** For AI-driven topic discovery, semantic linking, and knowledge surfacing.

- **Teams:** For chat-based Q&A, quick access, and embedding knowledge base links.

---

## **2\. Building Atomic, Interconnected Pages**

**SharePoint Online** is your best bet for atomic, self-contained pages:

- Create a **SharePoint site** (or

hub site) dedicated to your product knowledge base.

- Each **SharePoint page** represents a single feature, requirement, or FAQ—just like atomic objects.

- Use **metadata columns** (custom columns in document libraries or lists) to tag pages with type (feature, requirement, FAQ), status, owner, etc.

- Use **page links** and **web parts** (like “Highlighted Content” or “Link” web parts) to interconnect related pages. For example, a FAQ page can link to the relevant feature and requirement pages, and vice versa.

---

## **3\. Semantic Search in M365**

- **Microsoft Search** (in SharePoint, [Office.com](http://Office.com), Bing for Business) uses AI to understand intent, not just keywords. Users can ask questions in natural language, and Microsoft Search will surface the most relevant pages, even if the wording is different.

- **Viva Topics** (add-on): Uses AI to automatically identify topics (like features, requirements, etc.) across your content, creates topic cards, and links related content. When someone hovers over a topic,

they see a summary and links to all related knowledge base pages.

---

## **4\. Metadata and Navigation**

- Use **custom columns** in SharePoint libraries/lists for structured metadata (e.g., “Type”, “Related Feature”, “Related Requirement”).

- Use **Managed Metadata Service** for consistent tagging across your site.

- Build **custom views** and **filters** so users can browse by feature, requirement, FAQ, etc.

- Use **site navigation** and **hub site navigation** to create a traversable structure.

---

## **5\. Content Reuse and Consistency**

- Use **SharePoint page templates** for each type of knowledge base page (feature, requirement, FAQ) to ensure consistency.

- Use **web parts** like “Reusable Content” or “Embed” to include shared snippets across multiple pages.

- For more dynamic reuse, consider **OneNote** for quick, atomic notes that can be linked into SharePoint.

---

## **6\. Example User Journey**

- A user searches “How do I reset my password?” in SharePoint or [Office.com](http://Office.com).

- \*\*Microsoft

Search\*\* surfaces the relevant FAQ, even if the page is titled “Password Recovery Process.”

- The FAQ page links to the “Password Feature” page and the “Security Requirements” page.

- Each page is atomic, up-to-date, and the single source of truth for that topic.

---

## **7\. Advanced: Copilot and Viva Topics**

- **Copilot for Microsoft 365** (if licensed) can answer natural language questions by searching your SharePoint knowledge base, emails, Teams chats, and more.

- **Viva Topics** automatically builds a semantic map of your knowledge, making it even easier to traverse and discover related content.

---

## **Summary Table**

| Confluence Concept | M365 Equivalent | Notes | 
|---|---|---|
| Atomic Page | SharePoint Page | Each page = one feature/FAQ/requirement | 
| Labels/Metadata | SharePoint Columns/Tags |  | 

    | Use custom columns, managed metadata       |  

| Interlinking | Page Links, Web Parts | Use links, Highlighted Content, navigation |

| Semantic Search | Microsoft Search, Viva Topics | AI-powered, natural language, topic cards |

| Content Reuse | Page Templates, Reusable Parts | Templates, reusable content web parts |

| Traversable Graph | Navigation, Viva Topics | Topic cards, site navigation, Copilot |

---

**In short:**
You can absolutely build a semantic, interconnected, atomic knowledge base in M365 using SharePoint, Microsoft Search, and (optionally) Viva Topics and Copilot. The experience will be modern, AI-powered, and scalable—very similar to what you’d achieve in Confluence, but with the added benefit of deep integration into the rest of the M365 ecosystem.

If you want a step-by-step setup guide or a sample SharePoint site structure, just let me know!

**User:**

Compare the 2 options on ease of use and content discoverablity

**Abacus AI ChatLLM:**

> Routing to GPT-4.1

Okay, let's compare Confluence and Microsoft 365 (SharePoint Online + related tools) specifically on **ease of use** and **content discoverability** for building a semantic, interconnected knowledge base.

---

## **Ease Of Use**

### **Confluence**

- **Pros:**

   - **Simpler out-of-the-box experience:** Confluence is designed primarily as a collaboration and documentation platform. Creating pages, adding content, and linking pages is generally straightforward.

   - **Clear focus on content creation:** The editor is intuitive, and the platform encourages content creation and collaboration.

   - **Macros:** Macros provide a lot of functionality without needing code (e.g., Table of Contents, Excerpts, Page Properties).

- **Cons:**

   - **Customization limitations:** While flexible, deep customization (like custom search or complex metadata) often requires Marketplace apps or some technical knowledge.

   - **Admin overhead:** Managing a large, complex Confluence instance can become challenging,

especially without a dedicated admin.

### **Microsoft 365 (SharePoint Online)**

- **Pros:**

   - **Deep integration:** Seamless integration with other M365 apps (Teams, Office, etc.) can be a huge advantage for organizations already invested in the ecosystem.

   - **Power and flexibility:** SharePoint offers immense power and flexibility for customization, workflows, and governance.

- **Cons:**

   - **Steeper learning curve:** SharePoint can be overwhelming for new users. Setting up sites, libraries, metadata, and navigation requires more planning and technical knowledge.

   - **Complexity:** The sheer number of options and settings can make it harder to get started and maintain a clean, user-friendly experience.

   - **Admin-heavy:** SharePoint often requires more administrative overhead, especially for managing permissions, governance, and complex workflows.

### **Ease Of Use Verdict:**

- **Confluence wins on initial ease of use.** It's quicker to get started and create content.

- \*\*SharePoint

wins on long-term power and integration,\*\* but requires more effort to set up and maintain.

---

## **Content Discoverability**

### **Confluence**

- **Pros:**

   - **Good built-in search:** Confluence search is generally effective for keyword-based queries.

   - **Labels:** Labels are easy to add and use for filtering content.

   - **Macros for navigation:** Macros like "Children Display" and "Content by Label" help users find related content.

- **Cons:**

   - **Limited semantic search:** Without Atlassian Intelligence (Premium/Enterprise) or third-party integrations, search relies heavily on keyword matching.

   - **Information architecture:** A poorly organized space can make it difficult for users to find what they need.

### **Microsoft 365 (SharePoint Online)**

- **Pros:**

   - **Microsoft Search:** AI-powered search understands intent and context, providing more relevant results.

   - **Viva Topics:** Automatically surfaces related content and experts, making it easier to discover

knowledge.

    - **Metadata-driven navigation:** Well-defined metadata and custom views can guide users to the right content.

- **Cons:**

   - **Setup complexity:** Getting the most out of Microsoft Search and Viva Topics requires careful planning and configuration.

   - **Overwhelming search results:** If not properly configured, Microsoft Search can return too many results, making it hard to find the best answer.

### **Content Discoverability Verdict:**

- **Microsoft 365 (with Microsoft Search and Viva Topics) has the edge on semantic search and AI-driven discovery.**

- **Confluence is good for keyword-based search and structured navigation,** but requires more manual effort to organize content.

---

## **Summary Table**

| Feature | Confluence | Microsoft 365 (SharePoint Online) | 
|---|---|---|
| \*\*Ease |  |  | 

of Use\*\* | Easier to get started, intuitive editor | Steeper learning curve, requires more planning and admin |

| **Content Creation** | Simple, focused on content creation | Powerful, but can be overwhelming |

| **Search** | Good keyword-based search, limited semantic | AI-powered search (Microsoft Search, Viva Topics), more semantic |

| **Navigation** | Macros, labels, structured spaces | Metadata-driven views, site navigation, Viva Topics |

---

**Overall Recommendation:**

- **Choose Confluence if:** You need a quick, easy-to-use documentation platform with a focus on content creation and collaboration.

- **Choose Microsoft 365 (SharePoint Online) if:** You're already heavily invested in the M365 ecosystem, need powerful semantic search, and are willing to invest the time and effort to set up and maintain a more complex system.

Ultimately, the best choice depends on your organization's needs, technical

expertise, and existing infrastructure.

**User:**

We do our dev work using Jira and use confluence for documentation so it would probably be easier to get going. The only problem is our non technical people use m365 and the knowledge base is mostly for them

**Abacus AI ChatLLM:**

> Routing to GPT-4.1

Okay, that's a key piece of information! Given that your dev team is already comfortable with Jira and Confluence, and your non-technical users primarily use M365, here's a revised recommendation:

**Hybrid Approach: Best of Both Worlds**

Instead of choosing one platform, consider a hybrid approach that leverages the strengths of both Confluence and Microsoft 365, while addressing the needs of both your technical and non-technical teams.

Here's how you can make it work:

1. **Primary Knowledge Base in Confluence:**

   - Keep your core product documentation, feature specifications, requirements, and FAQs in Confluence, where your dev team is already working.

   - Use the strategies we discussed earlier (atomic pages, interlinking, labels, page properties) to build a well-structured, traversable knowledge graph.

2. **Surface Confluence Content in Microsoft 365:**

   - **Link to Confluence pages from SharePoint:** Create a landing page or hub in SharePoint Online for your non-technical users. This

page can contain links to key Confluence pages, organized by topic or user role.

- **Embed Confluence pages in Teams:** Use the Confluence app for Microsoft Teams to embed relevant Confluence pages directly into Teams channels. This allows non-technical users to access documentation without leaving their primary workspace.

- **Use Microsoft Search to find Confluence content:** Configure Microsoft Search to index your Confluence instance. This allows users to search for Confluence pages directly from SharePoint, [Office.com](http://Office.com), or Bing for Business.

1. **Bridge the Gap with Integrations:**

   - **Jira-Confluence integration:** Ensure your Jira issues are linked to relevant Confluence pages. This provides a seamless connection between development tasks and documentation.

   - **Consider a Confluence-SharePoint connector:** While not a native feature, some third-party connectors can sync content or metadata between Confluence and SharePoint. This could automate the process of surfacing Confluence

content in M365.

**Benefits of this Hybrid Approach:**

- **Leverages existing workflows:** Your dev team continues to use Jira and Confluence, while your non-technical users stay within their familiar M365 environment.

- **Centralized knowledge:** Confluence remains the single source of truth for product knowledge.

- **Easy access for non-technical users:** M365 integrations make it easy for non-technical users to find and access Confluence content without needing to learn a new platform.

- **Semantic search in M365:** By indexing Confluence in Microsoft Search, you can provide semantic search capabilities to your M365 users.

**Implementation Steps:**

1. **Set up your knowledge base in Confluence:** Follow the best practices we discussed earlier.

2. **Create a SharePoint landing page:** Design a user-friendly landing page in SharePoint with links to key Confluence pages.

3. **Install the Confluence app for Teams:** Add the Confluence app to relevant Teams channels and embed important

documentation.

1. **Configure Microsoft Search:** Follow Microsoft's documentation to connect Confluence as a data source for Microsoft Search.

2. **Train your users:** Provide training to both your technical and non-technical teams on how to use the new system.

**Considerations:**

- **Content synchronization:** If you need more than just links, explore third-party connectors for syncing content between Confluence and SharePoint.

- **Permissions:** Carefully manage permissions in both Confluence and SharePoint to ensure that users have access to the right content.

- **Maintenance:** Regularly review and update your knowledge base to keep it accurate and relevant.

**In summary:**

A hybrid approach allows you to leverage the strengths of both Confluence and Microsoft 365, providing a seamless knowledge base experience for all your users. By keeping your core documentation in Confluence and surfacing it in M365, you can ensure that everyone has access to the information they need, regardless of

their preferred platform.

Does this sound like a viable solution for your organization?

**User:**

Help me set up the SharePoint page with links to confluence

**Abacus AI ChatLLM:**

> Routing to GPT-4.1

Absolutely! Here’s a step-by-step guide to set up a **SharePoint Online page** that acts as a friendly landing hub for your non-technical users, with clear links to your Confluence knowledge base content.

---

## **Step 1: Plan Your SharePoint Landing Page**

Decide what you want to feature:

- Main categories (e.g., FAQs, Features, Requirements, How-To Guides)

- Quick links to most-used Confluence pages

- Search tips or instructions

- Contact/support info

---

## **Step 2: Create a New SharePoint Page**

1. **Go to your SharePoint site** (or create a new Communication Site for this purpose).

2. In the left menu, click **New** > **Page**.

3. Choose a layout (the “Blank” or “Visual” template is a good starting point).

---

## **Step 3: Add Sections and Web Parts**

1. **Add a Title** (e.g., “Product Knowledge Base” or “Support Center”).

2. **Add a Text Web Part** for a welcome message or instructions.

3. **Add a Quick Links Web Part:**

   - Click the **\+** icon to add a new web part.

   - Search for

and select **Quick Links**.

    - Click **Add link** and paste the URL of your Confluence page (e.g., your FAQ, feature list, or main knowledge base page).

    - Give each link a friendly name (e.g., “Product FAQs”, “Feature Documentation”, “Submit a Request”).

    - You can add icons or images for visual appeal.

1. **(Optional) Add a Hero Web Part:**

   - This is a large, visual section at the top for your most important links.

   - Add the Hero web part and configure tiles to link to your top Confluence pages.

---

## **Step 4: Get Confluence Page URLs**

- Open each Confluence page you want to link.

- Copy the URL from your browser.

- Paste it into the Quick Links or Hero web part in SharePoint.

---

## **Step 5: Organize and Publish**

- Arrange your links in logical groups (e.g., “Getting Started”, “Troubleshooting”, “Policies”).

- Add any other helpful web parts (e.g., a People web part for support contacts, or a File Viewer for downloadable resources).

- Click **Publish** when you’re

ready.

---

## **Step 6: Share and Promote**

- Share the SharePoint page link with your non-technical users.

- Pin it as a tab in Microsoft Teams channels if you use Teams.

- Add it to your company intranet or send it in onboarding materials.

---

## **Tips For a Great Experience**

- **Use clear, non-technical language** for link names and instructions.

- **Group related links** for easy scanning.

- **Add a “How to use this page” section** if your users are new to SharePoint or Confluence.

- **Keep the page updated** as your Confluence content grows or changes.

---

## **Example Layout**

**Title:** Product Knowledge Base
**Welcome Text:** “Welcome! Here you’ll find links to all our product documentation, FAQs, and support resources.”
**Quick Links:**

- Product FAQs (link to Confluence FAQ page)

- Feature Documentation (link to Confluence features page)

- Submit a Support Request (link to Confluence or Jira Service Desk)

- Getting Started Guide (link to onboarding doc)
   \*\*Support

Contacts:\*\*

- \[Add a People web part or contact info\]

---

If you want a sample SharePoint page structure or screenshots, let me know your preferred categories or the main Confluence pages you want to feature, and I can mock up a more tailored example!

**User:**

And how do I then use those confluence pages as data sources for ms search

**Abacus AI ChatLLM:**

> Routing to GPT-4.1

Great follow-up! **Making your Confluence pages searchable from Microsoft Search** (so users can find them from SharePoint, [Office.com](http://Office.com), or Bing for Business) is a powerful way to bridge the two ecosystems.

Here’s how you can do it:

---

## **1\. Use Microsoft Graph Connectors for Confluence**

Microsoft Search supports **external connectors** (called Microsoft Graph Connectors) that let you index content from third-party sources—including Confluence Cloud and Confluence Server/Data Center.

### **What This means:**

- Your Confluence pages become searchable from the Microsoft 365 search bar (in SharePoint, [Office.com](http://Office.com), Bing for Business, etc.).

- Users can find Confluence content using the same search experience as their M365 files and sites.

---

## **2\. Steps to Set Up the Confluence Graph Connector**

### **A. Prerequisites**

- You need to be a Microsoft 365 admin.

- You need admin access to your Confluence instance.

- Your organization must have Microsoft Search (included in most M365 busines

s/enterprise plans).

### **B. Choose the Right Connector**

- **Confluence Cloud:** Use the official [Atlassian Confluence Cloud Graph Connector](https://learn.microsoft.com/en-us/microsoftsearch/confluence-cloud-connector).

- **Confluence Server/Data Center:** Use the [Confluence On-Premises Graph Connector](https://learn.microsoft.com/en-us/microsoftsearch/confluence-onprem-connector).

### **C. Set Up the Connector**

1. Go to the [Microsoft 365 Admin Center](https://admin.microsoft.com/).

2. Navigate to **Settings** > **Search & intelligence** > **Data sources**.

3. Click **\+ Add** and select **Confluence Cloud** (or Server, as appropriate).

4. Follow the setup wizard:

   - **Authenticate** with your Confluence instance.

   - **Configure** what content to index (spaces, pages, permissions, etc.).

   - **Map properties** (metadata) if needed.

   - **Set up refresh schedules** (how often to sync new/updated content).

5. **Finish and save** the connector.

### **D. Permissions**

- The connector can

respect Confluence permissions, so users only see content they’re allowed to access.

---

## **3\. What Happens Next?**

- After setup, Microsoft Search will crawl and index your Confluence content.

- Users can search for Confluence pages from SharePoint, [Office.com](http://Office.com), or Bing for Business.

- Search results will show Confluence pages alongside SharePoint and OneDrive files, with a “Confluence” label.

---

## **4\. Resources and Documentation**

- [Confluence Cloud Graph Connector setup guide (Microsoft Docs)](https://learn.microsoft.com/en-us/microsoftsearch/confluence-cloud-connector)

- [Overview of Microsoft Graph Connectors](https://learn.microsoft.com/en-us/microsoftsearch/connectors-overview)

- [Atlassian’s own documentation on Microsoft Search integration](https://support.atlassian.com/confluence-cloud/docs/integrate-confluence-cloud-with-microsoft-search/)

---

## **5\. Tips**

- **Test with a small set of spaces/pages first** to ensure permissions and indexing work as expected.

- \*\*Communicate to

users\*\* that they can now find Confluence content from their familiar M365 search bar.

- **Review search analytics** in the Microsoft 365 admin center to see what users are searching for and optimize your content.

---

**In summary:**
Set up the Confluence Graph Connector in Microsoft 365 Admin Center, configure it to index your Confluence pages, and your users will be able to discover Confluence knowledge base content directly from Microsoft Search—no extra training or switching platforms needed!

If you want a step-by-step walkthrough with screenshots or have a specific scenario (Cloud vs. Server, permissions, etc.), let me know!

**User:**

These are my licenses. Is that enough to set up this search across m365 and confluence?

**Abacus AI ChatLLM:**

> Routing to GPT-4.1

Based on your screenshot, your current Microsoft 365 licenses are:

- **Azure Active Directory Premium P1**

- **Microsoft 365 Business Basic**

- **Microsoft Entra Suite Trial**

- **Office 365 E3**

- **Power BI Pro**

**Key points for Microsoft Search with Confluence:**

1. **Microsoft Search** is included with most Microsoft 365 business and enterprise subscriptions, including Business Basic and Office 365 E3. This means you have access to Microsoft Search features in SharePoint, [Office.com](http://Office.com), and Bing for Business.

2. **Graph Connectors** (to connect external data sources like Confluence) are available for Microsoft 365 enterprise customers. However, some advanced connectors and features may require Microsoft 365 E5 or additional licensing, but the basic connector for Confluence Cloud is available for E3 and above.

3. **Admin Access:** You’ll need admin rights to set up and configure the connector in the Microsoft 365 Admin Center.

**What you have:**

- **Office 365 E3**: Sufficient for Microsoft Search and

Graph Connectors.

- **Microsoft 365 Business Basic**: Also supports Microsoft Search, but Graph Connectors are best supported with E3/E5.

- **No E5 or Microsoft Viva licenses**: You won’t have access to some advanced AI/semantic features (like Viva Topics), but you can still index and search Confluence content.

**Summary:**
**Yes, your current licenses (especially Office 365 E3) are enough to set up Microsoft Search and connect to Confluence using the Microsoft Graph Connector.** You can make your Confluence pages searchable from SharePoint and other M365 search endpoints for your users.

If you want advanced AI-driven topic cards (Viva Topics) or analytics, you’d need additional Viva licenses, but for basic search and content discoverability, you’re good to go!

Let me know if you want a step-by-step guide for setting up the connector.