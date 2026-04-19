# GitHub - retlehs/quien: A better WHOIS lookup tool · GitHub

![rw-book-cover](https://repository-images.githubusercontent.com/1206549574/413d2c69-ba20-4b8e-98c8-41e20bbef966)

## Metadata
- Author: [[GitHub]]
- Full Title: GitHub - retlehs/quien: A better WHOIS lookup tool · GitHub
- Category: #articles
- Summary: Quien is a better WHOIS lookup tool with an interactive interface for domains and IPs. It shows info like WHOIS, DNS, mail, SSL, and tech stack details. You can install it easily with Homebrew or Go and use JSON output for scripting.
- URL: https://github.com/retlehs/quien

## Full Document
### retlehs/quien

main

Go to file

Code

Open more actions menu

#### Folders and files

#### Repository files navigation

* [README](https://github.com/retlehs/quien/#)
* [MIT license](https://github.com/retlehs/quien/#)

### quien

A better WHOIS lookup tool. Interactive TUI with tabbed views for WHOIS, DNS, mail, SSL/TLS, HTTP headers, and tech stack detection.

[![quien demo](https://github.com/retlehs/quien/raw/main/demo.gif)](https://github.com/retlehs/quien/blob/main/demo.gif)
#### Install

```
brew tap retlehs/tap
brew install retlehs/tap/quien

```

Or with Go:

```
go install github.com/retlehs/quien@latest

```

#### Usage

```
# Interactive prompt
quien

# Domain lookup (interactive TUI)
quien example.com

# IP address lookup
quien 8.8.8.8

# JSON output
quien --json example.com

```

#### Features

* **RDAP-first lookups** with WHOIS fallback for broad TLD coverage
* **IANA referral** for automatic WHOIS server discovery
* **Tech stack detection** including WordPress plugins, JS/CSS frameworks, and external services parsed from HTML
* **IP lookups** with reverse DNS, network info, and abuse contacts via RDAP
* **Automatic retry** with exponential backoff on all lookups
* **JSON subcommands** for scripting: `quien dns`, `quien mail`, `quien tls`, `quien http`, `quien stack`, `quien all`

>  **Tip:** If you want `quien` to replace your default WHOIS tool, you can add an alias to your shell config:
> 
>  
> ```
> alias whois=quien
> ```
>  

#### Agent skill

Add quien as a [agent skill](https://skills.sh/) so agents use it for domain and IP lookups:

```
npx skills add retlehs/quien

```
