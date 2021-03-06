#!/usr/bin/env bash
export ANSIBLE_LIBRARY=./
export ANSIBLE_MODULE_UTILS=./module_utils
export ANSIBLE_DOC_FRAGMENT_PLUGINS=./plugins/doc_fragments

declare -a arr=("tetration_application"
                "tetration_application_policy"
                "tetration_application_policy_ports"
                "tetration_application_policy_catchall"
                "tetration_inventory_tag_search"
                "tetration_inventory_tag_headers"
                "tetration_application_enforcement"
                "tetration_application_query"
                "tetration_inventory_filter"
                "tetration_rest"
                "tetration_role"
                "tetration_scope_commit_query_changes"
                "tetration_scope_query"
                "tetration_scope"
                "tetration_software_agent_query"
                "tetration_software_agent"
                "tetration_software_agent_config_profile"
                "tetration_software_agent_config_intent"
                "tetration_user"
                )

for i in "${arr[@]}"
do
    ansible-doc $i | cat > $i.txt

    if [ $PIPESTATUS -ne 0 ]; then
        exit 1 
    fi
done