# Mapa da Mina

Criando uma visualização dos partidos campeões em doação de campanha por munícipio.

Ferramentas utilizadas:
* [Dados do TSE](http://www.tse.jus.br/eleicoes/repositorio-de-dados-eleitorais)
* csvkit
* Python
* LibreOffice
* TileMill

A primeira coisa a fazer é baixar os dados do repositório do [TSE](http://www.tse.jus.br/eleicoes/repositorio-de-dados-eleitorais)

    wget http://agencia.tse.jus.br/estatistica/sead/odsele/prestacao_contas/segunda_parcial_2012.zip
    
Os csvs do TSE seguem um padrão comum no Brasil, mas incomum no resto mundo. O encoding é iso-8859-1 (ao invés do utf-8) e o separador é o ";" ao invés da ",".
Por isso o primeiro passo é utilizar o ``in2csv`` do csvkit para deixar o arquivo em ordem - isso vai demorar e consumir um bocado de memória.

    in2csv -e "iso-8859-1" -d ";" ReceitasCandidatos.csv > ReceitasCandidatos-clean.csv

A partir de agora podemos descartar o arquivo original e vamos trabalhar apenas com o ReceitasCandidatos-clean.csv

Feito isso, desenvolvi um script em python simples que varre o CSV somando os valores de doação por munícipio pra cada partido e depois seleciona o partido com maior volume de recursos.

Veja que aqui não estou diferenciando entre candidatos eleitos e não eleitos, vereadores ou prefeito... a ideia é saber o quanto cada partido arrecadou no municipio.

Para baixar o script, você pode baixar o source todo do git ou simplesmente:

    wget 

O arquivo esta configurado para ler o arquivo ReceitasCandidatos-clean.csv no próprio diretorio e gerar o csv ``partidoscampeoes.csv``.

    python script.py

Vou tentar documentar o código do script que - acho - ainda esta com alguns problemas, mas serve pro exercicio.

Agora precisamos combinar esse CSV com os códigos do IBGE e demais dados demográficos.

Para isso vamos usar o csvjoin e juntar a coluna "MUNIC" do arquivo ``partidoscampeoes.csv`` com a coluna "MUNIC" do arquivo ``munic.csv`` que esta disponível no repositório.

    csvjoin -c "MUNIC","MUNIC" partidoscampeoes.csv munic.csv > mapadamina.csv
    
Agora o arquivo ``mapadamina.csv`` esta pronto para ser transformado em um ``.dbf`` (formato de arquivo que define os atributos em um shapefile) para conectarmos com shapefile o QGis e abrir no Tilemill \o/

Abra o CSV no LibreOffice e mande salvar como ``m.dbf`` (quando fizermos a união o QGis vai usar o nome do arquivo como prefixo da propriedade, ai um nome curto é melhor).

(Ah, Você vai precisar do libreoffice-base instalado.)

Baixe o shapefile dos munícipios brasileiros:

    wget http://www.gismaps.com.br/divpol/municipios_br.zip
    
Abra o QGis, adicione o shape do brasil e o dbf do mapadamina.

Abra as propriedades do shape do brasil, vá em 'Uniões' e conecte o campo ``COD_MUNC`` com ``COD_IBGE_S`` (usamos o S porque nesse shape o código do IBGE só tem 6 digitos e não inclui o digito verificador.)

Agora é só mandar salvar como shape e abrir no TileMill e brincar!

No arquivo mapadamina.css tem o estilo que estou usando para visualizar. Have fun!

