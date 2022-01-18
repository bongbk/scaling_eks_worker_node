import boto3, sys, smtplib, time, getopt
import os

def usage(err):
    print (err)
    sys.exit(2)

def help():

    usage( "Scaling EKS Worker node by bongbk, email: ngocbongbk@gmail.com " + VERSION + "\n"+
              "Standard use:\t" + sys.argv[1] + " -O accessKey -W secretKey -r eu-west-1 -k eks-cluster -w nodename -n number_of_worker -m max_node")

def main():
    def check(status):
        if (len(status) == len(number_node)):
            print("Success scale: %s to %s" % (str(eks_id), str(status)) )
        else:
            print("Error scale %s to %s" % (str(eks_id), str(status)))

    if (len(sys.argv) < 2):
        print (len(sys.argv))
        help()

    region_id = None
    eks_id = None
    aws_access_key = None
    aws_secret_key = None
    node_name = None
    number_node = None
    max_size = None
    try:
        opts, args = getopt.getopt(sys.argv[1:], "O:W:r:k:w:n:m:h:",["aws-access-key=","aws-secret-key=","region_id=","eks_id=","node_name=","number_node=","max_size","help"])
    except getopt.GetoptError as err:
        usage(str(err))
    for opt, arg in opts:
        if opt in ['-O', '--aws-access-key']:
            aws_access_key = arg
        elif opt in ['-W', '--aws-secret-key']:
            aws_secret_key = arg
        elif opt in ['-r', '--region-id']:
            region_id = arg
        elif opt in ('-k', '--eks_id'):
            eks_id = arg
        elif opt in ('-w', '--node_name'):
            node_name = arg
        elif opt in ('-n', '--number_node'):
            number_node = arg
        elif opt in ('-n', '--max_size'):
            max_size = arg
        elif opt in ('-h', '--help'):
            help()

    conn = boto3.client('eks',region_name=region_id, aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)
    if (conn == None):
        print("Cannot connection pls check network")
        sys.exit(-1)
    result = []
    response = conn.update_nodegroup_config(
        clusterName=eks_id,
        nodegroupName=node_name,
        scalingConfig={
            'minSize': int(number_node),
            'maxSize': int(max_size),
            'desiredSize': int(number_node)
        }
    )
    ck_status=response['update']['params'][2]['value']
    check(ck_status)
    return
if __name__ == "__main__":
    os.environ["HTTP_PROXY"] = "http://proxyserver:port"
    os.environ["HTTPS_PROXY"] = "http://proxyserver:port"
    VERSION = "v.0.1"
    main()
