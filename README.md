# AMP-finder
### Determines the likelihood of a protein having antimicrobial properties. [AMP-finder.streamlit.app](https://amp-finder.streamlit.app/)

The program identifies the likelihood that a given amino acid sequence will have antimicrobial activity. The program uses 

1. Random Forrest classifier (implimented)
2. Gradient boost classifier (implimented)
3. Deep Neural network (not implimented)
4. Convolutional neural network (not implimented)
5. LSTM neural network (not implimented)

to make its predictions. The probabilities for each model is output by the program.

The RF, GB and DNN models use the amino acid composition as well as computed CTD features to make their predictions. More information on the computation of CTD features as well as pseudo amino acid composition can be foud [here](PROFEAT.2.descriptors.pdf). The computed AAC and CTD values can also be downloaded by the program. 

## How to use:
upload a .fasta file with the amino acid sequences you would like to check. The sequences must be combinations of the 20 common amino acids as any other amino acids will throw an error.

download the output as a .txt file. 

## About the models

All models are trained on the same data containing [active](AMP_sequence/AMP_sequence.fasta) and [inactive](nonAMP_sequence/nonAMP_sequence.fasta) peptides.

The RF models were made using scikit-learn with n=500 estimators in each model. 

The RF model places ![image](https://github.com/mornevwyk/AMP-finder/assets/117268241/482a485d-d433-4dc5-9d8d-0c7fd79af3ff)
