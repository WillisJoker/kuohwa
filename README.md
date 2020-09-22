# README #


## System Requirements
- CentOS 7
- Enable ISCSI
```shell=
yum install iscsi-initiator-utils
systemctl enable --now iscsid
```

## Use Persistent Volume
- Due to RWO, strategy of deployment must be Recreate
```yaml
strategy:
  type: Recreate
```

