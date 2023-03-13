# Fair_Healthcare_Rationing

### Libraries required
1. Pandas
2. Numpy
3. Pulp

To install the libraries , run `pip install pandas`, `pip install numpy` and `pip install pulp`. 

The data is provided in the `data-anonymized` directory. The names of the hospitals, Zip codes, and hospital center ids have been replaced by dummy names, zipcodes and center ids. This is done to preserve the anonymity of the author's location. The actual dataset will be published with the proceedings version. 

The Online and Offline algorithms are implemented in `solvers/online_maxutility_df.py` and `solvers/offline_maxutility_df.py` respectively.

To run the program, open `main.ipynb` in Jupyter notebook or Google Colab. This file is well documented. The comments are embedded in the file. The outputs will be saved in directory `Sol`

To analyze the solutions, run the file `analysis.ipynb`. This produces all the graphs and bar charts.
