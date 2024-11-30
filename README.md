# Note

---

If you are planning on provisioning the infrastructure as described here, keep the following in mind:

- Make sure you have an existing and working installation of both terraform (we used OpenTofu) and libvirt

- You need to download a Windows 10 (Professional) ISO and a Windows Server 2022 ISO

- The Windows 10 machines will configure themselves automatically with users described in the autounattend files, but the server needs to be set up manually

- The Windows 10 clients need to be joined to the domain manually.

- All clients need the implants installed manually

- The C2s were installed manually. Realm and Sliver were installed and ran through Docker utilizing host networking mode, HeadHunter was built and installed directly on the C2 machine.
