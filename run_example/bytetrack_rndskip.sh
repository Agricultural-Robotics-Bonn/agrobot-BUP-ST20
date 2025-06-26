python runner.py --yaml ../final_seq_info.yaml --image_yaml ../final_sequences.yaml --m2f ../mask2former_depthfiltered --image_loc imagedirectory --output_root saveloc --usebytetrack --track_buffer 5 --skip_files ../random_skips.pkl

python runner.py --yaml ../final_seq_info.yaml --image_yaml ../final_sequences.yaml --m2f ../mask2former_depthfiltered --image_loc imagedirectory --output_root saveloc --usebytetrack --match_thresh 1.0 --match_second 1.0 --match_unconfirmed 1.0 --track_buffer 5 --distance_criteria dr --radius_bt maximum --skip_files ../random_skips.pkl

python runner.py --yaml ../final_seq_info.yaml --image_yaml ../final_sequences.yaml --m2f ../mask2former_depthfiltered --image_loc imagedirectory --output_root saveloc --usebytetrack --match_thresh 1.0 --match_second 1.0 --match_unconfirmed 1.0 --track_buffer 1 --beta_bt 0.5 --radius_bt maximum --delta_bt summation --distance_criteria dre_delta --skip_files ../random_skips.pkl

python runner.py --yaml ../final_seq_info.yaml --image_yaml ../final_sequences.yaml --m2f ../mask2former_depthfiltered --image_loc imagedirectory --output_root saveloc --usebytetrack --match_thresh 1.0 --match_second 1.0 --match_unconfirmed 1.0 --track_buffer 1 --beta_bt 0.5 --radius_bt maximum --delta_bt summation --distance_criteria dre_sigma --skip_files ../random_skips.pkl
