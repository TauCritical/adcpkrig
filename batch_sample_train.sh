#!/bin/bash
#

python sample_train.py 6 20 4 40 4 v_mag
python sample_train.py 6 20 4 40 4 v_x
python sample_train.py 6 20 4 40 4 v_y
python sample_train.py 6 20 4 40 4 v_z
aws s3 cp 6_predicts_v_mag.pickle s3://adcpkrig/
aws s3 cp 6_predicts_v_x.pickle s3://adcpkrig/
aws s3 cp 6_predicts_v_y.pickle s3://adcpkrig/
aws s3 cp 6_predicts_v_z.pickle s3://adcpkrig/

python sample_train.py 7 40 4 10 4 v_mag
python sample_train.py 7 40 4 10 4 v_x
python sample_train.py 7 40 4 10 4 v_y
python sample_train.py 7 40 4 10 4 v_z
aws s3 cp 7_predicts_v_mag.pickle s3://adcpkrig/
aws s3 cp 7_predicts_v_x.pickle s3://adcpkrig/
aws s3 cp 7_predicts_v_y.pickle s3://adcpkrig/
aws s3 cp 7_predicts_v_z.pickle s3://adcpkrig/

python sample_train.py 8 40 4 20 4 v_mag
python sample_train.py 8 40 4 20 4 v_x
python sample_train.py 8 40 4 20 4 v_y
python sample_train.py 8 40 4 20 4 v_z
aws s3 cp 8_predicts_v_mag.pickle s3://adcpkrig/
aws s3 cp 8_predicts_v_x.pickle s3://adcpkrig/
aws s3 cp 8_predicts_v_y.pickle s3://adcpkrig/
aws s3 cp 8_predicts_v_z.pickle s3://adcpkrig/

python sample_train.py 9 40 4 40 4 v_mag
python sample_train.py 9 40 4 40 4 v_x
python sample_train.py 9 40 4 40 4 v_y
python sample_train.py 9 40 4 40 4 v_z
aws s3 cp 9_predicts_v_mag.pickle s3://adcpkrig/
aws s3 cp 9_predicts_v_x.pickle s3://adcpkrig/
aws s3 cp 9_predicts_v_y.pickle s3://adcpkrig/
aws s3 cp 9_predicts_v_z.pickle s3://adcpkrig/

python sample_train.py 10 10 2 20 2 v_mag
python sample_train.py 10 10 2 20 2 v_x
python sample_train.py 10 10 2 20 2 v_y
python sample_train.py 10 10 2 20 2 v_z
aws s3 cp 10_predicts_v_mag.pickle s3://adcpkrig/
aws s3 cp 10_predicts_v_x.pickle s3://adcpkrig/
aws s3 cp 10_predicts_v_y.pickle s3://adcpkrig/
aws s3 cp 10_predicts_v_z.pickle s3://adcpkrig/

python sample_train.py 11 10 8 20 8 v_mag
python sample_train.py 11 10 8 20 8 v_x
python sample_train.py 11 10 8 20 8 v_y
python sample_train.py 11 10 8 20 8 v_z
aws s3 cp 11_predicts_v_mag.pickle s3://adcpkrig/
aws s3 cp 11_predicts_v_x.pickle s3://adcpkrig/
aws s3 cp 11_predicts_v_y.pickle s3://adcpkrig/
aws s3 cp 11_predicts_v_z.pickle s3://adcpkrig/