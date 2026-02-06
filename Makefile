all: order.pdb

: compare_sequence.py
	echo "compare_sequence.py"
	
order.pdb: input/initial.pdb order_chain.py
	echo "order.pdb"

.PHONY all