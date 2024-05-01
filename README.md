"# guided-assembly-system" 

#  `pupil-apriltags` Installation Steps

`git clone --recursive https://github.com/pupil-labs/apriltags.git`

`cd apriltags`

`pip install -e .[testing]`

Source : https://pupil-apriltags.readthedocs.io/en/stable/

Keras Model (just screw/no screw) : https://drive.google.com/file/d/1J2iIAThAhM1T4xKaasfU8rZbFOhE1jGu/view?usp=sharing

Instructions

boot into ubuntu 
open terminal
	sudo passwd root
	(set password to password or anything)
	su
also go to https://github.com/zephingeorge/guided-assembly-system
get the ubuntu commands
also download the model.keras file, link for it youll find in the 
	github page of the repo. in readme.md file
you will need to download it and move it into 
	guided-assembly-system/neural-networks/model.keras before running the app.py file. 
