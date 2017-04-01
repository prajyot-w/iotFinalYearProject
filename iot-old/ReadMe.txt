Run following commands 

sudo bash setup.sh

to run script at startup 
first run `crontab -e`
then at bottom ... write following line

`@reboot python /execute.py`