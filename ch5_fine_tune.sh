for dir in PENSVM-A_Testing_*; do
	for FILE in "$dir"/*; do 
		python get_accuracy.py $FILE
		done
done
