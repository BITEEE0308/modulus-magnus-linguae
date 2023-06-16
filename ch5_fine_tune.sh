for dir in PENSVM-A_Testing_Ch5*; do
	for FILE in "$dir"/*; do 
		python get_accuracy.py $FILE
		done
done
