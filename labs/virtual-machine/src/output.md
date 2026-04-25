# Setup a linux virtual machine

We will be using [Kali Linux](https://www.kali.org/) for the
cybersecurity class. Any other linux environment will be fine (feel free
to reach out if you encounter any issues with software we use during
practical labs).

If you have already a linux machine skip the installation phase.

## Download ISO

Get your Kali Linux ISO
[here](https://www.kali.org/get-kali/#kali-installer-images).

<figure>
<img src="media/rId22.png" style="width:5.83333in;height:2.83115in"
alt="Kali" />
<figcaption aria-hidden="true"><p>Kali</p></figcaption>
</figure>

### Hypervisor setup

Now you need an hypervisor (something that runs virtual machines). We
will use Virtual Box which can be download from the [official
site](https://www.virtualbox.org/wiki/Downloads) (most likely you will
have to download the Windows Hosts version.) ![Virtual Box
homepage](media/rId26.png){width="5.833333333333333in"
height="2.8377154418197725in"}

Create a new virtual machine, as in pictures. ![Virtual box main
menu](media/rId29.webp){width="4.166666666666667in"
height="2.7777777777777777in"}

Give it a name and select the ISO you just downloaded. ![Create
VM](media/rId32.png){width="5.833333333333333in"
height="2.2412117235345583in"}

Finally, give it at least 2GB ram and 2CPUs and start the installation!

### Installation guide

Installation is very simple. Just follow the instructions!

First, you will see a screen like this:

<figure>
<img src="media/rId36.png" style="width:5.83333in;height:4.375in"
alt="Create VM" />
<figcaption aria-hidden="true"><p>Create VM</p></figcaption>
</figure>

Choose graphical install and go on, you will be asked for general
informations about languages and to create a user (provide username and
password).

<figure>
<img src="media/rId39.png" style="width:5.83333in;height:4.375in"
alt="Create VM" />
<figcaption aria-hidden="true"><p>Create VM</p></figcaption>
</figure>

Create a simple partition scheme and confirm choices (select `yes`):

![Create VM](media/rId42.png){width="5.833333333333333in"
height="4.375in"} ![Create
VM](media/rId45.png){width="5.833333333333333in" height="4.375in"}

Leave blank here and click `Continue`: ![Create
VM](media/rId48.png){width="5.833333333333333in" height="4.375in"}

Select default option for installation:

<figure>
<img src="media/rId51.png" style="width:5.83333in;height:4.375in"
alt="Create VM" />
<figcaption aria-hidden="true"><p>Create VM</p></figcaption>
</figure>

When the installation end, you should reboot in your new virtual
machine.
