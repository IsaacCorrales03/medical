from database import DataBaseManager

# Inicializar el gestor de base de datos
db = DataBaseManager()
db.create_tables()  # Asegurarse de que las tablas existan

# Lista de medicamentos con sus datos
medicamentos = [
    {
        "nombre": "Aciclovir",
        "uso": "Tratamiento del herpes simple y zóster.",
        "dosis": "400 mg cada 8 horas por 7 días.",
        "efectos_secundarios": "Náuseas, dolor abdominal, erupciones.",
        "recomendaciones_alimenticias": "Puede tomarse con o sin alimentos."
    },
    {
        "nombre": "Albendazol",
        "uso": "Tratamiento antiparasitario.",
        "dosis": "400 mg en dosis única (según parásito).",
        "efectos_secundarios": "Dolor abdominal, náuseas, mareos.",
        "recomendaciones_alimenticias": "Tomar con alimentos grasos para mejor absorción."
    },
    {
        "nombre": "Alendronato",
        "uso": "Osteoporosis.",
        "dosis": "70 mg una vez a la semana.",
        "efectos_secundarios": "Irritación esofágica.",
        "recomendaciones_alimenticias": "Tomar en ayunas, no comer por 30 minutos después."
    },
    {
        "nombre": "Alopurinol",
        "uso": "Gota, ácido úrico elevado.",
        "dosis": "100-300 mg al día.",
        "efectos_secundarios": "Reacciones cutáneas, dolor abdominal.",
        "recomendaciones_alimenticias": "Evitar alcohol, mariscos, carnes rojas."
    },
    {
        "nombre": "Amikacina",
        "uso": "Infecciones graves por bacterias resistentes.",
        "dosis": "Inyectable, según peso y tipo de infección.",
        "efectos_secundarios": "Toxicidad renal y auditiva.",
        "recomendaciones_alimenticias": "Sin interacción directa."
    },
    {
        "nombre": "Amitriptilina",
        "uso": "Depresión, dolor neuropático.",
        "dosis": "10-75 mg antes de dormir.",
        "efectos_secundarios": "Somnolencia, sequedad bucal.",
        "recomendaciones_alimenticias": "Evitar alcohol."
    },
    {
        "nombre": "Amoxicilina con ácido clavulánico",
        "uso": "Infecciones bacterianas resistentes.",
        "dosis": "875 mg/125 mg cada 12 h.",
        "efectos_secundarios": "Diarrea, náuseas.",
        "recomendaciones_alimenticias": "Tomar con alimentos."
    },
    {
        "nombre": "Atorvastatina",
        "uso": "Disminuye el colesterol.",
        "dosis": "10-40 mg al día.",
        "efectos_secundarios": "Dolores musculares, elevación enzimas hepáticas.",
        "recomendaciones_alimenticias": "Evitar jugo de toronja."
    },
    {
        "nombre": "Azitromicina",
        "uso": "Infecciones respiratorias, ITS.",
        "dosis": "500 mg/día por 3 días.",
        "efectos_secundarios": "Diarrea, náuseas.",
        "recomendaciones_alimenticias": "Tomar una hora antes o 2 horas después de alimentos."
    },
    {
        "nombre": "Biperideno",
        "uso": "Parkinsonismo, efectos extrapiramidales.",
        "dosis": "2-6 mg al día.",
        "efectos_secundarios": "Sequedad bucal, visión borrosa.",
        "recomendaciones_alimenticias": "Evitar alcohol."
    },
    {
        "nombre": "Bromazepam",
        "uso": "Ansiedad, insomnio.",
        "dosis": "1.5-3 mg dos veces al día.",
        "efectos_secundarios": "Somnolencia, dependencia.",
        "recomendaciones_alimenticias": "Evitar alcohol."
    },
    {
        "nombre": "Calcio (carbonato)",
        "uso": "Suplemento para huesos, osteoporosis.",
        "dosis": "500-1000 mg de calcio elemental al día.",
        "efectos_secundarios": "Estreñimiento, gases.",
        "recomendaciones_alimenticias": "Tomar con alimentos ricos en vitamina D."
    },
    {
        "nombre": "Carvedilol",
        "uso": "Insuficiencia cardíaca, hipertensión.",
        "dosis": "6.25-25 mg al día.",
        "efectos_secundarios": "Mareos, fatiga.",
        "recomendaciones_alimenticias": "Tomar con alimentos."
    },
    {
        "nombre": "Cefalexina",
        "uso": "Infecciones respiratorias y urinarias.",
        "dosis": "500 mg cada 6-8 horas.",
        "efectos_secundarios": "Náuseas, erupciones.",
        "recomendaciones_alimenticias": "Puede tomarse con alimentos."
    },
    {
        "nombre": "Ceftriaxona",
        "uso": "Infecciones graves, ITS.",
        "dosis": "Inyectable IM o IV según peso.",
        "efectos_secundarios": "Dolor local, diarrea.",
        "recomendaciones_alimenticias": "Sin interacción relevante."
    },
    {
        "nombre": "Cimetidina",
        "uso": "Reflujo, úlceras.",
        "dosis": "300-800 mg por día.",
        "efectos_secundarios": "Mareos, diarrea.",
        "recomendaciones_alimenticias": "Tomar con o sin alimentos."
    },
    {
        "nombre": "Ciprofloxacina (tópico)",
        "uso": "Infecciones oculares y óticas.",
        "dosis": "1-2 gotas cada 4-6 h.",
        "efectos_secundarios": "Ardor leve.",
        "recomendaciones_alimenticias": "No aplica."
    },
    {
        "nombre": "Clopidogrel",
        "uso": "Antiplaquetario, prevención de eventos cardiovasculares.",
        "dosis": "75 mg al día.",
        "efectos_secundarios": "Sangrado, hematomas.",
        "recomendaciones_alimenticias": "Puede tomarse con alimentos."
    },
    {
        "nombre": "Codeína + Paracetamol",
        "uso": "Dolor moderado.",
        "dosis": "1 tableta cada 6 horas.",
        "efectos_secundarios": "Somnolencia, estreñimiento.",
        "recomendaciones_alimenticias": "Evitar alcohol."
    },
    {
        "nombre": "Doxiciclina",
        "uso": "Infecciones respiratorias, ITS.",
        "dosis": "100 mg cada 12 horas.",
        "efectos_secundarios": "Náuseas, fotosensibilidad.",
        "recomendaciones_alimenticias": "Evitar lácteos y suplementos de calcio cerca de la toma."
    }
]

# Añadir cada medicamento a la base de datos
for med in medicamentos:
    db.add_medicamento(
        nombre=med["nombre"],
        uso=med["uso"],
        dosis=med["dosis"],
        efectos_secundarios=med["efectos_secundarios"],
        recomendaciones_alimenticias=med["recomendaciones_alimenticias"]
    )

print("Se han añadido todos los medicamentos correctamente.")

# Cerrar la conexión cuando hayamos terminado
db.close_connection()