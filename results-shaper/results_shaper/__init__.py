import argparse


def parse_args(raw_args=None):
    parser = argparse.ArgumentParser(description='Script to shape the report files from the tix-time-condenser into '
                                                 'the batches. This is to imitate the way the tix-time-processor takes '
                                                 'the files and computes them by separating them into different '
                                                 'directories. The idea behind this is to use the files for '
                                                 'exploratory analysis.')
    parser.add_argument('file_path',
                        help='The path where the reports are.')
    parser.add_argument('--tar', '-t', action='store_true', dest='is_tar',
                        help='Indicates that the input path is a tar file. In this case, a temporary directory will be '
                             'created to shape the output.')
    parser.add_argument('--gzip', '-z', action='store_true', dest='is_gz',
                        help='Indicates that the input path is gzipped. Implies it is a tar file.')
    parser.add_argument('--batch-size', '-b', default=19, type=int,
                        help='Indicates the size of each batch.')
    parser.add_argument('--output', '-o', action='store', default='batch-test-report.tar.gz', type=str,
                        help='The name of the output file. By default "batch-test-report.tar.gz".')
    args = parser.parse_args(raw_args)
    return args
