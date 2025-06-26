# bytetrack iou
python runner.py --yaml ../final_seq_info.yaml --image_yaml ../final_sequences.yaml --m2f ../mask2former_depthfiltered --image_loc image_directory --output_root /your/save/directory --usebytetrack

# bytetrack dr
python runner.py --yaml ../final_seq_info.yaml --image_yaml ../final_sequences.yaml --m2f ../mask2former_depthfiltered --image_loc image_directory --output_root /your/save/directory --usebytetrack --match_thresh 1.0 --match_second 1.0 --match_unconfirmed 1.0 --track_buffer 10 --distance_criteria dr

# bytetrack dre-d
python runner.py --yaml ../final_seq_info.yaml --image_yaml ../final_sequences.yaml --m2f ../mask2former_depthfiltered --image_loc image_directory --output_root /your/save/directory --usebytetrack --match_thresh 1.0 --match_second 1.0 --match_unconfirmed 1.0 --track_buffer 10 --beta_bt 0.5 --radius_bt maximum --delta_bt summation --distance_criteria dre_delta

# bytetrack dre-s
python runner.py --yaml ../final_seq_info.yaml --image_yaml ../final_sequences.yaml --m2f ../mask2former_depthfiltered --image_loc image_directory --output_root /your/save/directory --usebytetrack --match_thresh 1.0 --match_second 1.0 --match_unconfirmed 1.0 --track_buffer 10 --beta_bt 0.5 --radius_bt maximum --delta_bt maximum --distance_criteria dre_sigma
