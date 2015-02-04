backup_user_folder
===

These scripts are used for when I manually backup user directories using external hard drives. The first backup script will use a normal ``rsync`` to copy from source to destination excluding the ~/Library directory. The second revision of the backup_user_folder will use multiple rsync threads to copy the data a bit faster. You can safely increase the thread count in the script if you are using fast technology (aka SSD's, fast network, RAID, etc.). 15 threads is a pretty safe count for a single spinning drive. _Note:_ the second script will copy the ~/Library directory.



credit to the parallel rsync copy: [http://www.krazyworks.com/making-rsync-faster/]()