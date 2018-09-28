# Mutex

Prerequisites
--
To get a copy of the project and build it, first make sure you have [Git](https://git-scm.com/downloads), [Maven](https://maven.apache.org/download.cgi) and [JDK8](http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html) in your system.

Download sources
--
To pull the source code from repository:
```
git clone https://github.com/PathwayAndDataAbalysis/mutex
```
You can customize Mutex by editing sources with your favorite Java IDE, such as IntelliJ IDEA or Eclipse. If you don't want to use an IDE, follow the steps below.

Compile
--
Go into the project directory, and tell maven to compile the project.

```
cd mutex
mvn clean compile
```
Prepare Jar
--
```
mvn assembly:single
```
This will create mutex.jar under the target folder in the project directory.

<!--
Add PC.sif
--
For some reason tt looks like Google is limiting access to large files in googlecode repositories. Please download this file from http://cbio.mskcc.org/~ozgun/PC.sif.gz, and extract the file PC.sif into the working directory (same folder of `mutex.jar`). This file will be replaced with a directory named PC once the code is run.
-->

Run Mutex
--
To run Mutex, users first should prepare their dataset of gene alterations as a tab-delimited text file, where the first row contains column headings and first column contains gene symbols.

```
Symbol   Sample1    Sample2   Sample3   ...
Gene1      0           1         0      ...
Gene2      2           0         4      ...
Gene3      0           0         0      ...
  .
  .
```
Use following encoding for gene alterations.
--

* `0`: No alteration
* `1`: Mutation
* `2`: Amplification
* `3`: Deletion
* `4`: Mutation and amplification
* `5`: Mutation and deletion

Then users should prepare a file named `parameters.txt` and place it in a directory together with the dataset file. The `parameters.txt` file should contain a line that points to the dataset (assume the name of the dataset file is `dataset.txt`).

`data-file` = `dataset.txt`
The other possible parameters (below) are optional.

`max-group-size`: The maximum size of a result mutex group. Integer value. Default is `5`.

`first-level-random-iteration`: Number of randomization to estimate null distribution of member p-values in mutex groups. Integer. Default is `10000`.

`second-level-random-iteration`: Number of runs to estimate the null distribution of final scores. Integer. Default is `0`, meaning that estimation is not required.

`fdr-cutoff`: Users can select a specific FDR cutoff. Only applicable when there is an estimation of null distribution of scores, i.e., when `second-level-random-teration` is greater than `0`. When not provided, or when set to a negative value, the FDR cutoff that maximizes the expected value of true positives - false positives is used.

`search-on-signaling-network`: Whether to reduce the search space using the signaling network. true or false. Default is true. If this is set to true, but no network file is provided using the "network-file" argument, then a default signaling network that is composed from Pathway Commons, SPIKE and SignaLink databases is used.

`genes-file`: This parameter can be used to limit the search to a subset of genes. The file should contain a gene symbol per line.

`network-file`: To customize the signaling network, users can use this parameter. The network file should be a tab-delimited text file with 3 columns (`Gene Symbol 1<tab>interaction-type<tab>Gene Symbol 2`). The valid values for interaction-type are `controls-state-change-of` and `controls-expression-of`. The first type is meant to be used for post-translational modification relations between proteins, and the second relation is for transcriptional regulations.

Run Mutex with the following command.
--

`java -jar target/mutex.jar path/to/directory`
When the dataset is large, and FDR control is required, the execution time can be long. To accelerate the execution, second-level randomizations can be parallelized. The below code takes a run on the randomized network, and records the results in a file under the directory "randscores".

`java -jar target/mutex.jar path/to/directory random`
When a parameter in the analysis is changed, the cached data may become invalid, and the data-cache file and the randscores directory should be deleted before a new execution. Users do not need to clear the cached data if they only change fdr-cutoff or second-level-random-iteration.

Description of output files and their visualization
--
After a run, the result files are generated into the provided data directory.

`ranked-groups.txt`: Provides a ranked list of result groups, where the first column contains the score of the group. Use a text or spreadsheet editor to visualize this file.

`fdr-guide.txt`: Provides the mapping between a score cutoff, and the corresponding expected false discovery rates. Use a text or spreadsheet editor to visualize this file.

`result-groups.cus`: Provides a graph that shows result groups, their relations between, and one of their common targets, if a common target is not already in the result group. To visualize this file open [ChiBE](https://github.com/PathwayCommons/chibe), do "SIF -> Load SIF File", change the file filter from `sif` to `cus` in the dialog, and select this file.

`merged-network.sif`: Provides the minimal network that is produced using the result groups. Group boundaries are not displayed in this graph. Non-member common targets are displayed in a pale color. To visualize this file open [ChiBE](https://github.com/PathwayCommons/chibe), do "SIF -> Load SIF File", and select this file. Note that ChiBE also uses the file `merged-network.format`, so if you move the sif file, do not forget to move the format file along with it.

Citing Mutex
--
Please refer to below paper.

Babur, Özgün, et al. "[Systematic identification of cancer driving signaling pathways based on mutual exclusivity of genomic alterations](https://genomebiology.biomedcentral.com/articles/10.1186/s13059-015-0612-6)." *Genome biology* 16.1 (2015): 45.
