# Error handling in bash

![rw-book-cover](https://notifox.com/blog/bash-error-handling/bashscriptsarebrittle.png)

## Metadata
- Author: [[Mathis Van Eetvelde]]
- Full Title: Error handling in bash
- Category: #articles
- Summary: Bash scripts use exit codes to show if commands succeed or fail, with 0 meaning success and other numbers meaning errors. You can handle errors using if-else statements, the || operator, or the trap command to stop problems early. Alerting tools like Slack or Teams webhooks help notify you when errors happen in your scripts.
- URL: https://notifox.com/blog/bash-error-handling

## Full Document
#### Recent posts

#### Bash scripts are usually system glue

If you're a DevOps, Systems or Platform engineer, you almost certainly have bash scripts running *somewhere* in production. Usually in CI/CD pipelines or a CronJob (e.g. on Kubernetes). They're the glue between systems or sources of truth. Every good engineer knows it's a bad idea waiting to get worse, but it's often the fastest thing to ship.

I have been in multiple organizations where one or more CI/CD pipelines run on merged PRs. They execute a bash script that takes some form of data (usually YAML or JSON) and updates another system or state: another git repo, a Kubernetes cluster, SSM parameters, and so on.

These bash scripts are often thousands of lines long, contain many if-else branches and many different outcomes, all without proper unit tests or documentation. In many cases even the author has no idea what the script actually does one week after they wrote it, and that's when we're talking about the happy path where everything goes according to plan. Don't even get me started on when things go south.

**Let's face it. Your bash scripts are brittle!**

They break, and when they do the usual fix is to re-run the pipeline. You hope for a green checkmark (and that the pipeline is idempotent). If the re-run didn't fix it, you're in for a shitty day. When these scripts fail, the fallout is real: systems back up, data drifts out of sync, and sometimes you only notice when something is already seriously wrong.

In this blogpost I want to share some tips on how to make bash scripts less brittle and more readable by doing "proper" error handling!

#### Bash exit codes

Every bash command returns an exit code. This code gives you an idea how it finished. You can get this exit code of the last command with `$?`.

```
date -I # 2026-02-05

```

The exit code `0` indicates that the previous command exited without an error. Success! If the exit code is anything other than 0, it means there was some kind of issue.

```

echo $? # 1
 

```

The exit code of `ls /this-path-doesnt-exist` is `1` because that path really does not exist, and ls can therefore not list the files and directories on that path.

You'll find that a program or executable can also return an exit code higher than 1. For example:

* `126` indicates that you do not have permission to run that command
* `127` indicates that the command is not found
* `130` indicates the command was terminated by Control+C

There are only a handful of reserved UNIX exit codes, which include 126 and 127. Many programs have their own set of defined exit codes. cURL has them listed [here](https://everything.curl.dev/cmdline/exitcode.html).

```

# curl: (6) Could not resolve host: hello
echo $? # 6
 

# curl: (7) Failed to connect to localhost port 1 after 0 ms: Couldn't connect to server
echo $? # 7
 
curl --max-time 1 https://10.255.255.1
# curl: (28) Connection timed out after 1006 milliseconds

```

In many programming languages you can exit the program with a specified exit code by doing something along the lines of:

```
return 0 # C
sys.exit(1) # Python
os.Exit(2) # Go
process.exit(3) # Node.js
System.exit(4); # Java
# and so on
```

All that to say that the **ONLY** exit code that indicates success is **0**. Anything higher than 0 means that something has gone wrong.

#### Catching errors in bash

##### Default error behavior

In bash there are many ways to catch a non-zero exit! But it is important to know that the default behavior is to just move onto the next command if a failure happens!

```

echo "world"
 

```

You might have initially expected it to exit out of the script after the first non-zero exit code, like a normal programming language would fail or stop. But it does not!

An easy way to change this behavior is to use the `-e` option. It tells bash to immediately exit if a command fails (non-zero exit code). We can set this option using the `set` command.

```

 

echo "world"
 

```

If you execute that script you'll see that it exits right after it fails the first time, and does not print the "world".

As you'll learn later in this blogpost, there are some footguns and caveats you'll need to keep in mind when using `-e`.

This is great! If a command in your script fails, your entire script will screech to a halt instead of continuing to do more damage! Except in the real world, things **DO** fail and you want to handle that failure properly instead of just terminating everything.

Fortunately, bash can do this too!

##### Using if else

The built-in `if else` statements can be used fairly easily to catch an error in bash.

```
if some_command; then

```

If you execute the script below and `some_command` returns a `0` exit code, the script will print "success". If the command returns a non-zero code (doesn't matter which one, just as long as it is higher than 0) the script will print `failure`. By wrapping `some_command` in an if else statement, the script will not error out even if `-e` is enabled.

This is great, but what if we want to be able to distinguish between an exit code of `1` and `2`. Not a problem! We can assign the value of `$?` to an environment variable and use numeric comparison operators to compare error codes.

```

 
if [ $exit_code -eq 1 ]; then

elif [ $exit_code -eq 2 ]; then

    echo "exited with other exit code"

```

The `-eq` between the `[]` means `equal`. Other numeric comparison operators are `-ne` (not equal), `-gt` (greater than), etc.

If else statements are a great way to catch errors, but they can be very wordy. Thankfully, bash has more ways to catch errors!

##### Using logical operators

Everyone knows the `&&` operator in bash, it's the `AND` operator and allows you to "chain" together multiple commands.

```
echo "hello" && echo "world"

```

But not that many people know about the `||` operator. This operator is the `OR` operator. It runs a second command if the first command has a non-zero exit code. For example:

The `||` operator will **NOT** execute the second command if the first command does return a `0` exit code.

This is very frequently used for oneline error handling. Here are some common examples:

```

 
# if this fails, do something else
some_command || other_command
 
# echos message to stderr on failure only
curl not-valid || echo "curl command failed" >&2
```

##### Using trap

All the previous examples of catching errors are declared either inline, or immediately after the errors can happen. On paper, this is not a problem as there is nothing preventing you from using the `||` operator after every command on every line. However, your co-workers might not approve your PR if you do this. It's a very ugly and wordy way of dealing with errors.

A great way to "catch" all errors is by using the `trap` command. The `trap` command requires you to declare a response to a specific [signal](https://faculty.cs.niu.edu/~hutchins/csci480/signals.htm) before it happens. After you've executed the `trap` command, it will execute on any unhandled occurrence of that signal. In our case, we want to use the `ERR` signal.

```

 

 
# an error occurred on line 4
```

`trap` is powerful because it doesn't require you to explicitly expect an error at every single command in order to gracefully handle it. Out of all the methods mentioned in this blogpost, `trap` is by far the most obscure.

#### Common pitfalls

Next up I'd like to spell out some common bash pitfalls that have burned me one too many times!

##### Pipes hide failures

In bash you are very likely to use a pipe (`|`) to take the output of one command and *pipe* (or stream) it into the next. Unfortunately, pipes do not care if the previous command has returned a non-zero exit!

The first command fails (due to a missing file), then the second command runs successfully and returns a `0` exit code. Even with `-e` enabled, bash would not have considered this a failure, and would have continued as if nothing had happened.

This is dangerous due to the inherent nature of pipes; we care about the output of the first command and use it in the second. In my opinion, if you are using pipes it is reasonably expected that the second command is dependent on the first (otherwise you would just use `&&`).

Fortunately this mishap can be prevented by using the `pipefail` option. You can enable this by doing `set -o pipefail`.

In combination with the `||` operator, this can be very powerful.

```

cat missing-file.txt | wc -l || echo "something went awry!"
 

```

This can also be combined with the `-e` option to exit the program early altogether.

##### Undefined variables

If bash is your glue, you are no doubt setting and using variables.

In most cases you'll set a variable to the output of another command. If that command fails and the variable is used later you're in trouble!

```
USER_ID=$(grep "user_id" config.txt) # config.txt doesn't exist
 
echo "User is $USER_ID! " # User is !
```

One way to prevent an empty variable from ruining your day is by manually checking if the variable is "not empty" using an `if` statement and the `-z` (empty) operator.

```
USER_ID=$(grep "user_id" config.txt)
 
if [ -z "$USER_ID" ]; then
    echo "USER_ID is empty!"

```

Alternatively, you can use the `-n` to test if the string is (not empty).

```
USER_ID=$(grep "user_id" config.txt)
 
if [ -n "$USER_ID" ]; then
    echo "USER_ID is $USER_ID"

```

If you are setting many variables, this can get very wordy quickly. Fortunately we can use the `-u` flag/option to treat unset variables as an error!

```

USER_ID=$(grep "user_id" config.txt) 
 
echo "User is $USER_ID!" # fails right here when trying to use unset variable!
```

##### Combining options

You can combine the options discussed above! This results in a good set of default error handling behaviors that work for most scripts/applications. In mature production environments, it is rare to see a bash script without at least some of these enabled!

```

set -o pipefail # exit on errors in pipes
set -E # inherit ERR traps
```

Another option I hadn't mentioned before is the `-E` option. This option will make the `ERR` trap fire inside functions and sub-shells, making it even more powerful.

The best part is that you can combine them into a single line!

With that line (usually at the top of your bash script underneath the [shebang](https://en.wikipedia.org/wiki/Shebang_(Unix))) your script will:

* Catch the ERR signal inside functions
* Exit on uncaught errors
* Exit on unset variables
* Exit on errors inside pipes

#### When to use what

We've talked about several powerful ways of catching errors inside your bash scripts. The most difficult part is knowing when to use what method, and unfortunately this is not something I can give you a concrete answer to as it varies on a case by case basis.

**My advice is to optimize for read- and understand-ability.**

This means to use the `||` operator when the fallback/recovery step is short, such as printing an error or exiting the program right away.

On the flip side, there are many cases where an `if else` statement is preferred due to the complexity of handling the error.

```

 
if [ $rc -eq 1 ]; then

elif [ $rc -eq 2 ]; then

```

It's worth mentioning that for the example above `-e` cannot be set, as the script would fail when the command exists before we can capture it's exit code (as Redditor u/OneMoreTurn [pointed out](https://www.reddit.com/r/bash/comments/1qxdk4v/comment/o3vvd9u/) pointed out).

Another great reason for using `if else` statements is when the error handling is simple, but requires multiple steps.

```
if ! some_command; then

```

#### Alerting on errors

You now know how to catch errors, and prevent them from doing irreparable damage to your systems (or worse; your reputation)! But there's one thing we haven't talked about and that is how to alert yourself of the errors you just learned how to control.

If your script is running inside an event triggered pipeline, you'll most likely find out about it sooner than later due to a lack of a green checkmark in your CI/CD platform not letting you merge your PR. But when your bash script is ran as a CronJob at a set interval, there's a high likelihood you won't be made aware until you feel the cascading effect of the script failure. Especially if these jobs run inside an unassuming namespace on a tooling cluster no-one ever bothers to check.

Here are some real world examples:

1. A cronjob cleaning up S3 files marked for deletion broke causing your S3 bucket to grow in size costing your company thousands!
2. Your certificate renewal cronjob ran into a problem, now you've let your important certificates lapse causing an hour long outage!
3. The credentials in your database changed and now your `PG_DUMP` cronjob can't connect. It's been 4 weeks since the last backup and your main database just corrupted itself!

In these scenarios it would have been nice (or crucial) to be made aware of the fact that something went sideways!

##### Slack or Teams webhooks

A very common way to alert yourself of any kind of issue inside a bash script is by sending a message to a Slack or Teams webhook. It is paramount that you send the webhook message to a seldom posted to, yet frequently visited channel. Otherwise the alert will be buried and you will be none the wiser!

```

 
database_backup.sh || curl -sS -X POST \
  -H "Content-Type: application/json" \

```

##### Notifox CLI

One option that I am partial to is the Notifox CLI. It's a tool that lets you send both Email and SMS to pre-configured audiences. I built Notifox to solve exactly this problem.

If the error is more urgent you can configure it to send an SMS instead.

In many cases you would want to alert your team of a successful operation as well. You can do this by piping a message into the Notifox CLI.

```
echo "${domain} cert was renewed" | notifox send -a ops-team -c email
```

Whatever you use, the point is the same: when your script fails (or does something you care about), make sure you hear about it. If you want to try the Notifox CLI, it's on [GitHub](https://github.com/notifoxhq/notifox-cli); install and usage are in the repo.
