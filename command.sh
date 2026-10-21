git pull

echo '```' > Structure.md
tree -L 10 -I 'command.sh|__init__.py|README.md|.idea|__pycache__|Structure.md' >> Structure.md
echo '```' >> Structure.md

git add .
git commit -m "auto commit"
git push
