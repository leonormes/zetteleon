---
captured: "2026-04-09T09:52:32+01:00 2026-04-09T09:52:32+01:00"
created: 2026-04-09T08:52:33+00:00
modified: 2026-04-09T09:07:54+00:00
source: "https://gemini.google.com/app/69132958bcce26e2"
status: "processing"
tags: ["input"]
title: HEAD You said I want to build a solid pomodoro workflow...
type: "head"
---

## Raw Output / Content

You

I want to build a solid pomodoro workflow. I have tried it before but always loss track of it during the day. I am using focus to-do Version 7.3 (45) on my macbook, android pixel 9 phone and pixel 4 watch. But it is not quite right for me. I use obsidian and todoist. I also have jira for work. I have tried sunsama so that I can pull together all the different tasks and calendars into one place.

What I need is a synced pomodoro timer across laptop and other devices. If I start a timer on any of them I can see it on all devices. If I start a timer on my watch for things away from the laptop it should be running everywhere. I am not sure focus to-do does this. Sunsama has a pomodoro timer but it is not cross platform and is easy to loss sight of. How do I consolidate tasks and pomodoro? I want to keep using todoist

---

Gemini

It is incredibly frustrating when a productivity workflow fragments across different screens. You are entirely right about Sunsama; it is a brilliant aggregator for planning, but its Pomodoro feature feels like an afterthought that easily gets buried behind other windows.

Focus To-Do, while offering Mac, Android, and Wear OS apps, creates a major point of friction for you: it does not speak natively to Todoist or Jira. This forces you into double-entry, making you maintain separate task lists. That disconnect is exactly why it feels "not quite right".

To consolidate this, you need to separate your Planning Layer (Todoist, Jira, Obsidian) from your Execution Layer (your Pomodoro timer). Instead of migrating tasks, you need a timer that _pulls_ your existing tasks in.

### A Candid Note on "Real-Time" Watch Syncing

Before diving into the tools, it is worth gently correcting a common misconception about cross-device timers. Maintaining a true, second-by-second visual countdown synced perfectly across a Mac, an Android phone, and a Wear OS watch is technically restricted by aggressive battery-saving measures on mobile and wearable operating systems.

If you start a timer on your watch, the _state_ (started, paused, finished) will synchronise to your Mac, but you may occasionally have to wake the mobile or watch app for the visual ticking to "catch up".

### Top Recommendations to Harmonise Your Workflow

Here are the best ways to keep Todoist as your master list while running a synced Pomodoro workflow:

1\. RoundPie (formerly PomoDoneApp)–Best for Seamless Integration

- The Setup: RoundPie is arguably the most robust bridge for your specific tech stack. It connects directly to your Todoist and Jira accounts, pulling your tasks and tickets into its interface. When a 25-minute Pomodoro finishes, it can automatically log the time or check the task off in Todoist.
- Cross-Platform Sync: It features excellent, synchronised Mac and Android apps.
- The Watch Experience: It does not have a standalone Wear OS app. However, its rich Android persistent notification mirrors perfectly to your Pixel Watch. If you step away from your MacBook—perhaps for a quick walk around Southend-on-Sea to clear your head—you can pause, stop, or extend your running timer directly from your wrist.

2\. Toggl Track–Best for Native Wear OS Support

- The Setup: While primarily a time-tracking tool, Toggl Track features a dedicated Pomodoro mode on its Mac desktop app. You can use their browser extension to inject a Toggl timer button directly into the Todoist web app.
- Cross-Platform Sync: Flawless cloud synchronisation across Mac and Android.
- The Watch Experience: Toggl _does_ have a dedicated Wear OS app, allowing you to initiate and stop timers entirely independently from your wrist without relying on phone notifications.

_(Note: TickTick is the only major app that natively handles tasks, calendars, and cross-platform Wear OS/Mac Pomodoros perfectly in one ecosystem. However, since you explicitly want to keep Todoist, I would not recommend jumping ship just for the timer)._

The Verdict: If you want the absolute cleanest connection to Todoist and Jira without duplicating your to-do list, RoundPie is the most logical next step to act as your central execution engine.

Since RoundPie can pull tasks from multiple sources, do you prefer to keep your work tasks strictly siloed in Jira, or do you currently funnel your Jira tickets into Todoist to view everything in one place?

---

You

maybe the timer only needs to do the timing. i manage me tasks in todoist but use a pomodoro timer just for the time blocks? If i don't need to the pomodoro to have the tasks just the timing feature what are my best cross device options? Focus to-do still? Of are there lighter options

---

Gemini

Decoupling your tasks from your timer is a brilliant strategy. It completely removes the friction of double-entry and lets Todoist do what it does best, while you just focus on the ticking clock.

However, you have hit a very specific technological bottleneck: bridging the Apple ecosystem (your MacBook) and the Google ecosystem (your Android phone and Wear OS watch) in real-time.

Here is the candid truth about the current app landscape: truly minimalist timers rarely have cross-platform cloud synchronisation. Building the infrastructure to ping a timer state from a Google Wear OS watch, through a server, and instantly onto a Mac menu bar requires significant development resources. Because of this, most "lightweight" apps stick to one ecosystem (using Apple's iCloud for Mac/iOS, or Google's native sync for Android/Wear OS).

If you just want the timing feature across your exact devices, here are your best options:

### 1\. Focus To-Do (Still the Most Reliable Bridge)

Despite your reservations, Focus To-Do remains the undisputed champion for this specific hardware combination. It is one of the only apps on the market with dedicated, actively synced apps for macOS, Android, and Wear OS.

- How to make it "lighter": Stop fighting its task manager. Ignore the project folders, the deadlines, and the tags. Create a single, permanent task called "Focus Block" or just use the default "Inbox" and hit the play button. By treating it strictly as a "dumb" start/stop button, the app feels significantly less bloated.

### 2\. Toggl Track (The Cleaner UI Alternative)

If the Focus To-Do interface is still too cluttered for your taste, Toggl Track is the only other major player with native apps for Mac, Android, and Wear OS.

- How to use it as a simple timer: While Toggl is a heavy-duty time tracker for freelancers, its interface is actually remarkably clean. You can turn on the "Pomodoro Mode" in the desktop and mobile settings. Just like Focus To-Do, simply type "Focus" into the tracker and hit start. It will sync flawlessly to your wrist and phone.

### 3\. The Web-Based Compromise: Pomofocus.io

If you are willing to sacrifice the wrist experience for a beautifully minimalist interface on your laptop and phone, Pomofocus.io is worth mentioning.

- The Setup: It is a lightweight web app. You log in via your browser on the Mac and your Pixel phone. It syncs your timer state perfectly between the two.
- The Catch: There is no Wear OS app. If you step away from your desk, you will have to rely on your phone for the timer rather than your watch.

### The Verdict

If having the timer on your Pixel watch is an absolute non-negotiable requirement for when you step away from the laptop, Focus To-Do is still your best bet. You just have to change your relationship with the app and ignore its extra features.

If you were to stick with Focus To-Do but strictly as a "dumb" timer, what specific friction points from your past experience with it would you still need to work around?

---

You

how do I configure my watch to keep the timer running? I seem to have it in some aggressive battery saving that stops the timer running after a few seconds of not looking at it!

---

Gemini

The issue you are describing is a classic battle between Wear OS battery management and real-time apps. By default, your Pixel Watch 4 is designed to "suspend" background apps the moment your wrist drops to save power. When you look back, the app has to wake up and fetch the current state from the server, which is why it feels like it wasn't running.

To fix this for a Pomodoro workflow, you need to toggle three specific settings to keep the timer "alive" and visible.

### 1\. Enable "Always-on Display" (AOD)

This is the most important step. Without this, the watch completely shuts down the display and throttles the processor.

- On your watch, swipe down and tap Settings (gear icon).
- Tap Display.
- Toggle Always-on screen to On.
- _Note:_ In 2026, the Pixel Watch 4 has a high-efficiency mode that specifically lets Timers stay visible in a low-power state.

### 2\. Disable "Battery Saver" Mode

If your watch is in Battery Saver mode, it will kill background syncing and the Always-on Display regardless of your other settings.

- Swipe down on the watch face.
- Check the Battery icon. If it has a leaf or is orange, tap it and turn Battery Saver off.

### 3\. Change "Screen Timeout"

If the screen turns off too quickly, the app might be getting "paused" by the OS before it can properly sync its final state.

- Go to Settings > Display.
- Tap Screen timeout.
- Change this to 30 seconds (the maximum). This gives the app a longer "active" window to ensure the sync with your MacBook is solid before the screen dims.

### 4\. Special Optimization for "Focus To-Do"

Android/Wear OS has a feature called "Unrestricted" battery usage that you can apply to specific apps so the system doesn't "kill" them.

1. Open the Watch app on your Pixel 9 phone.
2. Go to Apps > Focus To-Do.
3. Look for App battery usage or Optimisation.
4. Change the setting from "Optimised" to Unrestricted.
	- _This tells your phone and watch: "I don't care about the battery life for this specific app; keep it running no matter what."_

---

Pro-Tip for Focus To-Do: To make the sync feel more "instant," try to always start the timer from the Watch, not the MacBook. Wear OS is much better at _sending_ an update to a computer than it is at _constantly listening_ for an update from one while in standby.

Does the timer usually stop exactly when the screen goes black, or does it just fail to "ring" when the time is actually up?
