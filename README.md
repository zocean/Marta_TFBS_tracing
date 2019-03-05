
## Introduction
This repo hosts the scripts used for tracing the evolution history of ruminants TFBS evolution using the birth-death probabilistic model developed by Yokoyama and Zhang et al. 2014 PLoS CB

## Method overview

The pipeline consists of three steps: data preprocessing, predict the branch-of-origin of TFBS in enhancer regions, and generation the final report. Script 'whole_pipeline.py' is the main script of the pipeline. 

1. data preprocessing (run_prep.sh)
    - calcualte the nucleotide background frequency inside the enhancer region
    - use TFM-Pvalue to get the log-likelihood cutoff for motif scanning

2. predict the branch-of-origin
    - scan tfbs in the multiple sequence alignment (e.g., run_evo/run_evo_scan_cattle.sh)
    - predict the branch-of-origin of TFBS (e.g run_evo/run_evo_predict_cattle.sh)

3. generation the final report
    - summarize the tfbs branch-of-origin in enhancers (e.g., run_evo/run_evo_summary_merge.sh)

## Credits
This pipeline was developed by Ma group @ Carnegie Mellon University. Part of the script is from ANTICE, a softwaare being developed for predicting the evolution of lineage-specific TFBS. This pipeline and ANTICE are implemented by Yang Zhang.

## License
This software is under MIT license.

## Contact
yangz6 at cs.cmu.edu
