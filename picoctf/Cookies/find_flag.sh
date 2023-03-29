for i in $(seq 1 28); do if ! (cat req$i | grep -Fq special); then
	echo "The flag is in req$i!"; cat req$i | grep pico; fi
done;

#for i in $(seq 1 29); do if (cat req$i | grep -Fq "special"); then; else echo "The word 'special' wasn't found in req$i"; fi; done;
