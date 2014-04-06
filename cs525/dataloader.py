from dota2py import api
from pymongo import MongoClient
import json
import sys, getopt,os

client = MongoClient(os.getenv('DOTABOT_DB_SERVER', 'localhost'), 27017)
db = client[os.getenv('DOTABOT_DB_NAME', 'dotabot')]
match_collection = db.matches



def load_data(key, dest, start_point, num):
    api.set_api_key(key)
    match_id = start_point
    store = [];
    count = 0;
    file_index = 0;
    valid_mode = [0, 1, 2, 3, 4, 5]
    for i in xrange(0, num):
        try:
            match = api.get_match_details(match_id + i)["result"]
            if match["game_mode"] in valid_mode:
                #store.append(match)
                match_collection.insert(gmd)
        except:
            continue

        if i% 100 == 0:
            print "finished %d", (i)

        #if len(store) %1000 == 0:
        #    print("store size = ", len(store))

        #if len(store) >= 10000:
        #    dest_file = open("{0}-{1}".format(dest, file_index), "a");
        #    json.dump(store, dest_file)
        #    dest_file.close()
        #    store = []
        #    file_index = file_index + 1

    #if len(store) > 0:
    #    dest_file = open("{0}-{1}".format(dest, file_index), "a");
    #    json.dump(store, dest_file)
    #    dest_file.close()

def main(argv):
    key = ""
    dest = ""
    start_point = 0
    num = 0
    try:
        opts, args = getopt.getopt(argv,"h:k:o:s:n:",["key=", "output=", "start=", "num="])
    except getopt.GetoptError:
        print 'dataloader.py -k <key> -o <outputfile> -s <first match id> -n <number of request>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'dataloader.py -k <key> -o <outputfile> -s <first match id> -n <number of request>'
            sys.exit()
        elif opt in ("-k", "--key"):
            key = arg
        elif opt in ("-o", "--output"):
            dest = arg
        elif opt in ("-s", "--start"):
            start_point = int(arg)
        elif opt in ("-n", "--num"):
            num = int(arg)

    load_data(key, dest, start_point, num)
    db.close()
    print 'done.'

if __name__ == "__main__":
    main(sys.argv[1:])
