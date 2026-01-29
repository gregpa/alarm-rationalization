# VSCode Quick Deploy Setup

## Quick Deploy Options

### Option 1: Command Palette (Easiest)
1. Press `Ctrl+Shift+P` (Windows/Linux) or `Cmd+Shift+P` (Mac)
2. Type "Run Task"
3. Select one of:
   - **🚀 Deploy to Production** - Interactive deployment with prompts
   - **⚡ Quick Push (No Prompts)** - Instant deploy with generic message
   - **🧪 Test Locally** - Run Streamlit locally
   - **✅ Validate Code** - Check for syntax errors

### Option 2: Keyboard Shortcut (Fastest)
1. Press `Ctrl+Shift+B` (Windows/Linux) or `Cmd+Shift+B` (Mac)
2. This runs the default build task: **🚀 Deploy to Production**

### Option 3: Terminal Menu
1. Click **Terminal** menu → **Run Task...**
2. Select your desired task

## Custom Keyboard Shortcuts (Optional)

Want a dedicated deploy key? Add this to your keybindings:

1. Press `Ctrl+Shift+P` → Type "Preferences: Open Keyboard Shortcuts (JSON)"
2. Add this:

```json
[
  {
    "key": "ctrl+shift+d",
    "command": "workbench.action.tasks.runTask",
    "args": "🚀 Deploy to Production"
  },
  {
    "key": "ctrl+alt+d",
    "command": "workbench.action.tasks.runTask",
    "args": "⚡ Quick Push (No Prompts)"
  }
]
```

Now you can:
- `Ctrl+Shift+D` - Deploy with prompts
- `Ctrl+Alt+D` - Quick deploy without prompts

## Tasks Available

| Task | Description | When to Use |
|------|-------------|-------------|
| 🚀 Deploy to Production | Interactive deploy script | When you want to review changes and write a good commit message |
| ⚡ Quick Push (No Prompts) | Instant deploy | Quick fixes, already reviewed changes |
| 🧪 Test Locally | Run Streamlit on localhost | Before deploying, test changes locally |
| ✅ Validate Code | Check Python syntax | Quick syntax check |

## Tips

- The default build shortcut (`Ctrl+Shift+B`) runs the deploy task
- All tasks show output in the terminal panel
- You can stop a running task with the trash can icon in the terminal
