# Synopsis

Failover is an important component of disaster recovery. It is a mechanism of routing the users’ traffic to the DR site, after the disaster gets confirmed in the primary site. In this project, the implementation of different automatic failover schemes is presented and tested for Disaster Recovery as a Service (DRaaS) in OpenStack. These Failover schemes are:
   • DNS Based Failover
   • Frontend Based Failover
   • Hybrid Based Failover.
Under different disaster scenarios, these automatic failover schemes are experimented and analyzed. These results suggest that a Hybrid scheme is more likely to recover quickly from the different levels of disaster.

# Prerequisites

• For any scheme to be used, at least two machines are required with OpenStack deployed on each.
• For DNS and Hybrid based scheme, account of NO-IP is required with at least one hostname provided by this (NO-IP is an open source DNS and Dynamic DNS service providers, for more info visit http://www.noip.com/)
• For Frontend scheme, you must have one extra machine. For Hybrid scheme you must have two extra machines apart from OpenStack deployed machines.
• Python 2.7 environment on each machine.

# Info Graphics
## DNS-based-failover
![alt tag](info_graphics/detailed_graphics/DNS/a_without_any_disaster.png) 
## Frontend-based-failover
![alt tag](info_graphics/detailed_graphics/Frontend/a_without_any_disaster.png) 
## Hybrid(Combination of DNS+Frontend)-based-failover
![alt tag](info_graphics/detailed_graphics/Hybrid/a_withoutAnyDisaster.png)  

# Installation

Clone this project, and navigate to dns_based directory. Inside this directory there are two directories as well named _drass-primary_ and _drass-secondary_. For any failover scheme, these two setup directories are compulsory to provide data synchronization between two main openstack nodes. Place _drass-primary_ into the primary openstack node and _draas-secondary_ into the secondary openstack node.
Both these directories contain some configuration files (draas.conf, keystone.conf, etc). These files are commented so you can figure it out that how to configure them according to your environment.
Once you get done with configuration, then just run the _draas-primary.sh_ and _draas-secondary.sh_ in the respected nodes. For choosing the failover scheme, you have to enable the required scheme name in _failover.conf_ file. Finally just run the _Draas.py_ file by typing **_‘python Draas.py’_**. Same process would be applied on the secondary node. Note: first you need to run _Draas.py_ on secondary site and then on primary site.

If you enable DNS-based scheme, then you don’t need any extra machine other than openstack deployed machines, the DNS code is integrated within the setup files of _draas-primary_ and _draas-secondary_. If you choose frontend-based scheme then you must have one extra machine (without OpenStack deployment) to run the frontend-based code over there. To run the frontend code, you need to do some configurations in _frontend.conf_ file which is contained in _frontend-based_ directory. The file is commented so you can easily figure it out that what things you need to configure. After this configuration, just run the **_‘sudo python frontend.py’_** file. If you choose hybrid-based scheme then you must have two extra machines. On first machine, place the _hybrid-primary_ and on the second machine place the _hybrid-secondary_ directory setup files. Again you need to do the mentioned configurations in the _hybrid.conf_ files contained in setup files of both these machines. After this configurations, just run the **_‘sudo python hybrid.py’_** file first in _hybrid-secondary_ and then in _hybrid-primary_ machine respectively.

Note: Any failover scheme you choose to proceed with, you must have two machines with OpenStack deployed on each. After running the _DraaS.py_ file on both, they must be having in synchronization state with each other in order to sync the data and logs.   

# Tests

If you want to test these schemes in order to measure the RTO or total downtime then run the **_TestingRTO.py_** file after updating with your hostname in the file.

# Contributors

Supervisors: Dr. Adnan Iqbal and Dr. Saqib Ilyas

 
# License

https://www.namal.edu.pk/pdrg/
