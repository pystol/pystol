# The official Pystol web dashboard

This is the web interface to monitor how actions are executed.

It allows to:

* Check the cluster state
* Check the default available Pystol actions.
* Check the executed Pystol actions.
* Run Pystol actions.

## How to contribute

This dashboard is located at [github.com/pystol/pystol](github.com/pystol/pystol).
Any pull request of issue report is welcomed.

## Running the Pystol Web interface as standalone.

The Pystol web interface can be used as a Kubernetes dashboard
to display the current state of your deployment.

**The Pystol UI is currently under heavy development**

In the case you are not using Pystol as your fault
injection platform you can still use this web UI
following the next steps.

```bash
git clone git@github.com:pystol/pystol.git
cd pystol/pystol-ui
pip3 install -r requirements.txt
export FLASK_APP=run.py
# Set up the DEBUG environment
#export FLASK_ENV=development
flask run --host=0.0.0.0 --port=3000
```

This will start the web interface and
show the Kubernetes cluster status.

You need to run the Flask server from
a machine with access to the cluster.
