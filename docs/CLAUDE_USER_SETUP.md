# Claude User Setup

Isolated environment for SDK development with latest Claude Code CLI.

---

## Why This Setup

- **jan's Claude Code** (v2.0.76): Patched Node.js version at `/home/jan/.claude/local/claude`
- **claude's Claude Code** (v2.1.3): Unpatched Node.js version at `/home/claude/.claude/local/claude`

Separate installs allow testing with latest CLI without affecting jan's patched version.

---

## Components

### 1. Claude User Account

```bash
# Created with:
sudo useradd -s /bin/bash -d /home/claude claude
sudo passwd claude
```

### 2. Group Permissions (jan can read/write claude's files)

```bash
sudo usermod -aG claude jan          # jan in claude group
sudo chown -R claude:claude /home/claude
sudo chmod -R g+rwX /home/claude
sudo find /home/claude -type d -exec chmod g+s {} \;  # setgid on dirs
# umask 002 in .bashrc ensures new files are group-writable
```

### 3. Claude Code CLI (npm/Node.js version)

```bash
# Installed via npm (not the bun binary installer)
npm install --prefix ~/.claude/local @anthropic-ai/claude-code@2.1.3

# Install location: ~/.claude/local/node_modules/@anthropic-ai/claude-code/
# Executable: ~/.claude/local/claude (wrapper that runs cli.js via Node.js)
```

### 4. GitHub SSH Access

Claude user needs access to jan's GitHub SSH key for git operations (push/pull).

```bash
# As jan — copy key and set group-readable permissions
sudo cp /home/jan/.ssh/id_ed25519 /home/claude/.ssh/id_ed25519
sudo chown jan:claude /home/claude/.ssh/id_ed25519
sudo chmod 640 /home/claude/.ssh/id_ed25519
```

Then create `/home/claude/.ssh/config` (as claude user):

```
Host github.com
    IdentityFile ~/.ssh/id_ed25519
    IdentitiesOnly yes
```

Verify with:
```bash
ssh -T git@github.com
# Expected: Hi yannbam! You've successfully authenticated...
```

Note: The SSH agent socket at `/run/user/1000/keyring/ssh` belongs to jan and is not accessible to claude — the key file copy is the right approach here.

---

### 5. Python Environment (pyenv-virtualenv)

```bash
# pyenv installed at /home/claude/.pyenv
# Python 3.12.11 compiled from source
# Virtualenv: claude-agent-sdk-dev

# Auto-activates in SDK directory via .python-version file
cd /home/claude/anthropic-sdks/claude-agent-sdk-python
# → activates claude-agent-sdk-dev automatically
```

---

## Quick Reference

| Item | jan | claude |
|------|-----|--------|
| Home | `/home/jan` | `/home/claude` |
| Claude CLI | 2.0.76 (patched) | 2.1.3 (unpatched) |
| CLI install | `~/.claude/local/node_modules/` | `~/.claude/local/node_modules/` |
| CLI executable | `~/.claude/local/claude` | `~/.claude/local/claude` |
| Python | pyenv 3.12.11 | pyenv 3.12.11 |
| SDK venv | `claude-agent-sdk-dev` | `claude-agent-sdk-dev` |
| Prompt color | Green | Purple |

---

## Switching Users

```bash
# From jan to claude
sudo -u claude -i

# Or su with password
su - claude
```

---

## Updating Claude Code for claude user

```bash
npm update -g @anthropic-ai/claude-code
# Or specific version:
npm install -g @anthropic-ai/claude-code@X.Y.Z
```

This does NOT affect jan's patched installation.
