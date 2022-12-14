## 不要なDocker Volumeの削除

-   ` $ docker volume rm $(docker volume ls -qf dangling=true)`
    or
-   `$ docker volume prune`
