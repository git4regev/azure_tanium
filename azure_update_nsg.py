import os
from azure.identity import AzureCliCredential
from azure.mgmt.resource import SubscriptionClient
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network import NetworkManagementClient

credential = AzureCliCredential()
subscription_client = SubscriptionClient(credential)

subscription = next(subscription_client.subscriptions.list())

compute_client = ComputeManagementClient(credential, subscription.subscription_id)
network_client = NetworkManagementClient(credential, subscription.subscription_id)

print ("\nAdding NSG rules for the following VMs in subscription {}".format(subscription.subscription_id))
for vm in compute_client.virtual_machines.list_all():
    vm_rg = ((vm.id).split("/"))[4]
    vm_nic = vm.network_profile.network_interfaces[0]
    nic = network_client.network_interfaces.get(vm_rg, os.path.basename(vm_nic.id))
    nsg = nic.network_security_group
    nsg_name = ((nsg.id).split("/"))[8]
    print ("\tVM: {}, NSG: {}, MAC: {}, IP: {} ".format(vm.name,nsg_name,nic.mac_address,(nic.ip_configurations)[0].private_ip_address))

    # Add port rules for Tanium clients
    network_client.security_rules.begin_create_or_update(vm_rg,nsg_name,"Allow17472InBound",
        {
            'access':'Allow',
            'description':'Tanium 17472 inbound',
            'destination_address_prefix':'*',
            'destination_port_range':'17472',
            'direction':'Inbound',
            'priority':400,
            'protocol':'Tcp',
            'source_address_prefix':'*',
            'source_port_range':'*',
        }
    )
    network_client.security_rules.begin_create_or_update(vm_rg,nsg_name,"Allow17472OutBound",
        {
            'access':'Allow',
            'description':'Tanium 17472 outbound',
            'destination_address_prefix':'*',
            'destination_port_range':'17472',
            'direction':'Outbound',
            'priority':400,
            'priority':400,
            'protocol':'Tcp',
            'source_address_prefix':'*',
            'source_port_range':'*',
        }
    )
    network_client.security_rules.begin_create_or_update(vm_rg,nsg_name,"Allow17475InBound",
        {
            'access':'Allow',
            'description':'Tanium 17475 inbound',
            'destination_address_prefix':'*',
            'destination_port_range':'17475',
            'direction':'Inbound',
            'priority':401,
            'protocol':'Tcp',
            'source_address_prefix':'*',
            'source_port_range':'*',
        }
    )
    network_client.security_rules.begin_create_or_update(vm_rg,nsg_name,"Allow17475OutBound",
        {
            'access':'Allow',
            'description':'Tanium 17475 outbound',
            'destination_address_prefix':'*',
            'destination_port_range':'17475',
            'direction':'Outbound',
            'priority':401,
            'protocol':'Tcp',
            'source_address_prefix':'*',
            'source_port_range':'*',
        }
    )
    network_client.security_rules.begin_create_or_update(vm_rg,nsg_name,"Allow17468OutBound",
        {
            'access':'Allow',
            'description':'Tanium 17468 outbound',
            'destination_address_prefix':'*',
            'destination_port_range':'17468',
            'direction':'Outbound',
            'priority':402,
            'protocol':'Tcp',
            'source_address_prefix':'*',
            'source_port_range':'*',
        }
    )