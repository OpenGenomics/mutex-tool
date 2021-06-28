cwlVersion: v1.0
class: CommandLineTool
label: mutex
    
requirements:
  DockerRequirement:    
    dockerPull: "opengenomics/mutex:v2.0.2"

baseCommand: ["mutex.py"]

inputs:
  data_file:
    type: File
    doc: Name of the data file. Mandatory.
    inputBinding:
      prefix: --data-file

  network_file:
    type: File
    doc: To customize the signaling network, users can use this parameter. The tab-delimited network file should contain 3 columns (Gene Symbol 1, interaction-type, Gene Symbol 2). Mandatory.
    inputBinding:
      prefix: --network-file

  max_group_size:
    type: int
    default: 5
    doc: The maximum size of a result mutex group. Integer value. Default is 5.
    inputBinding:
      prefix: --max-group-size

  first_level_random_iteration:
    type: int
    default: 10000
    doc: Number of randomization to estimate null distribution of member p-values in mutex groups. Integer. Default is 10000.
    inputBinding:
      prefix: --first-level-random-iteration

  second_level_random_iteration:
    type: int
    default: 100
    doc: Number of runs to estimate the null distribution of final scores. Integer. Default is 100. If FDR control on results is not required and only the ranking of the result groups is sufficient, set this parameter to 0.
    inputBinding:
      prefix: --second-level-random-iteration

  fdr_cutoff:
    type: float?
    doc: Users can select a specific FDR cutoff. When not provided, or when set to a negative value, the FDR cutoff that maximizes the expected value of true positives - false positives is used.
    inputBinding:
      prefix: --fdr-cutoff

  score_cutoff:
    type: float?
    inputBinding:
      prefix: --score-cutoff

  search_on_signaling_network:
    type: string
    default: "true"
    doc: Whether to reduce the search space using the signaling network. "true" or "false". Default is "true".
    inputBinding:
      prefix: --search-on-signaling-network

  genes_file:
    type: File?
    doc: This parameter can be used to limit the search to a subset of genes. The file should contain a gene symbol per line.
    inputBinding:
      prefix: --genes-file

  gene_ranking_file:
    type: File?
    inputBinding:
      prefix: --gene-ranking-file

  sample_to_tissue_mapping_file:
    type: File?
    inputBinding:
      prefix: --sample-to-tissue-mapping-file

  gene_limit:
    type: int?
    inputBinding:
      prefix: --gene-limit

  minimum_alteration_count_threshold:
    type: int?
    inputBinding:
      prefix: --minimum-alteration-count-threshold
  random:
    type: boolean
    default: false
    inputBinding:
      prefix: --random

outputs:
  ranked_groups:
    type: File
    outputBinding:
      glob: ./*/ranked-groups.txt

  fdr_guide:
    type: File
    outputBinding:
      glob: ./*/fdr-guide.txt

  result_groups:
    type: File
    outputBinding:
      glob: ./*/result-groups.cus

  merged_network:
    type: File
    outputBinding:
      glob: ./*/merged-network.sif

