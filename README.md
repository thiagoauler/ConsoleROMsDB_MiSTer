# ConsoleROMsDB_MiSTer

After taking a closer look in the "MiSTer Downloader" documentation, especifically about [custom databases](https://github.com/MiSTer-devel/Downloader_MiSTer/blob/main/docs/custom-databases.md), I kept wondering if it'd be possible to set a shared folder in my network containing all necessary ROMs and use "downloader.sh" to do all the work for me.

I made some experimentation and could finally set it. Three steps are necessary to accomplish this:
1. As I wanted to a shared folder as a provider, it's first necessary to setup a cifs folder directly in MiSTer. This is easily achievable using "cifs_mount.sh" script provided officially by [Scripts_MiSTer Repository](https://github.com/MiSTer-devel/Scripts_MiSTer). Just download "cifs_mount.sh", copy it to Scripts folder in /media/fat and configure it (the script is well documents and should not be any trouble). Execute it to have /media/fat/cifs folder available as your personal ROM repository.
2. Now its necessary to make "donwloader.sh" aware of your new intents... for this, you'll have to edit "downloader.ini" file.
