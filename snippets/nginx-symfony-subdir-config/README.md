每次把 Symfony2/3 项目部署到服务器时，基本上都是使用单独的一个域名指向项目的 web 目录，并使用 Symfony 官方提供的 Nginx 的配置文件进行配置，由于个人对 Nginx 的了解一直停留在比较基础的层面，所以也没有过多的去折腾，下面是这次折腾出来的结果，可以把 Symfony 项目放到子目录进行访问，子目录之外的地方可以放其他可访问资源。

```
server {
        listen   80;

        root /var/www;
        server_name code.mj.com;
        index index.html index.php app.php;

        if ($uri ~ \.(css|png|js|gif|jpg|mp3|mp4)$) {
                break;
        }

        location /dir1 {
                if ($uri ~ \.(css|png|js|gif|jpg|mp3|mp4)$) {
                        break;
                }

                if ($uri !~ \/(app|app_dev)\.php) {
                        rewrite (.*)$ /dir1/app.php/$1 last;
                }
        }

        location ~ \.php(\/|$) {
                fastcgi_split_path_info ^(.+\.php)(/.+)$;
                fastcgi_pass 127.0.0.1:9000;
                fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
                include fastcgi_params;
        }

        location ~ /\.ht {
                deny all;
        }
}
```