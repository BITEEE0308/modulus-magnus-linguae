for dir in PENSVM-A_Testing*; do
	for FILE in "$dir"/*; do 
		python get_accuracy.py $FILE
		done
done
