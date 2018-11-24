# scrapy_with_cron_in_wsl
Scrapy Framework example combined with cron in wsl
## What does the Script do?
It scrapes four specific routes of [https://www.telekom.de/](https://www.telekom.de/). Checks if the products are available and opens the browser to buy them.
## Set up Cronjob
### Add job to crontab
First you want to specify which command gets executed at which scheduled time. You do this in a crontab.
#### User
```sh
sudo crontab -u $USER -e
```
*comment: crontab -e opens the User crontab, and sudo crontab -e opens the Global crontab*
#### Global
```sh
sudo crontab -e
```

Now schedule the execution
```sh
┌───────────── minute (0 - 59)
│ ┌───────────── hour (0 - 23)
│ │ ┌───────────── day of month (1 - 31)
│ │ │ ┌───────────── month (1 - 12)
│ │ │ │ ┌───────────── weekday (0 - 6)
│ │ │ │ │
* * * * *  [command]
```
To execute my scraper every minute, use
```sh
* * * * * python3 /mnt/d/OneDrive/Workspace/Python/python_workspace/s7_telekom_available.py > /mnt/d/scrapy.txt
```
\* means every interval which is every minute for the first parameter, every hour for the second and so forth. It's good to write output to a file. With that, it's easy to check if the cron job runs appropiatly.
### Make sure to check Environment Variables
In the script the default browser gets opened (chrome at my example). I run it on WSL in the bash. So you need to make sure that cron (which gets executed by sudo) know where to execute the browser.
#### User
```sh
export BROWSER=/mnt/c/Windows/explorer.exe
```
#### Global
```sh
sudo echo BROWSER=/mnt/c/Windows/explorer.exe >> /etc/environment
```

## Run the Job
```sh
sudo cron
```
This will start the cronjob, which gets executed at the specific time managed in the crontab.

## Stop the Job
```sh
ps -e
```
shows every process. Search for cron and get the first value (process id).
```sh
sudo kill -9 pid
```
substitute the pid value. You stop the cronjob with the kill command.

## Important Comments
Use the user crontab command. I don't know why, but only that command works properly. If you use the global crontab -e, than the python script not get executed. That means you dont need to add the line to the sudo crontab -e!
### Cronjobs in WSL work in background
Even if you close the WSL terminal in VS Code, the cronjob will run continuesly!

### Additional Info
```sh
usermod -a -G crontab (username)
```
Will add yourself to crontab group. Don't know exactly why you need that and how that works. [Referenced StackOverflow Post](https://stackoverflow.com/questions/41281112/crontab-not-working-with-bash-on-ubuntu-on-windows)
