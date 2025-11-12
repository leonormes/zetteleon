# Preventing Automatic Updates by Filling Kindle Storage

## Metadata
- Author: [[Kindle Modding Wiki]]
- Full Title: Preventing Automatic Updates by Filling Kindle Storage
- Category: #articles
- Summary: Kindle devices can update automatically if they have enough free storage space. Filling the Kindle’s storage with dummy files stops these updates from happening. After jailbreaking, you can delete the dummy files to free up space again.
- URL: https://kindlemodding.org/jailbreaking/prevent-auto-update.html

## Full Document
####  Why Fill the Kindle’s Storage?

Kindle devices can automatically download and install firmware updates when they have enough free storage space. These updates can block jailbreaking methods. Automatic updates may occur when:

* You open the Kindle Store.
* You register your Kindle to an Amazon account.
* The device is connected to Wi-Fi, even briefly.
* The Kindle is rebooted while connected to the internet.

Filling the Kindle’s storage (leaving only 20-50 MB free) prevents the device from downloading and installing updates, as the update process requires more free space.

####  How to Fill the Kindle’s Storage

You can use a simple script to fill your Kindle’s storage with dummy files, leaving only a small amount of free space. This script is available in the [Kindle-Filler-Disk GitHub repository](https://github.com/bastianmarin/Kindle-Filler-Disk/) along with other useful scripts for Windows, macOS, and Linux.

![](https://kindlemodding.org/jailbreaking/Winterbreak/airplane_mode.png)
![](https://kindlemodding.org/jailbreaking/Prevent/usb-mode.png)
![](https://kindlemodding.org/jailbreaking/Prevent/github-files.png)
![](https://kindlemodding.org/jailbreaking/Prevent/root-main.png)
![](https://kindlemodding.org/jailbreaking/Prevent/run-script.png)
![](https://kindlemodding.org/jailbreaking/Prevent/final.png)
####  After Jailbreak: Freeing Up Space

Once you have completed the jailbreak process, you can safely delete the `fill_disk` folder to recover storage space. You may also remove only some of the files if you want to keep the disk nearly full for a while longer.

* **Windows:**  
 Open File Explorer and navigate to the folder containing `fill_disk`. Delete the `fill_disk` folder, or remove individual files inside it.
* **Linux / macOS:**  
 Open a terminal in the folder containing `fill_disk` and run:

 
```
rm -rf fill_disk

```
  Or remove individual files as needed.

This will restore your available disk space.

For more scripts and detailed guides, visit the [Kindle-Filler-Disk GitHub repository](https://github.com/bastianmarin/Kindle-Filler-Disk/).
