# Gemini Developer API

![rw-book-cover](https://ai.google.dev/static/site-assets/images/share-gemini-api.png)

## Metadata
- Author: [[Google AI for Developers]]
- Full Title: Gemini Developer API
- Category: #articles
- Summary: The Gemini Developer API lets you access AI models quickly. You can get an API key and start making requests in minutes. The example shows how to ask the AI to explain a topic simply.
- URL: https://share.google/K0coNq1SNFJ6eBGI0

## Full Document
Get a Gemini API key and make your first API request in minutes.

```
from google import genai

client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Explain how AI works in a few words",
)

print(response.text)

```

![](https://ai.google.dev/static/site-assets/images/image-generation-index.png)
![](https://ai.google.dev/static/site-assets/images/long-context-overview.png)
![](https://ai.google.dev/static/site-assets/images/structured-outputs-index.png)
