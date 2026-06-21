
docker stop jupyterhub; docker image rm classroom-notebook:latest jupyter/base-notebook:latest jupyterhub/jupyterhub:latest --force; docker rm jupyterhub jupyter-richardbranham --force


docker volume rm jupyterhub-user-richardbranham

rm -rf /srv/jupyterhub/users/richardbranham

docker exec -it jupyterhub bash

sqlite3 /srv/jupyterhub/jupyterhub.sqlite

SELECT id, name FROM users;

https://jhub.branham.us/user/richardbranham/proxy/5000/ <== Make sure the trailing slash is present!

https://jhub.branham.us/user/richardbranham/proxy/5000/csv

