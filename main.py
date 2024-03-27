#import reset_directory
import subprocess as s
import os
import sys
import glob
import time

# Function that prints the output.
def read_output():
    f = open('/home/kaldi/egs/spkdirzt/0006_callhome_diarization_v2_1a/exp/xvector_nnet_1a/xvectors_test/plda_scores_num_speakers/rttm', 'r')
    content = f.read()
    print(content)
    f.close()

# Remove previous files.   
def preprocessing():
    bash_out = s.run("rm -r data", text=True, shell=True)
    bash_out = s.run("mkdir data",  text=True, shell=True)
    bash_out = s.run("mkdir data/test",  text=True, shell=True)

# Extract the file name from the args.   
if len(sys.argv) == 1:
    try:
        FILE_NAME_WAV = glob.glob("*.wav")[0]
    except:
        raise ValueError("No .wav file in the root directory")
elif len(sys.argv) == 2:
    FILE_NAME_WAV = list(sys.argv)[1]
    if FILE_NAME_WAV[-4:] != ".wav":
        raise ValueError("Provided filename does not end in '.wav'")
else:
    raise ValueError("Too many arguments provided. Aborting")

FILE_NAME = FILE_NAME_WAV[:-4]

ORIGINAL_DIRECTORY = os.getcwd()

# nnet_dir stores the model.
nnet_dir="0006_callhome_diarization_v2_1a/exp/xvector_nnet_1a/"

# Enter number of speakers
print("Enter number of speakers: ")
nj = input()
start_time = time.time()

# Call the preprocessing function.
preprocessing()
os.chdir("./data/test")

SEG_NAME = FILE_NAME + "_SEG"

# Create data files required by Kaldi.

# Stores utterence to speaker mapping.
with open("utt2spk", "w") as f:
    f.write("{0} {1}".format(SEG_NAME, FILE_NAME))
    f.close()

# Stores speaker to utterence mapping.
with open("spk2utt", "w") as f:
    f.write("{0} {1}".format(FILE_NAME, SEG_NAME))
    f.close()

wav_path = os.getcwd() + "/" + FILE_NAME_WAV

# Stores the file path and speaker mapping.
with open("wav.scp", "w") as f:
    f.write("{0} {1}".format(FILE_NAME, wav_path))
    f.close()
    
# Stores the file name and number of speakers mapping.
with open("reco2num_spk", "w") as f:
    f.write("{0} {1}".format(FILE_NAME, nj))
    f.write("\n")
    f.close()
        

os.chdir(ORIGINAL_DIRECTORY)

# Extract Sample rate

bash_out = s.run("soxi {0}".format(FILE_NAME_WAV), stdout=s.PIPE, text=True, shell=True)
cleaned_list = bash_out.stdout.replace(" ","").split('\n')
sample_rate = [x for x in cleaned_list if x.startswith('SampleRate:')]
sample_rate = sample_rate[0].split(":")[1]


print(sample_rate)

# Read mfcc configuration file.
with open("./conf/mfcc_hires.conf", "r") as mfcc:
    # Read lines of file
    lines = mfcc.readlines()



# Set the sample frequency to the frequency of the file in mfcc configuration.    
# Identify the line that corresponds to setting the sample frequency and isolate it
line_idx = [lines.index(l) for l in lines if l.startswith('--sample-frequency=')]
line = lines[line_idx[0]]

# Reformat the line to use the sample rate of the .wav file
line = line.split("=")
line[1] = sample_rate + line[1][line[1].index(" #"):]
line = "=".join(line)

# Replace the relevant line in `lines` and write to file
lines[line_idx[0]] = line
final_str = "".join(lines)
with open("./conf/mfcc_hires.conf", "w") as mfcc:
    mfcc.write(final_str)

bash_out = s.run("cp {0} data/test/{0}".format(FILE_NAME_WAV), stdout=s.PIPE, text=True, shell=True)


bash_out = s.run("soxi -D " + wav_path, stdout=s.PIPE, text=True, shell=True)
wav_len = bash_out.stdout
print(wav_len)

# Create segments file.
with open("data/test/segments", "w") as f:
    f.write("{0} {1} 0.00 {2}".format(SEG_NAME, FILE_NAME,wav_len))
    f.close()


# main function
with open("main_log.txt", "w") as f:
    # Copy wav file into data folder
   # Create segemnted data/test dir
    bash_out = s.run("utils/fix_data_dir.sh data/test", stdout=f, text=True, shell=True)

    # EXTRACT FEATURES
    # Make MFCC features using configuration file provided
    bash_out = s.run("steps/make_mfcc.sh --nj 1 --mfcc-config conf/mfcc.conf --write-utt2num-frames true data/test exp/make_mfcc data/test_cmn", stdout=f, text=True, shell=True)


    bash_out = s.run("utils/fix_data_dir.sh data/test", stdout=f, text=True, shell=True)
                     
    # Extract and prepare features.
    bash_out = s.run("local/nnet3/xvector/prepare_feats.sh --nj 1 data/test data/test_cmn exp/test_cmn" , stdout=f, text=True, shell=True)
    
    bash_out = s.run("cp data/test/segments data/test_cmn", stdout=f, text=True, shell=True)  

    bash_out = s.run("utils/fix_data_dir.sh data/test_cmn", stdout=f, text=True, shell=True)

   
    # Create x-vectors of audio file.
    command = "diarization/nnet3/xvector/extract_xvectors.sh --nj 1 --window 1.5 --period 0.75 --apply-cmn false --min-segment 0.5 "+ nnet_dir+  " data/test_cmn "+nnet_dir+"xvectors_test" 
    bash_out = s.run(command, stdout=f, text=True, shell=True)

    #Score X-Vectors with PLDA
    command = "diarization/nnet3/xvector/score_plda.sh --target-energy 0.9 --nj 1 0006_callhome_diarization_v2_1a/exp/xvector_nnet_1a/xvectors_callhome2/ "+nnet_dir+"xvectors_test " +nnet_dir+"xvectors_test/plda_scores"
    bash_out = s.run(command, stdout=f, text=True, shell=True)

    threshold = "0.5"

    # Cluster the vectors according to the similarity.
    command = "diarization/cluster.sh --nj 1 --reco2num-spk data/test/reco2num_spk "+nnet_dir+"xvectors_test/plda_scores "+nnet_dir+"/xvectors_test/plda_scores_num_speakers"

    bash_out = s.run(command, stdout=f, text=True, shell=True)

    read_output()

print("Total time: ", time.time() - start_time)


