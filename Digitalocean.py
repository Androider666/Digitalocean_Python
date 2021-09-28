import requests
import json
regions = ("nyc3","nyc1","sfo1","nyc2","ams2","sgp1","lon1","ams3","fra1","tor1","sfo2","blr1","sfo3")
regions_info = "nyc 代表美国东部纽约，sfo代表美国西部加利福尼亚，lon代表英国伦敦, \
\nams代表荷兰阿姆斯特丹，tor代表加拿大多伦多，sgp代表新加坡，fra代表法国, blr代表德国，请直接复制粘贴，例如:sfo3\n"
sizes =  ("s-1vcpu-1gb","s-1vcpu-1gb-amd","s-1vcpu-1gb-intel","s-1vcpu-2gb","s-1vcpu-2gb-amd","s-1vcpu-2gb-intel","s-2vcpu-2gb","s-2vcpu-2gb-amd","s-2vcpu-2gb-intel","s-2vcpu-4gb","s-2vcpu-4gb-amd","s-2vcpu-4gb-intel","s-4vcpu-8gb","c-2","c2-2vcpu-4gb","s-4vcpu-8gb-amd","s-4vcpu-8gb-intel","g-2vcpu-8gb","gd-2vcpu-8gb","s-8vcpu-16gb","m-2vcpu-16gb","c-4","c2-4vcpu-8gb","s-8vcpu-16gb-amd","s-8vcpu-16gb-intel","m3-2vcpu-16gb","g-4vcpu-16gb","so-2vcpu-16gb","m6-2vcpu-16gb","gd-4vcpu-16gb","so1_5-2vcpu-16gb","m-4vcpu-32gb",
"c-8","c2-8vcpu-16gb","m3-4vcpu-32gb","g-8vcpu-32gb","so-4vcpu-32gb","m6-4vcpu-32gb","gd-8vcpu-32gb","so1_5-4vcpu-32gb","m-8vcpu-64gb","c-16","c2-16vcpu-32gb","m3-8vcpu-64gb","g-16vcpu-64gb","so-8vcpu-64gb","m6-8vcpu-64gb","gd-16vcpu-64gb","so1_5-8vcpu-64gb","m-16vcpu-128gb","c-32","c2-32vcpu-64gb","m3-16vcpu-128gb","m-24vcpu-192gb","g-32vcpu-128gb","so-16vcpu-128gb","m6-16vcpu-128gb","gd-32vcpu-128gb","m3-24vcpu-192gb","g-40vcpu-160gb","so1_5-16vcpu-128gb","m-32vcpu-256gb","gd-40vcpu-160gb",
"so-24vcpu-4vcpu-192gb","m3-32vcpu-256gb","so1_5-24vcpu-192gb","m6-32vcpu-256gb")
sizes_info = "s-1vcpu-1gb代表普通droplet,配置为1c1g；除s系列外其他都是独享cpu,如g,c,m. \nc2-4vcpu-8gb代表cpu加强(4c8g),m系列代表内存加强m3-4vcpu-32gb(4c32g),\n配置请直接从给出的选项中复制粘贴，如：s-1vcpu-1gb\n---------------------------------"
LinuxOS = ('freebsd-11-x64-zfs', 'freebsd-11-x64-ufs', 'freebsd-12-x64-ufs', 'freebsd-12-x64-zfs', 'rancheros', 'ubuntu-20-04-x64', 'fedora-34-x64', 'centos-7-x64', 'ubuntu-18-04-x64', 'centos-8-x64', 'debian-9-x64', 'debian-10-x64', 'fedora-33-x64', 'ubuntu-21-04-x64', 'ubuntu-20-10-x64', 'skaffolder-18-04', 'izenda-18-04', 'quickcorp-qcobjects-18-04', 'fathom-18-04', 'optimajet-workflowserver-18-04')
#data = {"ssh_keys":null,"backups":false,"ipv6":true,"user_data":null,"private_networking":null,"volumes": null,"tags":["web"]}

mytoken = input("请输入你的token值，确保输入正确\n")
auth = "Bearer "+ mytoken
headers ={
		"Content-Type":"application/json",
		"Authorization": auth
}
while 1:
	print("0 查看账户信息 \n1 创建指定个数droplet \n2 删除单个droplet \n3 查看所有droplet \n4 上传ssh密钥 \n5 查找所有ssh密钥")
	print("--------------")
	enter_code = input("请输入接下来操作对应的数字\n")
	if enter_code == '0':
		url_account = 'https://api.digitalocean.com/v2/account'
		response = requests.get(url_account,headers=headers)
		response_code = response.status_code
		if response_code == 200 :
			#print(response.text)
			info_obj = json.loads(response.text)["account"]
			print("邮箱:"+info_obj["email"])
			print("droplet限额:"+str(info_obj["droplet_limit"]))
			print("浮动ip限额:"+str(info_obj["floating_ip_limit"]))
			print("账户状态:"+info_obj["status"])
			print("================================")
			print("\n")
		elif response_code == 401 :
			print("unauthorized")
		elif response_code == 429 :
			print("request too many times")
		elif response_code == 500 :
			print("server error")
		else :
			print("other failure")
	elif enter_code == '1':
		url_create = "https://api.digitalocean.com/v2/droplets"
		data_create = {"ssh_keys":[],"backups":"false","ipv6":"true","user_data":"","private_networking":"","volumes":None,"tags":["web"]}
		print(":)  创建droplet之前务必保证已上传过一个ssh密钥，否则vps无法登录  (:")
		cont_droplets = input("输入需要创建的droplet个数:\n")
		if cont_droplets == '1':
			drop_name = input("请输入droplet名字：\n")
			data_create["name"]=drop_name
		else :
			drop_names = []
			print("请输入多个droplet名字，每行一个：\n")
			tmp_cont = int(cont_droplets)
			for i in range(0,tmp_cont):
				dropnm = input()
				drop_names.append(dropnm)
			data_create["names"]=drop_names

		for i in range(0,len(sizes)):
			if ((i+1)%8)>0 :
				print(sizes[i] + "   ", end="")
			else :
				print(sizes[i])
		print("\n")
		print("------"*20)
		drop_size = input("请从给出的选项中复制粘贴进行输入,不要包含空格:\n")
		print(regions_info)
		print("------"*20)
		for i in range(0,len(regions)):
			print(regions[i]+"  ",end="")
		print("\n")
		print("-----"*20)
		drop_region = input("请直接从给出的选项中复制粘贴进行输入，不要包含空格\n")
		for i in range(0,len(LinuxOS)):
			if (i+1)%6>0 :
				print(LinuxOS[i]+"  ",end="")
			else :
				print(LinuxOS[i]+"\n")
		drop_image = input("\n请直接出给出的选项中选择系统复制粘贴，不要包含空格：\n")
		drop_ssh = input("请输入已上传的ssh的id或者fingerprint,只能输入一个:\n")

		#data_create["name"]=drop_name
		data_create["region"]=drop_region
		data_create["size"]=drop_size
		data_create["image"]=drop_image
		data_create["ssh_keys"].append(drop_ssh)
		print("系统为:"+drop_image +"   配置为:"+drop_size +"  地区为："+drop_region)
		confirm_create = input("请确认是否创建，y表示创建，n表示退出")
		print(data_create)
		if confirm_create == "y":
			res_create = requests.post(url_create,headers=headers,data=json.dumps(data_create))
			if res_create.status_code == 202:
				print("=====================创建成功======================")
				print("\n")
			else :
				print("创建失败")

		else :
			print("退出")
	elif enter_code == "2":
		id_drop_del = input("请输入将要删除的droplet的id:\n")
		url_del_onedrop = "https://api.digitalocean.com/v2/droplets/"+id_drop_del
		res_del_onedrop = requests.delete(url_del_onedrop,headers=headers)
		if res_del_onedrop.status_code == 204:
			print("删除成功")
			print("\n")
		else :
			print("删除失败")
	elif enter_code == "3":
		url_qu =  "https://api.digitalocean.com/v2/droplets"
		res_qu = requests.get(url_qu,headers=headers)
		if res_qu.status_code == 200:
			res_qu_obj = json.loads(res_qu.text)["droplets"]
			for i in range(0,len(res_qu_obj)):
				item_drop = res_qu_obj[i]
				print("id:"+ str(item_drop.get("id"))+"   ",end="")
				print("内存:"+str(item_drop.get("memory"))+"MB   ",end="")
				print("cpu核心数:"+str(item_drop.get("vcpus"))+"v   ",end="")
				print("系统:"+item_drop.get("image").get("slug")+"   ",end="")
				print("地区:"+item_drop["region"]["name"]+"   ",end="")
				print("ip1:"+item_drop.get("networks").get("v4")[0].get("ip_address")+"   ",end="")
				print("ip2:"+item_drop.get("networks").get("v4")[1].get("ip_address")+"   ",end="")
				print("创建时间:"+item_drop.get("created_at")+" ",end="")
				print("\n")
			print("droplet个数为：{a}".format(a=len(res_qu_obj)))
		else:
			print("error")
	elif enter_code == "4":
		url_ssh_up = "https://api.digitalocean.com/v2/account/keys"
		name_ssh = input("请为即将上传的ssh密钥命名:\n")
		pubkey_ssh = input("请上传ssh公钥，建议完整复制粘贴:\n")
		data_sshup = {"name":name_ssh,"public_key":pubkey_ssh}
		res_sshup = requests.post(url_ssh_up,headers=headers,data=json.dumps(data_sshup))
		if res_sshup.status_code==201 :
			print("ssh 密钥上传成功")
			print("\n")
		else :
			print("ssh 密钥上传失败")
	elif enter_code == "5":
		url_sshdown = "https://api.digitalocean.com/v2/account/keys"
		res_sshdown = requests.get(url_sshdown,headers=headers)
		if res_sshdown.status_code == 200:
			sshkeys_obj = json.loads(res_sshdown.text).get("ssh_keys")
			for sshkey_item in sshkeys_obj:
				print("name:"+sshkey_item.get("name")+"  ",end="")
				print("id:"+str(sshkey_item.get("id"))+"  ",end="")
				print("fingerprint:"+sshkey_item.get("fingerprint")+"\n")
			print("ssh密钥个数为：{a}".format(a=len(sshkeys_obj)))
			print("\n")
		else :
			print("error to get ssh")

