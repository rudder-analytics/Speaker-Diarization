# Speaker-Diarization

We use Kaldi's Callhome recipe to train the speaker diarization model.

Callhome recipe: https://github.com/kaldi-asr/kaldi/tree/master/egs/callhome_diarization/v2

Speaker diarization Pre-trained model: https://kaldi-asr.org/models/m6

![Screenshot from 2024-03-28 13-26-07](https://github.com/rudder-analytics/Speaker-Diarization/assets/165159432/f29448c5-7212-471f-b647-df8718cda90e)

The Diarization process:

1. Data preparation: Create Kaldi's data files.

In this step, the files like wav.scp (stores wav file name to utterence mapping), utt2spk (stores utterence to speaker mapping), spk2utt (stores speaker to utterence mapping), reco2numspks (stores number of speakers to utterence mapping).

2. Feature extraction.

Next step is to extract MFCC and CMVN features. We used Kaldi’s make_mfcc.sh and prepare_feats.sh scripts for this purpose.

3. Create segments file

Once the features are extracted, next step is to create segments file detailing the start and end times of speech within the input file. The script: compute_vad_decision.sh is used to identify speech segments, crucial for accurate diarization.

4. X-vectors creation

In this step, the xvectors are created. These vectors serve as compact representations of each speaker's characteristics within the audio.

5. PLDA scoring

Once x-vectors are created, we apply Probabilistic Linear Discriminant Analysis (PLDA) to score the similarity between pairs of x-vectors.

6. Clustering and refinement

The next step is to use the PLDA scores as a basis for clustering the x-vector. After the intial clustering, we refine the clustering output. The goal is to ensure that segments from the same speaker are grouped together.

# Requirements

1. Kaldi: https://kaldi-asr.org/doc/install.html
2. Python and subprocess library.

# How to run the code: 

python main.py audio_file.wav

# Sample output:

         rec_id      start seg_duration    spk_id
SPEAKER new_4577 0   0.000   2.625 <NA> <NA> 2 <NA> <NA>
SPEAKER new_4577 0   2.625   0.750 <NA> <NA> 1 <NA> <NA>
SPEAKER new_4577 0   3.375  17.250 <NA> <NA> 2 <NA> <NA>
SPEAKER new_4577 0  20.625   3.000 <NA> <NA> 1 <NA> <NA>
SPEAKER new_4577 0  23.625   4.500 <NA> <NA> 2 <NA> <NA>
SPEAKER new_4577 0  28.125   8.250 <NA> <NA> 1 <NA> <NA>
SPEAKER new_4577 0  36.375  21.750 <NA> <NA> 2 <NA> <NA>
SPEAKER new_4577 0  58.125   3.000 <NA> <NA> 1 <NA> <NA>
SPEAKER new_4577 0  61.125   7.500 <NA> <NA> 2 <NA> <NA>
SPEAKER new_4577 0  68.625   1.500 <NA> <NA> 1 <NA> <NA>
SPEAKER new_4577 0  70.125   5.250 <NA> <NA> 2 <NA> <NA>
SPEAKER new_4577 0  75.375   5.250 <NA> <NA> 1 <NA> <NA>
SPEAKER new_4577 0  80.625  12.750 <NA> <NA> 2 <NA> <NA>
SPEAKER new_4577 0  93.375   1.500 <NA> <NA> 1 <NA> <NA>
SPEAKER new_4577 0  94.875   9.000 <NA> <NA> 2 <NA> <NA>
SPEAKER new_4577 0 103.875  11.250 <NA> <NA> 1 <NA> <NA>
SPEAKER new_4577 0 115.125   1.500 <NA> <NA> 2 <NA> <NA>
SPEAKER new_4577 0 116.625  10.500 <NA> <NA> 1 <NA> <NA>
SPEAKER new_4577 0 127.125  18.000 <NA> <NA> 2 <NA> <NA>
SPEAKER new_4577 0 145.125   3.750 <NA> <NA> 1 <NA> <NA>
SPEAKER new_4577 0 148.875  22.500 <NA> <NA> 2 <NA> <NA>
SPEAKER new_4577 0 171.375   3.750 <NA> <NA> 1 <NA> <NA>
SPEAKER new_4577 0 175.125   5.250 <NA> <NA> 2 <NA> <NA>
SPEAKER new_4577 0 180.375  10.500 <NA> <NA> 1 <NA> <NA>
SPEAKER new_4577 0 190.875   0.750 <NA> <NA> 2 <NA> <NA>
SPEAKER new_4577 0 191.625   3.000 <NA> <NA> 1 <NA> <NA>
SPEAKER new_4577 0 194.625   9.750 <NA> <NA> 2 <NA> <NA>
SPEAKER new_4577 0 204.375   9.750 <NA> <NA> 1 <NA> <NA>
SPEAKER new_4577 0 214.125   1.500 <NA> <NA> 2 <NA> <NA>
SPEAKER new_4577 0 215.625  36.750 <NA> <NA> 1 <NA> <NA>
SPEAKER new_4577 0 252.375   3.750 <NA> <NA> 2 <NA> <NA>
SPEAKER new_4577 0 256.125   2.250 <NA> <NA> 1 <NA> <NA>
SPEAKER new_4577 0 258.375   6.000 <NA> <NA> 2 <NA> <NA>
SPEAKER new_4577 0 264.375   3.000 <NA> <NA> 1 <NA> <NA>
SPEAKER new_4577 0 267.375   2.250 <NA> <NA> 2 <NA> <NA>
SPEAKER new_4577 0 269.625   1.500 <NA> <NA> 1 <NA> <NA>
SPEAKER new_4577 0 271.125  22.500 <NA> <NA> 2 <NA> <NA>
SPEAKER new_4577 0 293.625   4.777 <NA> <NA> 1 <NA> <NA>

References:

1. https://towardsdatascience.com/speaker-diarization-with-kaldi-e30301b05cc8
2. https://github.com/kaldi-asr/kaldi/issues/2523#issuecomment-408935477
