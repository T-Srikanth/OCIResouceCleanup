import oci

########## Configuration ####################
# Specify your config file location
configfile = "~/.oci/config"

print ("\n--[ Login check and getting all compartments from root compartment ]--")
compartments = Login(config, DeleteCompartmentOCID)
#calling SubscribedRegions() function
regions=SubscribedRegions(config)
processCompartments=[]
