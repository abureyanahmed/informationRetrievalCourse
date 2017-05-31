#make sure you call this file like: ./pushgit.sh "comment" "branch"
#eg: ./pushgit.sh "added a new bug" master
git add --all .
git commit -m "$1"
git push origin "$2"
