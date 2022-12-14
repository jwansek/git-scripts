#!/bin/bash

echo -n "Input repo name to delete (excluding the .git suffix): "
read repo

rm -fvr /srv/git/$repo.git
rm -fvr ~/$repo*
rm -fv /srv/www/repositories/$repo*

bash /srv/www/git-scripts/restart_ui.sh
