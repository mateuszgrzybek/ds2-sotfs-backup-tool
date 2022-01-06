### DS2 SotFS save backup tool

This is a small Python program that will take care of backing up your Dark Souls 2 saves (both original and SotFS).

#### How does it work?

On the initial run the program will ask you to specify the path to your DS2 save file's location. Keep in mind that it has to be an absolute path to the file.

On each consecutive run the script will use the path specified and will ask you to specify the backup interval in minutes.

Additionaly terminating the script will kill the DS2 process since it apparently prevents soul memory from saving (don't quote me on that).

Backups are stored in the **backups** directory.
Only 10 backups will be stored, the program will remove the oldest backup automatically if this amount is exceeded.
