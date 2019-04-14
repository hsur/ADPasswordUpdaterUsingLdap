# vim:fenc=utf-8 ff=unix ft=python ts=4 sw=4 sts=4 noet :

import ldap

class AD:
	conn = None

	def _unicodePassword(self, plainpasswd):
		return ('"%s"' % plainpasswd).encode("utf-16le")

	def __init__(self, server, base_dn):
		self.server = server
		self.base_dn = base_dn

		ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
		ldap.set_option(ldap.OPT_REFERRALS, 0)
		self.conn = ldap.initialize(self.server)

	def bind(self, netbiosname, username, password):
		try:
			username = "%s\\%s" % (netbiosname, username)
			self.conn.bind_s(username,password)
			return True
		except ldap.LDAPError as e:
			print(e)
			return False

	def get_userdn(self, loginname):
		filter = "(sAMAccountName=%s)" % (loginname,loginname)
		rt = self.conn.search_s(self.base_dn, ldap.SCOPE_SUBTREE, filter)
		for (dn,attrs) in rt:
			if dn:
				return dn
		return None

	def update_pwd(self, dn, newpass):
		unipass = self._unicodePassword(newpass)
		mod_attrs = [(ldap.MOD_REPLACE, 'unicodePwd', unipass)]
		try:
			self.conn.modify_s(dn, mod_attrs)
			return True
		except ldap.LDAPError as e:
			print(e)
			return False

	def unbind(self):
		try:
			self.conn.unbind_s()
			return True
		except ldap.LDAPError as e:
			print(e)
			return False
