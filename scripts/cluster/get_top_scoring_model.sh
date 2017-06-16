cluster_number=$1

rmfid=`awk -v clnum="$cluster_number" '$2==clnum {print}' cluster_traj_score_weight.dat | sort -r -n -k 4 | head -1 | awk '{print $1}'`
cp ../RMF/frame_$rmfid'.rmf' top_scoring_model_cluster_$cluster_number.rmf

