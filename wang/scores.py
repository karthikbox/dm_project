import json
import os
import networkx as nx
import math
import datetime

if __name__ == '__main__':
    print 'hi'
    data_dir="/home/karthik/yelp/mek/yelp_dataset_challenge_academic_dataset"
    data_gen_dir="/home/karthik/yelp/mek/data_generated"
    G=nx.read_gml(os.path.join(data_gen_dir,"wang_graph.gml"))
    #G=nx.read_gml(os.path.join(data_gen_dir,"wang_graph_test.gml"))
    print 'Graph G read'
    #print G.node[17]
    #print [n for n in nx.all_neighbors(G,17)]
    round_counter=5
    prev_weight={}
    diff_weight={}
    for n, d in G.nodes_iter(data=True):
        prev_weight[n]=d['weight']
        diff_weight[n]=0
    for i in range(round_counter):
        print 'run_counter ',i
        #calculating honesty
        star_thresh=1.0
        time_delta=datetime.timedelta(days=90)# 3 months
        print 'honesty start'
        for n,d in G.nodes_iter(data=True):
            #print n,' ',d
            reliability_store=0
            if d['type']==1:
                n_stars=d['stars']
                time_review=datetime.datetime.strptime(d['date'],"%Y-%m-%d")
                sync_trust=0
                async_trust=0
                for n1 in nx.all_neighbors(G,n):
                    if G.node[n1]['type']==2:
                        #this is a business of the review
                        #get reliability of this store
                        reliability_store=G.node[n1]['weight']
                        #get all reviews of this business
                        for n2 in nx.all_neighbors(G,n1):
                            #n2 is the id of a review
                            n2_stars=G.node[n2]['stars']
                            time_n2=datetime.datetime.strptime(G.node[n2]['date'],"%Y-%m-%d")
                            time_low=(time_review-time_delta)
                            time_high=(time_review+time_delta)
                            if  (time_n2 >= time_low) and (time_n2 <=time_high ):
                                #checking time windoow bounds
                                #bounds okay
                                #check stars difference
                                if math.fabs(n_stars - n2_stars) <= star_thresh:
                                    #stars diff okay
                                    #in sync...add all review's reviewer's trustworthiness
                                    for n3 in nx.all_neighbors(G,n2):
                                        if G.node[n3]['type']==0:
                                            #reviewer of review n2 is n3
                                            #get trustworthiness of n3 and add into sync_trust
                                            sync_trust+=G.node[n3]['weight']
                                else:
                                    # n2 doesnt satisfy stars difference bounds
                                    for n3 in nx.all_neighbors(G,n2):
                                        if G.node[n3]['type']==0:
                                            #reviewer of review n2 is n3
                                            #get trustworthiness of n3 and add into async_trust
                                            async_trust+=G.node[n3]['weight']
                agreement_score=sync_trust - async_trust
                agreement_score_norm=(2.0/(1+math.pow(math.e,-1*agreement_score)))-1
                d['weight']=math.fabs(reliability_store)*agreement_score_norm
        #end of review honesty score computation
        print 'trust start'
        #trustworthinesss start
        for n,d in G.nodes_iter(data=True):
            #print n,' ',d
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
                G.node[n]['weight']=(2.0/(1+(math.pow(math.e,-sum))))-1
        #trustworthinesss end
        print 'reliability start'
        #start reliability of store
        median_stars=3
        for n,d in G.nodes_iter(data=True):
            if d['type']==2:
                #n is a store
                theta=0
                for n1 in nx.all_neighbors(G,n):
                    #n1 is a review on store n
                    for n2 in nx.all_neighbors(G,n1):
                        if G.node[n2]['type']==0:
                            #n2 is a reviewer of the review n1
                            #if n2's trustworthiness is > 0 then consider
                            if G.node[n2]['weight'] > 0:
                                theta+=(G.node[n2]['weight'])*(G.node[n1]['stars']-median_stars)
                #now we have theta, calculate reliability R
                d['weight']=(2.0/(1+math.pow(math.e,-1*theta)))-1
        #end of reliability of store
        #compute deviation of new weight from old  weight
        print 'diff update start'
        for n, d in G.nodes_iter(data=True):
        #prev_weight[n]=d['weight']
            diff_weight[n]=prev_weight[n]-d['weight']
            prev_weight[n]=d['weight']
    print 'file write start'
    f1=open(os.path.join(data_gen_dir,'convergence.dat'),'w')
    for i in prev_weight.keys():
        f1.write(str(i)+';'+str(diff_weight[i])+'\n')
    f1.close()
