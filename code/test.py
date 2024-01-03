import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import time
import sys


from anoGraph import AnoGraph
from anoGraphK import AnoGraphK
from anoEdgeG import AnoEdgeG

def print_results(algorithm, dataset, scores, times, y, time_window = 0, edge_threshold= 0):
    """
    Plots the scores obtained and write the scores and execution time in a file.

    :param algorithm: Algorithm that was used.
    :param dataset_name: Name of the dataset.
    :param scores: Scores obtained.
    :param times: Time.
    :param y: Labels.
    :param time_window: Time window for edges to constitue a graph.
    :param edge_threshold: Number of anomalous edge for a graph to be considered anomalous.
    """ 
    if algorithm == 'AnoEdgeG':
        SUFFIX = f'{algorithm}_{dataset}'
    elif algorithm == 'AnoGraph' or algorithm == 'AnoGraphK':
        SUFFIX = f'{algorithm}_{dataset}_{time_window}_{edge_threshold}'
    with open(f'../results/scores_{SUFFIX}.txt', 'w') as file:
            for score, label in zip(scores, y):
                file.write(f"{score:.4f},{label}\n")
    blue_time = [t for t, y in zip(times, y) if y == 0]
    red_time = [t for t, y in zip(times, y) if y == 1]

    blue_scores = [score for score, y in zip(scores, y) if y == 0]
    red_scores = [score for score, y in zip(scores, y) if y == 1]

    # Plotting
    plt.scatter(blue_time, blue_scores, color='blue', label='y=0', s = 5)
    plt.scatter(red_time, red_scores, color='red', label='y=1', s = 1)

    plt.xlabel('Time')
    plt.ylabel('Scores')
    plt.title(f'{algorithm} on {dataset}')
    plt.legend()
    plt.savefig(f'../results/plot_{SUFFIX}.png')
    print('Figure saved')
    with open(f'../results/time_{SUFFIX}.txt', 'w+') as file:
        file.write(f'Time taken for each graph : {((end-start) / len(scores)):.4f} \n')
        file.write(f'Time taken in total : {(end-start):.4f}')


if __name__ == "__main__":

    if len(sys.argv) < 5 :
        print('Missing arguments')
        sys.exit(1)
    algorithm = sys.argv[1]
    rows = int(sys.argv[2])
    buckets = int(sys.argv[3])
    if algorithm == 'AnoEdgeG':
        decay = float(sys.argv[4])
    elif algorithm == 'AnoGraph' or algorithm == 'AnoGraphK':
        time_window = int(sys.argv[4])
        edge_threshold = int(sys.argv[5])
        if algorithm == 'AnoGraphK':
            K = int(sys.argv[6])
    else:
        print('Unknown algorithm!')
        sys.exit(1) 

    datasets = ['ISCX','DARPA','DDOS2019','IDS2018']
    if algorithm == 'AnoEdgeG':
        for dataset in datasets:
            plt.clf()
            folder = f'C:/Users/idris/Desktop/homework 4a/projet_dsp/data/{dataset}/'
            X = pd.read_csv(folder + 'Data.csv', header=None, names = ['source','destination','time'])
            y = pd.read_csv(folder+'Label.csv',header=None)
            y = y[y.columns[0]].tolist()


            model = AnoEdgeG(rows, buckets, decay)

            start = time.time()
            scores = []
            times = []
            for index, row in X.iterrows():
                u,v,t = tuple(row)
                w = 1
                model.learn_one((u,v,w,t))
                scores.append(model.score_one(u,v))
                times.append(t)
            end = time.time()
            print_results(algorithm, dataset, scores, times, y)
    else:
        for dataset in datasets:
            plt.clf()
            folder = f'C:/Users/idris/Desktop/homework 4a/projet_dsp/data/{dataset}/'
            X = pd.read_csv(folder + 'Data.csv', header=None, names = ['source','destination','time'])
            X['window'] = X['time'].apply(lambda x : x // time_window)
            y = pd.read_csv(folder+'Label.csv',header=None)
            y = y[y.columns[0]].tolist()


            def enumerate_graph(edges, labels):
                source, destination, time, window = edges.values.T
                ukeys, index = np.unique(window, True)
                source_splitted = np.split(source, index[1:])
                destination_splitted = np.split(destination, index[1:])
                weights_splitted = np.split([1 for i in range(len(edges))], index[1:])
                labels_splitted = np.split(labels, index[1:])
                X = pd.DataFrame({'window':ukeys, 'info':[list(zip(s,d,w)) for s,d,w in zip(source_splitted,destination_splitted,weights_splitted)]})
                y = [(sum(a) >= edge_threshold) for a in labels_splitted]
                return X,y
            
            X,y = enumerate_graph(X,y)
            if algorithm == 'AnoGraph':
                model = AnoGraph(rows, buckets)
            elif algorithm == 'AnoGraphK':
                model = AnoGraphK(rows, buckets, K)


            start = time.time()
            scores = []
            times = []
            for index, graph in X.iterrows():
                model.learn_one(graph['info'])
                scores.append(model.score_one())
                times.append(graph['window'])    
            end = time.time()
            print_results(algorithm, dataset, scores, times, y, time_window, edge_threshold)

        