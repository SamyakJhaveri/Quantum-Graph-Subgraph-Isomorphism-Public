## Instructions to run the programs in case you forget


1. To activate the virtual environment with the DWave Ocean SDK in it type:
    ```
        . ocean/bin/activate
    ```
    to activate the ocean environment that has all the necessary libraries and packages, including the 'dwave-ocean-sdk'. 

### Running the experiment conductor
1. Start a tmux sesssion on the remote server by doing the following:
    ```
        tmux
    ```
    A `tmux` session will open up in the terminal. running your code in the tmux session will alow you to let the code run on the server
    even when you are not ssh-ed into the server. i.e. you can close the terminal and let the program run on the server. to do that, type into a different terminal:
    ```
        tmux detach
    ```
    If you want to attach to the tmux session in which your code was set to run, type in:
    ```
        tmux attach
    ```
    Once you are done with the experiment, kill the tmux session by doing the following:
    ```
        tmux kill-session
    ```

2. In the ocean environment, go to the folder: '~/UCI Quantum Code Clone Detection Project/ Experiment Code/'
in there, you will find 'qccd_experiment_conductor_Script_for_experiment.py'. run it using python or python3. 
