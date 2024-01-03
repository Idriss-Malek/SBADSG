# SBADSG
Sketch-Based Anomaly Detection in Streaming Graphs  
Python implementation in River style of the paper : arXiv:2106.04486 [cs.DS]  
The paper can be found in the following link : https://arxiv.org/pdf/2106.04486.pdf  
## To run tests :  
Use the test.py file by running the following commands.  
- To run AnoEdgeG : `python test.py 'AnoEdgeG' rows buckets decay`  
- To run AnoGraph : `python test.py 'AnoEdgeG' rows buckets time_window edge_threshold`    
- To run AnoGraphK : `python test.py 'AnoEdgeG' rows buckets time_window edge_threshold K`    
The results are stored in result folder and are 3 files:  
- Time file where the execution time is written.  
- Plot file where the data is plotted to visualize the results of the algorithm.  
- Results file where predicted scores and true labels are stored.  
## To create ROC:
The roc.py file was created assuming that the user have already used test.py on all datasets and with all the pairs (time_window, edge_threshold) that are mentionned in the paper.  
Use the roc.py file by running the following commands.  
- To obtain ROC of all 4 datasets with AnoEdgeG : `python roc.py 'AnoEdgeG'`    
- To obtain Roc for all 4 pairs of parameters on one dataset with AnoGraph : `python roc.py 'AnoGraph' 'dataset'`    
- To obtain Roc for all 4 pairs of parameters on one dataset with AnoGraphK : `python roc.py 'AnoGraphK' 'dataset'`    
## Results
All the results have been uploaded in the results folder of the repo : (./results)
