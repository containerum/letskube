# Let's Kube

![Let's Kube](image.png)

**Work in progress** 

Example ansible playbooks for deploying a kubernetes cluster on centos-7 virtual cloud. 


**Requerements:**

- ansible >= 2.1  
- centos-7  


## Install 

Add our nodes in inventory. 

In group_vars:  
internal_net - internal subnet for kube-api, etcd, calico 

Start: 
```
ansible-playbook bootstrap.yaml -i inventory
```


## Roadmap 

- [x] install docker 17.12.1
- [x] install kubelet, kubectl, kubeadm 1.9.*
- [x] install etcd on host
- [x] init 1 master and many slave
- [x] make admin.conf
- [x] install calico
- [ ] install etcd on many host
- [ ] backup and restore etcd
- [ ] init multi master
- [ ] install flannel, canal
- [ ] update kubernetes cluster
