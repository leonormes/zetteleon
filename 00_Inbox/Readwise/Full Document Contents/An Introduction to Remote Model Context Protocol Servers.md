# An Introduction to Remote Model Context Protocol Servers

![rw-book-cover](https://towardsdatascience.com/wp-content/uploads/2025/07/mcp-image-fotor-2025062515338.png)

## Metadata
- Author: [[Thomas Reid]]
- Full Title: An Introduction to Remote Model Context Protocol Servers
- Category: #articles
- Summary: This article explains how to build, test, and deploy a remote MCP server that lets clients call useful tools over the internet. It shows how to run the server locally, then host it in the cloud using Render. Finally, it provides example code for accessing and testing the MCP server remotely.
- URL: https://towardsdatascience.com/an-introduction-to-remote-model-context-protocol-servers/

## Full Document
Writing, testing and using them

I last wrote about the Model Context Protocol (MCP) in early December 2024, shortly before the topic’s exponential growth into what it is today. I recall thinking at the time that one of the key things I felt had to happen to MCP to make the technology a game changer was the ability for MCP clients to access non-local MCP servers. That’s already happening, of course, but what if you want a piece of this action? How do you go about writing a remote MCP server, crafting useful tools for it, testing it, then deploying it to the cloud, for example, so that anyone can access the tools it exposes from any supported client anywhere in the world?

I’ll show you how to do all of those things in this article.

#### A quick recap on what an MCP server is

There are dozens of definitions for what an MCP server is. In my view, which is probably a bit of an oversimplification, an MCP server enables MCP-enabled clients, such as Cursor and Claude code, to call useful functions that the MCP server contains.   

 How is that different from you just writing a bunch of valuable tools and calling them in your code?

Well, the key is that*you’re* writing those tools. What about the potential universe of tools that exist that *someone else* has written? I’m sure you’ve heard the expression **“… there’s an app for that”**. In the not-too-distant future, that might become “**… there’s an MCP server for that**“. Ok, not as snappy but just as groundbreaking.

Until now, the vast majority of MCP servers have been written with the STDIO transport type in mind. This means that the onus is on *you* to host the server on your local system. That can sometimes be tricky and prone to error. Moreover, only you can access that server. And that is where remote (or Streamable HTTP) MCP servers come into their own. Hosted remotely, you only need to know the URL of the server and the names of the tools it provides, and you’re up and running with it in seconds.

So, if you’ve written something that others might find truly helpful, why not make a remote MCP server of it, host it in the cloud and let others use it too?

Ok, let’s do this.

#### My setup

I’ll be developing the code for the MCP server and its tools using Windows and Microsoft Visual Studio Code. I’ll be using Git Bash for my command line as it comes with some handy utilities that I’ll use, such as **curl** and **sed**. You’ll also need to install **Node.js** and the **uv** Python package utility. If you want to deploy the finished MCP server to the cloud, you’ll also need to store your code on GitHub, so you’ll need an account for that.

The first thing you should do is initialise a new project for your code, etc. Use the **uv** tool with the init flag for this. Next, we add an environment, switch to it and add all the external libraries that our code will use.

```
$ uv init remote-mcp
Initialized project `remote-mcp` at `/home/tom/projects/remote-mcp`
$ cd remote-mcp
$ ls -al
total 28
drwxr-xr-x 3 tom tom 4096 Jun 23 17:42 .
drwxr-xr-x 14 tom tom 4096 Jun 23 17:42 ..
drwxr-xr-x 7 tom tom 4096 Jun 23 17:42 .git
-rw-r--r-- 1 tom tom 109 Jun 23 17:42 .gitignore
-rw-r--r-- 1 tom tom 5 Jun 23 17:42 .python-version
-rw-r--r-- 1 tom tom 0 Jun 23 17:42 README.md
-rw-r--r-- 1 tom tom 88 Jun 23 17:42 main.py
-rw-r--r-- 1 tom tom 156 Jun 23 17:42 pyproject.toml

$ uv venv && source .venv/bin/activate
# Now, install the libraries we will use.
(remote-mcp) $ uv add fastapi 'uvicorn[standard]' mcp-server requests yfinance python-dotenv
```

#### What we’ll develop

We will develop an MCP server and two distinct tools for our MCP server to utilise. The first will be a Nobel Prize checker. You provide a Year, e.g, 1935, and a subject, e.g, Physics, and the MCP server will return information about who won the prize that year in that subject. The second tool will return the maximum recorded temperature for a city in the past week

First off, we’ll code our two tools and test them locally. Next, we will incorporate the tools into an MCP server running locally and test that setup. If it works as expected, we can deploy the MCP server and its tools to a remote cloud server and verify that it continues to function correctly.

###### Code Example 1— Getting Nobel prize information

The services of the Nobel Prize website are licensed under the Creative Commons zero license. You can see the details using the link below:

<https://www.nobelprize.org/about/terms-of-use-for-api-nobelprize-org-and-data-nobelprize-org>

Here is the base function we’ll use. Open up your code editor and save this content in a file called **prize\_tool.py**.

```
import requests
import os
import io
import csv

# from mcp.server.fastmcp import FastMCP
try:
    from mcp.server.fastmcp import FastMCP
except ModuleNotFoundError:
    # Try importing from a local path if running locally
    import sys
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from fastmcp import FastMCP

mcp = FastMCP(name="nobelChecker",stateless_http=True)

@mcp.tool()
def nobel_checker(year, subject):
    """
    Finds the Nobel Prize winner(s) for a given year and subject using the Nobel Prize API.

    Args:
        year (int): The year of the prize.
        subject (str): The category of the prize (e.g., 'physics', 'chemistry', 'peace').

    Returns:
        list: A list of strings, where each string is the full name of a winner.
              Returns an empty list if no prize was awarded or if an error occurred.
    """
    BASE_URL = "http://api.nobelprize.org/v1/prize.csv"
    
    # Prepare the parameters for the request, converting subject to lowercase
    # to match the API's expectation.
    params = {
        'year': year,
        'category': subject.lower()
    }
    
    try:
        # Make the request using the safe 'params' argument
        response = requests.get(BASE_URL, params=params)
        
        # This will raise an exception for bad status codes (like 404 or 500)
        response.raise_for_status()

        # If the API returns no data (e.g., no prize that year), the text will
        # often just be the header row. We check if there's more than one line.
        if len(response.text.splitlines()) <= 1:
            return [] # No winners found

        # Use io.StringIO to treat the response text (a string) like a file
        csv_file = io.StringIO(response.text)
        
        # Use DictReader to easily access columns by name
        reader = csv.DictReader(csv_file)
        
        winners = []
        for row in reader:
            full_name = f"{row['firstname']} {row['surname']}"
            winners.append(full_name)
            
        return winners

    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the API request: {e}")
        return [] # Return an empty list on network or HTTP errors

if __name__ == "__main__":
   data =  nobel_checker(1921,"Physics")
   print(data)
```

This script defines a small “nobel-checker” MCP (Model Context Protocol) tool that can be run either locally or inside a FastMCP server. After trying to import `FastMCP` from the `mcp.server` package, and falling back to a sibling `fastmcp` module if that import fails. It then constructs an MCP instance named **nobelChecker** with the stateless\_http=True flag, meaning that FastMCP will automatically expose a plain HTTP endpoint for one-shot calls. The decorated function **nobel\_checker** becomes an MCP tool. When invoked, it constructs a query to the Rest API using the supplied year and subject matter, and returns the name(s) of the prize winner for that year and subject (or a helpful message if not).

If we run the above code locally, we obtain output similar to the following, which indicates that the function is working correctly and performing its intended task.

```
['Albert Einstein']
```

###### Code Example 2— Getting city temperature information

For our second base function, we’ll write a tool that returns the highest temperature for a city over the last week. The weather data is provided by Open-Meteo.com. On their license page (“<https://open-meteo.com/en/license>), it states,

“API data are offered under [Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/)

You are free to **share:** copy and redistribute the material in any medium or format and **adapt:** remix, transform, and build upon the material. “

I have given the correct attribution and link to their license, which fulfills the terms of their license.

Create the Python file **temp\_tool.py** and enter this code.

```
# temp_tool.py

from mcp.server.fastmcp import FastMCP

mcp = FastMCP(name="stockChecker", stateless_http=True)

import requests
from datetime import datetime, timedelta

# This helper function can be reused. It's not tied to a specific API provider.
def get_coords_for_city(city_name):
    """
    Converts a city name to latitude and longitude using a free, open geocoding service.
    """
    # Using Open-Meteo's geocoding, which is also free and requires no key.
    GEO_URL = "https://geocoding-api.open-meteo.com/v1/search"
    params = {'name': city_name, 'count': 1, 'language': 'en', 'format': 'json'}
    
    try:
        response = requests.get(GEO_URL, params=params)
        response.raise_for_status()
        data = response.json()
        
        if not data.get('results'):
            print(f"Error: City '{city_name}' not found.")
            return None, None
            
        # Extract the very first result
        location = data['results'][0]
        return location['latitude'], location['longitude']
        
    except requests.exceptions.RequestException as e:
        print(f"API request error during geocoding: {e}")
        return None, None

@mcp.tool()
def get_historical_weekly_high(city_name):
    """
    Gets the highest temperature for a city over the previous 7 days using the
    commercially-friendly Open-Meteo API.

    Args:
        city_name (str): The name of the city (e.g., "New York", "London").

    Returns:
        float: The highest temperature in Fahrenheit from the period, or None if an error occurs.
    """
    # 1. Get the coordinates for the city
    lat, lon = get_coords_for_city(city_name)
    if lat is None or lon is None:
        return None # Exit if city wasn't found
        
    # 2. Calculate the date range for the last week
    end_date = datetime.now() - timedelta(days=1)
    start_date = datetime.now() - timedelta(days=7)
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')

    # 3. Prepare the API request for the Historical API
    HISTORICAL_URL = "https://archive-api.open-meteo.com/v1/era5"
    params = {
        'latitude': lat,
        'longitude': lon,
        'start_date': start_date_str,
        'end_date': end_date_str,
        'daily': 'temperature_2m_max', # The specific variable for daily max temp
        'temperature_unit': 'fahrenheit' # This API handles units correctly
    }
    
    try:
        print(f"Fetching historical weekly max temp for {city_name.title()}...")
        response = requests.get(HISTORICAL_URL, params=params)
        response.raise_for_status()
        data = response.json()
        
        daily_data = data.get('daily', {})
        max_temps = daily_data.get('temperature_2m_max', [])
        
        if not max_temps:
            print("Could not find historical temperature data in the response.")
            return None
            
        # 4. Find the single highest temperature from the list of daily highs
        highest_temp = max(max_temps)
        
        return round(highest_temp, 1)

    except requests.exceptions.RequestException as e:
        print(f"API request error during historical fetch: {e}")
        return None

if __name__ == "__main__":
   data =  get_historical_weekly_high("New York")
   print(data)

```

This function takes a city name and returns the highest recorded temperature in the city for the last week.

Here is a typical output when running locally.

```
Fetching historical weekly max temp for New York...
104.3
```

#### Creating our MCP server

Now that we’ve shown our functions are working, let’s incorporate them into an MCP server and get that running locally. Here is the server code you’ll need.

```
# mcp_server.py

import contextlib
from fastapi import FastAPI
from temp_tool import mcp as temp_mcp
from prize_tool import mcp as prize_mcp
import os
from dotenv import load_dotenv

load_dotenv()

# Create a combined lifespan to manage both session managers
@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    async with contextlib.AsyncExitStack() as stack:
        await stack.enter_async_context(temp_mcp.session_manager.run())
        await stack.enter_async_context(prize_mcp.session_manager.run())
        yield

app = FastAPI(lifespan=lifespan)
app.mount("/temp", temp_mcp.streamable_http_app())
app.mount("/prize", prize_mcp.streamable_http_app())

PORT = int(os.getenv("PORT", "10000"))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)
```

The only changes to our original prize\_tool and temp\_tool codebases are to delete the three lines at the bottom of each, which are used for testing. Remove these from both.

```
if __name__ == "__main__":
    data = nobel_checker(1921,"Physics")
    print(data)

and ...

if __name__ == "__main__":
    data = get_historical_weekly_high("New York")
    print(data)
```

#### Running the MCP server locally

To run our server, type the following command into a command-line terminal.

```
$ uvicorn mcp_server:app --reload --port 10000
$ # You can also use python mcp_server.py --reload --port 10000
$ #
INFO: Will watch for changes in these directories: ['C:\Users\thoma\projects\remote-mcp\remote-mcp']
INFO: Uvicorn running on http://127.0.0.1:10000 (Press CTRL+C to quit)
INFO: Started reloader process [3308] using WatchFiles
INFO: Started server process [38428]
INFO: Waiting for application startup.
[06/25/25 08:36:22] INFO StreamableHTTP session manager started streamable_http_manager.py:109
INFO StreamableHTTP session manager started streamable_http_manager.py:109
INFO: Application startup complete.
```

#### Testing our MCP server locally

We can use a Gitbash command terminal and curl for this. Make sure your server is up and running first. Let’s try our temperature checker tool first. The output can always be post-processed to bring out exactly the content you want in a more user-friendly format.

```
$ curl -sN -H 'Content-Type: application/json' -H 'Accept: application/json, text/event-stream' -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"get_historical_weekly_high","arguments":{"city_name":"New York"}}}' http://localhost:10000/temp/mcp/ | sed -n '/^data:/{s/^data: //;p}'

{"jsonrpc":"2.0","id":1,"result":{"content":[{"type":"text","text":"104.3"}],"isError":false}}
```

This shows the max temp in NY over the last week was 104.3 Fahrenheit.

And now we can test the prize checker tool.

```
$ curl -sN -H 'Content-Type: application/json' -H 'Accept: application/json, text/event-stream' -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"nobel_checker","arguments":{"year":1921,"category":"Physics"}}}' http://localhost:10000/prize/mcp/ | sed -n '/^data:/{s/^data: //;p}' 

{"jsonrpc":"2.0","id":1,"result":{"content":[{"type":"text","text":"Albert Einstein"}],"isError":false}}

```

Albert Einstein did indeed win the Nobel Prize for Physics in 1921.

#### Deploying our MCP server remotely

Now that we’re satisfied with our code and that the MCP server is working as expected locally, the next stage is to deploy it remotely, allowing anyone in the world to use it. There are a few options to do this, but perhaps the easiest (and initially the cheapest) is to use a service like **Render.**

Render is a modern cloud hosting platform — like a simpler alternative to AWS, Heroku, or Vercel — that lets you deploy full-stack apps, APIs, databases, background workers, and more, with minimal DevOps overhead. More to the point is that it’s free to get started and is more than enough for our needs. So head over to their [website](https://render.com/) and sign up.

Before deploying with Render, you must commit and send your code to a GitHub (or a GitLab/Bitbucket) repository. After that, on the Render website, choose to create a New web server,

![](https://contributor.insightmediagroup.io/wp-content/uploads/2025/06/r1.png)Image from the Render website
The first time, Render will ask for access to your GitHub (or Bitbucket/GitLab) account.

![](https://contributor.insightmediagroup.io/wp-content/uploads/2025/06/r2-1024x337.png)Image from the Render website
After that, you need to provide the commands to build your deployment and start your server. For example ….

![](https://contributor.insightmediagroup.io/wp-content/uploads/2025/06/r3-1024x289.png)Image from the Render website
Back on the ***Settings*** screen, click the ***Manual*** ***Deploy* *-> Deploy latest commit*** menu item, and a log of the build and deployment process will be displayed. After a few minutes, you should see the following messages indicating your deployment was successful.

```
...
...
==> Build successful 🎉
==> Deploying...
==> Running 'uv run mcp_server.py'
...
...
...
==> Available at your primary URL https://remote-mcp-syp1.onrender.com==> Available at your primary URL https://remote-mcp-syp1.onrender.com
...
Detected service running on port 10000
...
...
```

The vital address you need is the one marked as the primary URL. In our case, this is <https://remote-mcp-syp1.onrender.com>

###### Testing our remote MCP server

We can do this in the same way we tested the local running, i.e using curl. First, check on max temperature, this time Chicago. Note the change of URL to our new remote one.

```
$ curl --ssl-no-revoke -sN -H "Content-Type: application/json" -H "Accept: application/json, text/event-stream" -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"get_historical_weekly_high","arguments":{"city_name":"Chicago"}}}' https://remote-mcp-syp1.onrender.com/temp/mcp/|sed -n '/^data:/{s/^data: //;p}'

```

And our output?

```
{"jsonrpc":"2.0","id":1,"result":{"content":[{"type":"text","text":"95.4"}],"isError":false}}

```

The sharp-eyed among you may have noticed that we have included an extra flag **( — ssl-no-revoke)** in the above curl command compared to the one we used locally. This is simply due to a quirk in the way curl works under Windows. If you’re using WSL2 for Windows or Linux, you don’t need this extra flag.

Next, we test our remote Nobel prize checker. This time for Chemistry in 2024.

```
$  $ curl --ssl-no-revoke -sN 
-H 'Content-Type: application/json' 
-H 'Accept: application/json, text/event-stream' 
-d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"nobel_checker","arguments":{"year":2024,"subject":"Chemistry"}}}' 
'https://remote-mcp-syp1.onrender.com/prize/mcp/' | sed -n '/^data:/{s/^data: //;p}'

```

And the output?

```
{"jsonrpc":"2.0","id":1,"result":{"content":[{"type":"text","text":"David Baker"},{"type":"text","text":"Demis Hassabis"},{"type":"text","text":"John Jumper"}],"isError":false}}
```

If you want to try accessing the MCP server via code instead of using curl, here’s some example Python that illustrates calling the remote **nobel\_checker** tool.

```
import requests
import json
import ssl
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings

# Disable SSL warnings (equivalent to --ssl-no-revoke)
disable_warnings(InsecureRequestWarning)

def call_mcp_server(url, method, tool_name, arguments, request_id=1):
    """
    Call a remote MCP server
    
    Args:
        url (str): The MCP server endpoint URL
        method (str): The JSON-RPC method (e.g., "tools/call")
        tool_name (str): Name of the tool to call
        arguments (dict): Arguments to pass to the tool
        request_id (int): JSON-RPC request ID
    
    Returns:
        dict: Response from the MCP server
    """
    
    # Prepare headers
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream"
    }
    
    # Prepare JSON-RPC payload
    payload = {
        "jsonrpc": "2.0",
        "id": request_id,
        "method": method,
        "params": {
            "name": tool_name,
            "arguments": arguments
        }
    }
    
    try:
        # Make the request with SSL verification disabled
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            verify=False,  # Equivalent to --ssl-no-revoke
            stream=True   # Support for streaming responses
        )
        
        # Check if the request was successful
        response.raise_for_status()
        
        # Try to parse as JSON first
        try:
            return response.json()
        except json.JSONDecodeError:
            # If not JSON, return the text content
            return {"text": response.text}
            
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {str(e)}"}

# Example usage
if __name__ == "__main__":
    
    result = call_mcp_server(
        url="https://remote-mcp-syp1.onrender.com/prize/mcp/",
        method="tools/call",
        tool_name="prize_checker",
        arguments={"year": 2024, "subject": "Chemistry"}
    )
    print("MCP Tool Call Response:")
    print(json.dumps(result, indent=2))
```

The output is.

```
MCP Tool Call Response:
{
  "text": "event: messagerndata: {"jsonrpc":"2.0","id":1,"result":{"content":[{"type":"text","text":"David Baker"},{"type":"text","text":"Demis Hassabis"},{"type":"text","text":"John Jumper"}],"isError":false}}rnrn"
}
```

#### Summary

This article introduces how to **write, test, and deploy** your remote, Streamable HTTP Model Context Protocol (MCP) server in the cloud, enabling any MCP client to access functions (tools) remotely.

I showed you how to code some useful stand-alone functions — a Nobel prize checker and a city temperature information tool. After testing these locally using the **curl** command to ensure they worked as expected, we converted them into MCP tools and coded an MCP server. After deploying and successfully testing the MCP server locally, we looked at how to deploy our server to the cloud.

For that purpose, I demonstrated how to use Render, a cloud hosting platform, and walked you through the steps of signing up and deploying (for free) our MCP server app. We then used curl to test the remote server, confirming it was working as expected.

Finally, I also provided some Python code you can use to test the MCP server.

Feel free to test out my MCP server on Render for yourself. Note that because it’s on the free tier, the server spins down after a period of inactivity, which may result in a 30–60 second delay in retrieving results.
