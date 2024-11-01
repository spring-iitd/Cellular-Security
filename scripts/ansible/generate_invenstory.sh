#!/bin/bash
# generate_inventory.sh

# Function to generate ansible host config
generate_host_config() {
    local host=$1
    local config=$(vagrant ssh-config $host)
    
    local port=$(echo "$config" | awk '/Port/ {print $2}')
    local keyfile=$(echo "$config" | awk '/IdentityFile/ {print $2}')
    
    if [[ $host == ran_nw_* ]]; then
      cat << RAN_EOF
        $host:
          ansible_host: 127.0.0.1
          ansible_port: $port
          ansible_python_interpreter: /usr/bin/python3.10
          ansible_user: vagrant
          ansible_ssh_private_key_file: $keyfile
          ansible_ssh_common_args: '-o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -o PasswordAuthentication=no -o IdentitiesOnly=yes -o LogLevel=FATAL -o PubkeyAcceptedKeyTypes=+ssh-rsa -o HostKeyAlgorithms=+ssh-rsa'
RAN_EOF
    else
      cat << EOF
    $host:
      ansible_host: 127.0.0.1
      ansible_port: $port
      ansible_python_interpreter: /usr/bin/python3.10
      ansible_user: vagrant
      ansible_ssh_private_key_file: $keyfile
      ansible_ssh_common_args: '-o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -o PasswordAuthentication=no -o IdentitiesOnly=yes -o LogLevel=FATAL -o PubkeyAcceptedKeyTypes=+ssh-rsa -o HostKeyAlgorithms=+ssh-rsa'
EOF
        fi
    }

# Start generating inventory file
cat > ./scripts/ansible/inventory.ansible.yml << EOF
all:
  hosts:
$(generate_host_config "core_nw")
$(generate_host_config "ue_nw")
  children:
    attack_nodes:
      hosts:
$(generate_host_config "ran_nw_1")
$(generate_host_config "ran_nw_2")
$(generate_host_config "ran_nw_3")
$(generate_host_config "ran_nw_4")
$(generate_host_config "ran_nw_5")
$(generate_host_config "ran_nw_6")
$(generate_host_config "ran_nw_7")
$(generate_host_config "ran_nw_8")
$(generate_host_config "ran_nw_9")
$(generate_host_config "ran_nw_0")

EOF