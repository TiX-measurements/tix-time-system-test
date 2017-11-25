import tarfile
import tempfile
from os import path, listdir, makedirs, unlink
from os.path import join

import logging
from results_shaper import parse_args
from shutil import copy

logger = logging.getLogger(__name__)
temp_dir = None


def reshape_results(working_directory, batch_size):
    reports = list(filter(lambda file_name: file_name.endswith('.json'), sorted(listdir(working_directory))))
    previous_batch_reports = list()
    index = 0
    while index < len(reports):
        new_reports_qty = batch_size - len(previous_batch_reports)
        batch_reports = previous_batch_reports + reports[index: index + new_reports_qty]
        # reports names are of the kind `tix-report-xxxxxx.json` where xxxxxx is a UNIX Epoch
        batch_dir_name = batch_reports[0].split('.')[0].split('-')[-1]
        batch_dir_path = join(working_directory, batch_dir_name)
        makedirs(batch_dir_path)
        for report in batch_reports:
            src = join(working_directory, report)
            dst = batch_dir_path
            copy(src, dst)
        previous_batch_reports = batch_reports[(len(batch_reports) // 2):]
        index += new_reports_qty
    for report in reports:
        unlink(join(working_directory, report))


if __name__ == "__main__":
    args = parse_args()
    logger.debug(args)
    # abs_file_path = path.abspath(args.file_path)
    # abs_output_path = path.abspath(args.output)
    abs_file_path = args.file_path
    abs_output_path = args.output
    if args.is_tar or args.is_gz:
        logger.debug("Is a TAR file")
        if args.is_gz:
            logger.debug("Is a GZipped TAR file")
            open_mode = 'r:gz'
        else:
            open_mode = 'r'
        tar = tarfile.open(abs_file_path, mode=open_mode)
        temp_dir = tempfile.TemporaryDirectory()
        logger.info("Temporary directory {} created.".format(temp_dir.name))
        tar.extractall(path=temp_dir.name)
        working_directory = path.abspath(temp_dir.name)
        tar.close()
    else:
        working_directory = abs_file_path
    reshape_results(working_directory, args.batch_size)
    logger.info("Creating output TAR.")
    tar = tarfile.open(abs_output_path, mode='w:gz')
    tar.add(working_directory, arcname='')
    tar.close()
    logger.info("Output TAR successfully created.")
    if temp_dir is not None:
        temp_dir.cleanup()
        logger.info("Temporary directory destroyed.")
