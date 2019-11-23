<h1 style='text-align:center;'>git 常用命令</h1>
```shell
# settings
git config --global user.name "NAME"
git config --global user.email "email@qq.com"

# 初始化
git init

# 添加file
git add file1
git add file2
git add .

# 提交添加
git commit -m 'message'
```

```shell
# 查看状态和差异
git status
git diff file

# 查看提交日志
git log [--pretty=oneline]

# 版本回退
git reset --hard [HEAD^/commit_id]

# 查看命令日志
git reflog

# 撤销修改
git checkout -- readme.txt #意思就是，把readme.txt文件在工作区的修改全部撤销
git reset HEAD readme.txt #把暂存区的修改撤销掉（unstage），重新放回工作区

# 删除文件
git rm file
```

```shell
# 创建SSH Key
ssh-keygen -t rsa -C "youremail@example.com" #粘贴id_rsa.pub文件的内容到github

# 添加远程仓库
git remote add origin git@github.com:michaelliao/learngit.git

# 查看远程库
git remote

# 推送至远程仓库
git push [-u] origin master #第一次提交[-u]

# 克隆仓库
git clone git@github.com:michaelliao/gitskills.git
```

```shell
# 创建和切换分支
git branch dev
git checkout dev
git checkout -b dev #二合一
# 或
git switch dev 
git switch -c dev # create

# 查看分支
git branch

# 删除分支
 git branch -d dev

# 合并分支
git merge dev

# 查看分支合并图
git log --graph
```

```shell
# 查看标签
git tag 

# 创建标签
git tag tagName

# 删除标签
git tag -d v0.1

# 查看标签信息
git show tagName

# 给标签添加说明文字
git tag -a v0.1 -m "version 0.1 released" 1094adb #用-a指定标签名，-m指定说明文字

# 推送远程标签
git push origin v1.0

# 推送所有标签至远程
git push origin --tags

# 删除远程标签
git push origin :refs/tags/v0.9
```



