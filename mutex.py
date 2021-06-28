#!/usr/bin/env python

from __future__ import print_function

import argparse
import os
import subprocess
import sys
import uuid


def execute(cmd):
    print("RUNNING...\n", cmd, "\n")
    process = subprocess.Popen(cmd,
                               shell=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)

    while True:
        nextline = process.stdout.readline()
        if nextline == '' and process.poll() is not None:
            break
        sys.stdout.write(nextline)
        sys.stdout.flush()

    stderr = process.communicate()[1]

    if process.returncode != 0:
        print(
            "[ERROR] command:", cmd, "exited with code:", process.returncode,
            file=sys.stderr
        )
        print(stderr, file=sys.stderr)
        raise RuntimeError
    else:
        return process.returncode


def createLink(src, work_dir):
    dest = os.path.join(work_dir, os.path.basename(src))
    os.symlink(src, dest)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-d", "--data-file",
                        type=str,
                        required=True,
                        help="Name of the data file. Mandatory.")
    parser.add_argument("-m", "--max-group-size",
                        type=int,
                        default=5,
                        help="The maximum size of a result mutex group. Integer value. Default is 5.")
    parser.add_argument("-f", "--first-level-random-iteration",
                        type=int,
                        default=10000,
                        help="Number of randomization to estimate null distribution of member p-values in mutex groups. Integer. Default is 10000.")
    parser.add_argument("-s", "--second-level-random-iteration",
                        type=int,
                        default=100,
                        help="Number of runs to estimate the null distribution of final scores. Integer. Default is 100. If FDR control on results is not required and only the ranking of the result groups is sufficient, set this parameter to 0.")
    parser.add_argument("-fc", "--fdr-cutoff",
                        type=float,
                        help="Users can select a specific FDR cutoff. When not provided, or when set to a negative value, the FDR cutoff that maximizes the expected value of true positives - false positives is used.")
    parser.add_argument("-sc", "--score-cutoff",
                        type=float,
                        help="")
    parser.add_argument("-S", "--search-on-signaling-network",
                        type=bool,
                        help="Whether to reduce the search space using the signaling network. true or false. Default is true.")
    parser.add_argument("-g", "--genes-file",
                        type=str,
                        help="This parameter can be used to limit the search to a subset of genes. The file should contain a gene symbol per line.")
    parser.add_argument("-G", "--gene-ranking-file",
                        type=str,
                        help="")
    parser.add_argument("-st", "--sample-to-tissue-mapping-file",
                        type=str,
                        help="")
    parser.add_argument("-gl", "--gene-limit",
                        type=int,
                        help="")
    parser.add_argument("-n", "--network-file",
                        type=str,
                        required=True,
                        help="To customize the signaling network, users can use this parameter. The tab-delimited network file should contain 3 columns (Gene Symbol 1, interaction-type, Gene Symbol 2).")
    parser.add_argument("-ma", "--minimum-alteration-count-threshold",
                        type=int,
                        help="")
    parser.add_argument("--random",
                        action="store_true",
                        help="When the dataset is large, and FDR control is required, the execution time can be long. To accelerate the execution, second-level randomizations can be parallelized.")

    args = parser.parse_args()
    work_dir = os.path.join(os.getcwd(), str(uuid.uuid4()))
    os.mkdir(work_dir)

    createLink(args.data_file, work_dir)
    args.data_file = os.path.basename(args.data_file)

    createLink(args.network_file, work_dir)
    args.network_file = os.path.basename(args.network_file)

    if args.genes_file is not None:
        createLink(args.genes_file, work_dir)
        args.genes_file = os.path.basename(args.genes_file)

    if args.gene_ranking_file is not None:
        createLink(args.gene_ranking_file, work_dir)
        args.gene_ranking_file = os.path.basename(args.gene_ranking_file)

    with open("{0}/parameters.txt".format(work_dir), "wb") as fh:
        for k, v in vars(args).items():
            if v is not None and k is not "random":
                fh.write("{0} = {1}\n".format(k.replace("_", "-"), v))

    if args.random:
        execute("java -jar /opt/mutex.jar {0} random".format(work_dir))
    else:
        execute("java -jar /opt/mutex/target/mutex.jar {0}".format(work_dir))
