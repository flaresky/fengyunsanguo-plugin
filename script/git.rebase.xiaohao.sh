git fetch
git checkout xiaohao
git pull
git checkout $1
git rebase xiaohao
git commit -am "rebase to xiaohao"
git push origin $1
