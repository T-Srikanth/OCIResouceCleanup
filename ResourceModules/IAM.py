import oci
import time

WaitRefresh = 10

def Login(config,startcomp):
    identity = oci.identity.IdentityClient(config)
    user = identity.get_user(config["user"]).data
    print("Logged in as: {} @ {}".format(user.description, config["region"]))

    # Add first level subcompartments
    compartments = oci.pagination.list_call_get_all_results(identity.list_compartments, compartment_id=startcomp).data

    # Add 2nd level subcompartments
    for compartment in compartments:
        subcompartments = oci.pagination.list_call_get_all_results(identity.list_compartments, compartment_id=compartment.id).data
        for sub in subcompartments:
            compartments.append(sub)

    # Add start compartment to list
    compartment = identity.get_compartment(compartment_id=startcomp).data
    compartments.append(compartment)

    return compartments


def SubscribedRegions(config):
    regions = []
    identity = oci.identity.IdentityClient(config)
    regionDetails=identity.list_region_subscriptions(tenancy_id=config["tenancy"]).data
    
    #Add subscribed regions to list
    for detail in regionDetails:
        regions.append(detail.region_name)
        
    return regions        
