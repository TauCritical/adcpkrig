#!/bin/bash
#
python sample_train.py 2 10 4 20 4
aws s3 cp 2_predicts_v_mag.pickle s3://adcpkrig/
aws s3 cp 2_predicts_v_x.pickle s3://adcpkrig/
aws s3 cp 2_predicts_v_y.pickle s3://adcpkrig/
aws s3 cp 2_predicts_v_z.pickle s3://adcpkrig/

python sample_train.py 3 10 4 40 4
aws s3 cp 3_predicts_v_mag.pickle s3://adcpkrig/
aws s3 cp 3_predicts_v_x.pickle s3://adcpkrig/
aws s3 cp 3_predicts_v_y.pickle s3://adcpkrig/
aws s3 cp 3_predicts_v_z.pickle s3://adcpkrig/

python sample_train.py 4 20 4 10 4
aws s3 cp 4_predicts_v_mag.pickle s3://adcpkrig/
aws s3 cp 4_predicts_v_x.pickle s3://adcpkrig/
aws s3 cp 4_predicts_v_y.pickle s3://adcpkrig/
aws s3 cp 4_predicts_v_z.pickle s3://adcpkrig/

python sample_train.py 5 20 4 20 4
aws s3 cp 5_predicts_v_mag.pickle s3://adcpkrig/
aws s3 cp 5_predicts_v_x.pickle s3://adcpkrig/
aws s3 cp 5_predicts_v_y.pickle s3://adcpkrig/
aws s3 cp 5_predicts_v_z.pickle s3://adcpkrig/

python sample_train.py 6 20 4 40 4
aws s3 cp 6_predicts_v_mag.pickle s3://adcpkrig/
aws s3 cp 6_predicts_v_x.pickle s3://adcpkrig/
aws s3 cp 6_predicts_v_y.pickle s3://adcpkrig/
aws s3 cp 6_predicts_v_z.pickle s3://adcpkrig/

python sample_train.py 7 40 4 10 4
aws s3 cp 7_predicts_v_mag.pickle s3://adcpkrig/
aws s3 cp 7_predicts_v_x.pickle s3://adcpkrig/
aws s3 cp 7_predicts_v_y.pickle s3://adcpkrig/
aws s3 cp 7_predicts_v_z.pickle s3://adcpkrig/

python sample_train.py 8 40 4 20 4
aws s3 cp 8_predicts_v_mag.pickle s3://adcpkrig/
aws s3 cp 8_predicts_v_x.pickle s3://adcpkrig/
aws s3 cp 8_predicts_v_y.pickle s3://adcpkrig/
aws s3 cp 8_predicts_v_z.pickle s3://adcpkrig/

python sample_train.py 9 40 4 40 4
aws s3 cp 9_predicts_v_mag.pickle s3://adcpkrig/
aws s3 cp 9_predicts_v_x.pickle s3://adcpkrig/
aws s3 cp 9_predicts_v_y.pickle s3://adcpkrig/
aws s3 cp 9_predicts_v_z.pickle s3://adcpkrig/

python sample_train.py 10 10 2 20 2
aws s3 cp 10_predicts_v_mag.pickle s3://adcpkrig/
aws s3 cp 10_predicts_v_x.pickle s3://adcpkrig/
aws s3 cp 10_predicts_v_y.pickle s3://adcpkrig/
aws s3 cp 10_predicts_v_z.pickle s3://adcpkrig/

python sample_train.py 11 10 8 20 8
aws s3 cp 11_predicts_v_mag.pickle s3://adcpkrig/
aws s3 cp 11_predicts_v_x.pickle s3://adcpkrig/
aws s3 cp 11_predicts_v_y.pickle s3://adcpkrig/
aws s3 cp 11_predicts_v_z.pickle s3://adcpkrig/