from __future__ import with_statement

import os


def set():
	os.environ["eDocumentService_DB_USER"] = 'root'
	os.environ["eDocumentService_DB_PASS"] = '25536035'
	os.environ["eDocumentService_DB_HOST"] = '127.0.0.1'
	os.environ["eDocumentService_DB_PORT"] = '3306'
	os.environ["eDocumentService_DATABASE"] = 'eDocumentService'
	os.environ["eDocumentService_DB_BACKEND"] = 'mysql'

	os.environ["eDocumentService_MEMCACHED_SERVICE"] = '127.0.0.1:11211'

	host_ip = get_host_ip()
	if os.environ["eDocumentService_DB_HOST"] == 'host':
		os.environ["eDocumentService_DB_HOST"] = host_ip

	os.environ[
		"eDocumentService_SECRET_KEY"] = 'e_#e-byj7#a+$v7#wmocwd8wp)+&wajk0axt70dl@)nsx!*glq'

	os.environ["eDocumentService_OTP_ACCOUNT"] = 'eDocService'
	os.environ["eDocumentService_OTP_PASSWORD"] = '1qaz2wsx3edc'

	os.environ["eDocumentService_EMAIL_HOST"] = 'smtp.gmail.com'
	os.environ["eDocumentService_EMAIL_PORT"] = '587'
	os.environ["eDocumentService_EMAIL_HOST_USER"] = 'incloud@forblind.org.tw'
	os.environ["eDocumentService_EMAIL_HOST_PASSWORD"] = 'mxztxeygnivlghak'


# export DOCKER_HOST_IP=$(ip route | awk '/default/ { print $3 }')
def get_host_ip():
	import subprocess
	p = subprocess.Popen(['/sbin/ip', 'route'],
		stdout=subprocess.PIPE,
		stdin=subprocess.PIPE)
	stdout, stderr = p.communicate()
	p = subprocess.Popen(['awk', '/default/ { print $3 }'],
		stdout=subprocess.PIPE,
		stdin=subprocess.PIPE)
	stdout, stderr = p.communicate(stdout)
	return stdout.strip().decode('utf8')
