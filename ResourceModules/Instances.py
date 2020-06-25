import oci
import time
from datetime import datetime as dt
TODAY=dt.today()

WaitRefresh = 15

def DeleteInstancePools(config, Compartments):
    properlyTaggedItems = []
    improperlyTaggedItems = []
    object = oci.core.ComputeManagementClient(config)

    print ("\nGetting all InstancePools objects")
    for Compartment in Compartments:
        items = oci.pagination.list_call_get_all_results(object.list_instance_pools, compartment_id=Compartment.id).data
        for item in items:
            if item.lifecycle_state != "TERMINATED":
                try:
                    date_in_string=item.defined_tags["ExpirationTag"]["ExpirationDate(dd/mm/yyyy)"]
                    date_in_date=dt.strptime(date_in_string, "%d/%m/%Y")
                    if date_in_date<TODAY:
                        properlyTaggedItems.append(item)
                        print("- {} - {}".format(item.display_name, item.lifecycle_state))
                except:
                    improperlyTaggedItems.append(item)
    itemsPresent = True

    while itemsPresent:
        count = 0
        for item in properlyTaggedItems:
            try:
                itemstatus = object.get_instance_pool(instance_pool_id=item.id).data
                if itemstatus.lifecycle_state != "TERMINATED":
                    if itemstatus.lifecycle_state != "TERMINATING":
                        try:
                            print ("Deleting: {}".format(itemstatus.display_name))
                            object.terminate_instance_pool(instance_pool_id=itemstatus.id)
                        except:
                            print ("error trying to delete: {}".format(itemstatus.display_name))
                    else:
                        print("{} = {}".format(itemstatus.display_name, itemstatus.lifecycle_state))
                    count = count + 1
            except:
                print ("-----------------> error deleting {}, probably already deleted".format(item.display_name))
        if count > 0 :
            print ("Waiting for expired Objects to be deleted...")
            time.sleep(WaitRefresh)
        else:
            itemsPresent = False
    print ("All expired Objects deleted!")
    if improperlyTaggedItems:
        print("\n--Check the following improperly tagged resources--\n")
        for item in improperlyTaggedItems:
            print("{} = {}".format(item.display_name, item.lifecycle_state))

def DeleteInstanceConfigs(config, Compartments):
    properlyTaggedItems = []
    improperlyTaggedItems = []
    object = oci.core.ComputeManagementClient(config)

    print ("\nGetting all InstanceConfigurations")
    for Compartment in Compartments:
        items = oci.pagination.list_call_get_all_results(object.list_instance_configurations, compartment_id=Compartment.id).data
        for item in items:
            try:
                date_in_string=item.defined_tags["ExpirationTag"]["ExpirationDate(dd/mm/yyyy)"]
                date_in_date=dt.strptime(date_in_string, "%d/%m/%Y")
                if date_in_date<TODAY:
                    properlyTaggedItems.append(item)
                    print("{} ".format(item.display_name))
            except:
                improperlyTaggedItems.append(item)
    for item in properlyTaggedItems:
        print("deleting - {}".format(item.display_name))
        object.delete_instance_configuration(instance_configuration_id=item.id)

    print ("All expired Objects deleted!")
    if improperlyTaggedItems:
        print("\n--Check the following improperly tagged resources--\n")
        for item in improperlyTaggedItems:
            print("{}".format(item.display_name))    

def DeleteInstances(config, Compartments):
    properlyTaggedItems = []
    improperlyTaggedItems = []
    object = oci.core.ComputeClient(config)

    print ("\nGetting all Compute objects")
    for Compartment in Compartments:
        items = oci.pagination.list_call_get_all_results(object.list_instances, compartment_id=Compartment.id).data
        for item in items:
            if item.lifecycle_state != "TERMINATED":
                try:
                    date_in_string=item.defined_tags["ExpirationTag"]["ExpirationDate(dd/mm/yyyy)"]
                    date_in_date=dt.strptime(date_in_string, "%d/%m/%Y")
                    if date_in_date<TODAY:
                        properlyTaggedItems.append(item)
                        print("- {} - {}".format(item.display_name, item.lifecycle_state))
                except:
                    improperlyTaggedItems.append(item)

    itemsPresent = True

    while itemsPresent:
        count = 0
        for item in properlyTaggedItems:
            try:
                itemstatus = object.get_instance(instance_id=item.id).data
                if itemstatus.lifecycle_state != "TERMINATED":
                    if itemstatus.lifecycle_state != "TERMINATING":
                        try:
                            print ("Deleting: {}".format(itemstatus.display_name))
                            object.terminate_instance(instance_id=itemstatus.id)
                        except:
                            print ("error trying to delete: {}".format(itemstatus.display_name))
                    else:
                        print("{} = {}".format(itemstatus.display_name, itemstatus.lifecycle_state))
                    count = count + 1
            except:

                print ("-----------------> error deleting {}, probably already deleted: {}".format(item.display_name, item.lifecycle_state))
        if count > 0 :
            print ("Waiting for expired Objects to be deleted...")
            time.sleep(WaitRefresh)
        else:
            itemsPresent = False
    print ("All expired Objects deleted!")
    if improperlyTaggedItems:
        print("\n--Check the following improperly tagged resources--\n")
        for item in improperlyTaggedItems:
            print("{} = {}".format(item.display_name, item.lifecycle_state))
    

def DeleteImages(config, Compartments):
    properlyTaggedItems = []
    improperlyTaggedItems = []
    object = oci.core.ComputeClient(config)

    print("Getting all Custom Image objects")
    for Compartment in Compartments:
        items = oci.pagination.list_call_get_all_results(object.list_images, compartment_id=Compartment.id).data
        for item in items:
            if item.operating_system_version == "Custom" or item.base_image_id:
                try:
                    date_in_string=item.defined_tags["ExpirationTag"]["ExpirationDate(dd/mm/yyyy)"]
                    date_in_date=dt.strptime(date_in_string, "%d/%m/%Y")
                    if date_in_date<TODAY:
                        properlyTaggedItems.append(item)
                        print("- {} - {}".format(item.display_name, item.lifecycle_state))
                except:
                    improperlyTaggedItems.append(item)

    itemsPresent = True

    while itemsPresent:
        count = 0
        for item in properlyTaggedItems:
            try:
                itemstatus = object.get_image(image_id=item.id).data
                if itemstatus.lifecycle_state != "DELETED":
                        try:
                            print("Deleting: {}".format(itemstatus.display_name))
                            object.delete_image(image_id=itemstatus.id)
                        except:
                            print("error trying to delete: {}".format(itemstatus.display_name))
                else:
                    print("{} = {}".format(itemstatus.display_name, itemstatus.lifecycle_state))
                    count = count + 1
            except:
                print("-----------------> error deleting {}, probably already deleted".format(item.display_name))
        if count > 0:
            print("Waiting for all Objects to be deleted...")
            time.sleep(WaitRefresh)
        else:
            itemsPresent = False
    print("All expired Objects deleted!")
    if improperlyTaggedItems:
        print("\n--Check the following improperly tagged resources--\n")
        for item in improperlyTaggedItems:
            print("{} = {}".format(item.display_name, item.lifecycle_state))    


def DeleteDedicatedVMHosts(config, Compartments):
    properlyTaggedItems = []
    improperlyTaggedItems = []
    object = oci.core.ComputeClient(config)

    print ("\nGetting all Dedicated VM Hosts objects")
    for Compartment in Compartments:
        items = oci.pagination.list_call_get_all_results(object.list_dedicated_vm_hosts, compartment_id=Compartment.id).data
        for item in items:
            if item.lifecycle_state != "DELETED":
                itemDetails=object.get_dedicated_vm_host(dedicated_vm_host_id =item.id).data
                try:
                    date_in_string=itemDetails.defined_tags["ExpirationTag"]["ExpirationDate(dd/mm/yyyy)"]
                    date_in_date=dt.strptime(date_in_string, "%d/%m/%Y")
                    if date_in_date<TODAY:
                        properlyTaggedItems.append(item)
                        print("- {} - {}".format(item.display_name, item.lifecycle_state))
                except:
                    improperlyTaggedItems.append(item)

    itemsPresent = True

    while itemsPresent:
        count = 0
        for item in properlyTaggedItems:
            try:
                itemstatus = object.get_dedicated_vm_host(dedicated_vm_host_id =item.id).data
                if itemstatus.lifecycle_state != "DELETED":
                    if itemstatus.lifecycle_state != "DELETING":
                        try:
                            print ("Deleting: {}".format(itemstatus.display_name))
                            object.delete_dedicated_vm_host(dedicated_vm_host_id=itemstatus.id)
                        except:
                            print ("error trying to delete: {}".format(itemstatus.display_name))
                    else:
                        print("{} = {}".format(itemstatus.display_name, itemstatus.lifecycle_state))
                    count = count + 1
            except:

                print ("-----------------> error deleting {}, probably already deleted: {}".format(item.display_name, item.lifecycle_state))
        if count > 0 :
            print ("Waiting for expired Objects to be deleted...")
            time.sleep(WaitRefresh)
        else:
            itemsPresent = False
    print ("All expired Objects deleted!")
    if improperlyTaggedItems:
        print("\n--Check the following improperly tagged resources--\n")
        for item in improperlyTaggedItems:
            print("{} = {}".format(item.display_name, item.lifecycle_state))
