import streamlit as st
import random
import time

# Mögliche Noten
NOTEN = [1.0, 1.3, 1.7, 2.0, 2.3, 2.7, 3.0, 3.3, 3.7, 4.0, 5.0]

st.title("Uni-Noten Generator")

anzahl_klausuren = st.number_input("Wie viele Klausuren schreibst du dieses Semester?", min_value=1, max_value=20, value=1)
versuch = st.number_input("Wie vielter Versuch?" ,min_value=1, max_value=3,value=1)

if st.button("Note generieren"):
	# Basis-Durchfallquote
	fail_rate = 0.4
	# Erhöhe Durchfallquote je mehr Klausuren (z.B. +2% pro weitere Klausur)
	fail_rate += (anzahl_klausuren - 1) * 0.02
	fail_rate = min(fail_rate, 0.95)  # Maximal 95% Durchfallquote
	fail_rate -= (versuch - 1) * 0.2
    
	bestanden = random.random() > fail_rate
	time.sleep(1)
	if bestanden:
		
		# Bestehensnoten: 1.0 bis 4.0
		note = random.choice([n for n in NOTEN if n <= 4.0])
		st.success(f"Bestanden: {note}")
	else:
		note = 5.0
		st.error(f"Durchgefallen: {note}")
	
	
