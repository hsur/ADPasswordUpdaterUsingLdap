#!/usr/bin/env python
# vim:fenc=utf-8 ff=unix ft=python ts=4 sw=4 sts=4 noet :

from AD import AD

AD_SERVER = "ldaps://ad.example.com"
BASE_DN = "OU=ADDOMAIN,DC=ADDOMAIN,DC=example,DC=com"
NETBIOSNAME = 'ADDOMAIN'

ADMIN_USER = 'Administrator'
ADMIN_PASS = 'password'

user_login = 'hoge'
new_pass = 'newpassword'

ad = AD(AD_SERVER, BASE_DN)
ad.bind(NETBIOSNAME, ADMIN_USER, ADMIN_PASS)
dn = ad.get_userdn(user_login)

if dn != None:
	ret = ad.update_pwd(dn, new_pass)
	if ret:
		print("OK")
	else:
		print("NG")

ad.unbind()
