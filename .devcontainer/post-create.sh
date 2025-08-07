echo "Run poetry install"
poetry install

echo "Running devcontainer setup"
if [ -n "$DEVCONTAINER_SETUP" ]; then
    bash $DEVCONTAINER_SETUP
fi
