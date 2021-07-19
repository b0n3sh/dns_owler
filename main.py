#!venv/bin/python3

import re

queries = []
clients = {}
nl = '\n'
tab = '\t'

header = r"""
  ==========================================================================
  |     .___                            .__                                |
  |   __| _/____   ______   ______  _  _|  |   ___________        ___      |
  |  / __ |/    \ /  ___/  /  _ \ \/ \/ /  | _/ __ \_  __ \      (o,o)     |        
  | / /_/ |   |  \\___ \  (  <_> )     /|  |_\  ___/|  | \/     <  .  >    |   
  | \____ |___|  /____  >  \____/ \/\_/ |____/\___  >__|        --"-"---   |          
  |     \/    \/     \/                          \/            by b0n3sh.  |
  ==========================================================================
"""

with open('dnsmasq.log') as f:
    lines = f.read().split('\n')
    for line in lines:
        if "query[A]" in line:
            queries.append(line)

def parse_doc(clients):
    text = ""
    for ip in clients:
        temp = []
        text = text + f"""

<=== INFORME DE IP: {ip} ===>

    <> Dominios:"""
        for domain in clients[ip]['domains']:
            if clients[ip]['domains'][domain]['total_visits_domain'] == 1:
                temp.append(f"{domain} ha sido visitado {clients[ip]['domains'][domain]['total_visits_domain']} vez")
            else:
                temp.append(f"{domain} ha sido visitado {clients[ip]['domains'][domain]['total_visits_domain']} veces")

            temp.sort(key= lambda k: int(k.split()[-2]), reverse=True)
        for tempy in temp:
            text = text + f"""
            {tempy}
            """
    return text

for query in queries:
    splitted = query.split()
    full_domain = splitted[5]
    ip = splitted[7]
    date = '-'.join(splitted[0:3])
    if '.' not in full_domain:
        continue
    domain = '.'.join(full_domain.split('.')[-2:])

    if not ip in clients:
        clients[ip] = {}
        clients[ip]['domains'] = {}

    if not domain in clients[ip]['domains']:
            clients[ip]['domains'][domain] = {}

    if not full_domain in clients[ip]['domains'][domain]:
        clients[ip]['domains'][domain][full_domain] = {'visit_counter': 1, 'dates': []} 
    else:
        clients[ip]['domains'][domain][full_domain]['visit_counter'] += 1

    clients[ip]['domains'][domain][full_domain]['dates'].append(date)

for client in clients:
    for domain in clients[client]['domains']:
        visits = 0
        for subdomain in clients[client]['domains'][domain]:
            visits += clients[client]['domains'][domain][subdomain]['visit_counter']
        clients[client]['domains'][domain]["total_visits_domain"] = visits

with open('parsed.txt', 'w+') as c:
    c.write(header+'\n'*2)
    c.write(parse_doc(clients))
