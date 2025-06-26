# ourtracker iou
python runner.py --yaml ../final_seq_info.yaml --image_yaml ../final_sequences.yaml --m2f ../mask2former_depthfiltered --image_loc image_directory --output_root /your/save/directory

# ourtracker dr
python runner.py --yaml ../final_seq_info.yaml --image_yaml ../final_sequences.yaml --m2f ../mask2former_depthfiltered --image_loc image_directory --output_root /your/save/directory --distance_criteria dr --radius_ot minimum --threshold 1.0 --min_tracks 5 --keep_running 5

# ourtracker dre-d
python runner.py --yaml ../final_seq_info.yaml --image_yaml ../final_sequences.yaml --m2f ../mask2former_depthfiltered --image_loc image_directory --output_root /your/save/directory --distance_criteria dre_delta --radius_ot maximum --threshold 1.0 --min_tracks 10 --keep_running 2
