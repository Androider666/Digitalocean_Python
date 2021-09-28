# Digitalocean_Python

This is a python program which is used to create vps using the Digitalocean API.

Noted : 
This program doesn't have complete functions of digitalocean API, and it only has some simple functions to create vps. One more thing, you should upload rsa.pub (ssh public key) to your digitalocean account manully before you using this python program. And the vps created by this program only accept logging in by ssh privete key, not password.

---------------------------------------------------------------
该脚本仅仅实现了Digitalocean API的部分功能，可以简单的进行vps创建删除，账号信息查询。
需要注意的是在使用该python脚本创建vps之前，必须先将ssh的公钥上传到你的digitalocean账号，也就是本python脚本仅支持创建ssh密钥登录的vps,不支持创建用户名_密码登录的vps。
还有一点，使用脚本的时候不要挂代理，否则可能导致程序崩溃或者报错。
