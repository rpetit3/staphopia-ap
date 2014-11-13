#! /usr/bin/env python
""" Ruffus wrappers for assembly related tasks. """
import os

from staphopia.config import BIN
from staphopia.tasks import shared


def kmergenie(fastq, output_file, num_cpu):
    """ Predict the optimal value for K. """
    output_prefix = os.path.splitext(output_file)[0]
    kmergenie = shared.run_command(
        [BIN['kmergenie'], fastq, '-t', num_cpu, '-o', output_prefix],
        stdout=output_prefix + '.out',
        stderr=output_prefix + '.err'
    )

    # Clean up histograms
    shared.find_and_remove_files(os.path.dirname(output_file), '*histo*')
    return kmergenie


def sort_kmergenie(kmergenie_dat, output_file):
    """ Sort kmergenie output, retain top three values. """
    sort = shared.pipe_command(
        ['sort', '-k2,2rn', kmergenie_dat],
        ['head', '-n', '3'],
        stdout=output_file
    )
    return sort


def velvet(input_files, output_file, is_paired):
    """ Assemble using Velvet. """
    log_dir = output_file.replace('completed', 'logs')
    completed = []
    paired = '-shortPaired' if is_paired else '-short'
    fastq, kmergenie = input_files
    fh = open(kmergenie, 'r')
    for line in fh:
        k, total, cov_cutoff = line.rstrip().split(' ')
        output_dir = output_file.replace('completed', k)

        # Velveth
        shared.run_command(
            [BIN['velveth'], output_dir, k, paired, '-fastq.gz', fastq],
            stdout='{0}/{1}_velveth.out'.format(log_dir, k),
            stderr='{0}/{1}_velveth.err'.format(log_dir, k)
        )
        # Velvetg
        shared.run_command(
            [BIN['velvetg'], output_dir, '-cov_cutoff', cov_cutoff,
             '-min_contig_lgth', '100', '-very_clean', 'yes'],
            stdout='{0}/{1}_velvetg.out'.format(log_dir, k),
            stderr='{0}/{1}_velvetg.err'.format(log_dir, k)
        )

        completed.append(shared.try_to_complete_task(
            output_dir + '/contigs.fa',
            output_dir + '/completed'
        ))
    fh.close()

    if all(i for i in completed):
        if shared.complete_task(output_file):
            return True
        else:
            raise Exception("Unable to complete Velvet assembly.")
    else:
        raise Exception("One or more Velvet assemblies did not complete")


def cleanup_velvet(input_file, output_file):
    """ Clean up Velvet intermediate files. """
    base_dir = input_file.replace('completed', '')
    shared.find_and_remove_files(base_dir, '*PreGraph')
    velvet_dirs = shared.find_dirs(base_dir, "*", '1', '1')
    velvet_tar_gz = input_file.replace('completed', 'velvet.tar.gz')
    if shared.compress_and_remove(velvet_tar_gz, velvet_dirs):
        if shared.try_to_complete_task(velvet_tar_gz, output_file):
            return True
        else:
            raise Exception("Unable to complete Velvet clean up.")
    else:
        raise Exception("Cannot compress Velet output, please check.")


def spades(fastq, output_file, num_cpu):
    """ Assemble using Spades. """
    # Spades 3.1.1 hangs during the mismatch correction step until fixed treat
    # all reads as single end. I know this not optimal, but until something
    # better comes up we will go with it.
    #paired = '--12' if config['is_paired'] else '-s'
    paired = '-s'
    stdout, stderr = shared.run_command(['find', '-name', 'contigs.fa'])

    velvet_dirs = []
    for line in stdout.split('\n'):
        if line:
            velvet_dirs.append('--trusted-contigs')
            velvet_dirs.append(line)

    output_dir = output_file.replace('completed', '')
    shared.run_command(
        [BIN['spades'], paired, fastq, '--careful', '-t', num_cpu,
         '--only-assembler', '-o', output_dir] + velvet_dirs,
        stderr='{0}spades.err'.format(output_dir)
    )

    if shared.try_to_complete_task(output_dir + 'contigs.fasta', output_file):
        return True
    else:
        raise Exception("Spades assembly did not complete.")


def move_spades(spades_dir, contigs, scaffolds):
    """ Move final assembly to project root. """
    gzip_contigs = shared.run_command(
        ['gzip', '-c', spades_dir + '/contigs.fasta'],
        stdout=contigs
    )

    gzip_scaffolds = shared.run_command(
        ['gzip', '-c', spades_dir + '/scaffolds.fasta'],
        stdout=scaffolds
    )
    return [gzip_contigs, gzip_scaffolds]


def cleanup_spades(input_file, output_file):
    """ Cleanup the Spades directory. """
    base_dir = input_file.replace('completed', '')
    remove_these = ['*final_contigs*', '*before_rr*', '*pe_before_traversal*',
                    '*simplified_contigs*']
    for name in remove_these:
        shared.find_and_remove_files(base_dir, name)

    shared.find_and_remove_files(base_dir, "*scaffolds*", min_depth='2')

    spades_files = shared.find_files(base_dir, '*', '1', '1')
    spades_tar_gz = input_file.replace('completed', 'spades.tar.gz')
    if shared.compress_and_remove(spades_tar_gz, spades_files):
        if shared.try_to_complete_task(spades_tar_gz, output_file):
            shared.complete_task(input_file)
            return True
        else:
            raise Exception("Unable to complete Spades clean up.")
    else:
        raise Exception("Cannot compress spades output, please check.")


def makeblastdb(input_file, output_file):
    """ Make a blast database of an assembly. """
    temp_file = input_file + '.temp'
    shared.run_command(['gunzip', '-c', input_file], stdout=temp_file)

    output_prefix = output_file.replace('completed', 'assembly')
    shared.run_command(
        [BIN['makeblastdb'], '-in', temp_file, '-dbtype',
         'nucl', '-out', output_prefix],
        stdout=output_prefix + '.out',
        stderr=output_prefix + '.err'
    )

    shared.run_command(['rm', temp_file])

    if shared.try_to_complete_task(output_prefix + '.nin', output_file):
        return True
    else:
        raise Exception("makeblastdb did not complete successfully.")


def assembly_stats(input_file, output_file):
    """ Determine assembly statistics. """
    stats_file = input_file.replace('fasta.gz', 'stats')
    shared.run_command(
        [BIN['assemblathon_stats'], '-genome_size', '2800000', '-csv',
         input_file]
    )

    if shared.try_to_complete_task(stats_file, output_file):
        return True
    else:
        raise Exception("Assembly stats did not complete successfully.")
