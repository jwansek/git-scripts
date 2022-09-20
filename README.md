# git-scripts
Interactive scripts used for configuration of my git server - git.eda.gay

## Scripts

It is recommended to make symlinks to the home directory- e.g.:

`ln -s $(pwd)/add_git_key.sh ~/add_git_key && chmod +x ~/add_git_key`

`ln -s $(pwd)/del_repo.sh ~/del_repo && chmod +x ~/del_repo`

`ln -s $(pwd)/make_repo.py ~/make_repo && chmod +x ~/make_repo`

`ln -s $(pwd)/show_gitkey.py ~/show_gitkey && chmod +x ~/show_gitkey`

`ln -s $(pwd)/del_repo.sh ~/rm_repo && chmod +x ~/rm_repo`

Then repositories can be created with `ssh git@git.eda.gay "./make_repo"` or removed with `ssh git@git.eda.gay "./rm_repo"`.

## Web UI

Repositories that are set to public are rendered using [klaus](https://github.com/jonashaag/klaus), using a custom CSS file and Dockerfile. This is in the `klaus/` directory.
