#!/bin/bash
# setup.sh

# Create directory structure
mkdir -p {squid,snort,suricata,elasticsearch,kibana}/{logs,config,rules}

# Download Snort rules
wget https://www.snort.org/downloads/community/community-rules.tar.gz -O snort/rules/community-rules.tar.gz
tar -xzvf snort/rules/community-rules.tar.gz -C snort/rules/

# Download Emerging Threats rules for Suricata
wget https://rules.emergingthreats.net/open/suricata-6.0.3/emerging.rules.tar.gz -O suricata/rules/emerging.rules.tar.gz
tar -xzvf suricata/rules/emerging.rules.tar.gz -C suricata/rules/

# Set permissions
chmod -R 755 squid/
chmod -R 755 snort/
chmod -R 755 suricata/

# Build and start containers
docker-compose up -d

echo "Proxy with IPS/IDS is running!"
echo "Proxy: localhost:3128"
echo "Kibana Dashboard: http://localhost:5601"