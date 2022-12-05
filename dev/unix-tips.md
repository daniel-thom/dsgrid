# UNIX Workflow Tips on NREL's HPC Systems

This page aims to help new UNIX users become more efficient with HPC computers and file systems. It
describes common HPC usage patterns and is not intended to be a comprehensive guide to UNIX/Linux
systems or `bash`.

Please refer to these resources for thorough documentation and training.

- https://github.com/NREL/HPC/blob/master/general/bash/README.md: Detailed `bash` information
- https://github.com/NREL/HPC/tree/master/general/intro-to-linux: Introduction to Linux

[Conventions](#conventions) |
[Auto-completion](#auto-completion) |
[Keyboard shortcuts](#keyboard-shortcuts) |
[GNU core utilities](#gnu-core-utilities) |
[Editing files](#editing-files) |
[Zsh with Oh My Zsh](#zsh-with-oh-my-zsh) |
[Resource Monitoring](#resource-monitoring) |
[HPC Use Cases](#hpc-use-cases)


## Conventions
The page uses several `bash` features that you'll need to understand. This section describes them
briefly.

##### Environment variables
```
# Set by the system
$ echo "current user is $USER"
# User-defined
$ export MY_ENV_VAR=val1
$ echo "The value of MY_ENV_VAR is $MY_ENV_VAR"
```

##### Home directory
These examples are identical. `bash` will list the content of your home directory.
```
$ ls ~
$ ls /home/$USER
```

##### Pipes
In this example `bash` will forward all `stdout` from `squeue` to the `grep` utility which will
only print lines that contain the string `PD`.
```
$ squeue -u $USER | grep PD
```

##### Redirection
In this example `bash` will forward the output of the command into a file, overwriting it if it exists.
```
echo "hello world" > file.txt
```
In this example `bash` will append the text to the end of the file.
```
echo "hello world" >> file.txt
```

##### Command output substitution
This example will run the command `hostname` and insert the output into the string.
```
$ echo "current system hostname is $(hostname)"
# This is equivalent.
$ echo "current system hostname is `hostname`"
```

##### Shell expansion
In this example `bash` will expand the wildcard `*` characters to include all CSV files in a
directory tree. The included directories are all directories in the current directory that start
with `P` and all subdirectories of those.

**Note**: The `-f` option tells `ls` not to sort the output. You will get faster results on the
Lustre filesystem with this option.
```
$ ls -f P*/*/*.csv
```
`bash` returns each of those files to `ls`, and so this is equivalent to the following (assuming
these are the only directories and files that match):
```
$ ls -f P1/subdir1/file1.csv P1/subdir1/file2.csv P2/subdir1/file1.csv P2/subdir1/file2.csv
```

**Note**: Be mindful of the impact of this type of command on the Lustre filesystem and the current
node. The HPC team specifically recommends against running commands like `ls -l`, especially when
the returned results will be large. They also strongly recommend against running long filesystem
operations on a login node.

##### Configuration file
You can customize your `bash` configuration in the file `~/.bashrc`. In order for changes to take
effect you must restart the shell or run
```
$ source ~/.bashrc
```

## Auto-completion
Shells record the command you enter in a history file, up to some limit. You can use this history
to retrieve common commands and auto-complete them.

### Command history
The simplest way to retrieve your shell history is with the `history` command.
```
$ history
```
This is likely very long and not useful by itself. Filter the output with `grep`, like this:
```
$ history | grep squeue
```
or
```
$ history | grep squeue | less
```

### Auto-complete with a substring
`bash` supports a feature where, if you press the up arrow after starting a command, it will search
backward through your history to find matches. For example, if you type `sq` followed by the up
arrow key, it will rotate through your `squeue` commands.

This feature is disabled by default on Eagle. You can enable it in the file `~/.inputrc`. First,
check if you have this file and if so, what content is already present. Assuming you don't have it,
run this command (and press enter) and restart your shell to enable the feature.
```
$ cat << EOF >> ~/.inputrc
$include /etc/inputrc

# arrow up
"\e[A":history-search-backward
# arrow down
"\e[B":history-search-forward
EOF
```

There is another `bash` feature to consider enabling in the same file. By default, `bash` will only
tab-complete file paths up to the first non-matching character. Suppose a directory has two files:
`file1.txt` and `file2.txt`. If you type `ls fi` and then press `tab`, bash will auto-complete to
`file`. If you press `tab` again, it will show you the two complete filenames. But you have to type
`1` or `2` in order to complete the full name.

Some people prefer this behavior; others want `bash` to iterate through each possible option every
time `tab` is pressed (like in a Windows shell). You can enable that behavior by adding this line
to `~/.inputrc`.
```
$ echo '"#"\C-i": menu-complete' >> ~/.inputrc
```
Restart your shell to make it take effect.

**Note**: `zsh` enables both of these features by default. Refer to [this](#zsh-with-oh-my-zsh)
section.

### Ctrl-r / Ctrl-s
You can press `Ctrl-r` and then type a substring from a previous command. The
substring does not need to start with the beginning of the command. `bash` will
search backward through your history to find matches. Keep pressing
`Ctrl-r` to iterate. If you go too far, press `Ctrl-s` to reverse directions.

### history size
Check the current history sizes with these environment variables.
```
echo $HISTSIZE
50000
echo $HISTFILESIZE
50000
```
You can change them by adding lines like this to your `~/.bashrc` file.
```
export HISTSIZE=60000
export HISTFILESIZE=60000
```

## Aliases
`bash` provides a way for you to define shortcuts for common commands.

Suppose that you want to change the output of `squeue` so that it doesn't truncate fields.
The command can be customized like this:
```
$ squeue --format="%.8i %.9P %30j %10u %.8T %.12M %9N"
```
You don't want to type such a long command every time. Instead, add an alias to
your `~/.bashrc` file, like this:
```
alias squeue='squeue --format="%.8i %.9P %30j %10u %.8T %.12M %9N"'
```
Every time you invoke `squeue` you will actually run with the customized format. If you ever
need to invoke the original command, prepend `squeue` with a backslash.
```
$ \squeue
```
You can view current aliases with this command:
```
$ alias
```

## Keyboard shortcuts
Refer to this [cheatsheet](https://github.com/NREL/HPC/blob/master/general/bash/cheatsheet.sh) for
a comphensive list of bash features and keyboard shortcuts. This section highlights a few common
shortcuts.

- `Ctrl-a` / `Ctrl-e`: Jump to beginning / end of line.
- `Alt-f / Alt-b`: Jump by word forward / backward.
- `Ctrl-k`: Delete all text from the cursor to the end of the line.
- `Ctrl-u`: Delete all text regardless of cursor position.
- `Alt-d / Ctrl-w`: Delete by word forward / backward.
- `Ctrl-l`: Clear screen.
- `Esc then .`: Paste last argument from last command.


## GNU core utilities
The HPC systems include the [GNU core utilities](https://www.gnu.org/software/coreutils).

This section highlights some common utilities that can help with your workflows.

Run this command to get comprehensive information. If `pinfo` is installed, you may prefer its
format.
```
$ pinfo coreutils
$ info coreutils
```

Read the `info` pages to get more information about a specific command.
```
$ pinfo ls
```

[cat](#cat) | [less](#less) | [tail](#tail) | [grep](#grep) | [find](#find) | [watch](#watch) | [sed](#sed)

### cat
This command will dump the entire contents of the file to the terminal.
```
$ cat file.txt
```
### less
This command will incrementally read a file and print its contents. You move up and down as well as
search. It supports `vi` keyboard shortcuts.
```
$ less file.txt
```

### tail
The `head` and `tail` commands print the beginning or ending lines of a file. `tail` can be
particularly useful if you want to see a file as it's being updated.

Suppose you configured `slurm` to write `stderr` for your job like this:
```
#SBATCH --error=job_%j.e
```
The log file at runtime is `job_123456.e`. You can "follow" updates in your terminal by running
```
$ tail -f job_123456.e
```

### grep
Use `grep` to search files or command output for strings or regular expressions.

This example will perform a basic text search.
```
$ grep my_substring my_log_file.txt
```

This example will peform a search with a regular expression recursively with a specific file
type.
```
$ grep -r --include=*.csv "Golden.*CO" my_output_directory
```

This example will filter the continually-updating output of a log file.
```
$ tail -f job_123456.e | grep "the error pattern I'm looking for"
```

### find
Use the `find` command to locate files or directories and optionally run commands on them.

The HPC team recommends that you use `lfs find` instead of the regular `find` command because it
is less impactful to the Lustre filesystem. It has a subset of the subcommands of the regular
`find` command.

By default it will print the contents of a directory recursively.
```
$ lfs find my_directory
```

Use `-name` to limit the output to files that match a name.
```
$ lfs find my_directory -name "*.csv"
```

Use `-type` to limit the output to files or directories.
```
$ lfs find my_directory -type d
$ lfs find my_directory -type f
```

If you want to run a command on each output, pipe the output to the core utility `xargs`.
```
$ lfs find my_directory -name "*.csv" | xargs ls
```

### watch
This command will run a command periodically. Here are two HPC use cases where it can be helpful.

Check if your slurm job has started:
```
$ watch -n 60 squeue -u $USER
```
**Note**: Running this command too frequently or indefinitely can negatively impact the management
servers.

Check the memory utilization of your running job on a compute node.
```
$ ssh your-compute-node
$ watch free -g
```

### sed
`sed` is a stream editor. This section describes only one of its many useful features: in-place
text substitutions.

Suppose that you need to change a value in many files. This example combines shell expansion with
`sed` to perform an in-place substitution in a directory of files where a parameter called
`parameter` needs to be changed from `10` to `20`.
```
$ sed -i "s/parameter = 10/parameter = 20/" */*/config.toml
```

**Note**: The HPC team specifically recommends against running long filesystem operations on the
login node. If you need to make such a change on a large number of files, acquire a compute node.

### Make a pipeline
Suppose that you submitted a bunch of jobs with the wrong walltime. The jobs have not yet started,
and so you can update them without having to cancel and resubmit them. Here's how you can do it by
combining the concepts discussed so far.

Let's build the full command incrementally. We'll start by confirming that we will modify the
correct jobs.

**Note**: This command searches for `PENDING` or `PD`. `PD` is what is `squeue` returns by default.
`squeue` returns `PENDING` with the modification mentioned above.
```
$ squeue -u $USER | grep "PENDING\|PD"
```

Next, use `awk` to split each line by whitespace and extract the job ID. (`awk` is another core
utility that has many other features.)
```
$ squeue -u $USER | grep "PENDING\|PD" | awk '{print $1}'
```
That should have printed only your pending job IDs. Next, wrap that command in a for loop and make
scontrol commands. This example prints the commands so that we can verify their correctness.

```
$ for x in $(squeue -u $USER | grep "PENDING\|PD" | awk '{print $1}'); do echo "scontrol update jobid=$x TimeLimit=24:00:00"; done
```

Assuming that output is correct, here is the final command.
```
$ for x in $(squeue -u $USER | grep "PENDING\|PD" | awk '{print $1}'); do scontrol update jobid=$x TimeLimit=24:00:00; done
```

## Editing files
These text editors are installed on NREL's HPC systems:
- `emacs`
- `nano`
- `vim`

`nano` is simple and straightforward. `Emacs` and `Vim` are powerful but have a learning curve.

### Vim
The best way to learn Vim basics is with the built-in tutorial.
```
$ vimtutor
```

### Configuration file
You will likely need to customize Vim's behavior. For example, if you develop Python code, you need
to convert tabs to spaces. Put these lines in `~/.vimrc`:
```
autocmd FileType python set tabstop=4
autocmd FileType python set shiftwidth=4
autocmd FileType python set expandtab
```

## Zsh with Oh My Zsh
You can change your default shell from `bash` to `zsh` and install the Oh My Zsh
configuration framework to get friendlier auto-completion as well as a more
customizable environment. Refer to their [main site](https://ohmyz.sh/) for more
information and their [installation
page](https://github.com/ohmyzsh/ohmyzsh/wiki).

The default configuration provides the following benefits:
- Search backward through shell history for command matches with the up arrow key.
- Automatically adds directories you visit to the directory stack.
- Provides aliases to easily access directories you've visited.
- Tab completion completes each possible match.

Show all directories you've visited (same as `dirs -v`)
```
$ d
```
Change to directory in stack position 1. Also applies to 2 - 9.
```
$ 1
```
Go back one directory.
```
$ ..
```
Go back two directories.
```
$ ...
```

**Note**: You can get similar behavior with `bash` if you use `pushd` and `popd` instead of `cd`.

There are many plugins to further improve your experience. Some recommendations:

- `zsh-autosuggestions`: Provides suggestions to complete a command as you type.
- `z`: Provides tab-completion for recently-visited directories.

## Persistent sessions
There are cases where you need to run a shell on a remote server in a persistent session. Suppose
you use `salloc` to start an interactive session on a compute node. Your shell is what keeps the
allocation alive. If you have such a session on your laptop and close the lid such that the
computer goes to sleep, you will lose your allocation. Here's what you can do instead:

Start `tmux` on a specific login node (i.e., `el2.hpc.nrel.gov` and not `eagle.hpc.nrel.gov`). (The
`screen` application behaves similarly.)
```
$ tmux
```
`tmux` is now running as a server on the login node and starts a shell.

Acquire a compute node.
```
$ salloc ...
```
Start your work on the compute node.

While something is running, put your laptop to sleep. The network will drop. Later, resume the
laptop and reconnect to the *same* login node.
```
$ tmux attach
```
You will reconnect to the exact same shell that is holding your allocation alive. Resume your work.

`tmux` has many other features not covered here. Consult the manpage or online help for more
information.

**Note**: Be mindful that the login nodes are shared resources. Your `tmux` sessions will keep
running until you exit them or until the servers are rebooted. Close them when you finish your
work.


## Resource Monitoring
It is important to understand the memory and CPU utilization of your jobs so that you are efficient
with your allocations. This section describes how you can monitor your jobs while they are running.

The examples assume that you have ssh'd into a compute node.

### CPU
`htop` shows the current utilization of each CPU in the system in a nice graphical interface. The
`load average` field shows the aggregate CPU utilization. Eagle compute nodes have 36 cores. If
each core is being used at 100%, the load average will be 36.0. That is what you want.
```
$ htop
```

### Memory
View the current memory utilization.
```
$ free -g
```

Monitor the memory utilization at a two-second interval.
```
$ watch free -g
```

### Local storage
This command monitors the utilization of the local compute node storage. It does not monitor reads
and writes to the Lustre filesystem.
```
$ iostat -t 1 -xm
```

### GPUs
Monitor how processes are using the GPUs in the system.
```
$ nvidia-smi -l
```

```
$ nvidia-smi pmon
```

### Multiple nodes
If you need to monitor multiple nodes at the same time, try using `tmux` combined with the
external script below. It will allow you to run commands simultaneously on each node.

Download this script: https://raw.githubusercontent.com/johnko/ssh-multi/master/bin/ssh-multi

Start the script from a shell that is not within a tmux session.
```
$ ./ssh-multi node1 node2 nodeN
```
It will start `tmux` with one pane for each node and synchonize mode enabled. Typing in one pane
types everywhere.

### Post execution
Slurm records resource utilization stats of your jobs. You can retrieve them with the `sacct`
utility.

This example reports the max memory utiization as `MaxRSS`. Refer to the info page for information
on how to get other stats.
```
$ sacct -j JOB_ID --format=JobID,JobName%30,state,start,end,QOS,Partition,Account,MaxRSS
```

## HPC Use Cases
- [Make in-place subsitutions in files](#sed)
- [Follow updates to log files](#tail)
- [Keep an interactive node allocation alive across laptop network drop](#persistent-sessions)
- [Make changes to pending Slurm jobs](#make-a-pipeline)
- [Check CPU and memory utilization in compute nodes](#resource-monitoring)
