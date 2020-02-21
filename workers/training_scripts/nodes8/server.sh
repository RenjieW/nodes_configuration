export COMMAND='python image_classification.py --dataset cifar10 --model vgg11 --batch-size 64 --epochs 1 --kvstore dist_sync --log-interval 5'
cd /tmp/mxnet_job
DMLC_ROLE=server DMLC_PS_ROOT_URI=10.10.1.8 DMLC_NODE_HOST=10.10.1.8 DMLC_PS_ROOT_PORT=9092 DMLC_NUM_SERVER=2 DMLC_NUM_WORKER=6 $COMMAND &

