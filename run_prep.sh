# split multiz into separata maf
python /usr0/home/yangz6/bighive/TFBS_Marta/code/split_maf.py --maf /usr0/home/yangz6/bighive/TFBS_Marta/multiz/boreoMafChinese_May2015.maf --folder /usr0/home/yangz6/bighive/TFBS_Marta/multiz

# prepare nucleotide freq
python /usr0/home/yangz6/bighive/TFBS_Marta/code/get_bg.py --input /usr0/home/yangz6/bighive/TFBS_Marta/data/region/NuclFreq_cattleEnhanc.txt --output /usr0/home/yangz6/bighive/TFBS_Marta/data/region/cattleEnhanc.bg
python /usr0/home/yangz6/bighive/TFBS_Marta/code/get_bg.py --input /usr0/home/yangz6/bighive/TFBS_Marta/data/region/NuclFreq_cetartioEnhanc.txt --output /usr0/home/yangz6/bighive/TFBS_Marta/data/region/cetartioEnhanc.bg
python /usr0/home/yangz6/bighive/TFBS_Marta/code/get_bg.py --input /usr0/home/yangz6/bighive/TFBS_Marta/data/region/NuclFreq_mammalEnhanc.txt --output /usr0/home/yangz6/bighive/TFBS_Marta/data/region/mammalEnhanc.bg

# calculate motif pwm cutoff
python /usr0/home/yangz6/bighive/TFBS_Marta/code/get_pwm_cutoff.py --pwm /usr0/home/yangz6/bighive/TFBS_Marta/data/motif/pwm_vertebrates14March2017.txt --pwm_format jaspar --pvalue 0.0001 --background /usr0/home/yangz6/bighive/TFBS_Marta/data/region/cattleEnhanc.bg --output /usr0/home/yangz6/bighive/TFBS_Marta/result/cattle/pwm_cutoff.txt >/usr0/home/yangz6/bighive/TFBS_Marta/result/cattle/pwm_cutoff.log 2>&1 &
python /usr0/home/yangz6/bighive/TFBS_Marta/code/get_pwm_cutoff.py --pwm /usr0/home/yangz6/bighive/TFBS_Marta/data/motif/pwm_vertebrates14March2017.txt --pwm_format jaspar --pvalue 0.0001 --background /usr0/home/yangz6/bighive/TFBS_Marta/data/region/cetartioEnhanc.bg --output /usr0/home/yangz6/bighive/TFBS_Marta/result/cetartio/pwm_cutoff.txt >/usr0/home/yangz6/bighive/TFBS_Marta/result/cetartio/pwm_cutoff.log 2>&1 &
python /usr0/home/yangz6/bighive/TFBS_Marta/code/get_pwm_cutoff.py --pwm /usr0/home/yangz6/bighive/TFBS_Marta/data/motif/pwm_vertebrates14March2017.txt --pwm_format jaspar --pvalue 0.0001 --background /usr0/home/yangz6/bighive/TFBS_Marta/data/region/mammalEnhanc.bg --output /usr0/home/yangz6/bighive/TFBS_Marta/result/mammal/pwm_cutoff.txt >/usr0/home/yangz6/bighive/TFBS_Marta/result/mammal/pwm_cutoff.log 2>&1 &

