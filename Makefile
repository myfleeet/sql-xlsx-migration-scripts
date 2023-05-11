# Execute commands

main:
	python3 main.py


custom-vh:
	python3 custom_vehicle_history.py

zip:
	cd out && zip -r ./migration_`date +%Y-%m-%d_%H-%M-%S`.zip .