# Gemini CLI: Google's NEW Fully Free Opensource Coding Agent! Beats Claude Code!

![rw-book-cover](https://wsrv.nl/?url=https%3A%2F%2Fstorage.googleapis.com%2Fsnipd-public%2Fsideload%2Fsideload_image.png&w=512&h=512)

## Metadata
- Author: [[Your uploads]]
- Full Title: Gemini CLI: Google's NEW Fully Free Opensource Coding Agent! Beats Claude Code!
- Category: #podcasts
- URL: https://share.snipd.com/episode/816ee706-f3ff-496c-af60-67fb9c884bc5

## Highlights
- **Step-by-Step Instructions to Set Up Gemini CLI**
  **Prerequisites:**
  - Ensure you have **Node.js version 18 or higher** installed. 
  **Installation Steps:**
  1. **Open your terminal or command prompt.**
  2. **Install Gemini CLI using npx:**
  - Run the command: 
  ```bash
  npx @google-gemini/gemini-cli
  ``` 
  - Confirm installation by pressing **Y** when prompted. 
  3. **Alternatively, install via NPM:**
  - Run: 
  ```bash
  npm install -g @google-gemini/gemini-cli
  ``` 
  - After installation, start Gemini CLI with: 
  ```bash
  gemini
  ``` 
  4. **Configure the CLI:**
  - Choose your **theme** (default or others). 
  - Authenticate with your **Google account** or provide a Gemini API key for higher limits. 
  - For API key setup, follow the instructions to generate one from your Google account or use the free Google login for 1,000 requests/day. 
  5. **Start using Gemini CLI:**
  - Once logged in, you can type prompts, run commands, and integrate with your workflows directly in your terminal. 
  - Example: Type `write me a web scraper` or `summarize recent changes in my repo`. 
  **Additional Tips:**
  - **Clone repositories** and then run `gemini` inside the directory to work on specific projects. 
  - Explore commands like `search`, `clear`, `stats`, and integrate with MCP servers for extended functionality. 
  **Note:** 
  - Keep your Node.js updated. 
  - Refer to the [Github repo](https://github.com/google-gemini/gemini-cli) for detailed documentation and troubleshooting.
  Transcript:
  World of AI
  Now to get started it's really simple. It's something that will require you to have Node.js version 18 or higher so make sure you have this installed. I'll leave a link to this as well as everything else in the description below. But once you have this prerequisite fulfilled you can run this within the CLI. This is the command that you can use with npx. So simply open up your command prompt and simply paste in this command, which will work on installing the Gemini CLI into your terminal. All you need to do is click on Y to proceed the installation process, which will install the packages. And once that is complete, we can simply install or start it up with the Gemini command, which is a simple single command that you can then paste in, which is in your terminal. You also have the ability to install this using NPM after it'll open up. And this is what you'll be greeted with. This is the Gemini CLI. And you first have the ability to select the theme. So you can choose the default theme. You can choose different sorts of themes that fit your requirement. So in this case, I'm just going to leave it as the default one. After selecting the theme, you can then have it so that you can select the authentication method, you can log in with your Google account, or you can provide a Gemini API key. And this is so that you can use it for advanced use cases and increased limits. So this way, if you want to use it for more than 60 generations or requests an hour, or for more than 1,000 requests a day, you can then use your own API key. But you can simply authenticate with a Google account, which is completely free, and you will be able to access it 100% for free for 1,000 requests a day. So I'm going to authenticate with the Google account. After you finish authenticating it, you're going to be then greeted with this interface. And this is where you can then start typing in a message or you can add a certain type of path that you want to work in. Now, what they recommend is that you CD into a new project and then implement the Gemini command to start up the CLI and then you can have it do anything like write me a Gemini Discord bot That answers questions using FAQ or you can do something like have it deployed into an existing project where you clone it and then you can CD into the Gemini CLI directory and then you Can start up Gemini and you can ask it to give me a summary of all the changes that went in yesterday so let's actually try this out to showcase how it works so what i can do is simply within A new terminal i can open it up i can clone this repository of gemini cli and then i can head over into that cli directory so once it has finished cloning, I can then go into it. And then I can type in Gemini to start up the CLI. And then now I can write in any sort of prompt, like giving me a summary of all the changes that went in since I'm in that directory itself. So I can click enter and you can see right away it is going to work on executing this task. So right now it is working on determining the scope, figuring out what went through using web searching capabilities and it'll go through each step with you. So there's a human in the loop aspect to it. You can allow it once, you can allow always with the git command or you can click no so in this case i'm gonna allow it always to expedite this process and let's see what it was capable of Outputting for us and there we go we have an output this is where it talks about the new implementations of the key features and fixes the oauth 429 failover, the documentation and user Experiences. And these are some of the things that were changed within the GitHub repository of Google CLI. What's also cool is that you can connect to tools and MCP servers, and this is where you can have it even generate images using VO. So if you actually click on this, there's a couple of MCP servers for Google Cloud Gen Media APIs that you can actually work with. This is where you can have it create 30 second videos of anything. So in this case, you can see that there's a video of a cat that is being generated on a plane. Now, if you click on the slash command, there's so many different commands that you can use from asking about the version itself, authentication, clearing the chat, using MCPs. And they actually have an MD that talks about the configurations of MCPs, which I'll leave a link to in the description below. It's super simple to set up and there's a step-by process as to how you can use and set up MCPs. But going back into the CLI, you also have the ability to use various sorts of things like submitting a bug report and clear the chat obviously compress the context by replacing it with A summary open the full uh gemini cli documentation the editor uh and you also have so many other things like memory stats uh theme and the best part is there's external tools that you Can implement there's already built-in tools that are already within the CLI like the read folder read file searching text google search and so much more like saving memory so I can Do things like giving me the stats for my current session and it'll tell you the current tokens that were used, the input tokens and the output tokens. And then I can do something like using tools. This is where I can use something like Google search. So I can say search or tell me about the weather in New York City today. And then it is going to work on finding that using the Google search tool. It's going to search the web and give me the weather in NYC. Obviously, this is something that I wouldn't use within a CLI, but it's just to demonstrate the tool. And you can see right now it is talking about how hot it is in New York City. But let's do something else now. Let's clear the chat and let's say create a web app that is an image editor. And it is quite modern with a lot of features. Now let's send in this prompt and let's see what it's capable of outputting and how it's able to make the changes as well as the steps it takes to develop this web app and just like that it Was able to create our image app and this is where we can simply upload our image this is where i uploaded this and there's so many different tools that it had worked on so in this case i can Change the contrast i can change the brightness i can even change the hue. We're going to leave that as that. There's also custom filters that were already developed. You can even draw certain things within the actual editor itself. You can highlight certain sections. And there's a lot of different things that it was able to develop all on its own. ([Time 0:03:24](https://share.snipd.com/snip/6a24a454-17a9-4911-811b-5d05751cb014))
