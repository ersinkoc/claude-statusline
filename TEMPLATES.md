# Claude Statusline Templates

A collection of 20+ customizable statusline formats to match your personal style and workflow.

## Quick Start

```bash
# View all available templates
python select_template.py --list

# Set a template
python select_template.py --set vim

# Interactive selection
python select_template.py
```

## Available Templates

### 1. **compact** (Default)
Classic balanced format with all essential information.
```
[Opus 4.1] LIVE ~17:00 | 456msg 12.3M $90.0
```

### 2. **minimal**
Ultra-minimal, only the essentials.
```
O4.1 456m $90
```

### 3. **detailed**
Everything visible for maximum information.
```
Session #123 | Model: Opus 4.1 | Status: ACTIVE | Ends: 17:00 | Messages: 456 | Tokens: 12,345,678 | Cost: $89.99 | Remaining: 2h 0m
```

### 4. **emoji**
Rich with ASCII emoji indicators.
```
[O] (o) @17:00 #456 >12.3M $90.0
```
- `[O]` = Opus model
- `(o)` = Active status
- `@` = End time
- `#` = Message count
- `>` = Token count

### 5. **dev**
Developer-friendly format with technical notation.
```
[O4.1:LIVE] t=17:00 m=456 tok=12345k c=$89.99
```

### 6. **vim**
Vim statusline inspired format.
```
--INSERT-- O4.1 456L $90.0 [utf-8]
```
- Shows "INSERT" when active, "NORMAL" when idle
- Line count metaphor for messages

### 7. **powerline**
Powerline-style segmented display.
```
 O4.1 > ON > 456m > 12.3M > $90.0 
```

### 8. **matrix**
Cyberpunk/Matrix themed format.
```
[1] <O4.1> ::MSG:456 ::TOK:12345k ::CR:$89.99::
```
- Binary status indicator [1/0]
- Double colon separators

### 9. **nerd**
Clean format for nerd font users (ASCII compatible).
```
> O4.1 | 456 | 12.3M | $90.0
```

### 10. **zen**
Clean and peaceful, minimal distractions.
```
Opus 4.1 • 456 messages • $89.99
```

### 11. **hacker**
L33t speak for the underground.
```
[PWN3D] 04.1 m5g:456 t0k:12345k c0st:$90
```
- "PWN3D" when active, "N00B" when idle

### 12. **corporate**
Professional business format.
```
Model: Opus 4.1 | Status: Active | Units: 456 | Cost: $89.99 USD
```

### 13. **creative**
Artistic and playful presentation.
```
*O4.1* ~flowing~ [456 thoughts] [12.3M words] [$90.0 spent]
```
- "~flowing~" when active, "...paused..." when idle

### 14. **scientific**
Scientific notation for precision.
```
Model=O4.1 Active=T N=456 Tokens=1.23e+07 Cost=89.9900
```
- Boolean T/F for status
- Scientific notation for large numbers

### 15. **casual**
Friendly conversational format.
```
O4.1 is chatting - 456 messages so far ($89.99)
```

### 16. **discord**
Discord-style status format.
```
Playing Claude O4.1 • Online • 456 messages
```

### 17. **twitch**
Streaming platform inspired.
```
[LIVE] Coding with O4.1 | Chat: 456 | Viewers: 804
```
- Includes fun fake viewer count

### 18. **github**
GitHub activity style.
```
@O4.1 • 45 commits • 456 conversations • 12345k tokens
```
- Converts messages to "commits" metaphor

### 19. **terminal**
Classic command-line style.
```
claude@O4.1:~$ 456 msgs | $89.99
```

### 20. **json**
Structured JSON format for parsing.
```json
{"model":"O4.1","active":true,"msgs":456,"tokens":12345678,"cost":89.99}
```

## Configuration

### Method 1: Using the Template Selector

```bash
# Interactive mode with preview
python select_template.py

# Direct selection
python select_template.py --set terminal

# Via CLI tool
python claude_statusline.py manage template --set vim
```

### Method 2: Edit config.json

```json
{
  "display": {
    "template": "vim"
  }
}
```

### Method 3: Environment Variable

```bash
export CLAUDE_STATUSLINE_TEMPLATE=hacker
```

## Creating Custom Templates

To add your own template, edit `statusline_templates.py`:

```python
def custom_format(self, data: Dict[str, Any]) -> str:
    """Your custom format"""
    model = self._short_model(data.get('primary_model', '?'))
    msgs = data.get('message_count', 0)
    cost = data.get('cost', 0.0)
    
    return f"Your format here: {model} - {msgs} - ${cost}"
```

Then add it to the templates dictionary:

```python
self.templates = {
    # ... existing templates ...
    'custom': self.custom_format
}
```

## Template Components

Each template can access these data fields:

| Field | Description | Example |
|-------|-------------|---------|
| `primary_model` | Current model name | "Opus 4.1" |
| `active` | Session active status | true/false |
| `session_number` | Session ID | 123 |
| `session_end_time` | When session ends | "17:00" |
| `message_count` | Number of messages | 456 |
| `tokens` | Total tokens used | 12345678 |
| `cost` | Total cost in USD | 89.99 |
| `remaining_seconds` | Time left in session | 7200 |

## Best Practices

### For Different Environments

- **Windows Terminal**: All templates work, but avoid Unicode
- **macOS Terminal**: Full Unicode support, all templates work
- **Linux TTY**: Use ASCII-safe templates (minimal, dev, terminal)
- **SSH Sessions**: Prefer compact or minimal templates
- **tmux/screen**: vim, powerline, or terminal work well

### For Different Use Cases

- **Monitoring**: `detailed` or `scientific` for full information
- **Streaming**: `twitch` or `discord` for audience engagement
- **Development**: `dev`, `vim`, or `terminal` for technical focus
- **Presentations**: `corporate` or `zen` for clean display
- **Fun**: `hacker`, `matrix`, or `creative` for personality

## Switching Templates Dynamically

You can switch templates on-the-fly based on context:

```bash
# Work hours
python select_template.py --set corporate

# After hours
python select_template.py --set casual

# Debug mode
python select_template.py --set detailed
```

## Performance Notes

All templates have similar performance characteristics:
- Rendering time: <1ms
- Memory usage: Negligible
- Update frequency: Real-time

The template choice is purely aesthetic and doesn't affect data collection or processing.

## Troubleshooting

### Template Not Showing

```bash
# Check current template
python select_template.py --current

# Reset to default
python select_template.py --set compact
```

### Characters Not Displaying

Some templates use special characters. If you see garbled output:
1. Switch to an ASCII-safe template (minimal, dev, terminal)
2. Check terminal encoding (should be UTF-8)
3. Try a different terminal emulator

### Custom Template Not Working

1. Check syntax in `statusline_templates.py`
2. Ensure template is registered in `self.templates`
3. Test with sample data: `python statusline_templates.py`

## Examples by Personality

### The Minimalist
```bash
python select_template.py --set minimal
# Output: O4.1 456m $90
```

### The Data Scientist
```bash
python select_template.py --set scientific
# Output: Model=O4.1 Active=T N=456 Tokens=1.23e+07 Cost=89.9900
```

### The Gamer
```bash
python select_template.py --set discord
# Output: Playing Claude O4.1 • Online • 456 messages
```

### The Hacker
```bash
python select_template.py --set matrix
# Output: [1] <O4.1> ::MSG:456 ::TOK:12345k ::CR:$89.99::
```

### The Professional
```bash
python select_template.py --set corporate
# Output: Model: Opus 4.1 | Status: Active | Units: 456 | Cost: $89.99 USD
```

---

Choose the template that matches your style and workflow. Happy coding! 🎨