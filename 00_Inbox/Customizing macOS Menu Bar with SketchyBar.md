---
aliases: []
author: ["[[Gemini]]"]
confidence: 
created: 2025-12-14T00:00:00Z
description: "Created with Gemini"
epistemic: 
last_reviewed: 
modified: 2025-12-14T13:02:15Z
published:
purpose: 
review_interval: 
see_also: []
source: "https://gemini.google.com/share/fd70fe0491c4"
source_of_truth: []
status: 
tags: ["clippings"]
title: Customizing macOS Menu Bar with SketchyBar
type: 
uid: 
updated: 
---

<<Https://youtube.com/watch?v=O-sRSXqnwkw&si=kV6ZVyhiVM-uH>\_iQ>

Analyse this video and pull out all the tips into a useful list

That is a fascinating video on customising the macOS menu bar using SketchyBar. As per your Abstract-Conceptual and Top-Down cognitive style, I have structured the main tips around the underlying logic and function of customisation, focusing on the "how it works" to give you a concise mental model.

Here are the key tips and concepts for using SketchyBar, pulled from the video:

## Conceptual Framework and General Setup

The core concept is that SketchyBar completely replaces the default macOS menu bar, allowing for highly customisable items, each managed through its own script and configuration.

| **Concept/Component** | **Description** | **Timestamp** |
| --- | --- | --- |
| **SketchyBar Command** | Used for two main purposes: setting the **general appearance** of the bar and **adding items** to it. | \[[01:10](http://www.youtube.com/watch?v=O-sRSXqnwkw&t=70)\], \[[02:13](http://www.youtube.com/watch?v=O-sRSXqnwkw&t=133)\] |
| **Default Section** | A configuration block used to set properties (like padding, fonts, colours) that apply to *all* items by default, saving you from setting them individually. These can be overridden per item. | \[[01:27](http://www.youtube.com/watch?v=O-sRSXqnwkw&t=87)\] |
| **Adding an Item** | Use `sketchybar --add item <name>` to place a new module. You specify the item's name (e.g., `apple`, `front_app`) and position (`left` or `right`). | \[[02:13](http://www.youtube.com/watch?v=O-sRSXqnwkw&t=133)\] |
| **Setting Attributes** | Use `sketchybar --set <item_name> ...` to configure an item's properties, such as its icon, label drawing, and styling. | \[[02:35](http://www.youtube.com/watch?v=O-sRSXqnwkw&t=155)\] |
| **Script Attribute** | For complicated logic, you can link an item to an external shell script (`.sh`). The script runs when triggered (e.g., by an event or update frequency) and is responsible for setting the item's label or icon. | \[[03:52](http://www.youtube.com/watch?v=O-sRSXqnwkw&t=232)\] |
| **Events System** | SketchyBar can subscribe items to system-wide events (e.g., `front_app_switched`, `volume_change`, `media_change`). When an event occurs, the item's linked script is executed instantly. | \[[03:26](http://www.youtube.com/watch?v=O-sRSXqnwkw&t=206)\], \[[07:06](http://www.youtube.com/watch?v=O-sRSXqnwkw&t=426)\] |
| **Update Frequency** | For items not tied to a specific system event (or for non-Spotify music players, as noted), you can set a frequency (`--update_freq N`) to tell the script to run every `N` seconds to check and update its state. | \[[06:07](http://www.youtube.com/watch?v=O-sRSXqnwkw&t=367)\], \[[08:12](http://www.youtube.com/watch?v=O-sRSXqnwkw&t=492)\] |
| **Click Script** | Allows you to assign a specific action (like running an `open` command) when the user clicks on the menu bar item. | \[[05:58](http://www.youtube.com/watch?v=O-sRSXqnwkw&t=358)\] |

## Item-Specific Implementations

The following points illustrate how to implement common features by combining the concepts above:

- **Front Application Display:** Use the **`front_app_switched` event** and a script to dynamically update the label with the currently focused application's name. It's often set to have `icon.drawing=off` to only show the label text. | \[[03:18](http://www.youtube.com/watch?v=O-sRSXqnwkw&t=198)\], \[[03:39](http://www.youtube.com/watch?v=O-sRSXqnwkw&t=219)\]
- **Music/Media Display:** Subscribe the music item to the **`media_change` event** (for Spotify) and/or use a short **`update_freq`** (for terminal music players like RMPC) to keep the label updated with the playing song. | \[[07:06](http://www.youtube.com/watch?v=O-sRSXqnwkw&t=426)\], \[[06:15](http://www.youtube.com/watch?v=O-sRSXqnwkw&t=375)\]
- **Volume Control:** Subscribe to the **`volume_change` event**. The item's script can then retrieve the volume level and conditionally change the item's icon to reflect the level (e.g., low, medium, high). | \[[09:59](http://www.youtube.com/watch?v=O-sRSXqnwkw&t=599)\]
- **Disappearing Widgets:** To make an item disappear when a state is zero (e.g., volume is muted/zero), include logic in the update script to set the item's **`drawing` attribute to `off`** when the condition is met. | \[[10:42](http://www.youtube.com/watch?v=O-sRSXqnwkw&t=642)\]
- **Weather Module:** Use a moderate **`update_freq`** (e.g., every five minutes) to run a script that uses a **`curl` command** to fetch weather data as a JSON object, then parse the data to assign a visual icon and temperature label. | \[[08:12](http://www.youtube.com/watch?v=O-sRSXqnwkw&t=492)\]
- **Conditional Styling:** Use scripting logic to dynamically set the item's colour based on its value (e.g., setting the battery icon to orange below 20% or red below 10%). | \[[12:10](http://www.youtube.com/watch?v=O-sRSXqnwkw&t=730)\]
- **Creating Graphs:** Set an item's type to **`graph`**. The item's update script should calculate the value (e.g., CPU utilisation), normalise it to a number between 0 and 1, and use the **`push` flag** to add the value to the item's history, allowing SketchyBar to plot it over time. | \[[13:12](http://www.youtube.com/watch?v=O-sRSXqnwkw&t=792)\]

---

The video is available here: [Completely Replace and Customize Your MacOS Menu Bar with Sketchybar](http://www.youtube.com/watch?v=O-sRSXqnwkw)

Google Account

Leon Ormes

leonormes@gmail.com
