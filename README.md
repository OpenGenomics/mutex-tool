<<<<<<< HEAD
# Mutex Wrapper

CWL wrapper around [Mutex](https://github.com/pathwayanddataanalysis/mutex).
=======
# Mutex

Prerequisites
--
Make sure you have [GitHub](https://git-scm.com/downloads), [Docker](https://docs.docker.com/engine/install), and [cwltool](https://github.com/common-workflow-language/cwltool.git) installed in your system.

Download Sources
--
To pull the source code from repository:
```
git clone https://github.com/OpenGenomics/mutex
```
Prepare JSON File 
--
Go into the project directory and use a text editor to generate the JSON file.

```
cd mutex
cp mutex.template.json mutex.json
vi mutex.json
```
Replace '</full/path/to/data_matrix.txt>' and '</full/path/to/network_file.txt>' with the complete path to the input data and network files, respectively. Save work as 'mutex.json'. Additional optional arguments can be added to this file to override default settings. These settings include:

`max_group_size`                The maximum size of a result mutex group. Integer value. Default is 5.

`first_level_random_iteration`  Number of randomization to estimate null distribution of member p-values in mutex groups. Integer. Default is 10000.

`second_level_random_iteration` Number of runs to estimate the null distribution of final scores. Integer. Default is 100. If FDR control on results is not
                                required and only the ranking of the result groups is sufficient, set this parameter to 0.
                                
`fdr_cutoff`                    Users can select a specific FDR cutoff. When not provided, or when set to a negative value, the FDR cutoff that maximizes the
                                expected value of true positives - false positives is used.
                                
`score_cutoff`

`search_on_signaling_network`   Whether to reduce the search space using the signaling network. 'true' or 'false'. Default is 'true'.

`genes_file`                    This parameter can be used to limit the search to a subset of genes. The file should contain a gene symbol per line.

`gene_ranking_file`

`sample_to_tissue_mapping_file`

`gene_limit`

`minimum_alteration_count_threshold`

Prepare Data Matrix
--
Users first should prepare their dataset of gene alterations as a tab-delimited text file, where the first row contains column headings and first column contains gene symbols.

```
Symbol   Sample1    Sample2   Sample3   ...
Gene1      0           1         0      ...
Gene2      2           0         4      ...
Gene3      0           0         0      ...
  .
  .
```

Use the following encoding for gene alterations.

* `0`: No alteration
* `1`: Mutation
* `2`: Amplification
* `3`: Deletion
* `4`: Mutation and amplification
* `5`: Mutation and deletion

Prepare Network File
--
To customize the signaling network, make a tab-delimited network file containing 3 columns in the following format
`Gene Symbol 1<tab>interaction-type<tab>Gene Symbol 2`

Prepare Parameters File
--
Users should prepare a file named `parameters.txt` and place it in a directory together with the dataset file. The `parameters.txt` file should contain a line that points to the dataset (assume the name of the dataset file is `dataset.txt`) as follows:

`data-file` = `dataset.txt`

`network-file`                    To customize the signaling network, users should have a 3-column, tab-delimited text file as described above. The valid values
                                  for interaction-type are `controls-state-change-of` and `controls-expression-of`. The first type is meant to be used for post-
                                  translational modification relations between proteins, and the second relation is for transcriptional regulations.

The other possible parameters (below) are optional.

`max-group-size`:                 The maximum size of a result mutex group. Integer value. Default is `5`.

`first-level-random-iteration`:   Number of randomization to estimate null distribution of member p-values in mutex groups. Integer. Default is `10000`.

`second-level-random-iteration`:  Number of runs to estimate the null distribution of final scores. Integer. Default is `0`, meaning that estimation is not
                                  required.

`fdr-cutoff`:                     Users can select a specific FDR cutoff. Only applicable when there is an estimation of null distribution of scores, i.e., when
                                  `second-level-random-teration` is greater than `0`. When not provided, or when set to a negative value, the FDR cutoff that
                                  maximizes the expected value of true positives - false positives is used.

`search-on-signaling-network`:    Whether to reduce the search space using the signaling network. true or false. Default is true. If this is set to true, but no
                                  network file is provided using the "network-file" argument, then a default signaling network that is composed from Pathway
                                  Commons, SPIKE and SignaLink databases is used.

`genes-file`:                     This parameter can be used to limit the search to a subset of genes. The file should contain a gene symbol per line.



Run Mutex with the following command.
--

`cwltool mutex.cwl mutex.jar`

Description of output files and their visualization
--
After a run, the result files are generated into the working directory.

`ranked-groups.txt`:    Provides a ranked list of result groups, where the first column contains the score of the group. Use a text or spreadsheet editor to
                        visualize this file.

`fdr-guide.txt`:        Provides the mapping between a score cutoff, and the corresponding expected false discovery rates. Use a text or spreadsheet editor to
                        visualize this file.

`result-groups.cus`:    Provides a graph that shows result groups, their relations between, and one of their common targets, if a common target is not already in
                        the result group. To visualize this file open [ChiBE](https://github.com/PathwayCommons/chibe), do "SIF -> Load SIF File", change the file
                        filter from `sif` to `cus` in the dialog, and select this file.

`merged-network.sif`:   Provides the minimal network that is produced using the result groups. Group boundaries are not displayed in this graph. Non-member common
                        targets are displayed in a pale color. To visualize this file open [ChiBE](https://github.com/PathwayCommons/chibe), do "SIF -> Load SIF 
                        File", and select this file. Note that ChiBE also uses the file `merged-network.format`, so if you move the sif file, do not forget to 
                        move the format file along with it.

Citing Mutex
--
Please refer to below paper.

Babur, Özgün, et al. "[Systematic identification of cancer driving signaling pathways based on mutual exclusivity of genomic alterations](https://genomebiology.biomedcentral.com/articles/10.1186/s13059-015-0612-6)." *Genome biology* 16.1 (2015): 45.
>>>>>>> 32f26c71f05023591ac527d3024bd5d465c9fc20
