
## Introduction
This repo hosts the scripts used for tracing the evolution history of ruminants TFBS evolution using the birth-death probabilistic model developed by Yokoyama and Zhang et al. 2014 PLoS CB

## Method overview

The pipeline consists of three steps: data preprocessing, predict the branch-of-origin of TFBS in enhancer regions, and generation the final report. Script 'whole_pipeline.py' is the main script of the pipeline. 

1. data preprocessing
    - calcualte the nucleotide background frequency inside the enhancer region
    - use TFM-Pvalue to get the log-likelihood cutoff for motif scanning

2. predict the branch-of-origin
    - scan tfbs in the multiple sequence alignment
    - predict the branch-of-origin of TFBS

3. generation the final report
    - summarize the tfbs branch-of-origin in enhancers
