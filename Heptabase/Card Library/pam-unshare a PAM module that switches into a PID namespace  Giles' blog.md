# pam-unshare a PAM module that switches into a PID namespace  Giles' blog

Today in my 10% time at [PythonAnywhere](https://www.pythonanywhere.com/) (we're a bit less lax than [Google](http://uk.businessinsider.com/google-20-percent-time-policy-2015-4?r=US&IR=T)) I wrote [a PAM module](https://github.com/gpjt/pam-unshare) that lets you configure a Linux system so that when someone `su`s, `sudo`s, or `ssh`es in, they are put into a private PID namespace. This means that they can't see anyone else's processes, either via `ps` or via `/proc`. It's definitely not production-ready, but any feedback on it would be very welcome.

In this blog post I explain why I wrote it, and how it all works, including some of the pitfalls of using PID namespaces like this and how I worked around them.

### Why write it?

At PythonAnywhere we use a variety of tools to sandbox our users. To a certain extent, we've hand-rolled our own containerisation system using the amazing primitives provided by the Linux kernel.

One of the problems with our sandboxes right now is that they don't allow listing of processes using normal tools like `ps`. This is because, for security, we don't mount a `/proc` inside the filesystem visible from our users' code. The reason for that is that we don't want people to see each other's processes, because -- if you're careless -- there can be secret information on the command lines, and command lines are visible from `/proc` and thus from `ps`. Our one and only [security incident](https://blog.pythonanywhere.com/122/) so far came from an error in the system that handles this.

The right way to solve this kind of problem in Linux is to use a combination of PID namespaces and mount namespaces.

### Namespaces

There are two kinds of namespaces we're interested in for this module:

#### PID namespaces

As [the docs say](http://man7.org/linux/man-pages/man7/pid_namespaces.7.html), "PID namespaces isolate the process ID number space, meaning that processes in different PID namespaces can have the same PID." Allowing different processes to have the same PID isn't important to us for this -- but the isolation is what we want. We want the processes that a user uses when they log in to the system to be in a separate namespace to every other user's.

#### Mount namespaces

These were the first kind of namespaces to be introduced into Linux, so they're sometimes confusingly referred to simply as "namespaces". Again, going to [the docs](http://man7.org/linux/man-pages/man7/namespaces.7.html): "Mount namespaces isolate the set of filesystem mount points, meaning that processes in different mount namespaces can have different views of the filesystem hierarchy." This is useful because we want each of our process namespaces to have access to its own `/proc`. When you go into a process namespace, you may have a set of process IDs that are different to the external system. But if you have access to the external filesystem, then you can still see the `/proc` on the external filesystem -- so, `ps ax` will show you processes outside.

What we need is to get our processes into both a PID namespace and a mount namespace, then umount `/proc` so that we don't see the external filesystem's one, then mount it again so that we see the one appropriate to our PID namespace.

This is actually pretty simple to do from the command line, if you have a recent version of Linux with linux-utils 2.23 or higher (for Ubuntu, that's Vivid or later -- or you can upgrade Trusty using [this PPA from Ivan Larionov](https://launchpad.net/\~xeron-oskom/+archive/ubuntu/util-linux)). If you're on a Linux command line (as root) and you have the right version, you can try it out:

```
# unshare --pid -- /bin/sh -c /bin/bash
# echo $$
1
```

The first command is a slightly complicated way of getting into a PID namespace -- `unshare --pid` on its own doesn't work, for reasons that are still hazy in my mind... Anyway, once that's done, we `echo` the PID of the current bash process, and we get `1` -- so we're definitely in our own process namespace. However, if you run `ps ax` you'll see all of the processes in the parent PID namespace, because (as I said before) the `/proc` that we see in our filesystem is the one associated with the parent. Naturally, we can't umount `/proc` because we'd be trying to umount the directory everyone else in the system is using -- the system would complain that it's busy. So the next thing is to switch into our own mount namespace, then umount our own private `/proc`, then mount a fresh one:

```
# unshare --mount
# umount /proc
# mount -t proc proc /proc
# ps ax
  PID TTY      STAT   TIME COMMAND
    1 pts/0    S      0:00 /bin/bash
   42 pts/0    S      0:00 -bash
   57 pts/0    R+     0:00 ps ax
# ls /proc
1          consoles   execdomains  ipmi       kpagecount     misc          schedstat  sys            version
42         cpuinfo    fb           irq        kpageflags     modules       scsi       sysrq-trigger  version_signature
58         crypto     filesystems  kallsyms   latency_stats  mounts        self       sysvipc        vmallocinfo
buddyinfo  devices    fs           kcore      loadavg        net           slabinfo   timer_list     vmstat
bus        diskstats  interrupts   keys       locks          pagetypeinfo  softirqs   timer_stats    xen
cgroups    dma        iomem        key-users  mdstat         partitions    stat       tty            zoneinfo
cmdline    driver     ioports      kmsg       meminfo        sched_debug   swaps      uptime
```

Awesome! We're in our own namespace.

### PAM

Now, if when we wanted to go into namespaces we had complete control over the code, the above would be entirely sufficient. For example, on PythonAnywhere we have web-based consoles. When someone connects to one of those, we have complete control over the code that is executed before they can start typing in. We could do the two `unshare` commands, then the `/proc` remount, then `su` to the appropriate user account, and then we'd be done.

But we don't always have control over this code path. For example, people can log in using `ssh`. And controlling what's done when someone does that is the domain of PAM.

PAM is Pluggable Authentication Modules. A program can link with PAM and hand over all of its authentication to it. For example, when you `ssh` in, the `ssh` daemon asks PAM to authenticate your credentials.

PAM itself delegates the authentication process to a set of modules that are implemented as shared libraries. For example, there's one to do normal Unix authentication using `/etc/passwd` or `nsswitch` -- but you could also have ones to do biometric authentication or whatever.

The directory `/etc/pam.d` contains configuration files saying which auth modules should be used for each PAM client app -- what to use to auth `ssh`, what to use to auth `sudo`, and so on, along with some common stuff for everything. [The syntax is, frankly, vile](https://twitter.com/gpjt/status/720943681797296128), but it's just about understandable if you put your mind to it.

Anyway, that's all this got to do with our problem? Well, PAM has four kinds of plugins:

- **Authentication management** modules, which handle checking people's credentials.

- **Account management** modules, which can allow/disallow access even for people who'd be otherwise authorised, based on other factors (eg. time of day).

- **Authentication token management** modules which do things like allowing people to change their passwords.

- **Session management** modules, which do session setup and teardown stuff. A standard module of this type is [pam_env](http://linux.die.net/man/8/pam_env), which sets up environment variables.

The last one kind of modules is the place where we can hook in our code. There's already a `[pam-chroot](https://sourceforge.net/projects/pam-chroot/)`, which is a session management module that puts the user into a chroot jail. So my goal with this module was essentially to write something like that which did the same kind of thing, but for process namespaces.

### Implementation

Here's a minimal PAM session module that just prints stuff when people enter and leave a session (for example, when their `su` session starts, and when it ends):

```
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define  PAM_SM_SESSION
#include <security/pam_modules.h>

PAM_EXTERN int pam_sm_open_session(pam_handle_t *pamh, int flags, int argc, const char **argv) {
    printf("pam_basic pam_sm_open_session\n");
    return PAM_SUCCESS;
}

PAM_EXTERN int pam_sm_close_session(pam_handle_t *pamh, int flags, int argc, const char **argv) {
    printf("pam_basic pam_sm_close_session\n");
    return PAM_SUCCESS;
}
```

Save it as `pam_basic.c` and you can compile it with this:

```
gcc -c -fPIC -fno-stack-protector -Wall pam_basic.c
ld --shared -o pam_basic.so pam_basic.o -lpam
```

...then install it like this:

```
sudo cp pam_basic.so /lib/security/
```

...and enable it by adding this line towards the end of `/etc/pam.d/su` (before the `@include`s):

```
session required      pam_basic.so
```

Then try `su`ing to another user. You'll see the `open_session` and `close_session` messages as you enter and exit the `su`ed environment.

#### Enter the namespaces

So, you'd think that getting this to work with PID namespaces would be really simple; just make the appropriate system calls in the `pam_sm_open_session` function to switch to a new PID namespace, then to a new mount namespace, then `umount` and then `mount /proc`, and you're all set. The system function to switch into a new namespace is even called `unshare`, just like the command-line tool.

But, of course, it's a little bit more complicated than that. It comes down to processes.

When you make the `unshare` system call to enter a PID namespace, your current process's PID namespace is unaffected. Instead, the new namespace is used for any child processes you create using (eg.) `fork`. When you spin off your first child process after calling `unshare`, then that process is the "owner" of the PID namespace -- kind of like `init` is for the machine as a whole.

By contrast, the `unshare` for mount namespaces switches you into a new namespace right away.

Now, when you're doing an `su`, your PAM module is executed in-process by `su`, before it spins off the child process that will handle the user-switched session. So you can do the two `unshare`s in there, and you'll wind up with a child process that has its own mount and PID namespaces. But that will still have the external system's `/proc` mounted, so `ps ax` will still show all processes. No problem -- you can also `umount /proc` inside the PAM code. Now the user can't do `ps` at all.

But the re-mounting of `/proc` can't happen in the PAM process, because it's not in the new PID namespace. Remember, only its children will be. If we were to do the re-mount in the PAM process, we'd still get the `/proc` for the parent PID namespace.

So the trick is to do the re-mount in a child process. But the child process that's spun off by `su` is out of our control; it's a shell or whatever the user specified. Even worse, the child process will be run as the user we're `su`ing to, and only `root` can mount `/proc`.

OK, you might think -- perhaps, after setting things up so that the `su` process, thanks to the PAM module, is in the right mount namespace, and its children will be in the right PID namespace, we could umount `/proc`, then spin off a short-lived child process to do the re-mount of `/proc`, then when it's exited, continue?

What happens when you do that is that the PID namespace dies when your short-lived child process exits. Remember, the first child process you create after doing the `unshare` to enter the PID namespace is the "init" equivalent. When it dies, the PID namespace dies with it (and the kernel kills all of its child processes). (BTW I think this is why, when you kill the process you've specified in a `docker run` command, all of its child processes die -- even if you've detached them.)

My solution to this is a bit of a hack. I spin off a child process, which, being in a fresh PID namespace, will have PID 1. This is our parent process, our "init", and when it exits, the PID namespace will be shut down. But it's running as root, so it can mount `/proc` We know that the next process to be started in the namespace will have the PID 2. So, the child process mounts `/proc`, then waits until it sees a process with PID 2 -- then it waits for that process to die:

```
        while (kill(2, 0) == -1 && errno == ESRCH) {
            // short-lived busy wait
        }
        while (kill(2, 0) != -1 && errno != ESRCH) {
            // long-lived, poll twice a second
            usleep(500000);
        }
```

(If you're wondering why I'm using `kill(`*pid*`, 0)` and polling, rather than `waitpid` for the process to die, it's because process 2 isn't a child of process 1, and you can only use `waitpid` with your own child processes.).

This seems to work fine! Here's the complete source code of the current version, annotated. [GitHub repo here](https://github.com/gpjt/pam-unshare).

```
#define _GNU_SOURCE

#include <syslog.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdarg.h>
#include <errno.h>
#include <unistd.h>
#include <signal.h>

#include <sched.h>

#include <sys/mount.h>

#define  PAM_SM_SESSION
#include <security/pam_modules.h>
```

The standard import-y stuff. The only points of note are the `#define _GNU_SOURCE`, which is needed to use the `unshare` function, and the `#define  PAM_SM_SESSION`, which sets things up so that PAM knows we're writing a session management module.

```
static void _pam_log(int err, const char *format, ...) {
  va_list args;

  va_start(args, format);
  openlog("pam_unshare", LOG_PID, LOG_AUTHPRIV);
  vsyslog(err, format, args);
  va_end(args);
  closelog();
}
```

A nice wrapper around `syslog`, shamelessly stolen from [pam-chroot](https://code.google.com/archive/p/pam-chroot/).

```
PAM_EXTERN int pam_sm_open_session(pam_handle_t *pamh, int flags, int argc, const char **argv) {
```

So this is our entry point when a PAM session is started:

```
    const char *username;
    if (pam_get_user(pamh, &username, NULL) != PAM_SUCCESS) {
        _pam_log(LOG_ERR, "pam_unshare pam_sm_open_session: could not get username");
        return PAM_SESSION_ERR;
    }
    _pam_log(LOG_DEBUG, "pam_unshare pam_sm_open_session: %s: start", username);
```

Get the username of the person we're `su`ing to, or who we're `ssh`ing in as, or whatever. Useful for logging.

```
    _pam_log(LOG_DEBUG, "pam_unshare pam_sm_open_session: %s: about to unshare", username);
    int unshare_err = unshare(CLONE_NEWPID | CLONE_NEWNS);
    if (unshare_err) {
        _pam_log(LOG_ERR, "pam_unshare pam_sm_open_session: %s: error unsharing: %s", username, strerror(errno));
        return PAM_SESSION_ERR;
    }
    _pam_log(LOG_DEBUG, "pam_unshare pam_sm_open_session: %s: successfully unshared", username);
```

This does both of the unshares; the `CLONE_NEWPID` means that our child processes will be in their own PID namespace, and the `CLONE_NEWNS` put the current process, and all of its future children, into a new mount namespace.

```
    if (access("/proc/cpuinfo", R_OK)) {
        _pam_log(LOG_DEBUG, "pam_unshare pam_sm_open_session: %s: no need to umount /proc", username);
    } else {
```

If we're already in a situation where we don't have `/proc` then we don't want to blow up when we try to `umount` it, so this is a simple guard against that...

```
        _pam_log(LOG_DEBUG, "pam_unshare pam_sm_open_session: %s: about to umount /proc", username);
        int umount_err = umount("/proc");
        if (umount_err) {
            _pam_log(LOG_ERR, "pam_unshare pam_sm_open_session: %s: error umounting /proc: %s", username, strerror(errno));
            return PAM_SESSION_ERR;
        }
        _pam_log(LOG_DEBUG, "pam_unshare pam_sm_open_session: %s: successfully umounted /proc", username);
    }
```

And here we do the `umount` if we need to.

```
    _pam_log(LOG_DEBUG, "pam_unshare pam_sm_open_session: %s: about to kick off a subprocess", username);
    int pid = fork();
```

We've kicked off our subprocess:

If we're in the new child process...

```
        _pam_log(LOG_DEBUG, "pam_unshare pam_sm_open_session: %s: in subprocess, about to mount /proc", username);
        if (mount("proc", "/proc", "proc", MS_NOSUID|MS_NOEXEC|MS_NODEV, NULL)) {
            _pam_log(LOG_ERR, "pam_unshare pam_sm_open_session: %s: subprocess: error mounting /proc: %s", username, strerror(errno));
            exit(1);
        }
        _pam_log(LOG_DEBUG, "pam_unshare pam_sm_open_session: %s: in subprocess, successfully mounted /proc", username);
```

Do the umount.

```
        _pam_log(LOG_DEBUG, "pam_unshare pam_sm_open_session: %s: in subprocess, about to busy-wait for second child", username);
        while (kill(2, 0) == -1 && errno == ESRCH) {
        }
        _pam_log(LOG_DEBUG, "pam_unshare pam_sm_open_session: %s: in subprocess, second child has appeared, switching to slow-poll", username);

        while (kill(2, 0) != -1 && errno != ESRCH) {
            usleep(500000);
        }
        _pam_log(LOG_DEBUG, "pam_unshare pam_sm_open_session: %s: in subprocess, done waiting, exiting", username);

        exit(0);
    }
```

The do the wait for PID 2.

```
    _pam_log(LOG_DEBUG, "pam_unshare pam_sm_open_session: %s: done", username);
    return PAM_SUCCESS;
}
```

This is run if we're not in the child process -- just continue as normal.

```
PAM_EXTERN int pam_sm_close_session(pam_handle_t *pamh, int flags, int argc, const char **argv) {
    const char *username;
    if (pam_get_user(pamh, &username, NULL) != PAM_SUCCESS) {
        _pam_log(LOG_ERR, "pam_unshare pam_sm_close_session: could not get username");
        return PAM_SESSION_ERR;
    }
    _pam_log(LOG_DEBUG, "pam_unshare pam_sm_close_session: %s: start", username);
    _pam_log(LOG_DEBUG, "pam_unshare pam_sm_close_session: %s: done", username);
    return PAM_SUCCESS;
}
```

And that, of course, is just a dummy `pam_sm_close_session`, which needs to be there for completeness.

That's basically it.

### What's next?

I'm pretty pleased with how this worked out (especially given that I didn't really understand PAM or namespaces when I started working on this stuff this morning). But it's not quite what we need. We already have some pretty powerful code that sets up sandboxed filesystems, and this wouldn't be compatible with the module as I've written it. Possibly we'll simply use the unsharing portion of this, and then use another mechanism to handle the remounting of `/proc`.

But I figured it might be worth putting this code out there, just in case anyone else is interested in how PAM and namespaces interact, and what some of the pitfalls -- and their workarounds -- are.

Comments welcome!

### Acknowledgements

Many thanks to Ed Schmollinger for [pam-chroot](https://sourceforge.net/projects/pam-chroot/), which was the inspiration for all this, and to Jameson Little for [simple-pam](https://github.com/beatgammit/simple-pam), which was simple enough that I had the confidence to start off coding a PAM module.