# Multi VM setup

## Description

In this activity, you will learn how to make two different virtual
machines communicate.

You will create a dedicated virtual network on your hypervisor and
attach both virtual machines to it.

## Virtual Box

If you have Virtual Box as your hypervisor, you will need to go into
`Files -> Tools -> Network tools` and create a new host network by
clicking on the `New` button.

<figure>
<img src="media/rId21.png" style="width:5.83333in;height:1.14216in"
alt="Network Settings" />
<figcaption aria-hidden="true"><p>Network Settings</p></figcaption>
</figure>

Once you click on `New`, a new network will be created with a dedicated
IP LAN and a DHCP. Now you can use this network to make all your virtual
machines to communicate.

## Attaching Host to the created VM

#### Metasploitable

For Metasploitable2 is simple: just go into settings and choose from the
current NIC (it's not needed to enable a new one).

<figure>
<img src="media/rId25.png" style="width:5.83333in;height:3.22016in"
alt="IPv4 settings" />
<figcaption aria-hidden="true"><p>IPv4 settings</p></figcaption>
</figure>

Reboot the virtual machine and now it should have an IP from the virtual
network you created.

### Kali Linux

For example, if you want to attach Kali Linux to the new Network, go
into VM settings, enable an extra adapter and choose the `vboxnet0`.

<figure>
<img src="media/rId29.png" style="width:5.83333in;height:3.46175in"
alt="Kali Network Settings" />
<figcaption aria-hidden="true"><p>Kali Network Settings</p></figcaption>
</figure>

When you enable an extra NIC, you will likely have to configure it (by
default Kali configures only the first NIC). Start the virtual machine
and enable the connection like in the pictures below.

First, go to `Advanced Network Settings` and create a new Profile.

<figure>
<img src="media/rId32.png" style="width:5.83333in;height:3.03999in"
alt="Advanced Network Settings" />
<figcaption aria-hidden="true"><p>Advanced Network
Settings</p></figcaption>
</figure>

Choose Ethernet when asked. ![Profile
Type](media/rId35.png){width="5.833333333333333in"
height="3.0399923447069117in"}

Select `eth1` for the device. ![Profile
Type](media/rId38.png){width="5.833333333333333in"
height="3.0399923447069117in"}

Make sure, DHCP is enabled. ![IPv4
settings](media/rId41.png){width="5.833333333333333in"
height="3.0399923447069117in"}

## Result

Now you have two virtual machines in the same virtual network and you
can make practice on your own!

Here it is the result of nmap from Kali Linux in the virtual network
created.

<figure>
<img src="media/rId46.png" style="width:5.83333in;height:3.03999in"
alt="Nmap result" />
<figcaption aria-hidden="true"><p>Nmap result</p></figcaption>
</figure>
