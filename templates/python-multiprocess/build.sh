#!/bin/bash

PNAME=__PROJECTNAME__
VERSION=0.0.1
SCRATCH_DIR=$PNAME-$VERSION

rm -rf target
mkdir target && cd target && mkdir $SCRATCH_DIR

# 在这里将需要发布的文件，放到target目录下
cp -r ../bin ../conf ../lib ../src $SCRATCH_DIR

# 对发布的文件做一些处理，版本号替换，修改权限等
sed -i -e "s/__BUILD_VERSION__/$VERSION/" $SCRATCH_DIR/bin/__PROJECTNAME__.sh
chmod +x $SCRATCH_DIR/bin/*
# find $SCRATCH_DIR -name '*.sh' -exec chmod +x {} \;

# 添加log目录
#mkdir $SCRATCH_DIR/log

# 删除一些临时的文件
find -name '.svn' -exec rm -rf {} \; 2>/dev/null
find -name '.git' -exec rm -rf {} \; 2>/dev/null
find -name '.pyc' -exec rm -rf {} \; 2>/dev/null

# tar包用于自己打包测试
tar czf $SCRATCH_DIR.tar.gz $SCRATCH_DIR
# rpm包用于线下/线上的标准化部署
# fpm -s dir -t rpm -n $PNAME -v $VERSION --rpm-defattrfile=0755 --prefix=/usr/local/dev/prog.d $SCRATCH_DIR

#rm -rf $SCRATCH_DIR
