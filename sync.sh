#!/bin/bash

git submodule init
git submodule update

# install Node.js
curl https://raw.github.com/creationix/nvm/master/install.sh | sh

npm install 

# npm install hexo-deployer-git
# npm install hexo-generator-feed --save
# npm install hexo-generator-sitemap --save
# npm install hexo-generator-baidu-sitemap --save-dev
# npm install hexo-generator-searchdb --save


