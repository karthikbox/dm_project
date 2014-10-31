import json
import os
import pprint
import sys

if __name__ == '__main__':
    data_dir="/home/karthik/yelp/mek/yelp_dataset_challenge_academic_dataset"
    data_gen_dir="/home/karthik/yelp/mek/data_generated"
    user_file=os.path.join(data_dir,"yelp_academic_dataset_user.json")
    user_file_out=os.path.join(data_gen_dir,"yelp_user.csv")
    f=open(user_file,'r')
    f1=open(user_file_out,'w')
    f1.write("user_id;name;review_count;friend_count;is_elite;average_stars\n")
    for line in f:
#        data=json.load(line.strip('\n')
#        f1.write(data["user_id"])
        data=json.loads(line.strip('\n'))
        f1.write((data["user_id"]+";"+data["name"]+";"+str(data["review_count"])+";"+str(len(data["friends"]))+";"+str(len(data["elite"]))+";"+str(data["average_stars"])+"\n").encode('utf8'))
#        print data["user_id"]
    f1.close()
    f.close()
