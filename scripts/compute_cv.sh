# python /home/praharsh/Dropbox/research/nested-sampling-bryce-alex/nested_sampling/examples/harmonic/run_hparticle.py &
# script to reproduce nested sampling results
cd /home/praharsh//Dropbox/research/nested-sampling-bryce-alex/nested_sampling/examples/harmonic/
# 

nreplicas=10
python run_hparticle.py --nreplicas ${nreplicas} --ndof 3 --nproc 1 --nsteps 1000 --etol=1e-1 --stepsize=20 --stepsize=20
cd ../../scripts
# keep ndof to be 0 always, and check whether you're getting a constant line at 1.5. The reason to do this is because it's annoying that
# the C_V offset due to ndof is also 1.5 and it's confusing whether you're getting the offset or the actual value
python compute_cv.py ${nreplicas} /home/praharsh/Dropbox/research/nested-sampling-bryce-alex/nested_sampling/examples/harmonic/run_hparticle.energies /home/praharsh/Dropbox/research/nested-sampling-bryce-alex/nested_sampling/examples/harmonic/run_hparticle.replicas_final --Tmin 0.01 --Tmax 1 -P 1 --ndof 0