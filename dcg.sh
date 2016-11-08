#!/bin/bash
#########################################################################
# Author: (zfly1207@126.com)
# Created Time: 2015-01-12 18:56:21
# File Name: dcg.sh
# Description: 
#########################################################################

VERSION=0.1.0

declare -A LANGUAGE_MODEL_SUPPORT
LANGUAGE_SUPPORT="1.Python"
LANGUAGE_MODEL_SUPPORT['Python']="1.simple 2.multiprocess"
#LANGUAGE_MODEL_SUPPORT['PHP']="1.ccc 2.ddd 3.iii"
#LANGUAGE_MODEL_SUPPORT['Golang']="1.aaa 2.sss"

DEVELOPER="zfly1207@126.com"
DATETIME=$(date '+%Y-%m-%d %H:%M:%S')

PROJECT_LANG=""
PROJECT_MODE=""
PROJECT_NAME=""
PROJECT_NAME_FOR_CLASS=""

BASEPATH=$(dirname $0)
USERPATH=$(pwd)

ENVIRONMENT=~/.dcg
ENV_TEMPS=${ENVIRONMENT}/templates
ENV_GIT_HOUSE=${ENVIRONMENT}/.gitresources
GIT_BASE_URL="https://github.com/githubvip1207/code_generator.git"

# 代码执行结果状态判断
# $1 必须是$?
# $2 如果执行失败输出的提示信息
function assertSuccess(){
	if [[ ${1} -ne 0 ]]; then
		pecho "error: ${2}"; exit 1
	fi
}

function pecho(){
	echo -e $1
}

# 获取创建项目的语言
function inputProjectLang(){
	pecho "\nWhat language for your project? ${LANGUAGE_SUPPORT}:"
	read _lang

	_langSupport=(${LANGUAGE_SUPPORT})
	if [[ ${_lang} =~ ^[0-9]+$ && ${_lang} -le ${#_langSupport[@]} ]];then
			PROJECT_LANG=$(echo ${_langSupport[${_lang} - 1]} | awk -F'.' '{print $2}')
	else
		pecho "Sorry, does not support the language of your choice."
		exit 1
	fi
}

# 获取创建指定语言的模型
function inputProjectMode(){
	_modeSupport=${LANGUAGE_MODEL_SUPPORT[${PROJECT_LANG}]}
	pecho "\nWhat mode for your ${PROJECT_LANG} project? ${_modeSupport}"
	read _mode

	_modeSupport=(${_modeSupport})
	if [[ ${_mode} =~ ^[0-9]+$ && ${_mode} -le ${#_modeSupport[@]} ]];then
			PROJECT_MODE=$(echo ${_modeSupport[${_mode} - 1]} | awk -F'.' '{print $2}')
	else
		pecho "Sorry, ${PROJECT_LANG} does not support the mode of your choice."
		exit 1
	fi
}

# 获取创建爱你项目的项目名
function inputProjectName(){
	pecho "\nWhat you want to use the name of the project?"
	read _name
	if [[ "${_name}" != "" ]];then
		PROJECT_NAME=${_name}
		PROJECT_NAME_FOR_CLASS=$(echo ${_name} | sed "s/^[a-z]/\U&/g")
	else
		pecho "Sorry, project Name can not be empty."
		exit 1
	fi
}

# 获取用户的输入数据
function userInput(){
	inputProjectLang
	inputProjectMode
	inputProjectName
	pecho "\nYou want to use ${PROJECT_LANG} to create a name for ${PROJECT_NAME} project, and use ${PROJECT_MODE} model? [y/n]"
	read _license
	if [[ "${_license}" == "y" ]];then
		pecho "\n\nproject created, please wait..."
	else
		pecho "\nExit task..."; exit 0
	fi
}

# ========

# 构造配置基础目录
function constructEnvDir(){
	pecho "\nChecking your basic environment..."
	if [[ ! -d ${ENVIRONMENT} ]];then
		mkdir -p ${ENVIRONMENT} ${ENV_GIT_HOUSE} ${ENV_TEMPS}
	fi
	pecho "-> Done."
}

# 初始化模板仓库
function constructTemps(){
	pecho "\nChecking your template library..."
	if [[ ! -e ${ENV_GIT_HOUSE}/.git ]];then
		git clone ${GIT_BASE_URL} ${ENV_GIT_HOUSE}
	else
		cd ${ENV_GIT_HOUSE} && git pull
	fi
	cp -r ${ENV_GIT_HOUSE}/templates/* ${ENV_TEMPS}/
	pecho "-> Done."
}

# =======

# 部署以及修改用户项目信息
function dobuild(){
	pecho "\nBuilding your project..."
	declare -l _originalName=${PROJECT_LANG}-${PROJECT_MODE}
	declare -l _source=${ENV_TEMPS}/${_originalName}
	cd ${USERPATH} && cp -r ${_source} ./${PROJECT_NAME}
	cd ./${PROJECT_NAME}
	assertSuccess $? "Building Error(-1)"

	# 在centos上完成替换源码中的关键值可以只指定-i属性，不指定值即可。
	# 如：find . -type f | xargs sed -i "s/FULL/NAME/g"
	# 但是在Mac os上-i属性必须指定非空值，为了兼容性，这里指定-i的属性值为.dcgbak。即指定生成的临时备份
	# 文件的后缀，替换完成后再删除。
	# find ./ -type f | xargs sed -i".dcgbak" "s/4/5/g" && find ./ -name "*.dcgbak" -exec rm -rf {} \;
	# 在centos上完成rename文件名可以直接使用rename命令，
	# 如下：find . -name "$FULL*" -type f | xargs rename "$FULL" "$NAME"
	# 但是在Mac os上默认没有安装rename命令，即使手动安装也与centos上的使用方法不一致，需要指定options为-s
	# find ./ -type f -name "aaa*" | awk -F'aaa' '{printf("mv %s %s \n", $0, $1"bbb"$2)}'

	# 替换项目中的占位符，目前支持如下占位符：
	# __PROJECTNAME__ 当前用户输入的项目名 
	# __PROJECTNAME_CLASS__ 当前项目的主入口文件类名
	# __AUTHOR__ 开发者信息
	# __CREATE_DATETIME__ 项目创建时间，格式：2015-01-14 01:37:59
	find ./ -type f | xargs sed -i".dcgbak" "s/__PROJECTNAME__/${PROJECT_NAME}/g" && find ./ -name "*.dcgbak" -exec rm -rf {} \;
	assertSuccess $? "Building Error(-2)"
	find ./ -type f | xargs sed -i".dcgbak" "s/__PROJECTNAME_CLASS__/${PROJECT_NAME_FOR_CLASS}/g" && find ./ -name "*.dcgbak" -exec rm -rf {} \;
	assertSuccess $? "Building Error(-3)"
	find ./ -type f | xargs sed -i".dcgbak" "s/__AUTHOR__/${DEVELOPER}/g" && find ./ -name "*.dcgbak" -exec rm -rf {} \;
	assertSuccess $? "Building Error(-4)"
	find ./ -type f | xargs sed -i".dcgbak" "s/__CREATE_DATETIME__/${DATETIME}/g" && find ./ -name "*.dcgbak" -exec rm -rf {} \;
	assertSuccess $? "Building Error(-5)"

	# 修改项目的名
	find ./ -type f -name "${_originalName}*" | awk -F"${_originalName}" '{if(NF==2){printf("mv %s %s \n", $0, $1"'${PROJECT_NAME}'"$2)}}' | bash
	assertSuccess $? "Building Error(-6)"

	pecho "-> Building is complete, please enjoy your project.\n\n"
}

userInput
constructEnvDir && constructTemps	
dobuild

# vim: set noexpandtab ts=4 sts=4 sw=4 :
