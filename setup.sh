#!/bin/bash
#
# Claude Statusline - Setup Script (Linux / macOS)
# Installs the package and runs first-time initialization
#
set -e

BOLD="\033[1m"
GREEN="\033[32m"
YELLOW="\033[33m"
RED="\033[31m"
CYAN="\033[36m"
RESET="\033[0m"

echo ""
echo -e "${BOLD}========================================${RESET}"
echo -e "${BOLD}  Claude Statusline - Setup${RESET}"
echo -e "${BOLD}========================================${RESET}"
echo ""

# --- Check Python ---
PYTHON=""
for cmd in python3 python; do
    if command -v "$cmd" &>/dev/null; then
        version=$("$cmd" --version 2>&1 | grep -oP '\d+\.\d+' | head -1)
        major=$(echo "$version" | cut -d. -f1)
        minor=$(echo "$version" | cut -d. -f2)
        if [ "$major" -ge 3 ] && [ "$minor" -ge 8 ]; then
            PYTHON="$cmd"
            break
        fi
    fi
done

if [ -z "$PYTHON" ]; then
    echo -e "${RED}[!] Python 3.8+ is required but not found.${RESET}"
    echo "    Install Python from https://python.org"
    exit 1
fi

echo -e "${GREEN}[+]${RESET} Python: $($PYTHON --version)"

# --- Check pip ---
if ! $PYTHON -m pip --version &>/dev/null; then
    echo -e "${RED}[!] pip is not installed.${RESET}"
    echo "    Run: $PYTHON -m ensurepip --upgrade"
    exit 1
fi

echo -e "${GREEN}[+]${RESET} pip: $($PYTHON -m pip --version | cut -d' ' -f1-2)"

# --- Install or upgrade ---
echo ""
echo -e "${CYAN}Installing claude-statusline...${RESET}"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

if [ -f "$SCRIPT_DIR/pyproject.toml" ]; then
    # Installing from source
    echo -e "${YELLOW}[i]${RESET} Installing from source..."
    $PYTHON -m pip install -e "$SCRIPT_DIR" --quiet
else
    # Installing from PyPI
    echo -e "${YELLOW}[i]${RESET} Installing from PyPI..."
    $PYTHON -m pip install --upgrade claude-statusline --quiet
fi

echo -e "${GREEN}[+]${RESET} Package installed"

# --- Verify installation ---
if ! $PYTHON -m claude_statusline.cli --version &>/dev/null; then
    echo -e "${RED}[!] Installation verification failed${RESET}"
    exit 1
fi

VERSION=$($PYTHON -m claude_statusline.cli --version 2>&1)
echo -e "${GREEN}[+]${RESET} $VERSION"

# --- Check PATH ---
SCRIPTS_IN_PATH=false
if command -v claude-statusline &>/dev/null; then
    SCRIPTS_IN_PATH=true
fi

if [ "$SCRIPTS_IN_PATH" = false ]; then
    # Find where pip installed scripts
    SCRIPT_PATH=$($PYTHON -c "import sysconfig; print(sysconfig.get_path('scripts'))" 2>/dev/null || true)
    if [ -n "$SCRIPT_PATH" ] && [ -d "$SCRIPT_PATH" ]; then
        echo ""
        echo -e "${YELLOW}[!]${RESET} Scripts directory not in PATH: $SCRIPT_PATH"

        SHELL_NAME=$(basename "$SHELL")
        case "$SHELL_NAME" in
            bash)
                RC_FILE="$HOME/.bashrc"
                ;;
            zsh)
                RC_FILE="$HOME/.zshrc"
                ;;
            *)
                RC_FILE="$HOME/.profile"
                ;;
        esac

        echo -e "    Add to your ${CYAN}${RC_FILE}${RESET}:"
        echo -e "    ${BOLD}export PATH=\"$SCRIPT_PATH:\$PATH\"${RESET}"
        echo ""

        read -p "    Add to $RC_FILE now? [Y/n] " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]] || [[ -z $REPLY ]]; then
            echo "" >> "$RC_FILE"
            echo "# Claude Statusline" >> "$RC_FILE"
            echo "export PATH=\"$SCRIPT_PATH:\$PATH\"" >> "$RC_FILE"
            echo -e "    ${GREEN}[+]${RESET} Added to $RC_FILE"
            echo -e "    ${YELLOW}[i]${RESET} Run: source $RC_FILE"
            export PATH="$SCRIPT_PATH:$PATH"
        fi
    fi
fi

# --- Run init ---
echo ""
echo -e "${CYAN}Running first-time setup...${RESET}"
echo ""
$PYTHON -m claude_statusline.cli init

# --- Start daemon ---
echo -e "${CYAN}Starting daemon...${RESET}"
if command -v claude-statusline &>/dev/null; then
    claude-statusline daemon --start &
elif $PYTHON -m claude_statusline.cli daemon --start &>/dev/null & then
    true
fi
sleep 2

# --- Final test ---
echo ""
echo -e "${BOLD}========================================${RESET}"
echo -e "${BOLD}  Setup Complete!${RESET}"
echo -e "${BOLD}========================================${RESET}"
echo ""
echo -e "  ${GREEN}claude-statusline status${RESET}   - Show session status"
echo -e "  ${GREEN}claude-statusline theme${RESET}    - Browse 100 themes"
echo -e "  ${GREEN}claude-statusline --help${RESET}   - All commands"
echo ""

# Show a quick status preview
echo -e "${CYAN}Status preview:${RESET}"
$PYTHON -m claude_statusline.cli status 2>/dev/null || echo "(Status will be available after Claude Code generates data)"
echo ""
