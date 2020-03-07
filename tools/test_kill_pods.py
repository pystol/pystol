import matplotlib
matplotlib.use('Agg')
import random
import time
from scipy.stats import poisson
import matplotlib.pyplot as plt
import matplotlib.dates as md
from kubernetes import client, config
from kubernetes.client.rest import ApiException
import threading
import datetime

global_available=[]
global_unavailable=[]
global_kill=[]

t1_stop = threading.Event()
t2_stop = threading.Event()

def delete_pod(name, namespace):
    core_v1 = client.CoreV1Api()
    delete_options = client.V1DeleteOptions()
    try:
        api_response = core_v1.delete_namespaced_pod(
            name=name,
            namespace=namespace,
            body=delete_options)
    except ApiException as e:
        print("Exception when calling CoreV1Api->delete_namespaced_pod: %s\n" % e)

def get_pods(namespace=''):
    api_instance = client.CoreV1Api()
    try: 
        if namespace == '':
            api_response = api_instance.list_pod_for_all_namespaces()
        else:
            api_response = api_instance.list_namespaced_pod(namespace, field_selector='status.phase=Running')
        return api_response
    except ApiException as e:
        print("Exception when calling CoreV1Api->list_pod_for_all_namespaces: %s\n" % e)

def get_event(namespace, stop):

    while not stop.is_set():
        config.load_kube_config()
        configuration = client.Configuration()
        configuration.assert_hostname = False
        api_client = client.api_client.ApiClient(configuration=configuration)
        dat = datetime.datetime.now()
        api_instance = client.AppsV1beta1Api()
        api_response = api_instance.read_namespaced_deployment_status('example', namespace)
        global_available.append((dat,api_response.status.available_replicas))
        global_unavailable.append((dat,api_response.status.unavailable_replicas))
        time.sleep(2)
    t2_stop.set()
    print("Ending live monitor")

def run_histogram(namespace, stop):
    # random numbers from poisson distribution
    n = 500
    a = 0
    data_poisson = poisson.rvs(mu=10, size=n, loc=a)
    counts, bins, bars = plt.hist(data_poisson)
    plt.close()
    config.load_kube_config()
    configuration = client.Configuration()
    configuration.assert_hostname = False
    api_client = client.api_client.ApiClient(configuration=configuration)
    for experiment in counts:
        pod_list = get_pods(namespace=namespace)
        aux_li = []
        for fil in pod_list.items:
            if fil.status.phase == "Running":
                aux_li.append(fil)
        pod_list = aux_li

        # From the Running pods I randomly choose those to die
        # based on the histogram length
        to_be_killed = random.sample(pod_list, int(experiment))

        for pod in to_be_killed:
            delete_pod(pod.metadata.name,pod.metadata.namespace)
        print("To be killed: "+str(experiment))
        global_kill.append((datetime.datetime.now(), int(experiment)))
        print(datetime.datetime.now())
    print("Ending histogram execution")
    time.sleep(300)
    t1_stop.set()

def plot_graph():
    plt.style.use('classic')

    ax=plt.gca()
    ax.xaxis_date()
    xfmt = md.DateFormatter('%H:%M:%S')
    ax.xaxis.set_major_formatter(xfmt)

    x_available = [x[0] for x in global_available]
    y_available = [x[1] for x in global_available]
    plt.plot(x_available,y_available, color='blue')
    plt.plot(x_available,y_available, color='blue',marker='o',label='Available pods')

    x_unavailable = [x[0] for x in global_unavailable]
    y_unavailable = [x[1] for x in global_unavailable]
    plt.plot(x_unavailable,y_unavailable, color='magenta')
    plt.plot(x_unavailable,y_unavailable, color='magenta',marker='o',label='Unavailable pods')


    x_kill = [x[0] for x in global_kill]
    y_kill = [x[1] for x in global_kill]
    plt.plot(x_kill,y_kill,color='red',marker='o',label='Killed pods')

    plt.legend(loc='upper left')

    plt.savefig('foo.png', bbox_inches='tight')
    plt.close()


if __name__ == "__main__":
    namespace = "test-webapp"
    try:
        t1 = threading.Thread(target=get_event, args=(namespace, t1_stop))
        t1.start()
        t2 = threading.Thread(target=run_histogram, args=(namespace, t2_stop))
        t2.start()
    except:
        print "Error: unable to start thread"

    while not t2_stop.is_set():
        pass

    print ("Ended all threads")

    plot_graph()
