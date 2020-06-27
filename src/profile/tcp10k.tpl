{
    "tag":"unique_name",
	"globals":{
        "target":"10.11.1.5"
    },
    "portscan":{
        "module/portscan/tcp":{
            "name":"Module_SCAN_TCP",
            "maxport":"10000"
        }
    },
	"services":{
        "http":{
            "module/http/dirsearch":{
                "name":"Module_HTTP_dirsearch",
                "secure":"False"
                },
            "module/http/nikto":{
                "name":"Module_HTTP_nikto",
                "secure":"False"
                }
			},
        "https":{
            "module/http/dirsearch":{
                "name":"Module_HTTP_dirsearch",
                "secure":"True"
                },
            "module/http/nikto":{
                "name":"Module_HTTP_nikto",
                "secure":"True"
                }
			}
	},
    "ports":{
        "21":{
            "module/ftp/nmap_all":{
                "name":"Module_FTP_nmapall",
                "port":"21"
                }
            },
        "22":{
            "module/ssh/userenum":{
                "name":"Module_SSH_userenum",
                "userfile":"/usr/share/seclists/Usernames/top-usernames-shortlist.txt"
                }
            },
        "25":{
            "module/smtp/nmap_enum":{
                "name":"Module_SMTP_nmapenum",
                "port":"25"
                },
            "module/smtp/nmap_vuln":{
                "name":"Module_SMTP_nmapvuln",
                "port":"25"
                },
            "module/smtp/smtpvrfy":{
                "name":"Module_SMTP_VRFY",
                "userfile":"/usr/share/seclists/Usernames/top-usernames-shortlist.txt"
                }
            },
        "53":{
            "module/dns/dnsrecon":{
                "name":"Module_DNS_dnsrecon"
                }
            },
        "80":{
            "module/http/dirsearch":{
                "name":"Module_HTTP_dirsearch",
                "secure":"False"
                },
            "module/http/nikto":{
                "name":"Module_HTTP_nikto",
                "secure":"False"
                }
            },
        "443":{
            "module/http/dirsearch":{
                "name":"Module_HTTP_dirsearch",
                "secure":"True"
                },
            "module/http/nikto":{
                "name":"Module_HTTP_nikto",
                "secure":"True"
                }
        },
        "445":{
            "module/smb/smbmap":{
                "name":"Module_SMB_smbmap"
                },
            "module/smb/enum4linux":{
                "name":"Module_SMB_enum4linux"
                },
            "module/smb/nbtscan":{
                "name":"Module_SMB_nbtscan"
                },
            "module/smb/nmap_enum":{
                "name":"Module_SMB_nmapenum",
                "port":"445"
                },
            "module/smb/nmap_vuln":{
                "name":"Module_SMB_nmapvuln",
                "port":"445"
                }
        }
    },
    "generic":{
        "module/icmp/ping":{
            "name":"Module_ICMP_Ping"
            }
    }
}
