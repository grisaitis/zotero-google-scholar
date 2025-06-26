curl -sSL https://raw.githubusercontent.com/GitAlias/gitalias/main/gitalias.txt > ~/.gitalias
echo "Created ~/.gitalias with default git aliases."
echo $(ls -l ~/.gitalias)
git config --global include.path ~/.gitalias
