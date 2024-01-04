import sys
import pandas as pd
from sklearn import metrics
import matplotlib.pyplot as plt

result_folder = 'demo'

def plot_anograph(algorithm, dataset_name):
    """
    Plots the ROC for AnoGraph and AnoGraphK.

    :param algorithm: Algorithm that was used.
    :param dataset_name: Name of the dataset.
    """    

    output_file = f'../{result_folder}/ROC_{algorithm}_{dataset_name}.png'
    param = [(15,25),(30,50),(60,50),(60,100)]
    plt.figure(figsize=(8, 8))
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title(f'ROC Curve for {algorithm} on {dataset_name}')
    plt.legend(loc='lower right')

    for x in param:
        data = pd.read_csv(f'../{result_folder}/scores_{algorithm}_{dataset_name}_{x[0]}_{x[1]}.txt', header=None, names=['Score', 'Label'], sep=',')
        fpr, tpr, thresholds = metrics.roc_curve(data.Label, data.Score)
        roc_auc = metrics.auc(fpr, tpr)
        label_str = f'Area = {roc_auc:.2f} for {x}'
        plt.plot(fpr, tpr, lw=2, label=label_str)

    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.legend()  
    plt.savefig(output_file)

def plot_anoedge(algorithm):
    """
    Plots the ROC for AnoEdgeG.

    :param algorithm: Algorithm that was used.
    """ 
    output_file = f'../{result_folder}/ROC_{algorithm}.png'
    datasets = ['DARPA','ISCX','DDOS2019','IDS2018']
    plt.figure(figsize=(8, 8))
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title(f'ROC Curve for {algorithm}')
    plt.legend(loc='lower right')

    for dataset_name in datasets:
        data = pd.read_csv(f'../{result_folder}/scores_{algorithm}_{dataset_name}.txt', header=None, names=['Score', 'Label'], sep=',')
        fpr, tpr, thresholds = metrics.roc_curve(data.Label, data.Score)
        roc_auc = metrics.auc(fpr, tpr)
        label_str = f'Area = {roc_auc:.2f} for {dataset_name}'
        plt.plot(fpr, tpr, lw=2, label=label_str)

    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.legend()  
    plt.savefig(output_file)

def main():
    """
    Main function.
    """ 
    if len(sys.argv) < 2:
        print(f"Expected at least two arguments but got {len(sys.argv)}")
        sys.exit(1)

    algorithm = sys.argv[1]
    if algorithm == "AnoGraph":
        plot_anograph('AnoGraph', sys.argv[2])
    elif algorithm == "AnoGraphK":
        plot_anograph('AnoGraphK', sys.argv[2])
    elif algorithm == "AnoEdgeG":
        plot_anoedge('AnoEdgeG')


if __name__ == "__main__":
    main()