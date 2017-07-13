# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.

"""
def neighbor(gmap):
    neighboring_pairs = []
    for i in range(0, 4):
        for j in range(0, 4):
            if i < 3:
                neighboring_pairs.append((i,j,i+1,j))
                if j < 3:
                    neighboring_pairs.append((i,j,i,j+1))
    diff_neighbors = []
    sv_neighbors = []
    for index_pair in neighboring_pairs:
        if gmap[index_pair[0]][index_pair[1]] != 0 and gmap[index_pair[2]][index_pair[3]] != 0:
            diff = abs(gmap[index_pair[0]][index_pair[1]] - gmap[index_pair[2]][index_pair[3]])
            diff_neighbors.append(diff)
        if gmap[index_pair[0]][index_pair[1]] == gmap[index_pair[2]][index_pair[3]]:
            sv_neighbors.append(gmap[index_pair[0]][index_pair[1]])

    total_diff_neighbors = sum(diff_neighbors)
    total_sv = sum(sv_neighbors)

    return (total_diff_neighbors, total_sv)


def reward(gmap):
	reward_edge_strategy = []
	for i in range(0, 4):
		if gmap[i] == sorted(gmap[i]):
			reward_edge_strategy.append(max(gmap[i]))
	for j in range(0, 4):
		if gmap[3][j] >= gmap[2][j] and gmap[2][j] >= gmap[1][j] and gmap[1][j] >= gmap[0][j]:
			reward_edge_strategy.append(gmap[3][j])
            
	reward = sum(reward_edge_strategy)
	return reward
            

map1 = [[2,4,8,16],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
print(reward(map1))

map2 = [[2,4,8,16],[4,0,0,0],[8,0,0,0],[32,0,0,0]]
print(reward(map2))

map2 = [[2,4,8,16],[4,0,0,32],[8,0,0,64],[32,0,0,256]]
print(reward(map2))

map3 = [[2,4,8,16],[4,4,0,32],[8,0,0,64],[32,0,0,64]]
print(neighbor(map3))





diff_sides_2 = sum([(map2[3][i] - map2[0][i]) for  in zip(map2[0][i], map2[3][i])])
