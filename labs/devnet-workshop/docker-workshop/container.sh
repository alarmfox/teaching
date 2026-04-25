sudo mkdir -p /srv/debian-chroot
export CHROOT_DIR=/srv/debian-chroot
sudo debootstrap --arch=amd64 bookworm "${CHROOT_DIR}" http://deb.debian.org/debian

