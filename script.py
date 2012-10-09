import csv

arquivo = open('ReceitasCandidatos-clean.csv', 'r')
arquivo = csv.DictReader(arquivo)

final = {}

for a in arquivo:
    cod = a['Municipio']+'-'+a['UF']
    partido = a['Sigla  Partido']
    receita = float(a['Valor receita'].replace(',','.'))
    if final.has_key(cod):
        if final[cod].has_key(partido):
            final[cod][partido] += receita
        else:
            final[cod][partido] = receita
    else:
        final[cod] = { partido : receita }

champion = {}
for record in final:
    if not champion.has_key(record):
        champion[record] = { 'partido' : None, 'valor' : 0 }
        
    for p in final[record]:
        if final[record][p] > champion[record]['valor']:
            champion[record]['partido'] = p
            champion[record]['valor'] = final[record][p]

csv_dict = []
for c in champion:
    csv_dict.append({ 'MUNIC' : c, 'PARTIDO' : champion[c]['partido'], 'VALOR' : champion[c]['valor'] })

csv_file = open('partidoscampeoes.csv', 'w')
dw = csv.DictWriter(csv_file, fieldnames=csv_dict[0])
dw.writeheader()
for a in csv_dict:
    dw.writerow(a);


