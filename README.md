# Note

---

If you are planning on provisioning the infrastructure as described here, keep the following in mind:

- Make sure you have an existing and working installation of both terraform (we used OpenTofu) and libvirt

- You need to download a Windows 10 (Professional) ISO and a Windows Server 2022 ISO
    - We created an "autoboot" ISO, which is just the standard image but with a modification to not ask "Press any key to boot from CD/DVD...". See [here](https://serverfault.com/questions/353826/windows-boot-iso-file-without-press-any-key)
    - You should also download an instance of the VirtIO drivers since they get installed automatically by the autounattend if the disk is mounted. If you don't want to do this, make sure you comment that disk drive out from the Windows Client configuration

- The Windows 10 machines will configure themselves automatically with users described in the autounattend files, but the server needs to be set up manually

- The Windows 10 clients need to be joined to the domain manually.

- Scripts should be launched manually

- All clients need the implants installed manually

- The C2s were installed manually. Realm and Sliver were installed and ran through Docker utilizing host networking mode, HeadHunter was built and installed directly on the C2 machine.
