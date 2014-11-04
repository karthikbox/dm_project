#dataset_url=/home/karthik/yelp/mek/yelp_dataset_challenge_academic_dataset
import os
import networkx as nx
import json


def add_reviews(f,G):
    count=1
    print count
    for line in f:
        r=json.loads(line.strip('\n'))
        G.add_edge(r['user_id'],count)
        G.add_edge(r['business_id'],count)
        G.node[count]['type']=1
        G.node[r['user_id']]['type']=0
        G.node[r['business_id']]['type']=2
        G.node[count]['weight']=1
        G.node[count]['date']=r['date']
        G.node[count]['stars']=r['stars']
        G.node[r['user_id']]['weight']=1
        G.node[r['business_id']]['weight']=1
        #print G.node[r['user_id']]
        count+=1
        if count%100000==0:
            print count
        

if __name__ == '__main__':
    print 'hi'
    data_dir="/home/karthik/yelp/mek/yelp_dataset_challenge_academic_dataset"
    data_gen_dir="/home/karthik/yelp/mek/data_generated"
    f_review=open(os.path.join(data_dir,"yelp_academic_dataset_review.json"),'r')
    #f_review=open(os.path.join(data_dir,"test_review.json"),'r')
    #f=open(os.path.join(data_dir,"test_review.json"),'w')
#    for i in range(10):
#        line=f_review.readline()
#        f.write(line)
#    f.close()
    G=nx.Graph()
    #add users as nodes
    add_reviews(f_review,G)
    # print len(G.nodes())
    # c=1
    # for n in G.nodes(data=True):
    #     if n[1]['type']==1:
    #         print c,' ',n[0]
    #         c+=1

    #nx.write_gml(G,os.path.join(data_gen_dir,"wang_graph_test.gml"))
    nx.write_gml(G,os.path.join(data_gen_dir,"wang_graph.gml"))
    #print G.nodes()
    f_review.close()
