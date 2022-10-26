Measure baseline vs PATCH performance on EC2 across regions.


# Usage

    pulumi stack new    meta-benchmark
    pulumi stack select meta-benchmark
    ./make-keys.sh
    ./configure-keys.sh
    pulumi up --yes
    # grab several coffees
    ./ssh-grab-results.sh virginia
    ./ssh-grab-results.sh oregon
    ./ssh-grab-results.sh mumbai
    ./ssh-grab-results.sh frankfurt
    ./ssh-grab-results.sh tokyo
    python analyze.py > results.csv


# Configuration scrpits

    bench.sh           # confgures parameter grid for benchmarks to run
    make-bundle.sh     # confgures what code goes into the zip onto EC2 machines
    make-keys.sh       # makes a new SSH key pair
    configure-keys.sh  # registers keys to `pulumi config`


# Running

Regions: oregon, virginia, mumbai, tokyo, frankfurt.

    ssh-grab-results.sh <region>          # rsync results EC2 -> ./data
    ssh-there           <region>          # open an ssh shell to EC2
    scp-there.sh        <region> file.txt # copy file to EC2


# Analysis

    python analyze.py  # convert logs from data/ into CSV form for analysis
