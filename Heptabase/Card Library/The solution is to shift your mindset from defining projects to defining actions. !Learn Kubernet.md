---
created: 2026-05-04T08:01:26+00:00
modified: 2026-05-08T12:53:45+00:00
title: The solution is to shift your mindset from defining projects to defining actions. !Learn Kubernet
---

The solution is to shift your mindset from defining projects to defining actions. "Learn Kubernetes" is a project; it's a goal. It's not a task you can do in a single sitting. The trick is to break these projects down into a series of small, concrete, physical actions.

Here is a framework and a set of principles to help you define tasks effectively.

## The "Verb-Noun-Quantity" Framework

Every task you write down should be answerable by this simple structure. It forces clarity and gives you a clear "done" condition.

- Start with a specific Action Verb: Replace vague verbs like "learn," "organise," or "work on" with concrete, physical actions.
   - Instead of "learn," use Watch, Read, Write, Follow, Complete, Draft.
   - Instead of "organise," use Move, Create, Rename, Delete, List.
   - Instead of "document," use Outline, Write, Ask, Review, Diagram.
- Add a specific Noun: What exactly are you acting upon? Be precise.
   - Don't just say "read the docs"; say "read the 'Introduction to Pods' page on the Kubernetes website."
   - Don't just say "create a file"; say "create the [vpc.tf](http://vpc.tf) file."
- Define a Quantity or Time Limit: This is the secret to making tasks fit into time blocks. It defines the boundary and tells you when you are finished for now.
   - "Watch the first 20 minutes of the video…"
   - "Write three bullet points for the outline…"
   - "Complete one tutorial module…"
   - "Spend one 25-minute time block refactoring…"

### Applying the Framework to Your Examples

Let's break down your specific projects into actionable, time-block-friendly tasks.

Project: "Learn Kubernetes"

This is a huge topic. The first step is to break it down into learning modules.

- Vague Task: Learn Kubernetes
- Actionable Tasks:
   - Watch the first 25-minute video of 'Kubernetes for Beginners' on YouTube.
   - Read the 'Introduction' and 'Objects' sections of the official Kubernetes documentation.
   - Follow the official tutorial to install Minikube on my laptop.
   - Write a list of 5 key terms I learned from the introduction (e.g., Pod, Node, Deployment).
   - Run the kubectl get nodes command and screenshot the output.
      Each of these is a small, completable action that fits perfectly into a 30-60 minute time block. Finishing one gives you a sense of momentum.
      Project: "Document our deployment process"
      This involves investigation and writing. You can't do it all at once.

- Vague Task: Document our deployment process
- Actionable Tasks:
   - Create a new blank document in Confluence/Google Docs titled "Deployment Process Draft".
   - Outline the 5 main stages of deployment as I currently understand them in a bulleted list.
   - Schedule a 20-minute chat with \[Team Member's Name\] to ask about the front-end build step.
   - Review the [deploy-staging.sh](http://deploy-staging.sh) script and write comments for the first 10 lines to explain what they do.
   - Draw a simple flowchart of the process from 'git push' to 'live on server' using a tool like [diagrams.net](http://diagrams.net).
      Project: "Organise our infrastructure code"
      "Organise" is subjective. You need to define what an organised state looks like and then take small steps to get there.

- Vague Task: Organise our infrastructure code
- Actionable Tasks:
   - List all the current Terraform files and their locations in a temporary text file.
   - Research three different Terraform project structure guides and save the links.
   - Create a new folder named /networking.
   - Move the single file [vpc.tf](http://vpc.tf) from the root into the new /networking folder.
   - Run terraform plan to confirm that moving the file didn't break anything.
      The Ultimate Question for When You Are Stuck
      If you are ever looking at a task and feeling overwhelmed, ask yourself:

> "What is the smallest possible physical action I can take to move this forward?"

The answer isn't "write the document". It might be:

- "Open my text editor."
- "Create a new file."
- "Save the file as [README.md](http://README.md)."
- "Write the main heading."
   By practising this skill of breaking large projects into tiny, verb-driven actions, you will find it much easier to use your time blocks effectively. The goal is to make the next step so small and obvious that it's easier to do it than to procrastinate on it.

Excellent question. Defining learning goals effectively is the strategic layer that sits on top of defining daily tasks. If you get this right, breaking them down into actionable steps becomes much simpler. Just like with tasks, the key is to move from vague aspirations to concrete, measurable outcomes.

Let's build a systematic approach for you to define any learning goal, using the same principles of clarity and structure that help manage ADHD and procrastination.

The Problem with Vague Learning Goals

A goal like "Learn Kubernetes" is an aspiration, not a plan. It's unclear, immeasurable, and has no end point, which makes it perfect for procrastination. Your brain doesn't know what to do with it, so it does nothing.

We can fix this by using a two-part system:

- Define the Destination: Using a modified SMART framework to define what "done" looks like.
- Map the Journey: Breaking the goal down into a personal curriculum of projects and knowledge blocks.
   Part 1: Define the Destination with SMART-P Goals
   The standard SMART framework (Specific, Measurable, Achievable, Relevant, Time-bound) is a great start, but for learning, the "Measurable" part needs a specific focus on application. I call this SMART-P, where the 'P' stands for Project-Based.

- Specific: What, exactly, do you want to learn? Go one level deeper than the subject name.
   - Instead of: "Learn Python."
   - Try: "Learn to use Python for data analysis with the Pandas library."
- Project-Based (The new 'M'): How will you prove you've learned it? A goal isn't "knowing" something; it's being able to do something. Define a tangible project you can build.
   - Instead of: "I'll know it when I feel comfortable."
   - Try: "I will build a small application that scrapes data from a website and saves it to a CSV file."
- Achievable: Is this project realistic given your current knowledge and available time?
   - Instead of: "I will build a full social media site in a month."
   - Try: "I will build a command-line tool that lets me post updates to Twitter."
- Relevant: Why do you want to learn this? Connecting it to a personal interest or a career goal provides the motivation to push through challenges.
   - Example: "Learning this will allow me to automate a boring part of my job" or "This will help me build the personal project I've always dreamed of."
- Time-bound: When will you complete this project? A deadline creates focus.
   - Example: "I will have a working version of my web scraper by the end of next month."
      Putting it all together, "Learn Python" becomes:

> "My goal is to learn data analysis with Python's Pandas library (Specific). I will prove this by building a program that can analyse my monthly spending from a bank CSV file and generate a summary report (Project-Based & Achievable). I'm doing this to better manage my personal finances (Relevant), and I will have the report-generating script finished in 6 weeks (Time-bound)."

Part 2: Map the Journey from Goal to Tasks

Now that you have a clear destination (your project), you can work backwards to create a curriculum. This turns the overwhelming "learning" phase into a structured plan.

Step 1: Identify the Core Knowledge Blocks (Your "Curriculum")

What are the major concepts or skills you need to complete your project? Don't worry about details yet, just the main chapter headings.

- Goal: "Learn Kubernetes"
- Project: "Deploy my personal blog as a containerised application on a managed Kubernetes cluster."
- Core Knowledge Blocks:
   - Containerisation Fundamentals (What is Docker? How to build an image?)
   - Kubernetes Architecture (Nodes, Pods, Deployments, Services)
   - Writing Kubernetes Manifest (YAML files)
   - Networking in Kubernetes (How does traffic get to my app?)
   - Managing Secrets and Configs
   - Deploying to a Cloud Provider (e.g., GKE or EKS)
      Step 2: Break Each Block into Actionable Learning Tasks
      This is where you connect back to our previous conversation. For each block, define the small, verb-driven tasks you can timebox.

- From Block 1: "Containerisation Fundamentals"
   - Watch a 30-minute intro video on what Docker is.
   - Follow the official tutorial to install Docker on my machine.
   - Write a simple Dockerfile for a basic 'Hello World' web server.
   - Build the Docker image and run it locally.
- From Block 2: "Kubernetes Architecture"
   - Read the official Kubernetes documentation page for 'Pods'.
   - Write down my own one-sentence definition for 'Pod', 'Deployment', and 'Service'.
   - Watch a video explaining the difference between a Pod and a Deployment.
      You now have a structured learning plan, built from your high-level goal, that you can execute one time block at a time. This approach gives you clarity on what to do next, provides constant feedback on your progress, and builds momentum with every small task you complete.
