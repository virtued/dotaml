from pymongo import MongoClient
#from progressbar import ProgressBar, Bar, Percentage, FormatLabel, ETA
import numpy as np

np.set_printoptions(threshold=np.nan)

client = MongoClient()
db = client.dotabot
matches = db.matches

# We're going to create a training matrix, X, where each
# row is a different match and each column is a feature

# The features are bit vectors indicating whether heroes
# were picked (1) or not picked (0). The first N features
# correspond to radiant, and the last N features are
# for dire.

NUM_HEROES = 110
NUM_FEATURES = NUM_HEROES * 2

# Our training label vector, Y, is a bit vector indicating
# whether radiant won (1) or lost (-1)
NUM_MATCHES = matches.count()

# Initialize training matrix
X = np.zeros((NUM_MATCHES, NUM_FEATURES), dtype=np.int8)

# Initialize training label vector
Y = np.zeros(NUM_MATCHES, dtype=np.int8)

#widgets = [FormatLabel('Processed: %(value)d/%(max)d matches. '), ETA(), Percentage(), ' ', Bar()]
##pbar = ProgressBar(widgets=widgets, maxval=NUM_MATCHES).start()


leaver_count = 0;
kills_count = 0;
for i, record in enumerate(matches.find()):
    #pbar.update(i)

    if record['duration'] / 60 < 20:
        continue

    if record['human_players'] != 10:
        continue

    leaver_status = 0
    radian_kills = 0
    dire_kills = 0
    for player in record['players']:
        if player['leaver_status'] != 0:
            leaver_status = 1
            break
        if player['player_slot'] < 10:
            radian_kills += player['kills']
        else:
            dire_kills += player['kills']

    if leaver_status != 0:
        leaver_count += 1
        if leaver_count %10000 == 0:
            print("leavers: ", leaver_count)
        continue

    if abs(radian_kills - dire_kills) > 30:
        kills_count += 1
        if kills_count % 1000 == 0:
            print("diff kill", kills_count)
        continue

    if i % 5000 == 0:
        print("finished: ", i)


    Y[i] = 1 if record['radiant_win'] else 0
    players = record['players']
    for player in players:
        hero_id = player['hero_id'] - 1

        # If the left-most bit of player_slot is set,
        # this player is on dire, so push the index accordingly
        player_slot = player['player_slot']
        if player_slot >= 128:
            hero_id += NUM_HEROES

        X[i, hero_id] = 1

#pbar.finish()

print("Permuting, generating train and test sets.")
indices = np.random.permutation(NUM_MATCHES)
test_indices = indices[0:NUM_MATCHES/10]
train_indices = indices[NUM_MATCHES/10:NUM_MATCHES]

X_test = X[test_indices]
Y_test = Y[test_indices]

X_train = X[train_indices]
Y_train = Y[train_indices]

print("Saving output file now...")
np.savez_compressed('test_%d.npz' % len(test_indices), X=X_test, Y=Y_test)
np.savez_compressed('train_%d.npz' % len(train_indices), X=X_train, Y=Y_train)

