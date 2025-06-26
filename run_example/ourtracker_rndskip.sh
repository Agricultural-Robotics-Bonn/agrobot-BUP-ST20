python runner.py --yaml ../final_seq_info.yaml --image_yaml ../final_sequences.yaml --m2f ../mask2former_depthfiltered --image_loc imagedir --output_root saveloc  --skip_files skip_pickles/random_skips.pkl --min_tracks 2 --keep_running 10

python runner.py --yaml ../final_seq_info.yaml --image_yaml ../final_sequences.yaml --m2f ../mask2former_depthfiltered --image_loc imagedir --output_root saveloc --distance_criteria dr --radius_ot maximum --threshold 1.0 --min_tracks 2 --keep_running 10 --skip_files skip_pickles/random_skips.pkl

python runner.py --yaml ../final_seq_info.yaml --image_yaml ../final_sequences.yaml --m2f ../mask2former_depthfiltered --image_loc imagedir --output_root saveloc --distance_criteria dre_delta --radius_ot maximum --threshold 1.0 --min_tracks 5 --keep_running 10 --skip_files skip_pickles/random_skips.pkl
