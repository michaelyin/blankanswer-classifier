Python rest service to check if an image has answer (fill blank) from a student or not.  

1. setup PYTHONPATH  

PYTHONPATH="$(printf "%s:" /home/michael/PycharmProjects/blankanswer-classifier/net/wyun/*/)"  
or  
PYTHONPATH="$(printf "%s:" ./net/wyun/*/)"  
or  
export PYTHONPATH="$(printf "%s:" /home/michael/PycharmProjects/blankanswer-classifier/net/wyun/*/)"  

2. start app.py server  
python /home/michael/PycharmProjects/blankanswer-classifier/net/wyun/blankanswer/app.py  
or  
[hope@buzzy blankanswer-classifier]$ python ./net/wyun/blankanswer/app.py  
  
  
3. cuda1  
[xy00@cuda1:~/git/blankanswer-classifier$]   
export PYTHONPATH="$(printf "%s:" /home/xy00/git/blankanswer-classifier/*/)"    

[xy00@cuda1:~/git/blankanswer-classifier$]  
python /home/xy00/git/blankanswer-classifier/net/wyun/blankanswer/app.py
