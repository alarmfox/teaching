# Learn Linux Shell

## Anatomy of a Command

A Linux command typically consists of three parts:

1. **Command**: The action you want to perform.
2. **Options**: Flags or modifiers to change the behavior of the command.
3. **Arguments**: Additional information required by the command to execute.

Basic syntax:
```bash
command [options] [arguments]
```

## Essential Commands

### `ls` - List Directory Contents
Lists files and directories in the current directory.
```bash
ls [options] [directory]
```
**Options**:
- `-l`: Use long format, displaying detailed information (permissions, owner, size, etc.).
- `-a`: Include hidden files and directories (those starting with `.`).
- `-h`: Show human-readable sizes (e.g., KB, MB, GB).

### `cd` - Change Directory
Changes the current working directory.
```bash
cd [directory]
```

### `mkdir` - Create Directories
Creates new directories.
```bash
mkdir [directory_name]
```

### `touch` - Create Empty Files
Creates empty files or updates the timestamps of existing files.
```bash
touch [file_name]
```

### `rm` - Remove Files or Directories
Removes files or directories.
```bash
rm [options] [file/directory]
```
**Options**:
- `-r`: Recursively remove directories and their contents.
- `-f`: Force removal without confirmation (use with extreme caution).

### `cat` - Concatenate and Display Files
Displays the content of files to standard output.
```bash
cat [file_name]
```

### `chmod` - Change File Permissions
Modifies file or directory permissions (read, write, execute).
```bash
chmod [options] mode file
```
**Options/Modes**:
- `+`: Adds the specified permissions.
- `-`: Removes the specified permissions.
- `=`: Sets the permissions exactly as specified.

### `curl` - Transfer Data
Transfers data to or from a server, supporting various protocols (HTTP, HTTPS, FTP, etc.).
```bash
curl [options] [URL]
```
**Options**:
- `-O`: Save the downloaded file with its original name.
- `-o [file]`: Save the downloaded file with a specified name.
- `-L`: Follow redirects.
