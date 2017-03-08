Please use the 'code' folder for all scripts.
Please use the 'report' folder for the .tex file and other things related to the report.

Under code, there will be a folder "global_data" for any data we are storing in the repo -- this is stuff that we will push between us all, such as intermediate calculations and the results of training that we don't want to push onto the repo (e.g. the main dataset should *not* be here, because it is multiple GB).

Under code, you should make a symlink called "local_data" that points to a folder where you will store the big stuff on your own machine.  To do this in the UNIX command line, you use:

$ ln -s path/to/local/data local_data

where path/to/local/data is the (preferably absolute) path to wherever you want to store the big data on your local machine.

Also, under "report", there is a folder called "figs" which, surprise surprise, is where I think we ought to keep all the pictures and graphs that we want to put in the report.  Makes the TeXing easier once we get there.
