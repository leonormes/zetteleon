---
created: 2026-05-04T08:01:26+00:00
modified: 2026-05-26T11:43:55+00:00
title: Defining learning goals
---

## Defining Learning Goals

### The Problem with Vague Learning Goals

A goal like "Learn Kubernetes" is an aspiration, not a plan. It's unclear, immeasurable, and has no end point, which makes it perfect for procrastination. Your brain doesn't know what to do with it, so it does nothing.

We can fix this by using a two-part system:

- Define the Destination: Using a modified SMART framework to define what "done" looks like.
- Map the Journey: Breaking the goal down into a personal curriculum of projects and knowledge blocks.

### Part 1: Define the Destination with SMART-P Goals

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

### Part 2: Map the Journey from Goal to Tasks

Now that you have a clear destination (your project), you can work backwards to create a curriculum. This turns the overwhelming "learning" phase into a structured plan.

#### Step 1: Identify the Core Knowledge Blocks (Your "Curriculum")

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
