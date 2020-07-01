{
	"tag":"unique_name",
	"globals":{
		"target":"192.168.49.95,192.168.49.152"
		},
	"portscan":{
		"module/portscan/udp":{
			"name":"Module_SCAN_UDP",
			"maxport":"1000"
			}
	},
	"ports":{
		"25":{
			"module/smtp/nmap_enum":{
				"name":"Module_SMTP_nmapenum",
				"port":"25"
				},
			"module/smtp/nmap_vuln":{
				"name":"Module_SMTP_nmapvuln",
				"port":"25"
				}
		},
		"53":{
			"module/dns/dnsrecon":{
				"name":"Module_DNS_dnsrecon"
				}
		},
		"161":{
			"module/snmp/onesixtyone":{
				"name":"Module_SNMP_onesixtyone",
				"community":"/usr/share/seclists/Discovery/SNMP/common-snmp-community-strings-onesixtyone.txt"
				},
			"module/snmp/nmap_nse":{
				"name":"Module_SNMP_nmapnse",
				"port":"161"
				}
		}
	},
	"services":{
	},
	"generic":{
		"module/icmp/ping":{
			"name":"Module_ICMP_Ping"
			}
	}
}
