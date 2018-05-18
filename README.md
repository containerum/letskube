# Let's Kube

![Let's Kube](image.png)

**Work in progress**

Ansible playbooks for deploying a Kubernetes cluster on virtual machines with CentOS 7.


**Requirements:**

- Ansible *2.1 or higher*
- CentOS 7


## Installation

Add your nodes in inventory.

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
- [x] init 1 master and multiple slaves
- [x] make admin.conf
- [x] install calico
- [ ] install etcd on multiple hosts
- [ ] backup and restore etcd
- [ ] init multi-master
- [ ] install flannel, canal
- [ ] update Kubernetes cluster
