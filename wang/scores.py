import json
import os
import networkx as nx
import math

if __name__ == '__main__':
    print 'hi'
    data_dir="/home/karthik/yelp/mek/yelp_dataset_challenge_academic_dataset"
    data_gen_dir="/home/karthik/yelp/mek/data_generated"
    #G=nx.read_gml(os.path.join(data_gen_dir,"wang_graph.gml"))
    G=nx.read_gml(os.path.join(data_gen_dir,"wang_graph_test.gml"))
    print 'Graph G read'
    #print G.node[17]
    #print [n for n in nx.all_neighbors(G,17)]
    for n,d in G.nodes_iter(data=True):
        print n,' ',d
        #n is id [0,max]
        #d is dict of that node with id n
        if d['type']==0:
        #    print n,' ',d
            #reviewer
            sum=0
            for n1 in nx.all_neighbors(G,n):
                #n1 is id of the review
                if G.node[n1]['type']==1:
                    sum+=G.node[n1]['weight']
            #trust worthiness formula of reviewer .... done
            G.node[n]['weight']=(2/(1+(math.pow(math.e,-sum))))-1
            
        #break
#STEP 1: calculate trustworthiness
#find neighbours of reviewer from graph g, the reviews written by him type=1
#[d for n,d in G.nodes_iter(data=True)]

#loop_outer: iterate over nodes whose type=0 returns reviewer
  #loop_inner: all_neighbors(G,reviewer) #returns iterator
    #iterator.weight #keep adding sums to get honesty summary
  #end loop_inner:

#plug it in formula and assign weight=(2/(1+e^-summary))-1
#end loop_outer:

#STEP 2: calulate HONESTY
#2(a) get A(v,dt)
#loop_outer: iterate over nodes whose type=1 returns review
  
