echo "Run uv sync"
uv sync --frozen --dev

echo "Running devcontainer setup"
if [ -n "$DEVCONTAINER_SETUP" ]; then
    bash $DEVCONTAINER_SETUP
fi
