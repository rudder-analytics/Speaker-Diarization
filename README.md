# Speaker-Diarization

We use Kaldi's Callhome recipe to train the speaker diarization model.

Callhome recipe: https://github.com/kaldi-asr/kaldi/tree/master/egs/callhome_diarization/v2

Speaker diarization Pre-trained model: https://kaldi-asr.org/models/m6

![Screenshot from 2024-03-28 13-26-07](https://github.com/rudder-analytics/Speaker-Diarization/assets/165159432/f29448c5-7212-471f-b647-df8718cda90e)

The Diarization process:

1. Data preparation: Create Kaldi's data files.

In this step, we create files like wav.scp (stores wav file name to utterence mapping), utt2spk (stores utterence to speaker mapping), spk2utt (stores speaker to utterence mapping), reco2numspks (stores number of speakers to utterence mapping).

2. Feature extraction.
