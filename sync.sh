#!/bin/bash

git submodule init
git submodule update

# install Node.js
git clone http://github.com/creationix/nvm.git $HOME/.nvm
source ~/.profile
nvm install stable

npm install -g hexo
npm install 

# npm install hexo-deployer-git
# npm install hexo-generator-feed --save
# npm install hexo-generator-sitemap --save
# npm install hexo-generator-baidu-sitemap --save-dev
# npm install hexo-generator-searchdb --save


